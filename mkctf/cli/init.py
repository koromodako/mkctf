'''
file: init.py
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
async def init(args, repo):
    '''Initializes mkctf repository
    '''
    status = True

    if repo.get_conf() is None:
        repo.init()
        app_log.info("mkctf repository created.")

        if not args.json:
            repo.print_conf()

    else:
        app_log.error("already a mkctf repository.")
        status = False

    return {'status': status, 'conf': repo.get_conf()} if args.json else status

