road-to-roam
============

This repository is a collection of scripts with the goal to get highlights (and later maybe other annotations as well) from PDFs to Roam Research.
In my workflow, I use my remarkable 2 tablet to highlight PDFs and I want to make sure, these highlights are saved to my roam database.

There are many project to access the files on the remarkable cloud (e.g. remapy or rmapi) and there several project to extract highlights from the remarkable-annotated PDFs (e.g. remarkable-highlights, remarks and biff).
For my purposes I use remarkable-highlights since the output is a simple text file and PNG images.
Your needs might be different.

My workflow is currently like this:

- Load a PDF on my remarkable (either my using the app or using website-to-remarkable to get automatically the top posts from HackerNews and other websites)
- Highlight these PDFs
- Export the PDFs using the remarkable app's share functionality
- Upload the PDFs to dropbox

This is where these scripts here come into play: I run the script here on a regular basis to get the PDFs from Dropbox, extract the hightlights and images using remarkable-hightlights and finally use artpi/roam-research-private-api to add a new page for every PDF containing the extracted highlights.

# Installation

1. Clone this repository `git clone https://github.com/metaodi/road-to-roam.git`
1. If you want to fetch files from Dropbox, [create a new Dropbox app and generate an access token].
1. Copy the `.env.dist` file to `.env` and edit the values (save the Dropbox access token there)
1. Run `setup.sh` to create a new virtualenv and install all python dependencies (or simply run `pip install -r requirements.txt` if you don't want a new virtualenv)

# Usage



