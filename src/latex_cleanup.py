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

import argparse
import os
from pathlib import Path

# Argument setup
parser = argparse.ArgumentParser(
  description="Delete all temporary LaTex files contained in a folder.")

parser.add_argument('-f', '--folder', type=str,
  default="./",
  help='Folder to clean up from latex files. Default: Current')

parser.add_argument('-d', '--dry', action='store_true',
                    help='Dry run. Prints a list of files that would be cleaned up.')

parser.add_argument('-e', '--extensions', action='store_true',
                    help='Print a list of extensions that are considered temporary files.')

parser.add_argument('-r', '--recursive', action='store_true',
                    help='Recursively search subfolders for temporary files.')

parser.add_argument('--rm', action='store_true',
                    help='Use /bin/rm instead of trashing to delete files.')

args = parser.parse_args()

# Extract arguments
folder = args.folder
dry = args.dry
show_ext = args.extensions
recursive = args.recursive
rm = args.rm

# Get current path
folderpath = Path(folder)


def is_tex_folder(folderpath):
    """Determine if a folder contains any tex files.
    Args:
        folderpath: System path of folder.
    Returns:
        True, if folder contains at least one tex file, else False.
    """

    if [f for f in folderpath.glob("*.tex")]:
        return True

    return False


def get_extensions():
    # Extensions to cleanup
    extensions = [".aux", ".auxlock", ".bbl", ".bcf", ".blg", ".brf", ".dvi",
                  ".glo", ".idx", ".ilg", ".ind", ".log", ".lot", ".lof", ".ist",
                  ".out", ".ps", ".xml", ".gz", ".thm", ".md5", ".dpth",
                  ".toc", ".nls", ".nlo", ".nav", ".snm", ".upa", ".fls", ".fdb_latexmk",
                  ".Xabbr", ".Xglos", ".Xmathop", ".Xparam", ".Xsubsup", ".Xsym", ".Xincludes", ".gls"]

    # Remove possible duplicates
    extensions = list(set(extensions))

    return extensions


def get_excludes():
    # Folders to exlcude from cleanup
    excludes = [".git/", ".idea/"]
    return excludes


def latex_cleanup(folderpath, extensions, excludes, rm):
    """Cleanup temporary LaTex files in a LaTex folder.
    The folder must contain at least one .tex file to be a LaTex folder.
    Otherwise, no files are deleted.
    Args:
        folderpath: System path to the folder.
        extensions: A list of file extensions considered temporary files.
    Returns: List of deleted files. Returns None if no files were deleted.
    """

    # Get all temporary files
    if recursive:
        pattern = "**/*"
    else:
        pattern = "*"


    def exclude(file):
        res = False
        for ex in excludes:
            if ex in str(file):
                return True
        return False

    files = [f for f in folderpath.glob(pattern)
             if f.suffix in extensions \
             and not exclude(f)]

    # Delete files, if .tex file and temporary files were found
    if files:
        for file in files:
            if not dry:
                if rm:
                    os.system("/bin/rm '" + str(file) + "'")
                else:
                    os.system("gio trash '" + str(file) + "'")
        return files

    else:
        return None


if __name__ == "__main__":

    extensions = get_extensions()
    excludes = get_excludes()

    if show_ext:
        print(extensions)

    else:
        print("Cleaning up temporary LaTex files...")
        if recursive:
            print("Recursive cleanup...")
            print("Excluding folders", excludes)
        if dry:
            print("Dry run. Will not delete any files.")


        if is_tex_folder(folderpath):
            res = latex_cleanup(folderpath, extensions, excludes, rm)
            if res is None:
                print("No temporary LaTex files found.")

            else:
                if dry:
                    print("Found ", len(res), "temporary files:")
                    print([str(f) for f in res])
                else:
                    print("Trashed ", len(res), " temporary files.")

        else:
            print("No files were cleaned up. The folder is not a LaTex folder.")
