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

class Marmiton:
    @staticmethod
    def netloc():
        return 'www.marmiton.org'

    @staticmethod
    def readIngredients(recipe_json):
        ingredients_json = recipe_json['ingredients']
        ingredients = []
        for ing in ingredients_json:
            ingredients.append(ingredient.ingredient(
                ing['name'],
                ing['qty'],
                ing['unit']))
        return ingredients

    @staticmethod
    def readInstructions(instructions_json):
        instructions_html = '<b>Etape 1</b>\n\n' \
                + instructions_json[0]['text']
        instructions_plain = instructions_json[0]['text']
        etappe = 2
        for instruction in instructions_json[1:]:
            instructions_plain += '\n\n' + instruction['text']
            instructions_html += '\n\n<b>Etappe {}</b>\n\n{}' \
                    .format(etappe, instruction['text'])
            etappe += 1
        return instructions_plain, instructions_html

    @staticmethod
    def importRecipe(page):
        # m = re.search('<meta property="og:title" content="(.*)" />', page)
        # title = m.group(1)
        m = re.search(r'<script type="text/javascript">var Mrtn = Mrtn \|\| \{\}; Mrtn\.recipesData = (.+?);</script>', page)
        all_json = json.loads(m.group(1))
        recipe_json = all_json['recipes'][0]
        title = recipe_json['name']
        source = recipe_json['url']
        # portions = '{} personnes'.format(recipe_json['nb_pers'])
        categories = []
        ingredients = Marmiton.readIngredients(recipe_json)
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
        instructions_plain, instructions_html = Marmiton.readInstructions(
                instructions_json['recipeInstructions'])
        portions = instructions_json['recipeYield']
        return recipe.recipe(
                title = title,
                cooktime = cooktime,
                preptime = preptime,
                portions = portions,
                categories = categories,
                ingredients = ingredients,
                instructions_plain = instructions_plain,
                instructions_html = instructions_html,
                source = source)
