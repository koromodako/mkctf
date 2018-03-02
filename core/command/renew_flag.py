# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: renew_flag.py
#     date: 2018-03-02
#   author: paul.dautry
#  purpose:
#
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================================================
#  FUNCTIONS
# =============================================================================
from termcolor import colored
# =============================================================================
#  FUNCTIONS
# =============================================================================
def renew_flag(args, repo, logger):
    if not repo.cli.confirm('do you really want to renew flags?'):
        return True

    no_color = args.no_color
    category, slug = args.category, args.slug

    chall_sep = '=' * 80
    if not no_color:
        chall_sep = colored(chall_sep, 'blue', attrs=['bold'])

    for cat, challenges in repo.scan(category):
        for challenge in challenges:
            if slug is None or slug == challenge.slug():
                new_flag = challenge.renew_flag(args.size)

                chall_desc = "[{}] -> {}".format(challenge.category(),
                                                 challenge.slug())
                if not no_color:
                    chall_desc = colored(chall_desc, 'blue')

                print(chall_sep)
                print("{} => {}".format(chall_desc, new_flag))

    return True
