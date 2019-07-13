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
from recipe.recipe import recipe

class Marmiton:
    netloc = 'www.marmiton.org'

    @staticmethod
    def readIngredients(recipe_json):
        ingredients_json = recipe_json['ingredients']
        ingredients = []
        for ing in ingredients_json:
            ingredients.append(ingredient(
                ing['name'],
                ing['qty'],
                ing['unit']))
        return ingredients

    @staticmethod
    def readInstructions(instructions_json):
        instructions_html = ('<b>Etappe {}</b>\n\n{}' \
                             .format(etappe, instruction['text'])
                             for etappe, instruction in
                                 enumerate(instructions_json, start=1))
        instructions_html = '\n\n'.join(instructions_html)
        instructions_plain = '\n\n'.join(instruction['text']
                                         for instruction in instructions_json)
        return instructions_plain, instructions_html

    @classmethod
    def importRecipe(cls, page):
        # m = re.search('<meta property="og:title" content="(.*)" />', page)
        # title = m.group(1)
        m = re.search(r'<script type="text/javascript">var Mrtn = Mrtn \|\| \{\}; Mrtn\.recipesData = (.+?);</script>', page)
        all_json = json.loads(m.group(1))
        recipe_json = all_json['recipes'][0]
        title = recipe_json['name']
        source = recipe_json['url']
        # portions = '{} personnes'.format(recipe_json['nb_pers'])
        categories = []
        ingredients = cls.readIngredients(recipe_json)
        m = re.search(r'<div class="recipe-infos__timmings__detail">', page)
        timings_start_pos = m.start()
        prep_pattern = re.compile('<div class="recipe-infos__timmings__preparation">.*?<span class="recipe-infos__timmings__value">\s*(.*?)\s*</span>',
                re.MULTILINE | re.DOTALL)
        m = prep_pattern.search(page, timings_start_pos)
        preptime = m.group(1)
        cook_pattern = re.compile('<div class="recipe-infos__timmings__cooking">.*?<span class="recipe-infos__timmings__value">\s*(.*?)\s*</span>',
                re.MULTILINE | re.DOTALL)
        m = cook_pattern.search(page, timings_start_pos)
        cooktime = m.group(1)
        m = re.search(r'\{"\@context":"http:\/\/schema.org","@type":"Recipe",.+\}',
                      page)
        instructions_json = json.loads(m.group(0))
        instructions_plain, instructions_html = cls.readInstructions(
                instructions_json['recipeInstructions'])
        portions = instructions_json['recipeYield']
        return recipe(
                title = title,
                cooktime = cooktime,
                preptime = preptime,
                portions = portions,
                categories = categories,
                ingredients = ingredients,
                instructions_plain = instructions_plain,
                instructions_html = instructions_html,
                source = source)
