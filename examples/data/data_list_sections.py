#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : data_list_sections.py
# Author             : Podalirius (@podalirius_)
# Date created       : 23 Sep 2022


import pwndocapi

p = pwndocapi.pwndoc("192.168.1.19", 8443, verbose=True)
p.login("username", "password")

# List audit types
results = p.data.sections()
print("   [>] List sections (%d)" % len(results))
for l in results:
    print(l)
    #print("     └──> %s-%s" % (l["locale"], l["language"]))
