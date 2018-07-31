'''
file: enable.py
date: 2018-03-02
author: paul.dautry
purpose:

'''
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def enable(args, repo):
    '''Enables a challenge

    Arguments:
        args {Namespace} -- [description]
        repo {Repository} -- [description]
    '''
    status = repo.enable_chall(args.category, args.slug)
    return {'status': status} if args.json else status
