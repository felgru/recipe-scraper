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
from recipe.recipe import recipe, Amount

class AtelierDesChefs:
    netloc = 'www.atelierdeschefs.fr'

    @staticmethod
    def parseIngredients(ingredients_html):
        ingredients = []
        ingredient_pattern = re.compile(
            r'<li>\s*<span class="ingredient">(.+?) : </span>'
            r'\s*<span class="quantite bold">(\S+)\s*(.*?)</span>\s*</li>',
            re.MULTILINE)
        for m in ingredient_pattern.finditer(ingredients_html):
            name = m.group(1)
            quantity = m.group(2)
            unit = m.group(3)
            ingredients.append(ingredient(name, quantity, unit))
        return ingredients

    @staticmethod
    def parseTime(time, page):
        m = re.search(r'alt="Temps de ' + time + ' ".*?<span>\s*(.+?)\s',
                      page, re.MULTILINE | re.DOTALL)
        time = m.group(1)
        return time.replace('mn',' min')

    @staticmethod
    def parseInstructions(ld_json):
        inst_list = (s.replace('Etape :', 'Etape ')
                     for s in ld_json["recipeInstructions"])
        return instructions(inst_list)

    @classmethod
    def importRecipe(cls, page):
        m = re.search(r'<meta property="og:url" content="(.+?)">', page)
        source = m.group(1)
        m = re.search(r'<h1>Recette de (.+?)</h1>', page)
        title = m.group(1)
        ingredients_pattern = re.compile('<div class="ingredients.*?</div>',
                                         re.MULTILINE | re.DOTALL)
        m = ingredients_pattern.search(page)
        (ingr_begin, ingr_end) = (m.start(), m.end())
        ingredients = cls.parseIngredients(page[ingr_begin:ingr_end])
        m = re.search(r'<input type="hidden" name="nb_pers_recette" value="(.+?)">',
                page)
        persons = m.group(1)
        json_pattern = re.compile(
                r'<script type="application\/ld\+json">(.*?)</script>',
                re.MULTILINE | re.DOTALL)
        # start from the end of the last match to find the right json object
        m = json_pattern.search(page, m.end())
        # escape line endings, so json doesn't choke on them
        json_text = m.group(1).strip().replace('\r\n','\\n')
        ld_json = json.loads(json_text)
        instructions_plain = cls.parseInstructions(ld_json)
        preptime = cls.parseTime('préparation', page)
        cooktime = cls.parseTime('cuisson', page)
        return recipe(
                title = title,
                cooktime = cooktime,
                preptime = preptime,
                yields = Amount(persons, 'personnes'),
                categories = [],
                ingredients = ingredients,
                instructions_plain = instructions_plain,
                instructions_html = None,
                source = source)
