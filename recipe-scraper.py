#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018  Felix Gruber
#
# This file is part of recipe-scraper.
#
# recipe-scraper is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# recipe-scraper is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with recipe-scraper.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import os
import sys
import urllib

from imports import getUrl, importers, FallbackImporter
from exports import exporters

aparser = argparse.ArgumentParser(
        description='transform a recipe from a cooking website into' \
                    ' a machine-readable format')
aparser.add_argument('-o', metavar='OUTFILE', dest='outfile', default=None,
                     help='write to OUTFILE instead of stdout'
                          ', file format is chosen from the file extension')
aparser.add_argument('-f', '--format', action='store', default=None,
                     help='file extension of output format, default is ".mmf"'
                          ', i.e. Mealmaster')
# -i specifies the netloc of the webscraper to use,
# This is useful for development so that we can specify the scraper
# when reading from a saved html file.
aparser.add_argument('-i', '--input-site', dest='netloc',
                     action='store', default=None,
                     help=argparse.SUPPRESS)
aparser.add_argument('url', action='store',
                     help='URL of the recipe')
args = aparser.parse_args()
netloc = args.netloc or urllib.parse.urlparse(args.url).netloc
if not args.format:
    if args.outfile:
        args.format = os.path.splitext(args.outfile)[1]
    else:
        args.format = '.mmf'

try:
    importer = importers[netloc]
except KeyError:
    if args.netloc:
        print('unknown website argument:', netloc, file=sys.stderr)
        sys.exit(1)
    else:
        importer = FallbackImporter

if not args.format in exporters:
    print('unknown file extension:', args.format, file=sys.stderr)
    sys.exit(1)

recipe_page = getUrl(args.url)
recipe = importer.importRecipe(recipe_page)

out = exporters[args.format](recipe)

if args.outfile:
    print(out, file=open(args.outfile, 'w'))
else:
    print(out)
