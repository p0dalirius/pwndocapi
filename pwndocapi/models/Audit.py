#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : Audit.py
# Author             : Podalirius (@podalirius_)
# Date created       : 23 Sep 2022


from .User import User
from .Finding import Finding
from .AuditError import AuditError


class Audit(object):
    """
    Documentation for class Audit
    """

    def __init__(self, api, _id):
        super(Audit, self).__init__()
        self.data = {}
        self.api = api
        self._id = _id
        self.__load()

    def delete(self):
        """
        Delete an audit.

        This function sends a DELETE request to the /api/audits/%s endpoint to delete an audit.
        """
        self.api.audits_delete(self._id)

    def add_finding(self, title, vulnType, category, description, observation, remediation, references, remediationComplexity, priority, poc, scope, cvssv3, customFields=[]):
        """
        Add a finding to an audit.

        This function sends a POST request to the /api/audits/%s/findings endpoint to add a finding to an audit.
        """
        scope = "<ul>" + "".join(["<li><p>%s</p></li>" % vt for vt in scope]) + "</ul>"

        self.api.audit_add_finding(
            self._id,
            title=title,
            vulnType=vulnType,
            category=category,
            description=description,
            observation=observation,
            remediation=remediation,
            references=references,
            remediationComplexity=remediationComplexity,
            priority=priority,
            poc=poc,
            scope=scope,
            cvssv3=cvssv3,
            # cvssScore=cvssScore,
            # cvssSeverity=cvssSeverity,
            customFields=customFields
        )

    def delete_all_findings(self):
        """
        Delete all findings from an audit.

        This function sends a DELETE request to the /api/audits/%s/findings endpoint to delete all findings from an audit.
        """
        self.api.audit_delete_all_findings(self._id)

    ## Data =========================================================

    # Company ====

    def set_company(self):
        """
        Set the company for an audit.

        This function sends a PUT request to the /api/audits/%s/company endpoint to set the company for an audit.
        """
        pass

    def get_company(self):
        """
        Get the company for an audit.

        This function sends a GET request to the /api/audits/%s/company endpoint to get the company for an audit.
        """
        pass

    # Client ====

    def set_client(self):
        """
        Set the client for an audit.

        This function sends a PUT request to the /api/audits/%s/client endpoint to set the client for an audit.
        """
        pass

    def get_client(self):
        """
        Get the client for an audit.

        This function sends a GET request to the /api/audits/%s/client endpoint to get the client for an audit.
        """
        pass

    # Start date ====

    def set_start_date(self):
        """
        Set the start date for an audit.

        This function sends a PUT request to the /api/audits/%s/startDate endpoint to set the start date for an audit.
        """
        pass

    def get_start_date(self):
        """
        Get the start date for an audit.

        This function sends a GET request to the /api/audits/%s/startDate endpoint to get the start date for an audit.
        """
        pass

    # End date ====

    def set_end_date(self):
        """
        Set the end date for an audit.

        This function sends a PUT request to the /api/audits/%s/endDate endpoint to set the end date for an audit.
        """
        pass

    def get_end_date(self):
        """
        Get the end date for an audit.

        This function sends a GET request to the /api/audits/%s/endDate endpoint to get the end date for an audit.
        """
        pass

    # Reporting date ====

    def set_reporting_date(self):
        """
        Set the reporting date for an audit.

        This function sends a PUT request to the /api/audits/%s/reportingDate endpoint to set the reporting date for an audit.
        """
        pass

    def get_reporting_date(self):
        """
        Get the reporting date for an audit.

        This function sends a GET request to the /api/audits/%s/reportingDate endpoint to get the reporting date for an audit.
        """
        pass

    ##

    def __load(self):
        self.data = self.api.audits_get_by_id(self._id)
        if self.data is None:
            raise AuditError("Audit not found or Insufficient Privileges")
        #
        self.name = self.data["name"]
        self.language = self.data["language"]
        self.auditType = self.data["auditType"]
        self.collaborators = [User(self.api, u["_id"]) for u in self.data["collaborators"]]
        self.reviewers = [User(self.api, u["_id"]) for u in self.data["reviewers"]]
        self.creator = User(self.api, self.data["creator"]["_id"])
        self.findings = [Finding(self.api, self._id, f["_id"]) for f in self.api.audit_list_findings(self._id)]

    def __update(self):
        # self.api.audit_update(self._id, self.role, self.totpEnabled, self.username, self.firstname, self.lastname, self.email, self.phone)

        d = {
            "_id": self._id,
            "name": self.name,
            "language": self.language,
            "auditType": self.auditType,
            "collaborators": [
                {"_id": u._id, "username": u.get_username(), "firstname": u.get_firstname(), "lastname": u.get_lastname()}
                for u in self.collaborators
            ],
            "reviewers": [],
            "creator": {
                "_id": self.creator._id, "username": self.creator.get_username(), "firstname": self.creator.get_firstname(), "lastname": self.creator.get_lastname()
            },
            "customFields": [],
            "template": "61eac953c4f2a40011704dc5",
            "scope": self.scope,
            "client": self.client,
            "company": {
                "_id": "61ee740be5db6c00116efff7",
                "name": "Test company",
                "createdAt": "2022-01-24T09:40:27.730Z",
                "updatedAt": "2022-01-24T09:42:23.682Z",
                "__v": 0,
                "logo": "data:image/png;base64,iVBORw="
            }
        }
        self.__load()

    def __repr__(self):
        return "<Audit name='%s', id='%s'>" % (self.data["name"], self.data["_id"])
