from invoke import (
    task,
    run
)

import parsing
from parsing.mysql.table_fields import table_fields

# define projects directories
dirs = 'parsing'


@task
def pep8():
    cmd = 'pep8 tasks.py ' + dirs
    run_cmd(cmd)


@task
def pyflakes():
    cmd = 'pyflakes tasks.py ' + dirs
    run_cmd(cmd)


@task('pep8', 'pyflakes')
def check():
    pass


@task
def clean():
    run_cmd("find . -name '__pycache__' -exec rm -rf {} +")
    run_cmd("find . -name '*.pyc' -exec rm -f {} +")
    run_cmd("find . -name '*.pyo' -exec rm -f {} +")
    run_cmd("find . -name '*~' -exec rm -f {} +")
    run_cmd("find . -name '._*' -exec rm -f {} +")


@task('clean')
def clean_env():
    run_cmd('rm -r ./env && mkdir env && touch env/.keep')


# Computation tasks
@task
def parse_mysql():
    """Parse the mysql file to generate the tables"""
    run_cmd("python2.7 parsing/mysql/parse.py")


@task(help={"table": "Input table",
            "outputfile": "Output file, specify --stdout to write to stdout",
            "fields": "Fields to extract from the table"})
def get_fields(table, outputfile, fields):
    """Extract fields from a given table"""
    parsing.get_fields(table, outputfile, *fields.split())


@task(help={"table": "Table to list the fields"})
def list_fields(table):
    """Lists the available fields in the given table"""
    print("\n".join(table_fields[table]))


@task
def list_tables():
    """Lists the available tables"""
    print("\n".join(table_fields.keys()))


@task
def compute_login_id(input='dataset/raw/users.bson', output='dataset/id.txt'):
    get_fields_bson("login id", input, output)


@task
def compute_location(input='dataset/raw/users.bson',
                     output='dataset/location.txt'):
    get_fields_bson("login location", input, output)
    pairs = []
    f = open(output, "r")
    for line in f:
        ss = line.strip().split(",")
        if len(ss) == 1:
            user, comp = ss[0], ""
        elif ss[1].startswith("None"):
            user, comp = ss[0], ""
        else:
            user, comp = ss[0], ss[1]
        pairs.append((user, comp))
    f.close()
    f = open(output, "w")
    for pair in pairs:
        s = "%s,%s\n" % (pair[0], pair[1])
        f.write(s)
        f.flush()
    f.close()


@task
def compute_company(input='dataset/raw/users.bson',
                    output='dataset/company.txt'):
    get_fields_bson("login company", input, output)
    pairs = []
    f = open(output, "r")
    for line in f:
        ss = line.strip().split(",")
        if len(ss) == 1:
            user, comp = ss[0], ""
        elif ss[1].startswith("None"):
            user, comp = ss[0], ""
        else:
            user, comp = ss[0], ss[1]
        pairs.append((user, comp))
    f.close()
    f = open(output, "w")
    for pair in pairs:
        s = "%s,%s\n" % (pair[0], pair[1])
        f.write(s)
        f.flush()
    f.close()


@task
def compute_followers(input='dataset/raw/users.bson',
                      output='dataset/followers.txt'):
    get_fields_bson("login followers", input, output)


@task
def compute_date_joined_github(input='dataset/raw/users.bson',
                               output='dataset/date_joined_github.txt'):
    get_fields_bson("login created_at", input, output)


@task
def compute_last_active(input='dataset/raw/users.bson',
                        output='dataset/last_active.txt'):
    get_fields_bson("login updated_at", input, output)


@task
def compute_hireable(input='dataset/raw/users.bson',
                     output='dataset/hireable.txt'):
    get_fields_bson("login hireable", input, output)


@task
def precompute_issues_detected(input='dataset/raw/issues.bson',
                               output='dataset/issues_detected.txt'):
    get_fields_bson("user/login", input, output)


@task
def compute_issues_detected(input='dataset/raw/issues.bson',
                            output='dataset/issues_detected'):
    precompute_issues_detected(input, output + '.txt')
    run_cmd('python parsing/issues_detected.py %s.txt %s' % (output, output))


@task
def precompute_projects_contributed(
        input='dataset/raw/repo_collaborators.bson',
        output='dataset/projects_contributed.txt'):
    get_fields_bson("login", input, output)


@task
def compute_projects_contributed(input='dataset/raw/repo_collaborators.bson',
                                 output='dataset/projects_contributed'):
    precompute_projects_contributed(input, output + '.txt')
    run_cmd('python parsing/collaborators.py %s.txt %s' % (output, output))


@task
def compute_projects_language(input='dataset/raw/repos.bson',
                              output='dataset/projects_language'):
    # TODO:
    # we need to join the repo_collaborators and repos
    # in repo_collaborators, we don't have repo id
    # but we can use owner_id/repo_name as the id
    pass


@task
def precompute_issues_solved(input='dataset/raw/issues.bson',
                             output='dataset/issues_solved.txt'):
    get_fields_bson("state assignee/login", input, output)


@task
def compute_issues_solved(input='dataset/raw/issues.bson',
                          output='dataset/issues_solved'):
    precompute_issues_solved(input, output + '.txt')
    run_cmd('python parsing/issues_solved.py %s.txt %s' % (output, output))


@task
def precompute_languages(input='dataset/raw/repos.bson',
                         output='dataset/languages.txt'):
    get_fields_bson("owner/login language size", input, output)


@task
def compute_languages(input='dataset/raw/repos.bson',
                      output='dataset/languages'):
    precompute_languages(input, output + '.txt')
    run_cmd('python parsing/languages.py \
    dataset/languages.txt dataset/languages')


@task('compute_login_id', 'compute_followers', 'compute_languages')
def compute_all():
    pass


# Database insert tasks
@task
def insert_users(filename):
    add_to_db("-u " + filename)


@task(help={"category": "Category of the features",
            "filenames": "String of filenames separated by whitespace"})
def insert_features(category, filenames):
    """Insert multiple features into the database"""
    for f in filenames.split():
        insert_feature(category, f)


@task(help={"category": "Category of the feature",
            "filename": "Filename with scores"})
def insert_feature(category, filename):
    """Insert a feature into the database"""
    add_to_db("-c " + category + " -f " + filename)


def run_cmd(cmd):
    "Run a system command verbosely."
    print('Running \'' + cmd + '\'...')
    run(cmd)
    print('Done')


def get_fields_bson(fields, input, output, has_null=False):
    run_cmd('bsondump %s | python parsing/get_fields.py %s > %s 2> /dev/null' %
            (input, fields, output))


def add_to_db(args):
    cmd = "./db-tools/add_to_db.sh "
    run_cmd(cmd + args)
