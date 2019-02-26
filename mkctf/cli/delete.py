'''
file: delete.py
date: 2018-02-27
author: koromodako
purpose:

'''
# =============================================================================
#  IMPORTS
# =============================================================================
from mkctf.helper.log import app_log
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def delete(args, repo):
    '''Deletes a challenge
    '''
    slug = args.slug
    status = True

    if repo.delete_chall(slug):
        app_log.info(f"challenge {slug} successfully deleted.")
    else:
        app_log.error(f"challenge {slug} deletion failed.")
        status = False

    return {'status': status} if args.json else status
