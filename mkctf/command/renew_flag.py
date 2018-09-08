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
    '''
    if not args.force and not repo.cli.confirm('do you really want to renew flags?'):
        return {'status': True} if args.json else True

    no_color = args.no_color
    tags, slug = args.tags, args.slug

    chall_sep = '=' * 80
    if not no_color:
        chall_sep = colored(chall_sep, 'blue', attrs=['bold'])

    results = []

    for challenge in repo.scan(tags):
        if slug is None or slug == challenge.slug:
            new_flag = challenge.renew_flag(args.size)

            if args.json:
                results.append({
                    'slug': challenge.slug,
                    'tags': challenge.tags,
                    'flag': new_flag
                })
            else:
                chall_desc = f"{challenge.slug}{challenge.tags}"
                if not no_color:
                    chall_desc = colored(chall_desc, 'blue')

                print(chall_sep)
                print(f"{chall_desc} => {new_flag}")

    return results if args.json else True
