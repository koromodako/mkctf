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

def prog_prompt(indicator):
    """Returns global program prompt

    Arguments:
        indicator {str} -- [description]
    """
    return "[mkctf]({})> ".format(indicator)

def yaml_load(filepath):
    """Loads content of a YAML file

    Arguments:
        filepath {Path} -- Configuration file's path

    Returns:
        dict -- YAML configuration as a dictionary
    """
    with filepath.open() as f:
        return yaml.safe_load(f)

def yaml_dump(filepath, conf):
    """Write a configuration to a YAML configuration file

    Arguments:
        filepath {Path} -- Configuration file's path to write to
        conf {dict} -- Configuration values
    """
    with filepath.open('w') as f:
        f.write("""#
# This file was generated using mkctf utility. Do not edit it manually unless
# you know exactly what you're doing. #PEBCAK
#
""")
        yaml.safe_dump(conf, f, default_flow_style=False)

def load_config(conf_path):
    """Wrapper to add an abstraction level above configuration format

    Arguments:
        conf_path {Path} -- cf. yaml_load
    """
    return yaml_load(conf_path)
