#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'moonshawdo@gamil.com'
"""自动读取当前目录的README.md，并把IP自动组合成IP段范围"""

import os
import sys
import re

g_ipcheck = re.compile(r'"http://(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"')


def from_string(s):
    """Convert dotted IPv4 address to integer."""
    return reduce(lambda a, b: a << 8 | b, map(int, s.split(".")))


def to_string(ip):
    """Convert 32-bit integer to dotted IPv4 address."""
    return ".".join(map(lambda n: str(ip >> n & 0xFF), [24, 16, 8, 0]))


def get_ip():
    iplist = []
    with open(r"README.md","rb") as fd:
        for line in fd:
            match = g_ipcheck.search(line)
            if match is not None:
                for item in match.groups():
                    iplist.append(from_string(item))
    iplist.sort()
    print("total ip cnt: %d" % len(iplist) )
    iprangelist = []
    nbegin = 0
    lastint = 0
    for ipint in iplist:
        if nbegin == 0:
            lastint = ipint
            nbegin = ipint
        elif ipint == lastint + 1:
            lastint = ipint
        else:
            if nbegin == lastint:
                iprangelist.append(to_string(nbegin))
            else:
                iprangelist.append("%s-%s" % (to_string(nbegin),to_string(lastint)) )
            nbegin = ipint
            lastint = ipint
    if nbegin != 0:
        if nbegin == lastint:
            iprangelist.append(to_string(nbegin))
        else:
            iprangelist.append("%s-%s" % (to_string(nbegin),to_string(lastint)) )
    print("\n".join(iprangelist))


if __name__ == '__main__':
    get_ip()

