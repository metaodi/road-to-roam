#!/bin/bash
set -e
set -o pipefail

function cleanup {
  exit $?
}
trap "cleanup" EXIT

DIR="$(cd "$(dirname "$0")" && pwd)"
source $DIR/env/bin/activate
source $DIR/.env

# create a new temp directory
tmp_dir=$(mktemp -d -t road-to-roam-XXXXXXXXXX)
echo "Creating temp dir ${tmp_dir}"


$DIR/download_from_dropbox.py --path "" --output $tmp_dir
for pdf_file in $tmp_dir/*.pdf
do
    # extract the highlights
    hl_dir=$(mktemp -d -t road-to-roam-hl-XXXXXXXXXX)
    (
    cd $REMARKABLE_HIGHLIGHTS_PATH
    poetry run remarkable-highlights --out $hl_dir $pdf_file
    $DIR/upload_to_roam.sh
    )
done


# rm -rf $tmp_dir
