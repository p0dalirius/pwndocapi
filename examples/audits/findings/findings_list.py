#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : findings_list.py
# Author             : Podalirius (@podalirius_)
# Date created       : 23 Sep 2022


import pwndocapi
from pwndocapi.models import Audit


p = pwndocapi.pwndoc("192.168.1.19", 8443, verbose=True)
p.login("username", "password")

audit = Audit(p.api, "61f290a33cda22001122b69f")
print("audit:", audit)

print("   [>] Listing audit findings")
for f in audit.findings:
    print("     └──> (\x1b[93m%s\x1b[0m) \x1b[94m%s\x1b[0m" % (f._id, f.title))