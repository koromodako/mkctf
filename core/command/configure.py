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
    category, slug = args.category, args.chall_slug
    if category is None and slug is None:

        if repo.configure():
            logger.info("repo configured.")
            return True

        logger.error("repo configuration failed.")
        return False

    if category is not None and slug is not None:
        if repo.configure_chall(category, slug):
            logger.info("challenge configured.")
            return True

        logger.error("challenge configuration failed.")
        return False

    logger.error("use both --category and --chall-slug to configure a "
                 "challenge.")
    return False

