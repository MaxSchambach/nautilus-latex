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
import sys

try:
    import ConfigParser as configparser
except ImportError:
    import configparser

from gi.repository import Nautilus, GObject

SRC_PATH="@SRC_PATH@"

config = configparser.ConfigParser()

# Read config file, either in 'src' or in 'nautilus-latex-src'
_out = config.read(os.path.join(SRC_PATH, "config.ini"))

if _out == []:
    _out = config.read(os.path.join(SRC_PATH, "src/config.ini"))

if _out == []:
    raise RuntimeError("nautilus-latex: No config file found.")

compiler_def = config.get('default', 'compiler')
compiler = config.get('compiler', compiler_def).replace("'", "")
bib_def = config.get('default', 'bibliography')
bib = config.get('bibliography', bib_def).replace("'", "")

# Load modules from SRC path
sys.path.append(SRC_PATH)
from latex_cleanup import get_extensions, latex_cleanup, is_tex_folder
from support import get_path, get_tex_files, compile_tex


class LatexExtension(Nautilus.MenuProvider, GObject.GObject):
    def __init__(self):
        print("I am a change.")
        pass

    def get_file_items(self, window, files):

        # Read files
        if len(files) != 1:
            return

        file = files[0]
        if file.is_directory() or file.get_uri_scheme() != 'file':
            return

        if not file.get_uri().lower().endswith(".tex"):
            return

        filepath = get_path(file)
        folderpath = os.path.dirname(filepath)

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
            'activate', self.compile_menu_cb, filepath)

        # Sub Menu Item: LaTex Cleanup
        cleanup_menuitem = Nautilus.MenuItem(
            name='LatexExtension::Cleanup',
            label='Cleanup temporary LaTex files',
            tip='',
            icon='')
        cleanup_menuitem.connect(
            'activate', self.cleanup_menu_cb, folderpath)

        # Add menu items to main submenu
        top_submenu.append_item(cleanup_menuitem)
        top_submenu.append_item(compile_menuitem)

        # Add main submenu
        top_menuitem.set_submenu(top_submenu)

        return top_menuitem,

    def get_background_items(self, window, file):

        # Get system path to folder
        folderpath = get_path(file)

        # Check if folder contains tex files, no menu if not
        if not is_tex_folder(folderpath):
            return

        # Get list of tex files in folder
        tex_files = get_tex_files(folderpath)

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
            'activate', self.cleanup_menu_cb, folderpath)

        # Create submenu entry for every tex file in folder

        # Sub Menu Item: LaTex Compilation
        compile_menuitem = Nautilus.MenuItem(
            name='LatexExtension::CompileBG',
            label='Compile',
            tip='',
            icon='')

        # Compile Sub Menu
        compile_submenu = Nautilus.Menu()

        for tex_file in tex_files:

            # Get filename base
            tex_file_base = os.path.basename(tex_file)

            compile_sub_menuitem = Nautilus.MenuItem(
                name='LatexExtension::CompileSubBG' + tex_file_base,
                label=tex_file_base,
                tip='Compile file ' + tex_file_base,
                icon='')
            compile_sub_menuitem.connect(
                'activate', self.compile_menu_cb, tex_file)

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

    # Callback functions
    def compile_menu_cb(self, menu, filepath):
        print("Compiling LaTex file ", filepath)
        compile_tex(filepath, compiler, bib)

    def cleanup_menu_cb(self, menu, filepath):
        latex_cleanup(filepath, get_extensions())
