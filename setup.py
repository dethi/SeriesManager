#!/usr/bin/env python3
# -*-coding:Utf-8 -*
#
# Build a package of SeriesManager for Windows.
#
# Syntax:
# ./setup.py build
#
#
# Copyright (C) 2012 Deutsch Thibault <thibault.deutsch@gmail.com>
#
# This file is part of SeriesManager.
#
# SeriesManager is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# SeriesManager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

__APPNAME__ = "SeriesManager"
__VERSION__ = "0.1.0"
__AUTHOR__ = "Deutsch Thibault <thibault.deutsch@gmail.com>"
__WEB__ = "http://www.thionnux.fr/"
__LICENCE__ = "GPL"


# Libraries
#-----------------------------------------------------------------------------

from cx_Freeze import setup, Executable


# Functions
#-----------------------------------------------------------------------------

setup(
    name="SeriesManager",
    version="0.1.O",
    description="Renames the series downloaded.",
    executables=[Executable("windows_launcher.py")],
)
