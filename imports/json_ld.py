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

import json
import re

from recipe.instructions import instructions
from recipe.recipe import recipe, Amount

class JsonLdImporter:
    @classmethod
    def importRecipe(cls, page):
        json_ld = find_and_load_json_ld_recipe(page)
        if json_ld is None:
            raise RuntimeError('Generic JSON-LD importer did not find valid JSON-LD on given page.'
                               ' You might want to write a new importer for this site.')
        recipe = json_ld_to_recipe(json_ld)
        return recipe

# Functions to parse recipe entries in json ld.
# https://json-ld.org/
# https://schema.org/Recipe

def find_json_ld(page, start=0):
    json_pattern = re.compile(
            r'<script type="application\/ld\+json">(.*?)</script>',
            re.MULTILINE | re.DOTALL)
    m = json_pattern.search(page, start)
    if m is None:
        return None, len(page)
    # escape line endings, so json doesn't choke on them
    json_text = m.group(1).strip().replace('\r\n','\\n')
    return json_text, m.end()

def load_json_ld(json_text):
    ld_json = json.loads(json_text)
    return ld_json

def find_and_load_json_ld_recipe(page, start=0):
    json_text = True
    while json_text:
        json_text, start = find_json_ld(page, start)
        ld_json = load_json_ld(json_text)
        if ld_json.get('@type') == 'Recipe':
            return ld_json
    return None

def json_ld_to_recipe(ld_json, *, ingredient_parser=None, source=None):
    title = ld_json.get('name')
    cooktime = ld_json.get('cookTime')
    cooktime = Duration.from_ISO_8601(cooktime) \
               if cooktime is not None else None
    preptime = ld_json.get('prepTime')
    preptime = Duration.from_ISO_8601(preptime) \
               if preptime is not None else None
    yields = ld_json.get('recipeYield')
    if yields is not None:
        yields = Amount(*yields.split(maxsplit=1))
    categories = ld_json.get('recipeCategory', [])
    if categories and not isinstance(categories, list):
        categories = [categories]
    ingredients = ld_json.get('recipeIngredient', [])
    if ingredient_parser is not None:
        ingredients = [ingredient_parser(i) for i in ingredients]
    instr = ld_json.get('recipeInstructions')
    if instr is not None:
        if isinstance(instr, list) and instr and isinstance(instr[0], dict) \
           and instr[0].get('@type') == 'HowToStep':
               instr = (i['text'].strip() for i in instr)
        instr = instructions(instr)
    return recipe(
            title = title,
            cooktime = cooktime,
            preptime = preptime,
            yields = yields,
            categories = categories,
            ingredients = ingredients,
            instructions_plain = instr,
            instructions_html = None,
            source = source)

class Duration:
    def __init__(self, date = (None, None, None),
                       time = (None, None, None)):
        self.years = date[0]
        self.months = date[1]
        self.days = date[2]
        self.hours = time[0]
        self.minutes = time[1]
        self.seconds = time[2]

    @classmethod
    def from_ISO_8601(cls, s):
        assert s[0] == 'P'
        dur = dict(year=None,
                   month=None,
                   day=None,
                   hour=None,
                   minute=None,
                   second=None)
        time_start = s.find('T')
        if time_start < 0:
            time_start = len(s)
        date = cls._parse_iso_duration_substring(s[1:time_start], 'YMD')
        time = cls._parse_iso_duration_substring(s[time_start+1:], 'HMS')
        return cls(date, time)

    @staticmethod
    def _parse_iso_duration_substring(s, tokens):
        res = {t: None for t in tokens}
        pos = 0
        end = len(s)
        while pos < end:
            start_pos = pos
            pos += 1
            while pos < end and not s[pos].isalpha():
                pos += 1
            token = s[pos]
            res[token] = s[start_pos:pos]
            pos += 1
        return tuple(res[t] for t in tokens)

    def __str__(self):
        res = []
        if self.years:
            res.append(self.years + ' years')
        if self.months:
            res.append(self.months + ' months')
        if self.days:
            res.append(self.days + ' days')
        if self.hours:
            res.append(self.hours + ' h')
        if self.minutes:
            res.append(self.minutes + ' min')
        if self.seconds:
            res.append(self.seconds + ' s')
        return ' '.join(res)
