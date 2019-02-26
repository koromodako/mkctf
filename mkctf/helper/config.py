'''
file: config.py
date: 2018-02-27
author: koromodako
purpose:

'''
# =============================================================================
#  IMPORTS
# =============================================================================
from ruamel import yaml
# =============================================================================
#  FUNCTIONS
# =============================================================================
def yaml_load(filepath):
    '''Loads content of a YAML file
    '''
    with filepath.open() as fp:
        return yaml.safe_load(fp)

def yaml_dump(filepath, conf):
    '''Write a configuration to a YAML configuration file
    '''
    with filepath.open('w') as fp:
        fp.write("#\n"
                 "# This file was generated using mkCTF utility.\n"
                 "# Do not edit it manually unless you know exactly what you're doing.\n"
                 "# Keep #PEBCAK in mind.\n"
                 "#\n")
        yaml.safe_dump(conf, fp, default_flow_style=False)

def load_config(conf_path):
    '''Wrapper to add an abstraction level above configuration format
    '''
    return yaml_load(conf_path)
