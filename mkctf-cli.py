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
import json
import signal
from mkctf import MKCTFAPI
# =============================================================================
#  FUNCTIONS
# =============================================================================
##
## @brief      SIGINT handler
##
## @param      args  The arguments
##
def sigint_handler(*args):
    print("\nOuch... that's harsh you know... :/")
    exit(2)
##
## @brief      Entry point
##
def main():
    signal.signal(signal.SIGINT, sigint_handler)

    ns = MKCTFAPI.parse_args()

    api = MKCTFAPI(ns.repo_root, ns.debug, ns.quiet, ns.no_color)

    success = api.perform(ns)

    if isinstance(success, dict):
        print(json.dumps(success))
        success = True

    exit(0 if success else 1)
# =============================================================================
#  SCRIPT
# =============================================================================
if __name__ == '__main__':
    main()
