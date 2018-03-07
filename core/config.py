# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: config.py
#     date: 2018-02-27
#   author: paul.dautry
#  purpose:
#
#  license:
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================================================
#  IMPORTS
# =============================================================================
from ruamel import yaml
# =============================================================================
#  FUNCTIONS
# =============================================================================
##
## @brief      Returns global program prompt
##
def prog_prompt(indicator):
    return "[mkctf]({})> ".format(indicator)
##
## @brief      Loads a configuration from a YAML file
##
def yaml_load(fpath):
    with open(fpath, 'r') as f:
        return yaml.safe_load(f)
##
## @brief      Dumps a configuration to a YAML file
##
## @param      fpath  The fpath
## @param      conf   The conf
##
def yaml_dump(fpath, conf):
    with open(fpath, 'w') as f:
        f.write("""#
# This file was generated using mkctf utility. Do not edit it manually unless
# you know exactly what you're doing. #PEBCAK
#
""")
        yaml.safe_dump(conf, f, default_flow_style=False)
##
## @brief      Loads a configuration.
##
## @param      args  The arguments
##
def load_config(args):
    return yaml_load(args.glob_conf_path)
