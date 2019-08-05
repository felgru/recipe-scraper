# -*- coding: utf-8 -*-
#
# Copyright (C) 2018–2019  Felix Gruber
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

import json
import re

from recipe.ingredient import ingredient
from recipe.instructions import instructions
from recipe.recipe import Amount

from .json_ld import *

class Marmiton:
    netloc = 'www.marmiton.org'

    @classmethod
    def importRecipe(cls, page):
        m = re.search(r'<script type="text/javascript">var Mrtn = Mrtn \|\| \{\}; Mrtn\.recipesData = (.+?);</script>', page)
        metadata_json = json.loads(m.group(1))
        source = metadata_json['recipes'][0]['url']
        m = re.search(r'\{"\@context":"http:\/\/schema.org","@type":"Recipe",.+\}',
                      page)
        json_ld = load_json_ld(m.group(0))
        recipe = json_ld_to_recipe(json_ld,
                                   ingredient_parser = cls._parse_ingredient,
                                   source = source)
        instructions_html = ('<b>Etappe {}</b>\n\n{}' \
                             .format(etappe, instr)
                             for etappe, instr in
                                 enumerate(recipe.instructions_plain, start=1))
        recipe.instructions_html = instructions(instructions_html)
        return recipe

    @classmethod
    def _parse_ingredient(cls, ingr):
        ingr_pattern = re.compile(r'(\d\S*)?\s*\b(\S*? de|.*?)\s*\b(.+)')
        m = ingr_pattern.match(ingr)
        quantity = m.group(1) or None
        unit = m.group(2) or None
        amount = Amount(quantity, unit) if quantity is not None else None
        name = m.group(3)
        optional_pattern = re.compile(r'(.+) \(facultatif\)$')
        optional = optional_pattern.match(name)
        if optional is not None:
            name = optional.group(1)
        ingr = ingredient(name, amount, bool(optional))
        return ingr
