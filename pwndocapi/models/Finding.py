#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : Finding.py
# Author             : Podalirius (@podalirius_)
# Date created       : 23 Sep 2022


class Finding(object):
    """
    Documentation for class Finding
    """

    def __init__(self, api, _audit_id, _id):
        super(Finding, self).__init__()
        self.data = {}
        self.api = api
        self._audit_id = _audit_id
        self._id = _id
        self.__load()

    ##

    def __load(self):
        self.data = self.api.findings_get_by_id(self._audit_id, self._id)

        self.title = (self.data["title"] if "title" in self.data.keys() else None)
        self.vulnType = (self.data["vulnType"] if "vulnType" in self.data.keys() else None)
        self.description = (self.data["description"] if "description" in self.data.keys() else None)
        self.observation = (self.data["observation"] if "observation" in self.data.keys() else None)
        self.remediation = (self.data["remediation"] if "remediation" in self.data.keys() else None)
        self.references = (self.data["references"] if "references" in self.data.keys() else None)
        self.cvssv3 = (self.data["cvssv3"] if "cvssv3" in self.data.keys() else None)
        self.cvssScore = (self.data["cvssScore"] if "cvssScore" in self.data.keys() else None)
        self.cvssSeverity = (self.data["cvssSeverity"] if "cvssSeverity" in self.data.keys() else None)
        self.category = (self.data["category"] if "category" in self.data.keys() else None)
        self.customFields = (self.data["customFields"] if "customFields" in self.data.keys() else None)

    def __update(self):
        d = {
            "title": self.title,
            "vulnType": self.vulnType,
            "description": self.description,
            "observation": self.observation,
            "remediation": self.remediation,
            "references": self.references,
            "cvssv3": self.cvssv3,
            "cvssScore": self.cvssScore,
            "cvssSeverity": self.cvssSeverity,
            "category": self.category,
            "customFields": self.customFields
        }
        self.__load()
