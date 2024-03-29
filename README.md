road-to-roam
============

This repository is a collection of scripts with the goal to get highlights (and later maybe other annotations as well) from PDFs to Roam Research.
In my workflow, I use my [remarkable 2 tablet](https://remarkable.com/) to highlight PDFs and I want to make sure, these highlights are saved to my [Roam Research](https://roamresearch.com) database.

There are many projects to access the files on the remarkable cloud (e.g. remapy or rmapi) and there are several projects to extract highlights from the remarkable-annotated PDFs (e.g. remarkable-highlights, remarks and biff).
For my purposes I use remarkable-highlights since the output is a simple text file and PNG images.
Your needs might be different.

My workflow is currently like this:

- Load a PDF on my remarkable (either by using the app or using website-to-remarkable to get automatically the top posts from HackerNews and other websites)
- Highlight these PDFs
- Export the PDFs using the remarkable app's share functionality
- Upload the PDFs to dropbox

This is where these scripts here come into play: I run the script here on a regular basis to get the PDFs from Dropbox, extract the hightlights and images using remarkable-hightlights and finally use artpi/roam-research-private-api to add a new page for every PDF containing the extracted highlights.

# Installation

1. Clone this repository `git clone https://github.com/metaodi/road-to-roam.git`
1. Install https://github.com/benlongo/remarkable-highlights on your machine and define the path to your clone in your `.env`
1. If you want to fetch files from Dropbox, [create a new Dropbox app and generate an access token].
1. Copy the `.env.dist` file to `.env` and edit the values
1. Run `setup.sh` to create a new virtualenv and install all python dependencies (or simply run `pip install -r requirements.txt` if you don't want a new virtualenv)

# Usage

The script is run by GitHub Actions on a schedule.

