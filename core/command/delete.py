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
    if repo.delete_chall(args.category, args.chall_slug):
        logger.info("challenge {}/{} successfully deleted.")
        return True

    logger.error("challenge {}/{} deletion failed.")
    return False

