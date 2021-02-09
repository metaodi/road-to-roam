#!/bin/bash
set -e
set -o pipefail

function cleanup {
  exit $?
}
trap "cleanup" EXIT


DIR="$(cd "$(dirname "$0")" && pwd)"
source $DIR/.env

#$DIR/node_modules/.bin/roam-api -g $ROAM_API_GRAPH -e $ROAM_API_EMAIL -p $ROAM_API_PASSWORD search "pk19"
#node ./node_modules/roam-research-private-api/examples/quick_capture.js -g $ROAM_API_GRAPH -e $ROAM_API_EMAIL -p $ROAM_API_PASSWORD "test 123"
$DIR/node_modules/.bin/roam-api -g $ROAM_API_GRAPH -e $ROAM_API_EMAIL -p $ROAM_API_PASSWORD create "This will be prepended to my daily page"

