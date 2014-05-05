#!/usr/bin/python

import json, sys

ids = set()

for line in sys.stdin:
    fixed_line = "{" + line[line.find("login")-1:]
    user = json.loads(fixed_line)
    if not user["id"] in ids:
        print str(user["id"]) + "," + user["login"]
        ids.add(user["id"])
