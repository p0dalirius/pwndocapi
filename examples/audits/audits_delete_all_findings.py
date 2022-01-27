#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : audits_delete_all_findings.py
# Author             : Podalirius (@podalirius_)
# Date created       : 23 Sep 2022


from pwndocapi.models import Audit
import pwndocapi

p = pwndocapi.pwndoc("192.168.1.19", 8443, verbose=True)
p.login("username", "password")
audit = Audit(p.api, "621f45d19f5a2500137b64eb")

audit.delete_all_findings()
