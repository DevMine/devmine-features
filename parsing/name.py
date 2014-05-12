import sys

NULL = 'NULL'

def get_field(line, field):
    record = eval(line)
    return str(record[field])


for l in sys.stdin:
    try:
        print(",".join([get_field(l, 0), get_field(l, 1)]))
    except Exception as e:
        print("Error at line ", e, file=sys.stderr)
        print(l, file=sys.stderr)

