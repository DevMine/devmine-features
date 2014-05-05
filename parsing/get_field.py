#!/usr/bin/python

import json, sys

ids = set()

for line in sys.stdin:
    fixed_line = "{" + line[line.find("login")-1:]
    try:
        user = json.loads(fixed_line)
        if not user["id"] in ids:
            print str(user["id"]) + "," + str(user[sys.argv[1]])
            ids.add(user["id"])
    except Exception as e:
        print >> sys.stderr, "Problem reading line:", line.strip()
        print >> sys.stderr, e
