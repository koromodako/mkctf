'''
file: renew_flag.py
date: 2018-03-02
author: paul.dautry
purpose:

'''
# =============================================================================
#  FUNCTIONS
# =============================================================================
from termcolor import colored
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def renew_flag(args, repo):
    '''Renews one or more challenge flags

    Arguments:
        args {Namespace} -- [description]
        repo {Repository} -- [description]

    Returns:
        [type] -- [description]
    '''
    if not args.force and not repo.cli.confirm('do you really want to renew flags?'):
        return {'status': True} if args.json else True

    no_color = args.no_color
    category, slug = args.category, args.slug

    chall_sep = '=' * 80
    if not no_color:
        chall_sep = colored(chall_sep, 'blue', attrs=['bold'])

    results = []

    for cat, challenges in repo.scan(category):
        for challenge in challenges:
            if slug is None or slug == challenge.slug():
                new_flag = challenge.renew_flag(args.size)

                if args.json:
                    results.append({
                        'slug': challenge.slug(),
                        'category': challenge.category(),
                        'flag': new_flag
                    })
                else:
                    chall_desc = "[{}] -> {}".format(challenge.category(),
                                                     challenge.slug())
                    if not no_color:
                        chall_desc = colored(chall_desc, 'blue')

                    print(chall_sep)
                    print("{} => {}".format(chall_desc, new_flag))

    return results if args.json else True
