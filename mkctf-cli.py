#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    mkctf-cli.py
# date:    2017-01-13
# author:  paul dautry
# purpose:
#       This is a framework designed to create challenges and maintain them.
#       Entry point script.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#===============================================================================
#  IMPORTS
#===============================================================================
from json import dumps
from mkctf import MKCTFAPI
from signal import signal, SIGINT
from asyncio import get_event_loop
# =============================================================================
#  GLOBAL
# =============================================================================
loop = get_event_loop()
# =============================================================================
#  FUNCTIONS
# =============================================================================

def sigint_handler(*args):
    """Handles user interrupt signal

    Arguments:
        *args {tuple} -- [description]
    """
    print("\nOuch... that's harsh you know... :/")
    exit(2)

async def main():
    """Entry point
    """
    signal(SIGINT, sigint_handler)

    ns = MKCTFAPI.parse_args()

    api = MKCTFAPI(ns.repo_root, ns.debug, ns.quiet, ns.no_color)

    success = await api.perform(ns)

    if isinstance(success, dict):
        print(dumps(success))
        success = True

    exit(0 if success else 1)
# =============================================================================
#  SCRIPT
# =============================================================================
if __name__ == '__main__':
    loop.run_until_complete(main())
