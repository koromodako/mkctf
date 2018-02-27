# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: init.py
#     date: 2018-02-27
#   author: paul.dautry
#  purpose:
#
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================================================
#  IMPORTS
# =============================================================================
import os.path as path
from core.config import yaml_dump
# =============================================================================
#  FUNCTIONS
# =============================================================================
##
## @brief      { function_description }
##
## @param      args    The arguments
## @param      conf    The conf
## @param      logger  The logger
##
def init(args, conf, logger):
    conf_path = path.join(args.working_dir, conf['files']['config']['ctf'])

    if path.isfile(conf_path):
        logger.info("directory is already a mkctf repository.")
        return False

    yaml_dump(conf_path, {
        "working-dir": args.working_dir
    })
    return True
