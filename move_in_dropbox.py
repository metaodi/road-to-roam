#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Move a file from source to target in Dropbox

Usage:
  move_in_dropbox.py --source <path-to-source> --target <path-to-target>
  move_in_dropbox.py (-h | --help)
  move_in_dropbox.py --version

Options:
  -h, --help                    Show this screen.
  --version                     Show version.
  -s, --source <path-to-source> Path to Dropbox source file.
  -t, --target <path-to-target> Path to Dropbox target directory.

"""

import sys
import os
import tempfile
import dropbox
import traceback
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
from docopt import docopt
from dotenv import load_dotenv, find_dotenv

arguments = docopt(__doc__, version='Move file in Dropbox 1.0')
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
            source = arguments['--source']
            target = arguments['--target']
            result = dbx.files_move_v2(source, target)
            #print(result.metadata)
            print(f"Moved file from {source} to {target}.")
    except Exception as e:
        print("Error: %s" % e, file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        sys.exit(1)
