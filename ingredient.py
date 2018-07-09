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

class ingredient:
    def __init__(self, name, quantity, unit, optional=False):
        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.optional = optional

    def __str__(self):
        result = '{} {} {}'.format(self.quantity, self.unit, self.name)
        if self.optional:
            result += ' (optional)'
        return result

    def __repr__(self):
        return 'ingredient("{s.name}", {s.quantity}, "{s.unit}",' \
               ' optional={s.optional})'.format(s=self)
