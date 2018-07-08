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

import recipe

def recipeToMealMaster(recipe):
    ingredients = ''
    for ingredient in recipe.ingredients:
        ingredients += ' ' + unicode(ingredient) + '\n'
    return 'MMMMM----- Recipe via Meal-Master\n\n' \
           'Title: {r.title}\n' \
           'Cooktime: {r.cooktime}\n' \
           'Preparation Time: {r.preptime}\n' \
           'Yield: {r.portions}\n' \
           'Categories: {cats}\n\n' \
           '{ingredients}\n\n' \
           '{r.description}\n\n' \
           'MMMMM\n'.format(r=recipe, cats=', '.join(recipe.categories),
                            ingredients=ingredients)
