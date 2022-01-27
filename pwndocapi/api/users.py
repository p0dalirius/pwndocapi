#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : users.py
# Author             : Podalirius (@podalirius_)
# Date created       : 23 Sep 2022


from pwndocapi.models import Audit


class users(object):
    """
    Documentation for class users
    """

    def __init__(self, api):
        super(users, self).__init__()
        self.api = api
    
    def list(self):
        if self.api.isLoggedIn():
            return self.api.users_list()
        else:
            return None

    def create(self, name, language, auditType):
        if self.api.isLoggedIn():
            r = self.api.users_create(name, language, auditType)
            return Audit(self.api, _id=r['audit']['_id'])
        else:
            return None
