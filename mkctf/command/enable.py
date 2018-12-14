'''
file: enable.py
date: 2018-03-02
author: koromodako
purpose:

'''
#===============================================================================
#  IMPORTS
#===============================================================================
from mkctf.helper.log import app_log
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def enable(args, repo):
    '''Enables a challenge
    '''
    status = repo.enable_chall(args.slug)
    if status:
        app_log.info(f"{args.slug} enabled.")
    return {'status': status} if args.json else status
