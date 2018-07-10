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
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with recipe-scraper.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, print_function, unicode_literals)

import argparse
import sys

from web import getUrl

# importers
from marmiton import readRecipeFromMarmitonPage

# exporters
from gourmet import recipeToGourmet
from mealmaster import recipeToMealMaster

aparser = argparse.ArgumentParser(
        description='transform a recipe from a cooking website into' \
                    ' a machine-readable format')
aparser.add_argument('-f', '--format', action='store', default='m',
                     help='output format: m for mealmaster and g for gourmet')
aparser.add_argument('url', action='store',
                     help='URL of the recipe')
args = aparser.parse_args()

recipe_page = getUrl(args.url)
recipe = readRecipeFromMarmitonPage(recipe_page)
if args.format == 'm':
    print(recipeToMealMaster(recipe))
elif args.format == 'g':
    print(recipeToGourmet(recipe))
else:
    print('unknown format argument:', args.format)
    sys.exit(1)
