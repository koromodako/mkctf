#!/usr/bin/env python3
# -!- encoding:utf8 -!-
'''
file:    main.py
date:    2018-07-31
author:  paul dautry
purpose:
      This is a framework designed to create challenges and maintain them.
      Entry point script.
'''
#===============================================================================
#  IMPORTS
#===============================================================================
from sys import stderr
from json import dumps
from signal import SIGINT
from asyncio import get_event_loop
from mkctf import __banner__
from mkctf.api import MKCTFAPI
from mkctf.helper.log import app_log, enable_debug, disable_color, disable_logging
# =============================================================================
#  FUNCTIONS
# =============================================================================
def sigint_handler():
    '''Handles user interrupt signal
    '''
    app_log.warning("\nOuch... you just killed me... (x_x)")
    loop = get_event_loop()
    loop.stop()
    loop.close()

async def main():
    '''Main function
    '''
    stderr.write(__banner__)
    ns = MKCTFAPI.parse_args()

    ns.debug, ns.quiet, ns.no_color

    enable_debug(ns.debug)
    if ns.no_color:
        disable_color()
    if ns.quiet:
        disable_logging()

    api = MKCTFAPI(ns.repo_root)

    success = await api.perform(ns)

    if isinstance(success, dict):
        print(dumps(success))
        success = True

    return 0 if success else 1

def app():
    '''mkctf-cli script entry point
    '''
    loop = get_event_loop()
    loop.add_signal_handler(SIGINT, sigint_handler)
    loop.run_until_complete(main())
# =============================================================================
#  SCRIPT
# =============================================================================
if __name__ == '__main__':
    app()
