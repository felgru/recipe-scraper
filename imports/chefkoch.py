# -*- coding: utf-8 -*-
#
# Copyright (C) 2019  Felix Gruber
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

import re

from recipe.ingredient import ingredient
from recipe.recipe import Amount

from .json_ld import *

class Chefkoch:
    netloc = 'www.chefkoch.de'

    @classmethod
    def importRecipe(cls, page):
        url_pattern = re.compile(r'<link rel="canonical" href="(.+?)">')
        m = url_pattern.search(page)
        source = m.group(1)
        json_ld = find_and_load_json_ld_recipe(page, m.end())
        recipe = json_ld_to_recipe(json_ld,
                                   ingredient_parser = cls._parse_ingredient,
                                   source = source)
        return recipe

    @classmethod
    def _parse_ingredient(cls, ingr):
        ingr_pattern = re.compile('(.*?) (.*?) (.+)')
        m = ingr_pattern.match(ingr)
        quantity = m.group(1).rstrip('0').rstrip(',')
        unit = m.group(2).strip() or None
        name = m.group(3).replace(' ,', ',')
        return ingredient(name, Amount(quantity, unit))
