#!/bin/bash
set -e
set -o pipefail

function cleanup {
  exit $?
}
trap "cleanup" EXIT

DIR="$(cd "$(dirname "$0")" && pwd)"
[ -d $DIR/env ] && source $DIR/env/bin/activate
[ -f $DIR/.env ] && source $DIR/.env

# create a new temp directory
tmp_dir=$(mktemp -d -t road-to-roam-XXXXXXXXXX)
echo "Creating temp dir ${tmp_dir}"


$DIR/download_from_dropbox.py --path "" --output $tmp_dir
shopt -s nullglob
for pdf_file in $tmp_dir/*.pdf
do
    filename=`basename "${pdf_file}"`
    hl_name="${filename//[^[:alnum:]]/}"
    hl_dir="${tmp_dir}/${hl_name,,}-hl"
    # extract the highlights
    echo ""
    echo "Saving highlights to ${hl_dir}"
    (
    cd $REMARKABLE_HIGHLIGHTS_PATH
    [ -d $REMARKABLE_HIGHLIGHTS_PATH/env ] && source $REMARKABLE_HIGHLIGHTS_PATH/env/bin/activate
    poetry run remarkable-highlights --out $hl_dir "${pdf_file}"
    )
    # create dropbox link
    dropbox_link=$($DIR/create_dropbox_link.py --path "/${filename}")

    # upload highlights to roam
    title=$(echo $filename | sed 's/\([A-Z]\)/ \1/g' | sed 's/[^ ]\+/\L\u&/g' | sed 's/\.pdf$//g' | xargs)
    python $DIR/highlights_to_json.py --path $hl_dir --title "${title}" --url "${dropbox_link}" > $tmp_dir/hl.json
    jq -r '.[0].title' $tmp_dir/hl.json | $DIR/add_to_roam_daily_notes.sh
    cat $tmp_dir/hl.json | node $DIR/import_data_to_roam.js

    # move file to subdir
    $DIR/move_in_dropbox.py -s "/${filename}" -t "/synced-to-roam/${filename}"
done


rm -rf $tmp_dir
