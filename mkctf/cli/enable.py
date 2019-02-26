'''
file: enable.py
date: 2018-03-02
author: koromodako
purpose:

'''
#===============================================================================
#  IMPORTS
#===============================================================================
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def enable(api, args):
    '''Enables a challenge
    '''
    status = api.enable(args.slug)
    enabled = status['enabled']
    if enabled:
        print(f"{args.slug}: enabled")
    return enabled
