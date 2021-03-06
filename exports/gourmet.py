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

import xml.etree.ElementTree as ET

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

class Gourmet:
    file_extension = '.grmt'

    def __init__(self, recipe):
        self.recipe = recipe

    def __str__(self):
        gourmetDoc = ET.Element("gourmetDoc")
        r = ET.SubElement(gourmetDoc, "recipe", id="1")
        title = ET.SubElement(r, "title")
        title.text = self.recipe.title
        link = ET.SubElement(r, "link")
        link.text = self.recipe.source
        preptime = ET.SubElement(r, "preptime")
        preptime.text = str(self.recipe.preptime)
        cooktime = ET.SubElement(r, "cooktime")
        cooktime.text = str(self.recipe.cooktime)
        yields = ET.SubElement(r, "yields")
        yields.text = str(self.recipe.yields)
        ingrs = ET.SubElement(r, "ingredient-list")
        for ingredient in self.recipe.ingredients:
            ingrs.append(ingredientToGourmet(ingredient))
        instructions = ET.SubElement(r, "instructions")
        instructions.text = str(self.recipe.instructions_html) \
                if self.recipe.instructions_html \
                else str(self.recipe.instructions_plain)
        res = '<?xml version="1.0" encoding="UTF-8"?>\n' \
              '<!DOCTYPE gourmetDoc>\n' \
              + ET.tostring(gourmetDoc) \
                  .decode(encoding='utf8')
        return res
