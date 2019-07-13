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

class ingredient:
    def __init__(self, name, amount, optional=False):
        self.name = name
        self.amount = amount
        self.optional = optional

    @property
    def quantity(self):
        if self.amount is None:
            return None
        return self.amount.quantity

    @property
    def unit(self):
        if self.amount is None:
            return None
        return self.amount.unit

    def __str__(self):
        result = '{} {}'.format(self.amount, self.name)
        if self.optional:
            result += ' (optional)'
        return result

    def __repr__(self):
        return 'ingredient({s.name!r}, {s.amount!r}, optional={s.optional})' \
               .format(s=self)
