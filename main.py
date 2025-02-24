#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : main.py
# Author             : Podalirius (@podalirius_)
# Date created       : 23 Sep 2022


import pwndocapi
import argparse


def parseArgs():
    parser = argparse.ArgumentParser(description="Description message")

    parser.add_argument("-u", "--username", default=None, required=True, help='Pwndoc username')
    parser.add_argument("-p", "--password", default=None, required=True, help='Pwndoc password')
    parser.add_argument("-H", "--host", default=None, required=True, help='Pwndoc ip')
    parser.add_argument("-P", "--port", default=8443, required=False, help='Pwndoc port')
    parser.add_argument("-v", "--verbose", default=False, action="store_true", help='Verbose mode. (default: False)')
    
    return parser.parse_args()


if __name__ == '__main__':
    options = parseArgs()

    p = pwndocapi.pwndoc(options.host, options.port, verbose=options.verbose)
    p.login(options.username, options.password)

    # List audit types
    results = p.audits.create("PoC Audit", "fr", "TI Externe")
    print(results)
