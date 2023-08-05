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
# pylint: disable=too-many-branches
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

            for root, _, files in os.walk(path, topdown=False):
                if ".photoslibrary" in root:
                    logger.error(
                        "Refusing to rename things inside an icloud photo library, eek! (%s)",
                        root,
                    )
                    continue

                for name in files:
                    if os.path.isfile(os.path.join(root, name)):
                        rename_file(os.path.join(root, name), overwrite, logger, dry_run)
                    else:
                        logger.debug("Isn't a file, skipping: %s", os.path.join(root, name))
        else:
            for filename in os.listdir(path):
                filepath = os.path.join(path, filename)
                if not os.path.isfile(filepath):
                    logger.debug("Isn't a file, skipping: %s", filepath)
                    continue
                rename_file(filepath, overwrite, logger, dry_run)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()
