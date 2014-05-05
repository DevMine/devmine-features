import json
import sys


def fix_line(line):
    return "{" + line[line.find("),")+2:]


def read_field(record, f):
    r = record
    for p in f.split("/"):
        r = r[p]

    return str(r)


def read_file(source):
    for line in source:
        fixed_line = fix_line(line)
        try:
            record = json.loads(fixed_line)
            print(",".join([read_field(record, f) for f in sys.argv[1:]]))
        except Exception as e:
            print >> sys.stderr, "Problem reading line:", line.strip()
            print >> sys.stderr, e


if __name__ == "__main__":
    read_file(sys.stdin)
