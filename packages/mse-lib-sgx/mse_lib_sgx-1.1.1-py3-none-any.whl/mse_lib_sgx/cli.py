"""mse_lib_sgx.cli.bootstrap module."""

import argparse
import asyncio
import importlib
import logging
import sys
import sysconfig
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path

from hypercorn.asyncio import serve
from hypercorn.config import Config
from mse_lib_crypto.xsalsa20_poly1305 import decrypt_directory

from mse_lib_sgx import __version__, globs
from mse_lib_sgx.certificate import Certificate, to_wildcard_domain
from mse_lib_sgx.error import SecurityError
from mse_lib_sgx.http_server import serve as serve_sgx_secrets


def parse_args() -> argparse.Namespace:
    """Argument parser."""
    parser = argparse.ArgumentParser(
        description="Bootstrap ASGI/WSGI Python web application for Gramine"
    )
    parser.add_argument(
        "application",
        type=str,
        help="ASGI application path (as module:app)",
    )

    parser.add_argument(
        "--host",
        required=True,
        type=str,
        help="hostname of the configuration server, "
        "also the hostname of the app server if `--self-signed`",
    )
    parser.add_argument("--port", required=True, type=int, help="port of the server")
    parser.add_argument(
        "--app-dir",
        required=True,
        type=Path,
        help="path of the python web application",
    )
    parser.add_argument(
        "--uuid", required=True, type=str, help="unique application UUID"
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--debug", action="store_true", help="debug mode with more logging"
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "--self-signed",
        type=int,
        metavar="EXPIRATION_DATE",
        help="generate a self-signed certificate for the web app with a "
        "specific expiration date (Unix time)",
    )

    group.add_argument("--no-ssl", action="store_true", help="use HTTP without SSL")

    group.add_argument(
        "--certificate",
        type=Path,
        metavar="CERTIFICATE_PATH",
        help="custom certificate used for the SSL connection, "
        "private key must be sent through the configuration server",
    )

    return parser.parse_args()


class SslAppMode(Enum):
    """SSL Application Mode."""

    RATLS_CERTIFICATE = 1  # self-signed SGX certificate with quote
    CUSTOM_CERTIFICATE = 2  # provided by the code provider
    NO_SSL = 3  # no SSL, will be done by the SSL proxy


def run() -> None:
    """Entrypoint of the CLI.

    The program creates a self-signed certificate.

    Then starts a configuration server using HTTPS and this previous cert
    in order to allow the user to send some secrets params.

    Once all the secrets has been sent, three options:
    - (--self-signed) If the app owner relies on the enclave certificate,
      then start the app server using this same certificate
    - (--certificate) Start the app server using the certificate
      provided by the app owner. In that case, the certificate
      is already present in the workspace of the program
      but the private key is sent by the app owner
      when the configuration server is up.
    - (--no-ssl) If the app owner and the users trust the operator (cosmian)
      then don't use https connection.
    """
    args: argparse.Namespace = parse_args()

    globs.HOME_DIR_PATH.mkdir(exist_ok=True)
    globs.KEY_DIR_PATH.mkdir(exist_ok=True)
    globs.MODULE_DIR_PATH.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format="[%(asctime)s] [%(levelname)s] %(message)s",
    )

    ssl_private_key_path = None
    expiration_date = datetime.now() + timedelta(hours=10)
    common_name: str = to_wildcard_domain(args.host)

    if not common_name:
        raise SecurityError(f"Can't parse host to extract Common Name: {args.host}")

    ssl_app_mode: SslAppMode
    if args.no_ssl:
        # The conf server use the self-signed cert
        # No ssl for the app server
        ssl_app_mode = SslAppMode.NO_SSL
    elif args.certificate:
        # The conf server use the self-signed cert
        # The app server use the app owner cert
        ssl_app_mode = SslAppMode.CUSTOM_CERTIFICATE
        ssl_private_key_path = globs.KEY_DIR_PATH / "key.pem"
    else:
        # The conf server and the app server will use the same self-signed cert
        ssl_app_mode = SslAppMode.RATLS_CERTIFICATE
        expiration_date = datetime.utcfromtimestamp(args.self_signed)

    logging.info("Generating self-signed certificate...")

    cert: Certificate = Certificate(
        dns_name=args.host,
        subject=globs.SUBJECT,
        root_path=globs.KEY_DIR_PATH,
        expiration_date=expiration_date,
        ratls=True,
    )

    symkey_path: Path = globs.KEY_DIR_PATH / "code.key"

    if not symkey_path.exists():
        logging.info("Starting the configuration server...")
        # The app owner will send:
        # - the uuid of the app (see as an uniq token allowing to query the API)
        # - the key to decrypt the code
        # - (optional) the SSL private key if AppConnection.OWNER_CERTFICIATE
        serve_sgx_secrets(
            hostname="0.0.0.0",
            port=args.port,
            certificate=cert,
            uuid=args.uuid,
            need_ssl_private_key=ssl_app_mode == SslAppMode.CUSTOM_CERTIFICATE,
            timeout=globs.TIMEOUT,
        )

        if globs.CODE_SECRET_KEY is None:
            raise SecurityError("Code secret key not provided")

        symkey_path.write_bytes(globs.CODE_SECRET_KEY)

        if (
            ssl_app_mode == SslAppMode.CUSTOM_CERTIFICATE
            and globs.SSL_PRIVATE_KEY
            and ssl_private_key_path is not None
        ):
            ssl_private_key_path.write_text(globs.SSL_PRIVATE_KEY)

    decrypt_directory(
        dir_path=args.app_dir,
        key=symkey_path.read_bytes(),
        ext=".enc",
        out_dir_path=globs.MODULE_DIR_PATH,
    )

    config_map = {
        "bind": f"0.0.0.0:{args.port}",
        "alpn_protocols": ["h2"],
        "workers": 1,
        "accesslog": "-",
        "errorlog": "-",
        "worker_class": "uvloop",
        "wsgi_max_body_size": 2 * 1024 * 1024 * 1024,  # 2 GB
    }

    if ssl_app_mode == SslAppMode.CUSTOM_CERTIFICATE:
        config_map["certfile"] = args.certificate
        config_map["keyfile"] = ssl_private_key_path
    elif ssl_app_mode == SslAppMode.RATLS_CERTIFICATE:
        config_map["certfile"] = cert.cert_path
        config_map["keyfile"] = cert.key_path

    config = Config.from_mapping(config_map)

    logging.info("Loading the application...")
    module_name, application_name = args.application.split(":")

    sys.path.append(f"{globs.MODULE_DIR_PATH}")

    logging.debug("MODULE_PATH=%s", globs.MODULE_DIR_PATH)
    logging.debug("sys.path: %s", sys.path)
    logging.debug("sysconfig.get_paths(): %s", sysconfig.get_paths())
    logging.debug("application: %s", args.application)

    application = getattr(importlib.import_module(module_name), application_name)

    logging.info("Starting the application (mode=%s)...", ssl_app_mode.name)
    asyncio.run(serve(application, config))
