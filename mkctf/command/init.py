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
async def init(args, repo, logger):
    """Initializes mkctf repository

    Arguments:
        args {Namespace} -- [description]
        repo {Repository} -- [description]
        logger {Logger} -- [description]
    """
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

