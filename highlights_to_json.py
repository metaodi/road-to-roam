#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert highlights to JSON

Usage:
  highlights_to_json.py --path <path-to-highlights> --title <title-of-work> [--url <pdf-url>]
  highlights_to_json.py (-h | --help)
  highlights_to_json.py --version

Options:
  -h, --help                      Show this screen.
  --version                       Show version.
  -p, --path <path-to-highlights> Path to highlights directory.
  -t, --title <title-of-work>     Title of the work.
  -u, --url <pdf-url>             URL of the highlighted PDF.


This script parses the output of remarkable-highlights and tranforms
it to a JSON that is suitable for Roam Research.

"""

import sys
import os
import re
import json
import traceback
from docopt import docopt
from dotenv import load_dotenv, find_dotenv

arguments = docopt(__doc__, version='Convert highlights to JSON 1.0')
load_dotenv(find_dotenv())

__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(__file__)
    )
)


from pprint import pprint

try:
    hl_path = os.path.join(arguments['--path'], 'highlights.txt')
    highlights = []
    page_pattern = re.compile(r'page \d+:')
    with open(hl_path, 'r') as f:
        for line in f.readlines():
            line = " ".join(line.split())
            if line and not page_pattern.match(line):
                highlights.append(line)

    template_path = os.path.join(__location__, 'template.json')
    with open(template_path, 'r') as t:
        data = json.loads(t.read())

    data[0]['title'] = f"{data[0]['title']} {arguments['--title']}"
    data[0]['children'][6]['children'] = [{'string': hl} for hl in highlights]

    if arguments['--url']:
        data[0]['children'][7]['string'] = data[0]['children'][7]['string'].replace('<url>', arguments['--url'])
    print(json.dumps(data, sort_keys=True, indent=2))
except Exception as e:
    print("Error: %s" % e, file=sys.stderr)
    print(traceback.format_exc(), file=sys.stderr)
    sys.exit(1)
