# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: delete.py
#     date: 2018-02-27
#   author: paul.dautry
#  purpose:
#
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================================================
#  IMPORTS
# =============================================================================
from core.cli import CLI
# =============================================================================
#  FUNCTIONS
# =============================================================================
def delete(args, repo, logger):
    categ, slug = args.category, args.chall_slug
    if repo.delete_chall(categ, slug):
        logger.info("challenge {}/{} successfully deleted.".format(categ,
                                                                   slug))
        return True

    logger.error("challenge {}/{} deletion failed.".format(categ, slug))
    return False

