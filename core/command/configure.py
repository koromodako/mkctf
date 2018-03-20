# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: configure.py
#     date: 2018-02-27
#   author: paul.dautry
#  purpose:
#
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================================================
#  FUNCTIONS
# =============================================================================
def configure(args, repo, logger):
    category, slug = args.category, args.slug
    success = True

    if category is None and slug is None:

        if repo.configure(args.configuration):
            logger.info("repo configured.")
        else:
            logger.error("repo configuration failed.")
            success = False

    elif category is not None and slug is not None:

        if repo.configure_chall(category, slug, args.configuration):
            logger.info("challenge configured.")
        else:
            logger.error("challenge configuration failed.")
            success = False
    else:
        logger.error("use both --category and --chall-slug to configure a "
                     "challenge.")
        success = False

    return {'status': success} if args.json else success
