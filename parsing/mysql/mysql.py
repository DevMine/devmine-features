#!/usr/bin/python2.7
from __future__ import print_function as fprint
from mysql_regexp import *
from table_fields import *
import re

def parse_mysql(path):
    table_file = {}

    for table in table_regexp.keys():
        table_file[table] = open("dataset/tables/" + table, "w")

    for l in open(path):
        try:
            if l.startswith("INSERT INTO"):
                table = l.split()[2][1:-1]
                if table in table_regexp:
                    for match in re.finditer(table_regexp[table], l):
                        fields = [match.group(f) for f in table_fields[table]]
                        fprint(",".join(fields), file = table_file[table])
        except Exception as e:
            fprint("error at line ", i, e)


if __name__=="__main__":
    parse_mysql("dataset/mysql")
