'''
file: delete.py
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
async def delete(args, repo):
    '''Deletes a challenge

    Arguments:
        args {Namespace} -- [description]
        repo {Repository} -- [description]
    '''
    category, slug = args.category, args.slug
    status = True

    if repo.delete_chall(category, slug):
        app_log.info("challenge {}/{} successfully deleted.", category, slug)
    else:
        app_log.error("challenge {}/{} deletion failed.", category, slug)
        status = False

    return {'status': status} if args.json else status
