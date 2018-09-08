'''
file: config.py
date: 2018-02-27
author: paul.dautry
purpose:

'''
# =============================================================================
#  IMPORTS
# =============================================================================
from ruamel import yaml
# =============================================================================
#  FUNCTIONS
# =============================================================================
def prog_prompt(indicator):
    '''Returns global program prompt
    '''
    return f"[mkctf]({indicator})> "

def yaml_load(filepath):
    '''Loads content of a YAML file
    '''
    with filepath.open() as f:
        return yaml.safe_load(f)

def yaml_dump(filepath, conf):
    '''Write a configuration to a YAML configuration file
    '''
    with filepath.open('w') as f:
        f.write("#\n"
                "# This file was generated using mkCTF utility.\n"
                "# Do not edit it manually unless you know exactly what you're doing.\n"
                "# Keep #PEBCAK in mind.\n"
                "#\n")
        yaml.safe_dump(conf, f, default_flow_style=False)

def load_config(conf_path):
    '''Wrapper to add an abstraction level above configuration format
    '''
    return yaml_load(conf_path)
