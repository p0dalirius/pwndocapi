#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : data.py
# Author             : Podalirius (@podalirius_)
# Date created       : 23 Sep 2022


class data(object):
    """
    Documentation for class data
    """

    def __init__(self, api):
        super(data, self).__init__()
        self.api = api
    
    def languages(self):
        if self.api.isLoggedIn():
            return self.api.data_languages()
        else:
            return None

    def custom_fields(self):
        if self.api.isLoggedIn():
            return self.api.data_custom_fields()
        else:
            return None

    def audit_types(self):
        if self.api.isLoggedIn():
            return self.api.data_audit_types()
        else:
            return None

    def sections(self):
        if self.api.isLoggedIn():
            return self.api.data_sections()
        else:
            return None

    def vulnerability_categories(self):
        if self.api.isLoggedIn():
            return self.api.data_vulnerability_categories()
        else:
            return None