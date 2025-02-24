#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : vulnerabilities.py
# Author             : Podalirius (@podalirius_)
# Date created       : 23 Sep 2022


class vulnerabilities(object):
    """
    Documentation for class vulnerabilities
    """

    def __init__(self, api):
        super(vulnerabilities, self).__init__()
        self.api = api
    
    def list(self, lang):
        """
        List all vulnerabilities.

        This function sends a GET request to the /api/vulnerabilities endpoint to list all vulnerabilities.
        """
        if self.api.isLoggedIn():
            return self.api.vulnerabilities_list(lang)
        else:
            return None