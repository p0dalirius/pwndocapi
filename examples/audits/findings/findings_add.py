#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : findings_add.py
# Author             : Podalirius (@podalirius_)
# Date created       : 23 Sep 2022


import pwndocapi
from pwndocapi.models import Audit


if __name__ == '__main__':
    p = pwndocapi.pwndoc("192.168.1.19", 8443, verbose=True)
    p.login("username", "password")

    audit = Audit(p.api, "621f45d19f5a2500137b64eb")
    print("[>] Using audit:", audit)

    audit.add_finding("title1", "vulnType", "description", "observation", "remediation", "references", "CVSS:3.0/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:L/A:N", "0", "High", "category")

    audit.add_finding("title2", "vulnType", "description", "observation", "remediation", "references", "CVSS:3.0/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:L/A:N", "0", "High", "category")
