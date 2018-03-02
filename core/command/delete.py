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
    if repo.delete_chall(category, slug):
        logger.info("challenge {}/{} successfully deleted.".format(category,
                                                                   slug))
        return True

    logger.error("challenge {}/{} deletion failed.".format(category, slug))
    return False
