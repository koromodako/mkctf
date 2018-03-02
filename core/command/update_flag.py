# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: update_flag.py
#     date: 2018-03-02
#   author: paul.dautry
#  purpose:
#
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================================================
#  FUNCTIONS
# =============================================================================
def update_flag(args, repo, logger):
    if not repo.cli.confirm('do you really want to update flags?'):
        return False

    category, slug = args.category, args.slug

    raise NotImplementedError('implement me!')


