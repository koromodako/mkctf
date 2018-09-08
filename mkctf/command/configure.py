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
    '''
    slug = args.slug
    success = True
    if slug is None:
        # configure repo
        if repo.configure(args.configuration):
            app_log.info("repo configured.")
        else:
            app_log.error("repo configuration failed.")
            success = False
    else:
        # configure a challenge
        if repo.configure_chall(slug, args.configuration):
            app_log.info("challenge configured.")
        else:
            app_log.error("challenge configuration failed.")
            success = False

    return {'status': success} if args.json else success
