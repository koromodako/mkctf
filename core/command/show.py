# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: show.py
#     date: 2018-02-27
#   author: paul.dautry
#  purpose:
#
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================================================
#  IMPORTS
# =============================================================================
from termcolor import colored
from core.formatting import TAB
from core.formatting import dict2str
# =============================================================================
#  FUNCTIONS
# =============================================================================
def __print_chall(logger, challenge, no_color):
    """Prints a challenge

    Arguments:
        logger {Logger} -- [description]
        challenge {Challenge} -- [description]
        no_color {bool} -- [description]

    Returns:
        bool -- [description]
    """
    conf = challenge.get_conf()
    if conf is None:
        logger.error("configuration missing. Run `mkctf configure "
                     "-c {} -s {}`".format(challenge.category(),
                                           challenge.slug()))
        return False

    static = ' [STANDALONE]' if conf['standalone'] else ''

    chall_entry = "{t}{t}- {slug}{static}".format(t=TAB,
                                                  slug=challenge.slug(),
                                                  static=static)
    if not no_color:
        color = 'green' if conf['enabled'] else 'red'
        chall_entry = colored(chall_entry, color, attrs=['bold'])
        del conf['enabled']

    del conf['standalone']
    del conf['category']
    del conf['slug']

    text = dict2str(conf).replace("\n", "\n{t}{t}{t}".format(t=TAB))

    print(chall_entry)
    print(text[1:])

    return True

async def show(args, repo, logger):
    """Shows a list of all challenges

    Arguments:
        args {Namespace} -- [description]
        repo {Repository} -- [description]
        logger {Logger} -- [description]

    Returns:
        [type] -- [description]
    """
    found = False
    success = True
    results = {}
    category, slug = args.category, args.slug

    if not args.json:
        print("challenges:")

    for cat, challenges in repo.scan(category):

        if not args.json:
            print("{}+ {}".format(TAB, cat))

        results[cat] = {}

        for challenge in challenges:
            if slug is None or slug == challenge.slug():
                found = True
                try:
                    if args.json:
                        results[cat][challenge.slug()] = challenge.get_conf()
                    elif not __print_chall(logger, challenge, args.no_color):
                        success = False
                except Exception as e:
                    logger.error("configuration is invalid (missing key: "
                                 "{}).".format(e))
                    success = False

    if not found:
        logger.warning("no challenge found matching given constraints.")

    return results if args.json else success
