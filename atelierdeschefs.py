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

import json
import re
import sys

import ingredient
import recipe

class AtelierDesChefs:
    @staticmethod
    def netloc():
        return 'www.atelierdeschefs.fr'

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
            ingredients.append(ingredient.ingredient(name, quantity, unit))
        return ingredients

    @staticmethod
    def parseInstructions(ld_json):
        inst_list = ld_json["recipeInstructions"]
        instructions_plain = inst_list[0]
        for instruction in inst_list[1:]:
            instructions_plain += '\n\n' + instruction
        return instructions_plain

    @staticmethod
    def importRecipe(page):
        m = re.search(r'<meta property="og:url" content="(.+?)">', page)
        source = m.group(0)
        m = re.search(r'<span itemprop="title">\s*(.+?)\s*</span>', page)
        title = m.group(0)
        ingredients_pattern = re.compile('<div class="ingredients.*?</div>',
                                         re.MULTILINE | re.DOTALL)
        m = ingredients_pattern.search(page)
        (ingr_begin, ingr_end) = (m.start(), m.end())
        ingredients = AtelierDesChefs.parseIngredients(page[ingr_begin:ingr_end])
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
        instructions_plain = AtelierDesChefs.parseInstructions(ld_json)
        print(instructions_plain)
        m = re.search(r'alt="Temps de préparation ".*?<span>\s*(.+?)\s',
                      page, re.MULTILINE | re.DOTALL)
        preptime = m.group(1)
        m = re.search(r'alt="Temps de cuisson ".*?<span>\s*(.+?)\s',
                      page, re.MULTILINE | re.DOTALL)
        cooktime = m.group(1)
        return recipe.recipe(
                title = title,
                cooktime = cooktime,
                preptime = preptime,
                portions = persons + ' personnes',
                categories = [],
                ingredients = ingredients,
                instructions_plain = instructions_plain,
                instructions_html = None,
                source = source)
