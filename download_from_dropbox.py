#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Download files from dropbox directory

Usage:
  download_from_dropbox.py --path <path-to-dropbox-directory> --output <path-to-local-directory>
  download_from_dropbox.py (-h | --help)
  download_from_dropbox.py --version

Options:
  -h, --help                             Show this screen.
  --version                              Show version.
  -p, --path <path-to-dropbox-directory> Path to Dropbox directory.
  -o, --output <path-to-local-directory> Path to local directory to save the downloaded files.

"""

import sys
import os
import tempfile
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
from docopt import docopt
from dotenv import load_dotenv, find_dotenv

arguments = docopt(__doc__, version='Download files from Dropbox 1.0')
load_dotenv(find_dotenv())


from pprint import pprint

TOKEN = os.getenv('DROPBOX_TOKEN', '')

if __name__ == '__main__':
    try:
        # Check for an access token
        if (len(TOKEN) == 0):
            sys.exit("ERROR: Looks like you didn't add your access token. "
                "Add it to your `.env` file as DROPBOX_TOKEN.")

        # Create an instance of a Dropbox class, which can make requests to the API.
        with dropbox.Dropbox(TOKEN) as dbx:

            # Check that the access token is valid
            try:
                dbx.users_get_current_account()
            except AuthError:
                sys.exit(
                    "ERROR: Invalid access token; try re-generating an "
                    "access token from the app console on the web."
                )
            path = arguments['--path']
            output = arguments['--output']
            result = dbx.files_list_folder(path)
            for entry in result.entries:
                try:
                    local_path = os.path.join(output, entry.name)
                    dbx.files_download_to_file(local_path, entry.path_lower, entry.rev)
                    print(f"Saved {entry.name} to {local_path}")
                except AttributeError:
                    continue
            print("Done!")
    except Exception as e:
        print("Error: %s" % e, file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        sys.exit(1)
