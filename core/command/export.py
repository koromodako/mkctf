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
import os
import tarfile
import os.path as path
from core.hashing import hash_file
# =============================================================================
#  FUNCTIONS
# =============================================================================
##
## @brief      { function_description }
##
## @param      logger            The logger
## @param      export_dir        The export dir
## @param      include_disabled  The include disabled
## @param      chall             The chall
##
def __export_chall(logger, export_dir, include_disabled, chall):
    if not chall.is_static():
        logger.warning("challenge ignored (not static): "
                       "{}/{}.".format(chall.category(),chall.slug()))
        return False

    if not include_disabled and not chall.enabled():
        logger.warning("challenge ignored (disabled): "
                       "{}/{}.".format(chall.category(),chall.slug()))
        return False

    logger.info("exporting {}/{}...".format(chall.category(),
                                            chall.slug()))

    archive_name = "{}.{}.tgz".format(chall.category(), chall.slug())
    archive_path = path.join(export_dir, archive_name)
    with tarfile.open(archive_path, 'w:gz') as arch:
        for entry in chall.exportable():
            arch.add(entry.path, arcname=entry.name)

    checksum_path = "{}.sha256".format(archive_path)
    with open(checksum_path, 'w') as f:
        f.write("{}  {}\n".format(hash_file(archive_path), archive_name))

    logger.info("done.")
    return True
##
## @brief      { function_description }
##
## @param      args    The arguments
## @param      repo    The repo
## @param      logger  The logger
##
def export(args, repo, logger):
    export_dir = path.abspath(args.export_dir)
    category, slug = args.category, args.slug
    include_disabled = args.include_disabled

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

        return __export_chall(logger, export_dir, include_disabled, chall)

    for category, challenges in repo.scan(category):
        for chall in challenges:
            __export_chall(logger, export_dir, include_disabled, chall)

    return True
