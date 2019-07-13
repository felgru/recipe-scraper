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

class MealMaster:
    file_extension = '.mmf'

    def __init__(self, recipe):
        self.recipe = recipe

    def __str__(self):
        ingredients = ''
        for ingredient in self.recipe.ingredients:
            ingredients += ' ' + str(ingredient) + '\n'
        return 'MMMMM----- Recipe via Meal-Master\n\n' \
               'Title: {r.title}\n' \
               'Cooktime: {r.cooktime}\n' \
               'Preparation Time: {r.preptime}\n' \
               'Yield: {r.portions}\n' \
               'Categories: {cats}\n' \
               'Link: {r.source}\n\n' \
               '{ingredients}\n\n' \
               '{r.instructions_plain}\n\n' \
               'MMMMM\n'.format(r=self.recipe,
                                cats=', '.join(self.recipe.categories),
                                ingredients=ingredients)
