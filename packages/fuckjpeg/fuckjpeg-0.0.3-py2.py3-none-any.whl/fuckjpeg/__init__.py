""" Utility functions for fuckjpeg """

import os
from logging import Logger

__version__ = "0.0.3"


def rename_file(filename: str, overwrite: bool, logger: Logger, dry_run: bool) -> bool:
    """ Renames a single file """
    if not filename.endswith(".jpeg"):
        logger.debug("Filename '%s' doesn't end with .jpeg, skipping.", filename)
        return False

    if ".photoslibrary" in filename:
        logger.error(
            "Refusing to rename things inside an icloud photo library, eek! (%s)",
            filename,
        )
        return False

    logger.debug("Starting to rename %s", filename)
    splitfile = filename.split(".")
    newbits = splitfile[:-1]
    newbits.append("jpg")
    newfilename = ".".join(newbits)

    if os.path.exists(newfilename):
        if not overwrite:
            logger.warn("%s already exists, overwrite not set, skipping.", newfilename)
            return False
        logger.debug("Removing %s", newfilename)
        if not dry_run:
            os.remove(newfilename)

    logger.info("Renaming %s to %s", filename, newfilename)
    if not dry_run:
        os.rename(filename, newfilename)
    return True
