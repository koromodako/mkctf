# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: export.py
#     date: 2018-03-02
#   author: paul.dautry
#  purpose:
#
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================================================
#  IMPORTS
# =============================================================================
import os.path as path
from tarfile import TarFile
# =============================================================================
#  FUNCTIONS
# =============================================================================
##
## @brief      { function_description }
##
## @param      logger  The logger
## @param      args    The arguments
## @param      chall   The chall
##
def __export_chall(logger, args, chall):
    if (args.include_disabled or chall.enabled()) and chall.is_static():
        logger.info("exporting {}/{}...".format(chall.category(),
                                                chall.slug()))

        archive = "{}.tgz".format(chall.slug())

        with TarFile(path.join(export_dir, archive), 'w:gz') as a:
            for entry in chall.exportable():
                a.add(entry.path, arcname=entry.name)

        logger.info("done.")
        return True

    logger.warning("challenge ignored: {}/{}.".format(chall.category(),
                                                      chall.slug()))
    return False
##
## @brief      { function_description }
##
## @param      args    The arguments
## @param      repo    The repo
## @param      logger  The logger
##
def export(args, repo, logger):
    export_dir = path.abspath(args.export_dir)
    category, slug = args.category, args.chall_slug

    if category is None and slug is not None:
        logger.error("you must specify --category if you use --chall-slug.")
        return False

    os.makedirs(export_dir, exist_ok=True)

    if slug is not None:
        chall = repo.find_chall(category, slug)
        if chall is None:
            logger.error("challenge not found: {}/{}".format(chall.category(),
                                                             chall.slug()))
            return False

        return __export_chall(logger, args, chall)
