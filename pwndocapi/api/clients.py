#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : clients.py
# Author             : Podalirius (@podalirius_)
# Date created       : 23 Sep 2022


class clients(object):
    """
    A Python native library to automate reporting vulnerabilities into pwndoc.
    """

    def __init__(self, api):
        super(clients, self).__init__()
        self.api = api
        
