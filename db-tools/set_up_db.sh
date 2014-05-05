#!/bin/bash
set -o nounset
set -o errexit

source ./definitions.sh

# Check if Postgres wrapper scripts are available
if hash createdb 2>/dev/null; then
    dropdb $DB
    createdb $DB

    psql $DB -q << EOF
    CREATE TABLE $FEATURES_TABLE(
      FID   SERIAL PRIMARY KEY,
      NAME  TEXT UNIQUE NOT NULL);
    CREATE TABLE $USERS_TABLE(
      UID   INT PRIMARY KEY NOT NULL,
      LOGIN TEXT UNIQUE NOT NULL);
    CREATE TABLE $SCORES_TABLE(
      SID   SERIAL PRIMARY KEY,
      ULOGIN TEXT           NOT NULL REFERENCES $USERS_TABLE(LOGIN),  
      FNAME  TEXT           NOT NULL REFERENCES $FEATURES_TABLE(NAME),
      SCORE  INT            NOT NULL);
EOF
    exit 0
else
    echo "Postgresscript createdb could not be found"
    exit 1
fi
