#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : errors.py
# Author             : Podalirius (@podalirius_)
# Date created       : 23 Sep 2022


class PwnDocAPIException(Exception):
    """
    Base class for all PwnDoc API exceptions.
    """
    pass


class MissingTOTP(PwnDocAPIException):
    """
    Exception raised when a TOTP is missing.
    """
    def __init__(self, message, value):
        self.message = message
        self.value = value
        super().__init__(self.message)


class FailedLogin(PwnDocAPIException):
    """
    Exception raised when a login attempt fails.
    """
    def __init__(self, message, value):
        self.message = message
        self.value = value
        super().__init__(self.message)


class FailedConnection(PwnDocAPIException):
    """
    Exception raised when a connection to the API fails.
    """
    def __init__(self, message, value):
        self.message = message
        self.value = value
        super().__init__(self.message)