# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: create.py
#     date: 2018-02-27
#   author: paul.dautry
#  purpose:
#
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================================================
#  FUNCTIONS
# =============================================================================

async def create(args, repo, logger):
    """Creates a challenge

    Arguments:
        args {Namespace} -- [description]
        repo {Repository} -- [description]
        logger {Logger} -- [description]
    """
    status = repo.create_chall(args.configuration)
    return {'status': status} if args.json else status

