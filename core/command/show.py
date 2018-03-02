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
##
## @brief      { function_description }
##
def __print_chall(logger, challenge, no_color):
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
##
## @brief      { function_description }
##
## @param      args    The arguments
## @param      repo    The repo
## @param      logger  The logger
##
## @return     { description_of_the_return_value }
##
def show(args, repo, logger):
    found = False
    success = True
    category, slug = args.category, args.slug

    print("challenges:")
    for cat, challenges in repo.scan(category):
        print("{}+ {}".format(TAB, cat))

        for challenge in challenges:
            if slug is None or slug == challenge.slug():
                found = True
                try:
                    if not __print_chall(logger, challenge, args.no_color):
                        success = False
                except Exception as e:
                    logger.error("configuration is invalid (missing key: "
                                 "{}).".format(e))
                    success = False

    if not found:
        logger.warning("no challenge found matching given constraints.")

    return success
