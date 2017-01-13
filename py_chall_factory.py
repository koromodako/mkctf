#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    py_chall_factory.py
# date:    2017-01-13
# author:  paul dautry
# purpose:
#       This is a framework designed to create challenges and maintain them.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#===============================================================================
#  IMPORTS
#===============================================================================
import os
import sys
import signal
from core.logger import Logger
from core.cli_option_parser import CLIOptionsParser
from core.dispatcher import Dispatcher
from core.utils import read_input
from core.functions import configure
from core.functions import create_challenge
from core.functions import delete_challenge
from core.functions import list_challenges
from core.functions import build_challenge
from core.functions import package_challenge
from core.functions import debug_on
from core.functions import verbose_on
from core.functions import usage
#===============================================================================
#  GLOBALS
#===============================================================================
DEBUG = False
VERBOSE = False
OPTIONS = [
        #['-c', '--configure', 'Create a configuration file for the framework', configure, False],
        ['-n', '--new', 'Create a new challenge', create_challenge, False],
        ['-r', '--remove', 'Delete an existing challenge', delete_challenge, False],
        ['-l', '--list', 'List all challenges', list_challenges, False],
        ['-b', '--build', 'Build a specific challenge or all challenges', build_challenge, False],
        ['-p', '--package', 'Package a specific challenge or all challenges', package_challenge, False],
        ['-d', '--debug', 'Run in debugging mode', debug_on, True],
        ['-v', '--verbose', 'Run in verbose mode', verbose_on, True],
        ['-h', '--help', 'Display help message', usage, False]
    ]
#===============================================================================
#  FUNCTIONS/CLASSES
#===============================================================================
def init(dispatcher):
    Logger.inf('initializing dispatcher...')
    for opt in OPTIONS:
        dispatcher.add(opt[0], opt[3])

def dispatcher_call(dispatcher, options_parser, opt):
    if opt == '-h':
        dispatcher.call(opt, prog=options_parser.prog, options=OPTIONS)
    else:
        dispatcher.call(opt)

def process_options(dispatcher, options_parser):
    processed = False
    dispatch_later = []
    for opt in OPTIONS:
        if options_parser.has_option(opt[0]) or options_parser.has_option(opt[1]):
            if opt[4]:
                dispatcher_call(dispatcher, options_parser, opt[0])
            else:
                dispatch_later.append(opt[0])
    processed = (len(dispatch_later) > 0)
    if processed:
        for opt in dispatch_later:
            dispatcher_call(dispatcher, options_parser, opt)
    return processed

def print_menu():
    print('\n------------------------ PyChallFactory Menu ------------------------\n')
    k = 0
    for opt in OPTIONS:
        k += 1
        print('\t%2d - %s' % (k, opt[2]))
    print('\t Q - Quit\n')
    print('---------------------------------------------------------------------')

def menu(dispatcher, options_parser):
    while True:
        print_menu()
        choice = read_input('What do you want to do ?\n')
        if choice == 'Q':
            break
        else:
            if not choice.isdigit():
                Logger.err("choice must be a digit if not 'Q' !")
                continue
            choice = int(choice, 10)
            if choice > len(OPTIONS) or choice < 1:
                Logger.err("choice must be comprised between 1 and %d or 'Q'" % (len(OPTIONS)))
                continue
            dispatcher_call(dispatcher, options_parser, OPTIONS[choice-1][0])

def sigint_handler(*args):
    print()
    exit(0)

#===============================================================================
#  MAIN SCRIPT
#===============================================================================

if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)
    options_parser = CLIOptionsParser(sys.argv)
    if not options_parser.parse():
        Logger.fat(options_parser.error)
    dispatcher = Dispatcher()
    init(dispatcher)
    if not process_options(dispatcher, options_parser):
        menu(dispatcher, options_parser)
    print('\nSee you soon! :)\n')
    exit(0)