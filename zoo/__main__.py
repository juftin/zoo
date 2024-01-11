"""
Zoo CLI
"""

import asyncio
import json
import logging
import pathlib
from dataclasses import dataclass

import click
import uvicorn
from click import Context
from fastapi_users.exceptions import UserAlreadyExists

from zoo._version import __application__, __version__
from zoo.app import ZooFastAPI, app
from zoo.config import ZooSettings, app_config
from zoo.models.users import create_user

logger = logging.getLogger(__name__)


@dataclass
class ZooContext:
    """
    Context Object Passed Around Application
    """

    app: ZooFastAPI
    config: ZooSettings


@click.group(invoke_without_command=True, name=__application__)
@click.version_option(version=__version__, prog_name=__application__)
@click.option("-h", "--host", default="localhost", help="Host to listen on")
@click.option("-p", "--port", default=8000, help="Port to listen on", type=int)
@click.option("-d", "--debug", is_flag=True, help="Enable debug mode", default=False)
@click.pass_context
def cli(context: click.Context, host: str, port: int, *, debug: bool) -> None:
    """
    Zoo CLI
    """
    context.obj = ZooContext(app=app, config=app_config)
    if context.obj.config.DEBUG is True or debug is True:
        context.obj.config.DEBUG = True
        logging.root.setLevel(logging.DEBUG)
    if context.invoked_subcommand is None:
        uvicorn.run(context.obj.app, host=host, port=port)


@cli.command()
@click.pass_obj
def openapi(context: ZooContext) -> None:
    """
    Generate openapi.json
    """
    openapi_body = context.app.openapi()
    logger.debug(openapi_body)
    json_file = pathlib.Path(__file__).parent.parent / "docs" / "openapi.json"
    logger.info("Generating OpenAPI Spec: %s", json_file)
    json_file.write_text(json.dumps(openapi_body, indent=2))


@cli.command()
@click.option("-e", "--email", help="User email to create", type=str, required=True)
@click.option(
    "-p",
    "--password",
    default="admin",
    help="Password to create",
    type=click.STRING,
    required=True,
)
@click.pass_context
def users(context: Context, email: str, password: str) -> None:
    """
    Create users
    """
    _ = context
    logger.info("Creating user: %s", email)
    try:
        user = asyncio.run(create_user(email=email, password=password))
        logger.info("Created user: %s", user.id)
    except UserAlreadyExists:
        logger.info("User already exists: %s", email)
        context.exit(1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if not app_config.DOCKER:
        app_config.rich_logging(loggers=[logging.getLogger()])
    cli()
