#!/bin/bash
set -o nounset
set -o errexit

source ./definitions.sh

SEPARATOR=","

GenerateFeatureInserts () {
    local FILENAME=$1
    local FEATURENAME=$2

    echo "SET AUTOCOMMIT TO OFF;"
    echo "BEGIN;"

    echo "DELETE FROM $FEATURES_TABLE WHERE NAME = '$FEATURENAME';"
    echo "DELETE FROM $SCORES_TABLE WHERE FNAME = '$FEATURENAME';"

    echo "INSERT INTO $FEATURES_TABLE (NAME) VALUES ('$FEATURENAME');"

    local BEFORE="INSERT INTO $SCORES_TABLE (ULOGIN,FNAME,SCORE) VALUES ("
    local AFTER=");"
    awk -v before="$BEFORE" -v after="$AFTER" -v fname="$FEATURENAME" -v OFS="," -v q="'" -F "$SEPARATOR" '{ print before q $1 q, q fname q, q $2 q after }' $FILENAME

    echo "COMMIT;"
    echo "SET AUTOCOMMIT TO ON;"
}

GenerateUserInserts () {
    local FILENAME=$1

    echo "SET AUTOCOMMIT TO OFF;"
    echo "BEGIN;"

    local BEFORE="INSERT INTO $USERS_TABLE (LOGIN) VALUES ("
    local AFTER=");"

    awk -v before="$BEFORE" -v after="$AFTER" -v OFS="," -v q="'" -F "$SEPARATOR" '{ print before q $1 q after }' $FILENAME

    echo "COMMIT;"
    echo "SET AUTOCOMMIT TO ON;"
}

CheckDbExists () {
    local EXISTS=$(psql -U $DB_USER | grep $DB | wc -l)
    if [ "$EXISTS" -lt "1" ]; then
        echo "ERROR: Postgresql DB $DB does not exist"
        exit 1
    fi
}

# Check if Postgres wrapper scripts are available
if hash psql 2>/dev/null; then
    while getopts "u:f:h" opt; do
        case $opt in
            u) 
                CheckDbExists
                GenerateUserInserts $OPTARG | psql -U $DB_USER -q $DB
                ;;
            f) 
                CheckDbExists
                BASE_FILE_EXT=$(basename "$OPTARG")
                BASE_FILE="${BASE_FILE_EXT%.*}"
                GenerateFeatureInserts $OPTARG $BASE_FILE | psql -U $DB_USER -q $DB
                ;;
            h)
                echo "Usage: $0 [-u file]* [-f file]*"
                echo "In order to use this command, make sure you have a"
                echo "Postgres database named $DB running."
                echo "Options: -u file: Add all users in file to db."
                echo "                  File format: login"
                echo "         -f file: Add all scores in file to db."
                echo "                  The filename without extension will be the name of the feature."
                echo "                  File format: uname,score"
                echo "         -h     : Displays this help."
                ;;
            \?) echo "Invalid option: -$OPTARG" >&2
                ;;
        esac
    done
    exit 0
else
    echo "psql could not be found"
    exit 1
fi
