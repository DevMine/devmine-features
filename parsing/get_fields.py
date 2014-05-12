import sys
import os
from mysql.table_fields import table_fields

NULL = 'NULL'


def get_fields(table, outfile, *fields):
    field_list = table_fields[os.path.basename(table)]
    fields = list(map(field_list.index, fields))

    out = open(outfile, "w")
    for line in open(table):
        try:
            line_fields = eval('[' + line + ']')
            print(",".join([str(line_fields[field]) for field in fields]),
                  file=out)
        except Exception as e:
            print("Error ", e, " at line:", file=sys.stderr)
            print(line, file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python ", sys.argv[0],
              " inputfile outputfile field1 field2 ...")
    else:
        get_fields(sys.argv[1], sys.argv[2], *sys.argv[3:])
