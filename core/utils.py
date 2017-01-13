#!/usr/bin/env python3
# -!- encoding: utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    utils.py
# date:    2017-01-13
# author:  paul dautry
# purpose:
#       Implements some helpers
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def read_input(prompt, allow_empty=False, expect_digit=False):
    """read_input"""
    uinput = ''
    if not isinstance(prompt, str):
        error('read_input prompt argument must be a string.')
    uinput = input('[?] > ' + prompt)
    while not allow_empty and len(uinput) == 0:
        uinput = input(prompt)
    while expect_digit and not uinput.isdigit():
        uinput = input(prompt)
    if expect_digit:
        uinput = int(uinput, 10)
    return uinput