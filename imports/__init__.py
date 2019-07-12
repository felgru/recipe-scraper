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

from .atelierdeschefs import AtelierDesChefs
from .marmiton import Marmiton
from .web import getUrl

class Importers(dict):
    def add_scraper(self, scraper_class):
        key = scraper_class.netloc()
        self[key] = scraper_class

importers = Importers()
importers.add_scraper(AtelierDesChefs)
importers.add_scraper(Marmiton)
