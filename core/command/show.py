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
from core.formatting import TAB
from core.formatting import dict2str
# =============================================================================
#  FUNCTIONS
# =============================================================================
##
## @brief      { function_description }
##
def __print_chall(logger, category, chall):
    print("{t}{t}- {slug}".format(t=TAB, slug=chall.slug()))
    conf = chall.get_conf()

    if conf is None:
        logger.error("configuration missing. Run `mkctf configure "
                     "--category={} -c {}`".format(category, chall.slug()))
        return False

    del conf['slug']

    text = dict2str(conf).replace("\n", "\n{t}{t}{t}".format(t=TAB))
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
    success = True
    chall_slug = args.chall_slug

    print("challenges:")
    for category, challenges in repo.scan(args.category):
        print("{}+ {}".format(TAB, category))

        for chall in challenges:
            if chall_slug is None or chall_slug == chall.get_conf('slug'):
                try:
                    if not __print_chall(logger, category, chall):
                        success = False
                except Exception as e:
                    logger.error("configuration is invalid (missing key: "
                                 "{}).".format(e))
                    success = False

    return success
