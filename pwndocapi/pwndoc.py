#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : pwndoc.py
# Author             : Podalirius (@podalirius_)
# Date created       : 23 Sep 2022


from .API import API
from .api import *


class pwndoc(object):
    """
    A Python native library to automate reporting vulnerabilities into pwndoc.
    """

    def __init__(self, host, port=443, verbose=True):
        super(pwndoc, self).__init__()
        self.verbose = verbose
        self.api = API(host, port, verbose=verbose)
        #
        self.audits = audits(self.api)
        self.clients = clients(self.api)
        self.companies = companies(self.api)
        self.data = data(self.api)
        self.users = users(self.api)
        self.vulnerabilities = vulnerabilities(self.api)

    def login(self, username, password):
        """
        Login to the API.

        This function sends a POST request to the /api/users/token endpoint to login to the API.
        """
        return self.api.login(username, password)

    def isLoggedIn(self):
        """
        Check if the user is logged in.

        This function returns the value of the loggedin attribute.
        """
        return self.api.loggedin
