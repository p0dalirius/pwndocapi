#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : audits_create.py
# Author             : Podalirius (@podalirius_)
# Date created       : 23 Sep 2022


import pwndocapi


p = pwndocapi.pwndoc("192.168.1.19", 8443, verbose=True)
p.login("username", "password")

# List audit types
audit = p.audits.create("PoC Audit", "fr", "TI Externe")
print("audit:", audit)
