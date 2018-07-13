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
        key = format_class.format_string()
        self[key] = format_class

class Importers(dict):
    def add_scraper(self, scraper_class):
        key = scraper_class.netloc()
        self[key] = scraper_class

aparser = argparse.ArgumentParser(
        description='transform a recipe from a cooking website into' \
                    ' a machine-readable format')
aparser.add_argument('-f', '--format', action='store', default='m',
                     help='output format: m for mealmaster and g for gourmet')
# -i specifies the netloc of the webscraper to use,
# This is useful for development so that we can specify the scraper
# when reading from a saved html file.
aparser.add_argument('-i', '--input-site', dest='netloc',
                     action='store', default=None,
                     help=argparse.SUPPRESS)
aparser.add_argument('url', action='store',
                     help='URL of the recipe')
args = aparser.parse_args()

importers = Importers()
importers.add_scraper(AtelierDesChefs)
importers.add_scraper(Marmiton)
if not args.netloc:
    args.netloc = urllib.parse.urlparse(args.url).netloc

if args.netloc in importers:
    recipe_page = getUrl(args.url)
    recipe = importers[args.netloc].importRecipe(recipe_page)
else:
    print('unknown website argument:', args.netloc)
    sys.exit(1)

exporters = Exporters()
exporters.add_format(MealMaster)
exporters.add_format(Gourmet)
if args.format in exporters:
    out = exporters[args.format](recipe)
else:
    print('unknown format argument:', args.format)
    sys.exit(1)
print(out)
