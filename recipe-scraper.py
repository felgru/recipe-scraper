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

from web import getUrl

# importers
from atelierdeschefs import AtelierDesChefs
from marmiton import Marmiton

# exporters
from gourmet import Gourmet
from mealmaster import MealMaster

class Exporters(dict):
    def add_format(self, format_class):
        key = format_class.file_extension()
        self[key] = format_class

class Importers(dict):
    def add_scraper(self, scraper_class):
        key = scraper_class.netloc()
        self[key] = scraper_class

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
if not args.netloc:
    args.netloc = urllib.parse.urlparse(args.url).netloc
if not args.format:
    if args.outfile:
        args.format = os.path.splitext(args.outfile)[1]
    else:
        args.format = '.mmf'

importers = Importers()
importers.add_scraper(AtelierDesChefs)
importers.add_scraper(Marmiton)
if not args.netloc in importers:
    print('unknown website argument:', args.netloc, file=sys.stderr)
    sys.exit(1)

exporters = Exporters()
exporters.add_format(MealMaster)
exporters.add_format(Gourmet)
if not args.format in exporters:
    print('unknown file extension:', args.format, file=sys.stderr)
    sys.exit(1)

recipe_page = getUrl(args.url)
recipe = importers[args.netloc].importRecipe(recipe_page)

out = exporters[args.format](recipe)

if args.outfile:
    print(out, file=open(args.outfile, 'w'))
else:
    print(out)
