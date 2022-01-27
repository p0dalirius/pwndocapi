#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : audits_list.py
# Author             : Podalirius (@podalirius_)
# Date created       : 23 Sep 2022


import pwndocapi

p = pwndocapi.pwndoc("192.168.1.19", 8443, verbose=True)
p.login("username", "password")

# List audit types
results = p.audits.list()
print("   [>] Listing audits (%d)" % len(results))
for audit in results:
    print("     └──> (\x1b[93m%s\x1b[0m) (lang:\x1b[95m%s\x1b[0m) \x1b[94m%s\x1b[0m" % (audit["_id"], audit["language"], audit["name"]))
