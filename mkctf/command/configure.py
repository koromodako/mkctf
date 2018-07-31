'''
file: configure.py
date: 2018-02-27
author: paul.dautry
purpose:

'''
# =============================================================================
#  IMPORTS
# =============================================================================
from mkctf.helper.log import app_log
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def configure(args, repo):
    '''Configures mkctf repository or a specific challenge

    Arguments:
        args {Namespace} -- [description]
        repo {Repository} -- [description]
    '''
    category, slug = args.category, args.slug
    success = True

    if category is None and slug is None:

        if repo.configure(args.configuration):
            app_log.info("repo configured.")
        else:
            app_log.error("repo configuration failed.")
            success = False

    elif category is not None and slug is not None:

        if repo.configure_chall(category, slug, args.configuration):
            app_log.info("challenge configured.")
        else:
            app_log.error("challenge configuration failed.")
            success = False
    else:
        app_log.error("use both --category and --chall-slug to configure a "
                     "challenge.")
        success = False

    return {'status': success} if args.json else success
