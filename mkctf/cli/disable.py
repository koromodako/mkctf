'''
file: disable.py
date: 2018-03-02
author: koromodako
purpose:

'''
#===============================================================================
#  IMPORTS
#===============================================================================
#
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def disable(api, args):
    '''Enables a challenge
    '''
    status = api.disable(args.slug)
    disabled = status['disabled']
    if disabled:
        print(f"{args.slug}: disabled")
    return disabled
