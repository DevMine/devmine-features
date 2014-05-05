import json
import sys

user_id = dict()
follows = []


for line in sys.stdin:
    fixed_line = "{" + line[line.find("login")-1:]
    user = json.loads(fixed_line)
    user_id[user["login"]] = user["id"]
    follows.append((user["login"], user["follows"]))

follows_int = []

for (a, b) in follows:
    if a in user_id and b in user_id:
        print(user_id[a], user_id[b])
