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

import os

# Python 3 and 2 compatible
try:
    from urllib import unquote
except ImportError:
    from urllib.parse import unquote

def get_path(file):
    """Get file path from a NautilusVFSFile file.

    Args:
        file:

    Returns: System path of the NautilusVFSFile file.

    """

    # Get filepath, remove file:// prefix
    filepath = file.get_uri()[7:]
    return unquote(os.path.abspath(filepath))


def get_tex_files(folder):
    """Get a list of tex files in a folder.

    Args:
        folder:

    Returns: List of tex files in a folder. If no files are found, returns None.

    """

    file_list = []

    # Go through current folder
    for file in os.listdir(folder):
        # Check if file ends with extension
        if file.lower().endswith(".tex"):
            file_list.append(os.path.join(folder, file))

    if len(file_list) == 0:
        return None

    else:
        return file_list


def compile_tex(filepath, compiler, bib):

    dir = os.path.dirname(filepath)
    filename = "./" + os.path.basename(filepath)
    filebase = "./" + os.path.splitext(filename)[0]

    output = " > /dev/null"

    command = "cd '" + dir + "' && "
    command += compiler + " '" + filename + "' " +  output + " && "
    command += compiler + " '" + filename + "' " + output + " && "
    command += bib + " '" + filename + "' " + output + " && "
    command += compiler + " '" + filename + "' " + output
    res = os.system(command)
    return res
