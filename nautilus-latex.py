# Copyright (C) 2018  Maximilian Schambach
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Nautilus extension for LaTex related tasks.
"""

import os

try:
    from urllib import unquote
except ImportError:
    from urllib.parse import unquote

try:
    import ConfigParser
except ImportError:
    import configparser

from gi.repository import Nautilus, GObject

config = configparser.ConfigParser()

# Read config file, either in 'src' or in 'nautilus-latex-src'
_out = config.read('nautilus-latex-src/config.ini')

if _out == []:
    _out = config.read('src/config.ini')

if _out == []:
    raise RuntimeError("nautilus-latex: No config file found.")

compiler_def = config['default']['compiler']
compiler = config['compiler'][compiler_def]
bib_def = config['default']['bibliography']
bib = config['bibliography'][bib_def]


class LatexExtension(Nautilus.MenuProvider, GObject.GObject):
    def __init__(self):
        pass

    def get_file_items(self, window, files):

        # Read files
        if len(files) != 1:
            return

        file = files[0]
        if file.is_directory() or file.get_uri_scheme() != 'file':
            return

        print("FILES: ", file.get_uri_scheme())

        # Top Menu
        top_menuitem = Nautilus.MenuItem(name='LatexExtension::Latex',
                                         label='LaTex',
                                         tip='',
                                         icon='')

        # Main Sub Menu
        top_submenu = Nautilus.Menu()

        # Menu Item: LaTex Compilation
        compile_menuitem = Nautilus.MenuItem(
            name='LatexExtension::Compile',
            label='Compile File',
            tip='',
            icon='')
        compile_menuitem.connect(
            'activate', self.compile_menu_activate_cb, file)

        # Add menu items to main submenu
        top_submenu.append_item(compile_menuitem)

        # Add main submenu
        top_menuitem.set_submenu(top_submenu)

        return top_menuitem,


    def get_background_items(self, window, file):
        # Top Menu
        top_menuitem = Nautilus.MenuItem(name='LatexExtension::LatexBG',
                                         label='LaTex',
                                         tip='',
                                         icon='')

        # Main Sub Menu
        top_submenu = Nautilus.Menu()

        # Sub Menu Item: LaTex Cleanup
        cleanup_menuitem = Nautilus.MenuItem(
            name='LatexExtension::CleanupBG',
            label='Cleanup temporary LaTex files',
            tip='',
            icon='')
        cleanup_menuitem.connect(
            'activate', self.cleanup_menu_background_activate_cb, file)

        # Sub Menu Item: LaTex Compilation
        compile_menuitem = Nautilus.MenuItem(
            name='LatexExtension::CompileBG',
            label='Compile',
            tip='',
            icon='')

        # Compile Sub Menu
        compile_submenu = Nautilus.Menu()
        compile_sub_menuitem = Nautilus.MenuItem(
            name='LatexExtension::CompileSub1BG',
            label='Compile 1.tex',
            tip='',
            icon='')
        compile_sub_menuitem.connect(
            'activate', self.compile_menu_background_activate_cb, file)

        # Add compile submenu items
        compile_submenu.append_item(compile_sub_menuitem)

        # Add compile submenu
        compile_menuitem.set_submenu(compile_submenu)

        # Add menu items to main submenu
        top_submenu.append_item(cleanup_menuitem)
        top_submenu.append_item(compile_menuitem)

        # Add main submenu
        top_menuitem.set_submenu(top_submenu)

        return top_menuitem,

    # File item actions
    def compile_menu_activate_cb(self, menu, file):
        print("Compiling file...")
        ...

    # Background item actions
    def cleanup_menu_background_activate_cb(self, menu, file):
        print("Cleanup LaTex files...")
        ...

    def compile_menu_background_activate_cb(self, menu, file):
        print("Compile LaTex file ONE...")
        ...
