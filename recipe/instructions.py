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

from collections.abc import Iterable

class instructions:
    def __init__(self, data):
        if isinstance(data, str):
            self.data = data
        elif isinstance(data, Iterable):
            self.data = list(data)
        else:
            raise TypeError('Invalid type: {};'.format(type(data))
                    + ' instructions expect to be constructed'
                      ' from string or iterable.')

    def is_list(self):
        return isinstance(self.data, list)

    def __iter__(self):
        if not self.is_list():
            raise ValueError('Trying to iterate over instructions that'
                             ' are not given as a list.')
        return iter(self.data)

    def __str__(self):
        data = self.data
        if isinstance(data, str):
            return data
        else:
            return '\n\n'.join(data)

    def __repr__(self):
        return 'instructions({!r})'.format(self.data)
