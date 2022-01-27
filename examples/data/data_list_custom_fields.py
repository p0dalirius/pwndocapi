#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : data_list_custom_fields.py
# Author             : Podalirius (@podalirius_)
# Date created       : 23 Sep 2022


import pwndocapi

p = pwndocapi.pwndoc("192.168.1.19", 8443, verbose=True)
p.login("username", "password")

# List custom fields
results = p.data.custom_fields()
print("[>] List custom fields (%d)" % len(results))
for cf in results:
    print(cf)