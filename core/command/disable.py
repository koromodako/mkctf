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
def disable(args, repo, logger):
    status = repo.disable_chall(args.category, args.slug)
    return {'status': status} if args.json else status
