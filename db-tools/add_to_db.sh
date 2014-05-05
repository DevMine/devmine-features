#!/bin/bash
set -o nounset
set -o errexit

source ./definitions.sh

SEPARATOR=","

GenerateFeatureInserts () {
    local FILENAME=$1
    local FEATURENAME=$2

    #TODO delete all old entries for feature from db
    echo "DELETE FROM $FEATURES_TABLE WHERE NAME = '$FEATURENAME';"

    echo "INSERT INTO $FEATURES_TABLE (NAME) VALUES ('$FEATURENAME');"

    local BEFORE="INSERT INTO $SCORES_TABLE (ULOGIN,FNAME,SCORE) VALUES ("
    local AFTER=");"
    awk -v before="$BEFORE" -v after="$AFTER" -v fname="$FEATURENAME" -v OFS="," -v q="'" -F "$SEPARATOR" '{ print before q $1 q, q fname q, q $2 q after }' $FILENAME
}

GenerateUserInserts () {
    local FILENAME=$1

    local BEFORE="INSERT INTO $USERS_TABLE (UID, LOGIN) VALUES ("
    local AFTER=");"
    awk -v before="$BEFORE" -v after="$AFTER" -v OFS="," -v q="'" -F "$SEPARATOR" '{ print before $1, q $2 q after }' $FILENAME
}

# Check if Postgres wrapper scripts are available
if hash psql 2>/dev/null; then
    EXISTS=$(psql -l | grep $DB | wc -l)
    if [ "$EXISTS" -gt "0" ]; then
        while getopts "yu:f:" opt; do
            case $opt in
                u) GenerateUserInserts $OPTARG | psql -q $DB
                    ;;
                f) 
                    BASE_FILE_EXT=$(basename "$OPTARG")
                    BASE_FILE="${BASE_FILE_EXT%.*}"
                    GenerateFeatureInserts $OPTARG $BASE_FILE | psql -q $DB
                    ;;
                \?) echo "Invalid option: -$OPTARG" >&2
                    ;;
            esac
        done
        exit 0
    else
        echo "Postgresql DB $DB does not exist"
        exit 1
    fi
else
    echo "psql could not be found"
    exit 1
fi
