#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : pwndoc.py
# Author             : Podalirius (@podalirius_)
# Date created       : 23 Sep 2022


from .API import API
from .api import *


class pwndoc(object):
    """
    Documentation for class pwndoc
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

    def login(self, username, password):
        return self.api.login(username, password)

    def isLoggedIn(self):
        return self.api.loggedin