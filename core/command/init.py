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
# =============================================================================
#  FUNCTIONS
# =============================================================================
##
## @brief      { function_description }
##
## @param      args         The arguments
## @param      glob_conf    The global conf
## @param      logger       The logger
##
def init(args, repo, logger):
    status = True

    if repo.get_conf() is None:
        repo.init()
        logger.info("mkctf repository created.")

        if not args.json:
            repo.print_conf()

    else:
        logger.error("already a mkctf repository.")
        status = False

    return {'status': status, 'conf': repo.get_conf()} if args.json else status

