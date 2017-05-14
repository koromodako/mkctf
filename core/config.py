#!/usr/bin/env python3
# -!- encoding: utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    config.py
# date:    2017-01-15
# author:  paul dautry
# purpose:
#       Contains interface to configuration file
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
import json
from core.logger import Logger

class Config(object):
    K_WORKSPACE     = 'workspace'
    K_CATEGORIES    = 'categories'
    K_DIRECTORIES   = 'directories'
    K_FILES         = 'files' 
    """docstring for Configuration"""
    def __init__(self):
        super(Config, self).__init__()
        self.config = {
            Config.K_WORKSPACE: '~/challenges',
            Config.K_CATEGORIES: [
                'bugbounty', 
                'crypto', 
                'forensics', 
                'misc', 
                'programming', 
                'pwn', 
                'reverse', 
                'web'
            ],
            Config.K_DIRECTORIES: [
                'server-files', 
                'public-files', 
                'exploit', 
                'src'
            ],
            Config.K_FILES: [
                [ 'writeup.md', False ], 
                [ 'flag.txt', False ], 
                [ 'public-files/description.md', False ], 
                [ 'exploit/exploit', True ]
            ]
        }

    def load(self, configfile):
        if not os.path.isfile(configfile):
            Logger.err('specified configfile is not a file or cannot be found.')
            return False
        Logger.inf('configuration file is: %s' % configfile)
        with open(configfile, 'r') as f:
            try:
                conf = json.loads(f.read())
            except Exception as e:
                conf = None
        if conf is None:
            Logger.err('failed to read configuration file!')
            return False
        self.config = conf
        return True

    def save(self, configfile):
        with open(configfile, 'w') as f: 
            f.write(json.dumps(self.config, indent=4))

    def set_property(self, key, value):
        self.config[key] = value

    def get_property(self, key, default=None):
        return self.config.get(key, default)
    
