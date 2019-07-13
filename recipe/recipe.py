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

class recipe:
    def __init__(self, title, cooktime, preptime, yields, categories,
                 ingredients, instructions_plain=None,
                 instructions_html=None, source=None):
        self.title = title
        self.cooktime = cooktime
        self.preptime = preptime
        self.yields = yields
        self.categories = categories
        self.ingredients = ingredients
        self.instructions_plain = instructions_plain
        self.instructions_html = instructions_html
        self.source = source

class Amount:
    def __init__(self, quantity, unit=None):
        self.quantity = quantity
        self.unit = unit

    def __str__(self):
        if self.unit is None:
            return str(self.quantity)
        return '{s.quantity} {s.unit}'.format(s=self)

    def __repr__(self):
        if self.unit is None:
            return 'Amount({!r})'.format(self.quantity)
        return 'Amount({s.quantity!r}, {s.unit!r})'.format(s=self)
