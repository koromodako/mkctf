# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: disable.py
#     date: 2018-03-02
#   author: paul.dautry
#  purpose:
#
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================================================
#  FUNCTIONS
# =============================================================================

async def disable(args, repo, logger):
    """Disables a challenge

    Arguments:
        args {Namespace} -- [description]
        repo {Repository} -- [description]
        logger {Logger} -- [description]
    """
    status = repo.disable_chall(args.category, args.slug)
    return {'status': status} if args.json else status
