#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : audits.py
# Author             : Podalirius (@podalirius_)
# Date created       : 23 Sep 2022


from ..models import Audit


class audits(object):
    """
    Documentation for class audits
    """

    def __init__(self, api):
        super(audits, self).__init__()
        self.api = api
    
    def list(self):
        if self.api.isLoggedIn():
            return self.api.audits_list()
        else:
            return None

    def create(self, name, language, auditType):
        if self.api.isLoggedIn():
            r = self.api.audit_create(name, language, auditType)
            return Audit(self.api, _id=r['audit']['_id'])
        else:
            return None
