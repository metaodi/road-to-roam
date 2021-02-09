#!/bin/bash
set -e
set -o pipefail

function cleanup {
  exit $?
}
trap "cleanup" EXIT


# install python dependencies
[ ! -d env ] && python3 -m venv env
source env/bin/activate

pip3 install --upgrade pip
pip3 install -r requirements.txt

# install node dependencies
npm install
