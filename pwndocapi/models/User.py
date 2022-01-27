#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : User.py
# Author             : Podalirius (@podalirius_)
# Date created       : 23 Sep 2022


class User(object):
    """
    Documentation for class User
    """

    def __init__(self, api, _id):
        super(User, self).__init__()
        self.data = {}
        self.api = api
        self._id = _id
        self.__load()
        #
        self.username = (self.data["username"] if "username" in self.data.keys() else None)
        self.role = (self.data["role"] if "role" in self.data.keys() else None)
        self.totpEnabled = (self.data["totpEnabled"] if "totpEnabled" in self.data.keys() else None)
        self.username = (self.data["username"] if "username" in self.data.keys() else None)
        self.firstname = (self.data["firstname"] if "firstname" in self.data.keys() else None)
        self.lastname = (self.data["lastname"] if "lastname" in self.data.keys() else None)
        self.email = (self.data["email"] if "email" in self.data.keys() else None)
        self.phone = (self.data["phone"] if "phone" in self.data.keys() else None)

    def delete(self):
        self.api.user_delete(self._id)

    ## Data =========================================================

    # role ====

    def set_role(self, value):
        self.role = value
        self.__update()

    def get_role(self):
        self.__load()
        return self.role

    # totpEnabled ====

    def set_totpEnabled(self, value: bool):
        self.totpEnabled = bool(value)
        self.__update()

    def get_totpEnabled(self):
        self.__load()
        return self.totpEnabled

    # username ====

    def set_username(self, value):
        self.username = value
        self.__update()

    def get_username(self):
        self.__load()
        return self.username

    # firstname ====

    def set_firstname(self, value):
        self.firstname = value
        self.__update()

    def get_firstname(self):
        self.__load()
        return self.firstname

    # lastname ====

    def set_lastname(self, value):
        self.lastname = value
        self.__update()

    def get_lastname(self):
        self.__load()
        return self.lastname

    # email ====

    def set_email(self, value):
        self.email = value
        self.__update()

    def get_email(self):
        self.__load()
        return self.email

    # phone ====

    def set_phone(self, value):
        self.phone = value
        self.__update()

    def get_phone(self):
        self.__load()
        return self.phone

    ##

    def __load(self):
        self.data = self.api.user_get_by_id(self._id)

    def __update(self):
        self.api.user_update(self._id, self.role, self.totpEnabled, self.username, self.firstname, self.lastname, self.email, self.phone)
        self.__load()

    def __repr__(self):
        return "<User username='%s', id='%s'>" % (self.data["username"], self.data["_id"])
