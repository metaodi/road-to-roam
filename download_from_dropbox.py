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

# 1. list all files in RoadToRoam directory
# 2. Download all files to local ooutput directory
# 3. run remarkable-hightligh on all PDFs
# 4. Upload highlights to Roam

# Add OAuth2 access token to `.env` file
# You can generate one for yourself in the App Console.
# See <https://blogs.dropbox.com/developers/2014/05/generate-an-access-token-for-your-own-account/>
TOKEN = os.getenv('DROPBOX_TOKEN', '')

LOCALFILE = 'my-file.txt'
BACKUPPATH = '/my-file-backup.txt'

# Uploads contents of LOCALFILE to Dropbox
def backup():
    with open(LOCALFILE, 'rb') as f:
        # We use WriteMode=overwrite to make sure that the settings in the file
        # are changed on upload
        print("Uploading " + LOCALFILE + " to Dropbox as " + BACKUPPATH + "...")
        try:
            dbx.files_upload(f.read(), BACKUPPATH, mode=WriteMode('overwrite'))
        except ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().reason.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()

# Change the text string in LOCALFILE to be new_content
# @param new_content is a string
def change_local_file(new_content):
    print("Changing contents of " + LOCALFILE + " on local machine...")
    with open(LOCALFILE, 'wb') as f:
        f.write(new_content)

# Restore the local and Dropbox files to a certain revision
def restore(rev=None):
    # Restore the file on Dropbox to a certain revision
    print("Restoring " + BACKUPPATH + " to revision " + rev + " on Dropbox...")
    dbx.files_restore(BACKUPPATH, rev)

    # Download the specific revision of the file at BACKUPPATH to LOCALFILE
    print("Downloading current " + BACKUPPATH + " from Dropbox, overwriting " + LOCALFILE + "...")
    dbx.files_download_to_file(LOCALFILE, BACKUPPATH, rev)

# Look at all of the available revisions on Dropbox, and return the oldest one
def select_revision():
    # Get the revisions for a file (and sort by the datetime object, "server_modified")
    print("Finding available revisions on Dropbox...")
    entries = dbx.files_list_revisions(BACKUPPATH, limit=30).entries
    revisions = sorted(entries, key=lambda entry: entry.server_modified)

    for revision in revisions:
        print(revision.rev, revision.server_modified)

    # Return the oldest revision (first entry, because revisions was sorted oldest:newest)
    return revisions[0].rev

if __name__ == '__main__':
    # Check for an access token
    if (len(TOKEN) == 0):
        sys.exit("ERROR: Looks like you didn't add your access token. "
            "Add it to your `.env` file as DROPBOX_TOKEN.")

    # Create an instance of a Dropbox class, which can make requests to the API.
    print("Creating a Dropbox object...")
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
        # maybe temp dir per file and extract highlight in the same dir?
        for entry in result.entries:
            local_path = os.path.join(output, entry.name)
            dbx.files_download_to_file(local_path, entry.path_lower, entry.rev)
            pprint(entry)
            print(f"Saved {entry.name} to {local_path}")

        print("Done!")
