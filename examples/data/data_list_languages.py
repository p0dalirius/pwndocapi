#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : data_list_languages.py
# Author             : Podalirius (@podalirius_)
# Date created       : 23 Sep 2022


import pwndocapi

p = pwndocapi.pwndoc("192.168.1.19", 8443, verbose=True)
p.login("username", "password")

# List audit types
results = p.data.languages()
print("   [>] List languages (%d)" % len(results))
for l in results:
    print("     └──> (locale:%s) (language:%s)" % (l["locale"], l["language"]))
