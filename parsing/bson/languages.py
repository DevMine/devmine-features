import sys


def read_languages(source, outdir):
    # Read
    user_langs = {}
    languages = set()

    for line in source:
        try:
            user, language, lines = line.strip().split(",")
            if(language != 'None'):
                languages.add(language)
                if user in user_langs:
                    if language in user_langs[user]:
                        user_langs[user][language] += int(lines)
                    else:
                        user_langs[user][language] = int(lines)
                else:
                    user_langs[user] = {language: int(lines)}
        except Exception as e:
            print("Problem reading line:", line.strip(), file=sys.stderr)
            print(e, file=sys.stderr)

    # Write
    files = {}
    for language in languages:
        files[language] = open(outdir + "/" + language + ".txt", "w")

    for user in user_langs:
        for l in user_langs[user]:
            if(user_langs[user][l] > 0):
                files[l].write(user + ',' + str(user_langs[user][l]) + '\n')

    for f in files.values():
        f.flush()
        f.close()

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("Please specify an output directory")
    elif(len(sys.argv) == 2):
        read_languages(sys.stdin, sys.argv[1])
    else:
        print(sys.argv[1], sys.argv[2])
        read_languages(open(sys.argv[1]), sys.argv[2])
