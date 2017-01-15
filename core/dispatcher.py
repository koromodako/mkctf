#!/usr/bin/env python3
# -!- encoding: utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    dispatcher.py
# date:    2017-01-13
# author:  paul dautry
# purpose:
#       Created to evolutive functionnality-oriented application. 
#       Associates each command with a function.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def not_implemented(params):
    print('Dispatcher: not implemented')

class Dispatcher(object):
    """docstring for Dispatcher"""
    def __init__(self):
        super(Dispatcher, self).__init__()
        self.dispatch = { }
        self.error = 'n/a'

    def add(self, key, func):
        if not callable(func):
            self.error = 'Given argument for function is not callable.'
            return False
        self.dispatch[key] = func
        return True

    def call(self, key, **kwargs):
        self.dispatch.get(key, not_implemented)(kwargs)
