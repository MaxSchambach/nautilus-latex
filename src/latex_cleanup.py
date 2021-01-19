#!/usr/bin/python

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


"""Script and CLI to delete all temporary LaTex files"""
import os
import argparse

# Argument setup
parser = argparse.ArgumentParser(
  description="Delete all temporary LaTex files contained in a folder.")

parser.add_argument('-f', '--folder', type=str,
  default="./",
  help='Folder to clean up from latex files. Default: Current')

parser.add_argument('-e', '--extensions', action='store_true',
                    help='Print a list of extensions that are considered temporary files.')

args = parser.parse_args()

# Extract arguments
folder = args.folder
show_ext = args.extensions

# Get current path
folderpath = os.path.abspath(folder)


def is_tex_folder(folderpath):
    """Determine if a folder contains any tex files.

    Args:
        folderpath: System path of folder.

    Returns:
        True, if folder contains at least one tex file, else False.
    """

    # Go through folder
    for file in os.listdir(folderpath):

        if file.lower().endswith(".tex"):
            return True

    return False


def get_extensions():
    # Extensions to cleanup
    extensions = [".aux", ".auxlock", ".bbl", ".bcf", ".blg", ".brf", ".dvi",
                  ".glo", ".idx", ".ilg", ".ind", ".log", ".lot", ".lof", ".ist",
                  ".out", ".ps", ".xml", ".synctex.gz", ".thm", ".md5", ".dpth",
                  ".toc", ".nls", ".nlo", ".nav", ".snm", ".upa", ".fls", ".fdb_latexmk",
                  ".xabbr", ".xglos", ".xmathop", ".xparam", ".xsubsup", ".xsym", ".xincludes", ".gls"]
    # Remove possible duplicates
    extensions = list(set(extensions))
    extensions.sort()

    return extensions


def latex_cleanup(folderpath, extensions):
    """Cleanup temporary LaTex files in a LaTex folder.

    The folder must contain at least one .tex file to be a LaTex folder.
    Otherwise, no files are deleted.

    Args:
        folderpath: System path to the folder.

        extensions: A list of file extensions considered temporary files.

    Returns: List of deleted files. Returns None if no files were deleted.

    """

    file_list = []

    # Go through folder
    for file in os.listdir(folderpath):
        # Check if file ends with extension
        for ext in extensions:
            if file.lower().endswith(ext):
                file_list.append(os.path.join(folderpath, file))

    # Delete files, if .tex file and temporary files were found
    if len(file_list) != 0:
        for file in file_list:
            os.system("gio trash '" + file + "'")
        return file_list

    else:
        return None


if __name__ == "__main__":

    extensions = get_extensions()

    if show_ext:
        print(extensions)

    else:
        print("Cleaning up temporary LaTex files...")

        if is_tex_folder(folder):
            res = latex_cleanup(folder, extensions)
            if res is None:
                print("No temporary LaTex files found.")

            else:
                print("Trashed ", len(res), " temporary files.")

        else:
            print("No files were cleaned up. The folder is not a LaTex folder.")
