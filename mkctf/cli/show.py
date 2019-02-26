'''
file: show.py
date: 2018-02-27
author: koromodako
purpose:

'''
# =============================================================================
#  IMPORTS
# =============================================================================
from termcolor import colored
from mkctf.helper.log import app_log
from mkctf.helper.formatting import TAB, format_dict2str
# =============================================================================
#  FUNCTIONS
# =============================================================================
def __print_chall(challenge, no_color):
    '''Prints a challenge
    '''
    conf = challenge.get_conf()
    if conf is None:
        app_log.error(f"configuration missing. Run `mkctf configure -s {challenge.slug}`")
        return False

    static = ' [STANDALONE]' if conf['standalone'] else ''

    chall_entry = f"{TAB}{TAB}- {challenge.slug}{static}"
    if not no_color:
        color = 'green' if conf['enabled'] else 'red'
        chall_entry = colored(chall_entry, color, attrs=['bold'])
        del conf['enabled']

    del conf['standalone']
    del conf['slug']

    text = format_dict2str(conf).replace("\n", f"\n{TAB}{TAB}{TAB}")

    print(chall_entry)
    print(text[1:])

    return True

async def show(args, repo):
    '''Shows a list of all challenges
    '''
    found = False
    success = True
    results = {}
    tags, slug = args.tags, args.slug

    if not args.json:
        print("challenges:")

    results = {}
    for challenge in repo.scan(tags):
        if slug is None or slug == challenge.slug:
            found = True
            try:
                if args.json:
                    results[challenge.slug] = challenge.get_conf()
                elif not __print_chall(challenge, args.no_color):
                    success = False
            except Exception as e:
                app_log.error(f"configuration is invalid (missing key: {e}).")
                success = False

    if not found:
        app_log.warning("no challenge found matching given constraints.")

    return results if args.json else success
