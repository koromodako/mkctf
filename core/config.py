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
import pyaml
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
        return pyaml.yaml.load(f)
##
## @brief      Dumps a configuration to a YAML file
##
## @param      fpath  The fpath
## @param      conf   The conf
##
def yaml_dump(fpath, conf):
    with open(fpath, 'w') as f:
        pyaml.yaml.dump(conf, f)
##
## @brief      Loads a configuration.
##
## @param      args  The arguments
##
def load_config(args):
    return yaml_load(args.glob_conf_path)
