#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : API.py
# Author             : Podalirius (@podalirius_)
# Date created       : 23 Sep 2022


import json
import requests

# Disable warings of insecure connection for invalid certificates
requests.packages.urllib3.disable_warnings()
# Allow use of deprecated and weak cipher methods
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
except AttributeError:
    pass


from .models.Audit import Audit


DEBUG = False


class API(object):
    """
    Documentation for class API
    """

    def __init__(self, host, port=443, ssl=True, verbose=True):
        super(API, self).__init__()
        if ssl == True:
            self.target = "https://%s:%d" % (host, port)
        else:
            self.target = "http://%s:%d" % (host, port)
        self.session = requests.Session()
        self.loggedin = False
        self.verbose = verbose
        self.user = {"token": "", "refreshToken": ""}

    def login(self, username, password):
        r = self.session.post(
            self.target + "/api/users/token",
            json={"username": username, "password": password, "totpToken": ""},
            verify=False
        )
        if r.json()["status"] == "success":
            if self.verbose:
                print("[>] Successfully logged in.")
            self.user = {
                "token": r.json()["datas"]["token"],
                "refreshToken": r.json()["datas"]["refreshToken"]
            }
            self.session.cookies.set("token", "JWT%20" + self.user["token"])
            self.loggedin = True
        elif r.json()["status"] == "error":
            if self.verbose:
                print("[!] Login error. (%s)" % r.json()["status"])
            self.loggedin = False
        return self.loggedin

    # Users ===========================================================================

    def users_list(self):  # ok
        return self.__api_get("/api/users")

    def user_get_by_id(self, _id):  # ok
        user = None
        for u in self.users_list():
            if u['_id'] == _id:
                user = u
                break
        if user is None:
            if self.verbose:
                print("[!] API error. (Unknown user id %s)" % _id)
            return None
        else:
            return self.user_get_by_username(user["username"])

    def user_get_by_username(self, username):  # ok
        return self.__api_get("/api/users/%s" % username)

    def user_update(self, _id, role, totpEnabled, username, firstname, lastname, email, phone):
        return self.__api_put("/api/users/%s" % _id, jsondata={
            "role": role,
            "totpEnabled": totpEnabled,
            "_id": _id,
            "username": username,
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "phone": phone
        })

    # Audits ==========================================================================

    def audits_list(self):  # ok
        return self.__api_get("/api/audits")

    def audits_get_by_id(self, _audit_id):  # ok
        return self.__api_get("/api/audits/%s" % _audit_id)

    def audit_add_finding(self, _audit_id, title, vulnType, category, description, observation, remediation, references, remediationComplexity, priority, poc, scope, cvssv3, cvssScore, cvssSeverity, customFields=[]):
        return self.__api_post(
            "/api/audits/%s/findings" % _audit_id,
            jsondata={
                "title": title,
                "vulnType": vulnType,
                "category": category,
                "description": description,
                "observation": observation,
                "remediation": remediation,
                "references": references,
                "remediationComplexity": remediationComplexity,
                "priority": priority,
                "cvssv3": cvssv3,
                "cvssScore": cvssScore,
                "cvssSeverity": cvssSeverity,
                "poc": poc,
                "scope": scope,
                "customFields": customFields
            }
        )

    def audit_list_findings(self, _audit_id):
        return self.__api_get("/api/audits/%s/" % _audit_id)["findings"]

    def audit_delete_all_findings(self, _audit_id):
        for finding in self.audit_list_findings(_audit_id):
            self.findings_delete_by_id(_audit_id, finding['_id'])

    def audit_delete_all_findings(self, _audit_id):
        for finding in self.audit_list_findings(_audit_id):
            self.findings_delete_by_id(_audit_id, finding['_id'])

    def audit_create(self, name, language, auditType):  # ok
        return self.__api_post("/api/audits", jsondata={"name": name, "language": language, "auditType": auditType})

    def audit_delete(self, _audit_id):  # ok
        return self.__api_delete("/api/audits/%s" % _audit_id)

    def audit_update(self, _audit_id):
        raise NotImplementedError("PUT /api/audits/%s not implemented yet for update")
        return self.__api_put("/api/audits/%s" % _audit_id, jsondata={
            "_id": _audit_id
        })

    # Data ============================================================================

    def data_languages(self):
        return self.__api_get("/api/data/languages")

    def data_custom_fields(self):
        return self.__api_get("/api/data/custom-fields")

    def data_audit_types(self):
        return self.__api_get("/api/data/audit-types")

    def data_sections(self):
        return self.__api_get("/api/data/sections")

    def data_vulnerability_categories(self):
        return self.__api_get("/api/data/vulnerability-categories")

    # Findings ==

    def findings_get_by_id(self, _audit_id, _finding_id):  # ok
        return self.__api_get("/api/audits/%s/findings/%s" % (_audit_id, _finding_id))

    def findings_delete_by_id(self, _audit_id, _finding_id):  # ok
        return self.__api_delete("/api/audits/%s/findings/%s" % (_audit_id, _finding_id))

    # Vulnerabilities =================================================================
    def vulnerabilities_list(self, lang):
        return self.__api_get("/api/vulnerabilities/%s" % lang)

    # Internal Methods =========================================================

    def __api_get(self, endpoint):
        r = self.session.get(self.target + endpoint, verify=False)
        if DEBUG == True:
            print("[debug] GET %s" % endpoint)
            print(json.dumps(r.json(), indent=4))
        if r.json()["status"] == "success":
            return r.json()["datas"]
        elif r.json()["status"] == "error":
            if self.verbose:
                print("[!] API error. (%s)" % r.json()["datas"])

    def __api_put(self, endpoint, jsondata):
        r = self.session.put(self.target + endpoint, json=jsondata, verify=False)
        if DEBUG == True:
            print("[debug] PUT %s" % endpoint)
            print(json.dumps(r.json(), indent=4))
        if r.json()["status"] == "success":
            return r.json()["datas"]
        elif r.json()["status"] == "error":
            if self.verbose:
                print("[!] API error. (%s)" % r.json()["datas"])

    def __api_post(self, endpoint, jsondata):
        r = self.session.post(self.target + endpoint, json=jsondata, verify=False)
        if DEBUG == True:
            print("[debug] POST %s" % endpoint)
            print(json.dumps(r.json(), indent=4))
        if r.json()["status"] == "success":
            return r.json()["datas"]
        elif r.json()["status"] == "error":
            if self.verbose:
                print("[!] API error. (%s)" % r.json()["datas"])

    def __api_delete(self, endpoint):
        r = self.session.delete(self.target + endpoint, verify=False)
        if DEBUG == True:
            print("[debug] DELETE %s" % endpoint)
            print(json.dumps(r.json(), indent=4))
        if r.json()["status"] == "success":
            return r.json()["datas"]
        elif r.json()["status"] == "error":
            if self.verbose:
                print("[!] API error. (%s)" % r.json()["datas"])

    # Methods =========================================================

    def isLoggedIn(self):
        return self.loggedin
