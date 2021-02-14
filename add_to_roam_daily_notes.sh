#!/bin/bash
set -e
set -o pipefail

function cleanup {
  exit $?
}
trap "cleanup" EXIT


DIR="$(cd "$(dirname "$0")" && pwd)"
[ -f $DIR/.env ] && source $DIR/.env

while read line; do
  $DIR/node_modules/.bin/roam-api -g $ROAM_API_GRAPH -e $ROAM_API_EMAIL -p $ROAM_API_PASSWORD create "[[${line}]]"
done < /dev/stdin


