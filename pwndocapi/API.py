#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : API.py
# Author             : Podalirius (@podalirius_)
# Date created       : 23 Sep 2022


import json
import requests

# Disable warings of insecure connection for invalid certificates
requests.packages.urllib3.disable_warnings()
try:
    # Allow use of deprecated and weak cipher methods
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
except AttributeError:
    pass


from .models.Audit import Audit
from .api.errors import MissingTOTP, FailedLogin, FailedConnection


DEBUG = False


class API(object):
    """
    A Python native library to automate reporting vulnerabilities into pwndoc.
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

    def login(self, username, password, totp=""):
        """
        Login to the API.

        This function sends a POST request to the /api/users/token endpoint to login to the API.
        """
        r = self.session.post(
            self.target + "/api/users/token",
            json={"username": username, "password": password, "totpToken": totp},
            verify=False
        )
        jsonresponse = r.json()

        if jsonresponse["status"] == "success":
            if self.verbose:
                print("[>] Successfully logged in.")
            self.user = {
                "token": jsonresponse["datas"]["token"],
                "refreshToken": jsonresponse["datas"]["refreshToken"]
            }
            self.session.cookies.set("token", "JWT%20" + self.user["token"])
            self.loggedin = True

        elif jsonresponse["status"] == "error":
            if self.verbose:
                print("[!] Login error. (%s)" % jsonresponse["datas"])
            self.loggedin = False

        if jsonresponse["datas"] == "Example text about missing TOTP":
            raise MissingTOTP("authentication error", jsonresponse["datas"])
        if jsonresponse["datas"] == "Example text about failed login":
            raise FailedLogin("authentication error", jsonresponse["datas"])
        if jsonresponse["datas"] == "Example text about failed network connection":
            raise FailedConnection("authentication error", jsonresponse["datas"])
            
        return self.loggedin

    # Users ===========================================================================

    def users_list(self):
        """
        Retrieve a list of users.

        This function sends a GET request to the /api/users endpoint to retrieve a list of users.
        It requires the user to be logged in to the API.

        Returns:
            list: A list of users if the request is successful.
            None: If the user is not logged in or the request fails.
        """
        return self.__api_get("/api/users")

    def user_get_by_id(self, _id):
        """
        Retrieve a user by their ID.

        This function sends a GET request to the /api/users/%s endpoint to retrieve a user by their ID.
        It requires the user to be logged in to the API.

        Returns:
            dict: A dictionary representing the user if the request is successful.
            None: If the user is not logged in or the request fails.
        """

        user = None

        # Search for the user in the list of users
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

    def user_get_by_username(self, username):
        """
        Retrieve a user by their username.

        This function sends a GET request to the /api/users/%s endpoint to retrieve a user by their username.
        It requires the user to be logged in to the API.

        Returns:
            dict: A dictionary representing the user if the request is successful.
            None: If the user is not logged in or the request fails.
        """
        return self.__api_get("/api/users/%s" % username)

    def user_update(self, _id, role, totpEnabled, username, firstname, lastname, email, phone):
        """
        Update a user's information.

        This function sends a PUT request to the /api/users/%s endpoint to update a user's information.
        It requires the user to be logged in to the API.

        Returns:
            dict: A dictionary representing the updated user if the request is successful.
            None: If the user is not logged in or the request fails.
        """
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

    def audits_list(self):
        """
        Retrieve a list of audits.

        This function sends a GET request to the /api/audits endpoint to retrieve a list of audits.
        It requires the user to be logged in to the API.

        Returns:
            list: A list of audits if the request is successful.
            None: If the user is not logged in or the request fails.
        """
        return self.__api_get("/api/audits")

    def audits_get_by_id(self, _audit_id):
        """
        Retrieve an audit by its ID.

        This function sends a GET request to the /api/audits/%s endpoint to retrieve an audit by its ID.
        It requires the user to be logged in to the API.

        Returns:
            dict: A dictionary representing the audit if the request is successful.
            None: If the user is not logged in or the request fails.
        """
        return self.__api_get("/api/audits/%s" % _audit_id)

    def audit_add_finding(self, _audit_id, title, vulnType, category, description, observation, remediation, references, remediationComplexity, priority, poc, scope, cvssv3, customFields=[]):
        """
        Add a finding to an audit.

        This function sends a POST request to the /api/audits/%s/findings endpoint to add a finding to an audit.
        It requires the user to be logged in to the API.

        Returns:
            dict: A dictionary representing the added finding if the request is successful.
            None: If the user is not logged in or the request fails.
        """
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
                # "cvssScore": cvssScore,
                # "cvssSeverity": cvssSeverity,
                "poc": poc,
                "scope": scope,
                "customFields": customFields
            }
        )

    def audit_list_findings(self, _audit_id):
        """
        Retrieve a list of findings for an audit.

        This function sends a GET request to the /api/audits/%s/findings endpoint to retrieve a list of findings for an audit.
        It requires the user to be logged in to the API.

        Returns:
            list: A list of findings if the request is successful.
            None: If the user is not logged in or the request fails.
        """
        return self.__api_get("/api/audits/%s/" % _audit_id)["findings"]

    def audit_delete_all_findings(self, _audit_id):
        """
        Delete all findings for an audit.

        This function sends a DELETE request to the /api/audits/%s/findings endpoint to delete all findings for an audit.
        It requires the user to be logged in to the API.

        Returns:
            None: If the user is not logged in or the request fails.
        """
        for finding in self.audit_list_findings(_audit_id):
            self.findings_delete_by_id(_audit_id, finding['_id'])

    def audit_delete_all_findings(self, _audit_id):
        """
        Delete all findings for an audit.

        This function sends a DELETE request to the /api/audits/%s/findings endpoint to delete all findings for an audit.
        It requires the user to be logged in to the API.

        Returns:
            None: If the user is not logged in or the request fails.
        """
        for finding in self.audit_list_findings(_audit_id):
            self.findings_delete_by_id(_audit_id, finding['_id'])

    def audit_create(self, name, language, auditType):
        """
        Create an audit.

        This function sends a POST request to the /api/audits endpoint to create an audit.
        It requires the user to be logged in to the API.

        Returns:
            dict: A dictionary representing the created audit if the request is successful.
            None: If the user is not logged in or the request fails.
        """
        return self.__api_post("/api/audits", jsondata={"name": name, "language": language, "auditType": auditType})

    def audit_delete(self, _audit_id):
        """
        Delete an audit.

        This function sends a DELETE request to the /api/audits/%s endpoint to delete an audit.
        It requires the user to be logged in to the API.

        Returns:
            None: If the user is not logged in or the request fails.
        """
        return self.__api_delete("/api/audits/%s" % _audit_id)

    def audit_update(self, _audit_id):
        """
        Update an audit.

        This function sends a PUT request to the /api/audits/%s endpoint to update an audit.
        It requires the user to be logged in to the API.

        Returns:
            None: If the user is not logged in or the request fails.
        """
        raise NotImplementedError("PUT /api/audits/%s not implemented yet for update")
        return self.__api_put("/api/audits/%s" % _audit_id, jsondata={
            "_id": _audit_id
        })
    
    def audit_get_sections(self, _audit_id):
        """
        List custom sections of the given audit

        This function sends a GET request to the /api/audits/%s/sections/ endpoint to 
        list all the sections of the given audit.
        It requires the user to be logged in to the API.

        Returns:
            None: If the user is not logged in or the request fails.
        """
        #raise NotImplementedError("GET /api/audits/%s/sections not implemented yet for update")
        return self.__api_get("/api/audits/%s/sections" % _audit_id)
    
    def audit_update_custom_field(self, _audit_id, section_id, custom_fields):
        """
        Update custom fields from a section

        This function sends a PUT request to the /api/audits/%s/sections/%s endpoint to update a custom field
        It requires the user to be logged in to the API.

        Returns:
            dict: a list of custom_fields to be added inside 
            None: If the user is not logged in or the request fails.
        """
        #raise NotImplementedError("PUT /api/audits/%s/sections/%s not implemented yet for update")
        jsondata = {"customFields":custom_fields,
                    "field":"test",
                    "name":"test",
                    "_id":section_id
                }
        return self.__api_put("/api/audits/%s/sections/%s" % (_audit_id,section_id), jsondata=jsondata)


    def audit_list_hosts(self, _audit_id):
        """
        Retrieve a list of hosts for an audit.

        This function sends a GET request to the /api/audits/%s/network endpoint to retrieve a list of hosts for an audit.
        It requires the user to be logged in to the API.

        Returns:
            list: A list of findings if the request is successful.
            None: If the user is not logged in or the request fails.
        """
        return self.__api_get("/api/audits/%s/network" % _audit_id)

    def audit_nmap_import(self, _audit_id, datas):
        """
        import an nmap report.

        This function sends a PUT request to the /api/audits/%s/network endpoint to update an audit.
        It requires the user to be logged in to the API.

        Returns:
            None: If the user is not logged in or the request fails.
        """
        #raise NotImplementedError("PUT /api/audits/%s/network not implemented yet for update")
        return self.__api_put("/api/audits/%s/network" % _audit_id,datas)
        
    # Data ============================================================================

    def data_languages(self):
        """
        Retrieve a list of languages.

        This function sends a GET request to the /api/data/languages endpoint to retrieve a list of languages.
        It requires the user to be logged in to the API.

        Returns:
            list: A list of languages if the request is successful.
            None: If the user is not logged in or the request fails.
        """
        return self.__api_get("/api/data/languages")
    
    def data_language_create(self, locale, language):
        """
        Create a new language.

        This function sends a POST request to the "/api/data/languages" endpoint to create a new language entry,
        specifying the desired locale code and language name.
        The user must be authenticated to perform this action.

        Returns:
            dict: A dictionary with information about the created language if the request is successful.
            None: If the request fails or the user is not logged in.
        """
        return self.__api_post("/api/data/languages", jsondata={"locale":locale,"language": language})

    def data_custom_fields(self):
        """
        Retrieve a list of custom fields.

        This function sends a GET request to the /api/data/custom-fields endpoint to retrieve a list of custom fields.
        It requires the user to be logged in to the API.

        Returns:
            list: A list of custom fields if the request is successful.
            None: If the user is not logged in or the request fails.
        """
        return self.__api_get("/api/data/custom-fields")

    def data_custom_field_create(self, fieldType, label, display, displaySub, size, offset, required, description, text, options, position):
        """
        Create a new custom field.

        This function sends a POST request to the "/api/data/custom-fields" endpoint to create a new custom field
        with the specified parameters. It requires the user to be authenticated.

        Returns:
            dict: A dictionary with information about the created custom field if the request is successful.
            None: If the request fails or the user is not logged in.
        """
        jsondata = {
                    "fieldType": fieldType,
                    "label": label,
                    "display": display,
                    "displaySub": displaySub,
                    "size": size,
                    "offset": offset,
                    "required": required,
                    "description": description,
                    "text": text,
                    "options": options,
                    "position": position
                }
        return self.__api_post("/api/data/custom-fields", jsondata=jsondata)

    def data_audit_types(self):
        """
        Retrieve a list of audit types.

        This function sends a GET request to the /api/data/audit-types endpoint to retrieve a list of audit types.
        It requires the user to be logged in to the API.

        Returns:
            list: A list of audit types if the request is successful.
            None: If the user is not logged in or the request fails.
        """
        return self.__api_get("/api/data/audit-types")

    def data_audit_type_create(self, name, templates,sections,hidden):
        """
        Create a new audit type.

        This function sends a POST request to the "/api/data/audit-types" endpoint to create a new audit type
        with the specified parameters. The user must be authenticated.

        Returns:
            dict: A dictionary containing details about the created audit type if the request is successful.
            None: If the request fails or the user is not logged in.
        """
        return self.__api_post("/api/data/audit-types", jsondata={"name":name,"templates": templates,"sections":sections,"hidden": hidden})

    def data_sections(self):
        """
        Retrieve a list of sections.

        This function sends a GET request to the /api/data/sections endpoint to retrieve a list of sections.
        It requires the user to be logged in to the API.

        Returns:
            list: A list of sections if the request is successful.
            None: If the user is not logged in or the request fails.
        """
        return self.__api_get("/api/data/sections")
    
    def data_section_create(self, field, name, locale, text, icon):
        """
        Create a new section.

        This function sends a POST request to the "/api/data/sections" endpoint to create a new section
        with the specified parameters. The user must be authenticated.

        Returns:
            dict: A dictionary containing details about the created section if the request is successful.
            None: If the request fails or the user is not logged in.
        """
        return self.__api_post("/api/data/sections", jsondata={"field":field,"name": name,"locale":locale,"text": text,"icon":icon})

    def data_vulnerability_categories(self):
        """
        Retrieve a list of vulnerability categories.

        This function sends a GET request to the /api/data/vulnerability-categories endpoint to retrieve a list of vulnerability categories.
        It requires the user to be logged in to the API.

        Returns:
            list: A list of vulnerability categories if the request is successful.
            None: If the user is not logged in or the request fails.
        """
        return self.__api_get("/api/data/vulnerability-categories")
        
    def data_vulnerability_category_create(self, name):
        """
        Create a new vulnerability category.

        This function sends a POST request to the "/api/data/vulnerability-categories" endpoint to create
        a new vulnerability category with the specified name. The user must be authenticated.

        Returns:
            dict: A dictionary containing information about the created vulnerability category if the request is successful.
            None: If the request fails or the user is not logged in.
        """
        return self.__api_post("/api/data/vulnerability-categories", jsondata={"name": name})
    
    def data_vulnerability_type(self):
        """
        Retrieve a list of vulnerability types.

        This function sends a GET request to the "/api/data/vulnerability-types" endpoint to retrieve 
        a list of available vulnerability types. The user must be authenticated to access this endpoint.

        Returns:
            list: A list of vulnerability types if the request is successful.
            None: If the user is not logged in or if the request fails.
        """
        return self.__api_get("/api/data/vulnerability-types")

    def data_vulnerability_type_create(self, name, locale):
        """
        Create a new vulnerability type.

        This function sends a POST request to the "/api/data/vulnerability-types" endpoint to create
        a new vulnerability type with the specified parameters. The user must be authenticated.

        Returns:
            dict: A dictionary containing details about the created vulnerability type if the request is successful.
            None: If the request fails or the user is not logged in.
        """
        return self.__api_post("/api/data/vulnerability-types", jsondata={"name": name,"locale": locale})
    
    # Findings =================================================================

    def findings_get_by_id(self, _audit_id, _finding_id):
        """
        Retrieve a finding by its ID.

        This function sends a GET request to the /api/audits/%s/findings/%s endpoint to retrieve a finding by its ID.
        It requires the user to be logged in to the API.

        Returns:
            dict: A dictionary representing the finding if the request is successful.
            None: If the user is not logged in or the request fails.
        """
        return self.__api_get("/api/audits/%s/findings/%s" % (_audit_id, _finding_id))

    def findings_delete_by_id(self, _audit_id, _finding_id):
        """
        Delete a finding by its ID.

        This function sends a DELETE request to the /api/audits/%s/findings/%s endpoint to delete a finding by its ID.
        It requires the user to be logged in to the API.

        Returns:
            None: If the user is not logged in or the request fails.
        """
        return self.__api_delete("/api/audits/%s/findings/%s" % (_audit_id, _finding_id))

    # Vulnerabilities =================================================================

    def vulnerabilities_list(self, lang):
        """
        Retrieve a list of vulnerabilities.

        This function sends a GET request to the /api/vulnerabilities/%s endpoint to retrieve a list of vulnerabilities.
        It requires the user to be logged in to the API.

        Returns:
            list: A list of vulnerabilities if the request is successful.
            None: If the user is not logged in or the request fails.
        """
        return self.__api_get("/api/vulnerabilities/%s" % lang)

    # Templates ===============================================================
    def get_templates(self):
        """
        Retrieve the Word templates uploaded to the pwndoc instance

        This function sends a GET request to the /api/templates endpoint to retrieve a list of word templates.
        It requires the user to be logged in to the API.

        Returns:
            list: List of templates
            None: If the user is not logged in or the request fails.
        """
        return self.__api_get("/api/templates")
    
    def upload_template(self, template_name, template_content_base64, template_file_extension):
        """
        Upload the given Word templates in base64

        This function sends a POST request to the /api/templates endpoint to upload word templates.
        It requires the user to be logged in to the API.

        Returns:
            dict: A dictionary representing the finding if the request is successful.
            None: If the user is not logged in or the request fails.
        """
        jsondata = {
                    "name": template_name,
                    "file": template_content_base64,
                    "ext": template_file_extension,
                }
        return self.__api_post("/api/templates", jsondata=jsondata)

    # Internal Methods =========================================================

    def __api_get(self, endpoint):
        """
        Internal method to send a GET request to the API.

        This method sends a GET request to the specified endpoint and returns the response data.
        """
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
        """
        Internal method to send a PUT request to the API.

        This method sends a PUT request to the specified endpoint with the provided JSON data and returns the response data.
        """
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
        """
        Internal method to send a POST request to the API.

        This method sends a POST request to the specified endpoint with the provided JSON data and returns the response data.
        """
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
        """
        Internal method to send a DELETE request to the API.

        This method sends a DELETE request to the specified endpoint and returns the response data.
        """
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
        """
        Check if the user is logged in.

        This method returns the value of the loggedin attribute.
        """
        return self.loggedin
