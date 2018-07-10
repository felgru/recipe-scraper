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

import io
import xml.etree.ElementTree as ET

import recipe

def ingredientToGourmet(ingredient):
    ingrXML = ET.Element("ingredient")
    if ingredient.optional:
        ingrXML.attr['optional'] = "yes"
    if ingredient.quantity:
        amount = ET.SubElement(ingrXML, "amount")
        amount.text = str(ingredient.quantity)
    if ingredient.unit:
        unit = ET.SubElement(ingrXML, "unit")
        unit.text = ingredient.unit
    item = ET.SubElement(ingrXML, "item")
    item.text = ingredient.name
    key = ET.SubElement(ingrXML, "key")
    key.text = ingredient.name
    return ingrXML

def recipeToGourmet(recipe):
    gourmetDoc = ET.Element("gourmetDoc")
    r = ET.SubElement(gourmetDoc, "recipe")
    ET.SubElement(r, "title", text=recipe.title)
    ET.SubElement(r, "link", text=recipe.source)
    ET.SubElement(r, "cooktime", text=recipe.cooktime)
    ET.SubElement(r, "yields", text=recipe.portions)
    ingrs = ET.SubElement(r, "ingredient-list")
    for ingredient in recipe.ingredients:
        ingrs.append(ingredientToGourmet(ingredient))
    instructions = ET.SubElement(r, "instructions")
    instructions.text = recipe.instructions
    res = '<?xml version="1.0" encoding="UTF-8"?>\n' \
          '<!DOCTYPE gourmetDoc>\n' \
          + ET.tostring(gourmetDoc) \
              .decode(encoding='utf8')
    return res
