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
import os
import os.path as path
from core.challenge import Challenge
# =============================================================================
#  FUNCTIONS
# =============================================================================
##
## @brief      Shows the chall.
##
## @param      chall_path  The chall path
## @param      conf        The conf
## @param      logger      The logger
##
## @return     { description_of_the_return_value }
##
def _show_chall(chall_path, conf, logger):
    chall = Challenge(chall_path)

    if not chall.exists():
        logger.error("invalid chall_path: {}".format(chall_path))
        return False

    if chall.conf() is None:
        logger.warning("missing configuration -> patching challenge.")
        chall.create_default()

    chall.print_conf()
    return True
##
## @brief      { function_description }
##
## @param      args    The arguments
## @param      conf    The conf
## @param      logger  The logger
##
## @return     { description_of_the_return_value }
##
def show(args, conf, logger):
    if args.challenge is None:

        if args.category is None:

            for category in os.listdir(args.working_directory):

                category_path = path.join(args.working_directory, category)
                for challenge in os.listdir(category_path):
                    chall_path = path.join(category_path, challenge)
                    if not _show_chall(chall_path):
                        return False

            return True

        category_path = path.join(args.working_directory, args.category)
        if not path.isdir(category_path):
            logger.error("invalid category_path: {}".format(category_path))
            return False

        for challenge in os.listdir(category_path):
            chall_path = path.join(category_path, challenge)
            if not _show_chall(chall_path):
                return False

        return True

    if args.category is None:
        logger.error("missing --category option.")
        return False

    chall_path = path.join(args.working_directory, args.category, args.challenge)


    return _show_chall(chall_path, conf, logger)
