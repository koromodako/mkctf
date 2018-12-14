'''
file: disable.py
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
async def disable(args, repo):
    '''Disables a challenge
    '''
    status = repo.disable_chall(args.slug)
    if status:
        app_log.info(f"{args.slug} disabled.")
    return {'status': status} if args.json else status
