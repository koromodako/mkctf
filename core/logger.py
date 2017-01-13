#!/usr/bin/env python3
# -!- encoding: utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    logger.py
# date:    2017-01-13
# author:  paul dautry
# purpose:
#       This is a traditionnal logging class
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Logger(object):
    DEBUG = False
    VERBOSE = False

    @staticmethod
    def fat(msg, end='\n'):
        print('[!] > %s' % msg, end=end)
        exit(1)

    @staticmethod
    def err(msg, end='\n'):
        print('[E] > %s' % msg, end=end)

    @staticmethod
    def wrn(msg, end='\n'):
        print('[W] > %s' % msg, end=end)

    @staticmethod
    def dbg(msg, end='\n'):
        if Logger.DEBUG:
            print('[D] > %s' % msg, end=end)
    
    @staticmethod
    def inf(msg, end='\n'):
        if Logger.VERBOSE:
            print('[I] > %s' % msg, end=end)
        
        