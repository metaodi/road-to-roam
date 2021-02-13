#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create link for file in dropbox

Usage:
  create_dropbox_link.py --path <path-to-dropbox-file> 
  create_dropbox_link.py (-h | --help)
  create_dropbox_link.py --version

Options:
  -h, --help                             Show this screen.
  --version                              Show version.
  -p, --path <path-to-dropbox-directory> Path to Dropbox file.

"""

import sys
import os
import tempfile
import traceback
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
from docopt import docopt
from dotenv import load_dotenv, find_dotenv

arguments = docopt(__doc__, version='Download files from Dropbox 1.0')
load_dotenv(find_dotenv())

TOKEN = os.getenv('DROPBOX_TOKEN', '')

from pprint import pprint

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
            try:
                shared_link_metadata = dbx.sharing_create_shared_link_with_settings(path)
                print(shared_link_metadata.url)
            except ApiError as err:
                if err.error.is_shared_link_already_exists():
                    shared_links = dbx.sharing_list_shared_links(path) 
                    print(shared_links.links[0].url)
                else:
                    raise
    except Exception as e:
        print("Error: %s" % e, file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        sys.exit(1)
