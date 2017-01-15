#!/usr/bin/env python3
# -!- encoding: utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    config.py
# date:    2017-01-15
# author:  paul dautry
# purpose:
#       Contains interface to configuration file
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from configparser import ConfigParser

class Config(object):
    S_DIR = 'DIR'
    K_WORKSPACE = 'workspace'
    K_PACKAGES = 'packages'
    """docstring for Configuration"""
    def __init__(self, configfile='py_chall_factory.ini'):
        super(Config, self).__init__()
        self.configfile = configfile
        self.parser = ConfigParser()
        self.error = 'n/a'

    def load(self, configfile=None):
        if configfile is not None:
            if not os.path.isfile(configfile):
                self.error = 'sepcified configfile is not a file or cannot be found.'
                return False
            self.configfile = configfile
        if len(self.parser.read(self.configfile)) == 0:
            self.error = 'failed to read configuration file!'
            return False
        return True

    def save(self, configfile=None):
        if configfile is not None:
            if not os.path.isfile(configfile):
                self.error = 'sepcified configfile is not a file or cannot be found.'
                return False
            self.configfile = configfile
        with open(self.configfile, 'w') as f: 
            self.parser.write(f)

    def set_property(self, section, key, value):
        if not self.parser.has_section(section):
            self.parser.add_section(section)
        self.parser.set(section, key, value)

    def get_property(self, section, key, default=None):
        return self.parser.get(section, key, fallback=default)
    
