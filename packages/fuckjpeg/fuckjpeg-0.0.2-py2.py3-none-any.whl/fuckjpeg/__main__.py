#!/usr/bin/env python3

""" CLI interface for fuckjpeg """

import os
import logging
import click

from . import rename_file


@click.command()
@click.argument("path", type=click.Path())
@click.option(
    "-o",
    "--overwrite",
    is_flag=True,
    default=False,
    help="Ignore existing files and overwrite them.",
)
@click.option(
    "-r",
    "--recursive",
    is_flag=True,
    default=False,
    help="Set this and supply a path, recursively apply the fun. Use with caution, obviously.",
)
@click.option(
    "-l",
    "--log-level",
    type=click.Choice(["debug", "info", "warn"]),
    default="info",
    help="Set logging level",
)
@click.option(
    "-n",
    "--dry-run",
    is_flag=True,
    default=False,
    help="Do a dry run, don't actually make changes.",
)
def cli(
    path: str, overwrite: bool, recursive: bool, log_level: str, dry_run: bool
) -> None:
    """Renames files with .jpeg to .jpg because fuck that.

    You can supply a filename or a directory, and if it's a directory it'll do all the files."""
    if log_level.upper() == "DEBUG":
        log_format = ""
    else:
        log_format = "%(message)s"
    logging.basicConfig(level=getattr(logging, log_level.upper()), format=log_format)
    logger = logging.getLogger(__name__)

    if dry_run:
        logger.warning("*** In dry-run mode, won't actually take any action ***")

    if os.path.isfile(path):
        rename_file(path, overwrite, logger, dry_run)
    else:
        if recursive:
            logger.debug("Recursive mode engaged!")
            for root, dirs, files in os.walk(path, topdown=False):
                for name in files:
                    rename_file(os.path.join(root, name), overwrite, logger, dry_run)
                for name in dirs:
                    rename_file(os.path.join(root, name), overwrite, logger, dry_run)
        for filename in os.listdir(path):
            rename_file(os.path.join(path, filename), overwrite, logger, dry_run)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()
