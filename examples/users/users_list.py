#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : users_list.py
# Author             : Podalirius (@podalirius_)
# Date created       : 23 Sep 2022


import pwndocapi

p = pwndocapi.pwndoc("192.168.1.19", 8443, verbose=True)
p.login("username", "password")

# List audit types
results = p.users.list()
print("   [>] Listing users (%d)" % len(results))
for u in results:
    print("     └──> (\x1b[93m%s\x1b[0m) (username:\x1b[95m%s\x1b[0m) \x1b[94m%s %s\x1b[0m" % (u["_id"], u["username"], u["firstname"], u["lastname"]))
