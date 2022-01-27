#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : data_list_audit_types.py
# Author             : Podalirius (@podalirius_)
# Date created       : 23 Sep 2022


import pwndocapi

p = pwndocapi.pwndoc("192.168.1.19", 8443, verbose=True)
p.login("username", "password")

# List audit types
results = p.data.audit_types()
print("   [>] List audit (%d)" % len(results))
for audit in results:
    print(audit)
    print("     └──> %s" % audit["name"])
    for t in audit["templates"]:
        print("        └──> (%s) %s" % (t["locale"], t["template"]))