# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: init.py
#     date: 2018-02-27
#   author: paul.dautry
#  purpose:
#
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================================================
#  IMPORTS
# =============================================================================

from core.repository import Repository
# =============================================================================
#  FUNCTIONS
# =============================================================================
##
## @brief      { function_description }
##
## @param      args    The arguments
## @param      conf    The conf
## @param      logger  The logger
##
def init(args, conf, logger):
    repo = Repository(args.working_dir, conf, logger)

    if repo.exists():
        logger.info("already a mkctf repository.")
        return False

    repo.init()

    return True
