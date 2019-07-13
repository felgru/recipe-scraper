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

class Exporters(dict):
    def __init__(self):
        from importlib import import_module
        import inspect
        from os.path import join
        from os import walk
        _, _, filenames = next(walk(__path__[0]))
        for f in filenames:
            if f == '__init__.py':
                continue
            mod = inspect.getmodulename(join(__path__[0], f))
            if mod is None:
                continue
            mod = import_module('.'+mod, __name__)
            for elem in dir(mod):
                elem = getattr(mod, elem)
                if inspect.isclass(elem) and hasattr(elem, 'file_extension'):
                    self.add_format(elem)

    def add_format(self, format_class):
        key = format_class.file_extension
        self[key] = format_class

exporters = Exporters()

__all__ = ['exporters']
