# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: delete.py
#     date: 2018-02-27
#   author: paul.dautry
#  purpose:
#
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================================================
#  FUNCTIONS
# =============================================================================
def delete(args, repo, logger):
    category, slug = args.category, args.slug
    status = True

    if repo.delete_chall(category, slug):
        logger.info("challenge {}/{} successfully deleted.".format(category,
                                                                   slug))
    else:
        logger.error("challenge {}/{} deletion failed.".format(category, slug))
        status = False

    return {'status': status} if args.json else status
