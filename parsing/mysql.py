#!/usr/bin/python2.7
import re


def number_group(name):
    return '(?P<' + name + '>[0-9]*|NULL)'


def string_group(name):
    group = "'([^\\\\']{0,}(\\\\('|\\\\){0,1}){0,1}){0,}'|NULL)"
    return "(?P<" + name + ">" + group


def construct_regex(groups):
    return re.compile("\(" + ",".join(groups) + "\)")

regex_commits = construct_regex([number_group("id"),
                                 string_group("sha"),
                                 number_group("author_id"),
                                 number_group("committer_id"),
                                 number_group("project_id"),
                                 string_group("created_at"),
                                 string_group("ext_ref_id")])

regex_counters = construct_regex([number_group("id"),
                                  string_group("date"),
                                  number_group("commit_comments"),
                                  number_group("commit_parents"),
                                  number_group("commits"),
                                  number_group("followers"),
                                  number_group("organization_members"),
                                  number_group("projects"),
                                  number_group("users"),
                                  number_group("issues"),
                                  number_group("pull_requests"),
                                  number_group("issue_comments"),
                                  number_group("pull_request_comments"),
                                  number_group("pull_request_history"),
                                  number_group("watchers"),
                                  number_group("forks")])

regex_followers = construct_regex([number_group("follower_id"),
                                   number_group("user_id"),
                                   string_group("timestamp"),
                                   string_group("ext_ref_id")])

regex_forks = construct_regex([number_group("forked_project_id"),
                               number_group("forked_from_id"),
                               number_group("fork_id"),
                               string_group("created_at"),
                               string_group("ext_ref_id")])

regex_issue_comments = construct_regex([number_group("issue_id"),
                                        number_group("user_id"),
                                        string_group("comment_id"),
                                        string_group("created_at"),
                                        string_group("ext_ref_id")])

regex_issue_events = construct_regex([string_group("event_id"),
                                      number_group("issue_id"),
                                      number_group("actor_id"),
                                      string_group("action"),
                                      string_group("action_specific"),
                                      string_group("created_at"),
                                      string_group("ext_ref_id")])

regex_issue_labels = construct_regex([number_group("label_id"),
                                      number_group("issue_id")])

regex_issues = construct_regex([number_group("id"),
                                number_group("repo_id"),
                                number_group("reporter_id"),
                                number_group("assignee_id"),
                                number_group("pull_request"),
                                number_group("pull_request_id"),
                                string_group("created_at"),
                                string_group("ext_ref_id"),
                                number_group("issue_id")])

regex_organization_members = construct_regex([number_group("org_id"),
                                              number_group("user_id"),
                                              string_group("created_at")])

regex_project_commits = construct_regex([number_group("project_id"),
                                         number_group("commit_id")])

regex_project_members = construct_regex([number_group("repo_id"),
                                         number_group("user_id"),
                                         string_group("created_at"),
                                         string_group("ext_ref_id")])

regex_projects = construct_regex([number_group("id"),
                                  string_group("url"),
                                  number_group("owner_id"),
                                  string_group("name"),
                                  string_group("description"),
                                  string_group("language"),
                                  string_group("created_at"),
                                  string_group("ext_ref_id"),
                                  number_group("forked_from"),
                                  number_group("deleted")])

regex_pull_request_comments = construct_regex([number_group("pull_request_id"),
                                               number_group("user_id"),
                                               string_group("comment_id"),
                                               number_group("position"),
                                               string_group("body"),
                                               number_group("commit_id"),
                                               string_group("created_at"),
                                               string_group("ext_ref_id")])

regex_pull_request_commits = construct_regex([number_group("pull_request_id"),
                                              number_group("commit_id")])

regex_pull_request_history = construct_regex([number_group("id"),
                                              number_group("pull_request_id"),
                                              string_group("created_at"),
                                              string_group("ext_ref_id"),
                                              string_group("action"),
                                              number_group("actor_id")])

regex_pull_requests = construct_regex([number_group("id"),
                                       number_group("head_repo_id"),
                                       number_group("base_repo_id"),
                                       number_group("head_commit_id"),
                                       number_group("base_commit_id"),
                                       number_group("user_id"),
                                       number_group("pullreq_id"),
                                       number_group("intra_branch"),
                                       number_group("merged")])

regex_repo_labels = construct_regex([number_group("id"),
                                     number_group("repo_id"),
                                     string_group("name"),
                                     string_group("ext_ref_id")])

regex_repo_milestones = construct_regex([number_group("id"),
                                         number_group("repo_id"),
                                         string_group("name"),
                                         string_group("ext_ref_id")])

regex_users = construct_regex([number_group("id"),
                               string_group("login"),
                               string_group("name"),
                               string_group("company"),
                               string_group("location"),
                               string_group("email"),
                               string_group("created_at"),
                               string_group("ext_ref_id"),
                               string_group("type")])

regex_watchers = construct_regex([number_group("repo_id"),
                                  number_group("user_id"),
                                  string_group("created_at"),
                                  string_group("ext_ref_id")])

table_regexp = {
    "commits": regex_commits,
    "counters": regex_counters,
    "followers": regex_followers,
    "forks": regex_forks,
    "issues": regex_issues,
    "organization_members": regex_organization_members,
    "project_commits": regex_project_commits,
    "project_members": regex_project_members,
    "pull_request": regex_pull_requests,
    "users": regex_users,
    "watchers": regex_watchers
}

table_fields = {"commits":
                [
                    "author_id",
                    "committer_id",
                    "project_id",
                    "created_at"
                ],
                "counters":
                [
                    "id",
                    "date",
                    "commit_comments",
                    "commit_parents",
                    "commits",
                    "followers",
                    "organization_members",
                    "projects",
                    "users",
                    "issues",
                    "pull_requests",
                    "issue_comments",
                    "pull_request_comments",
                    "pull_request_history",
                    "watchers",
                    "forks"
                ],
                "followers":
                [
                    "follower_id",
                    "user_id"
                ],
                "forks":
                [
                    "forked_project_id",
                    "forked_from_id",
                    "created_at"
                ],
                "issues":
                [
                    "repo_id",
                    "reporter_id",
                    "assignee_id",
                    "created_at"
                ],
                "organization_members":
                [
                    "org_id",
                    "user_id",
                    "created_at"
                ],
                "project_commits":
                [
                    "project_id",
                    "commit_id"
                ],
                "project_members":
                [
                    "repo_id",
                    "user_id",
                    "created_at"
                ],
                "projects":
                [
                    "id",
                    "owned_id",
                    "name",
                    "language",
                    "created_at",
                    "forked_from",
                    "deleted"
                ],
                "pull_requests":
                [
                    "id",
                    "head_repo_id",
                    "base_repo_id",
                    "head_commit_id",
                    "base_commid_id",
                    "user_id",
                    "merged"
                ],
                "users":
                [
                    "id",
                    "login",
                    "name",
                    "company",
                    "location",
                    "email",
                    "created_at",
                    "type"
                ],
                "watchers":
                [
                    "repo_id",
                    "user_id",
                    "created_at"
                ]}

table_file = {}

for table in table_regexp.keys():
    table_file[table] = open("../dataset/out/" + table, "w")

with open("../dataset/mysql-2014-04-02.sql") as f:
    i = 0
    for l in f:
        try:
            i += 1
            if l.startswith("INSERT INTO"):
                table = l.split()[2][1:-1]
                if table in table_regexp:
                    for match in re.finditer(table_regexp[table], l):
                        fields = [match.group(f) for f in table_fields[table]]
                        out = ",".join(fields)
                        print >> table_file[table], out
        except Exception as e:
            print "error at line ", i, e
