# =============================================================================
#  IMPORTS
# =============================================================================
from ruamel.yaml import YAML
# =============================================================================
#  FUNCTIONS
# =============================================================================
def config_load(filepath):
    '''Loads content of a YAML file
    '''
    return YAML(typ='safe').load(filepath)

def config_dump(filepath, conf):
    '''Write a configuration to a YAML configuration file
    '''
    with filepath.open('w') as fp:
        fp.write("#\n"
                 "# This file was generated using mkCTF utility.\n"
                 "# Do not edit it manually unless you know exactly what you're doing.\n"
                 "# Keep #PEBCAK in mind.\n"
                 "#\n")
        yaml=YAML(typ='safe')
        yaml.default_flow_style = False
        yaml.dump(conf, fp)
