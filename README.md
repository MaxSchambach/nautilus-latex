# Latex Temporary Files Cleanup

This is a simple CLI (and Nautilus extension) to delete (or rather: trash) temporary files created by running a full LaTex compilation. 
The CLI trashes files only if the folder contains a ``.tex`` file and is thus considered a LaTex folder.

![](https://github.com/MaxSchambach/github-binaries/blob/master/latex-cleanup.gif)


## Installation

To install both the CLI and the Nautilus extension, simply run from the main repository folder:

    make
    
This installs the script to ``/usr/bin`` and the Nautilus extension to ``~/.local/share/nautilus-python/extensions/``.
If you need to, change the paths in the according install scripts in the `´setup`` folder.

If you only want to install the script or the Nautilus extension (which depends on the script) , run ``make install-cli`` respectively ``make install-extension``.  The Nautilus extension depends on the CLI and the ["nautilus-python" (or "python-nautilus") package](https://github.com/GNOME/nautilus-python/). 

## Uninstallation

To uninstall both the CLI and the extension, simply run

    make uninstall
   
from within the repository folder. To uninstall only the script or the extension, run run ``make uninstall-cli`` respectively ``make uninstall-extension``. 

## Usage

### Command Line Interface
The CLI deletes all temporary LaTex files either from a specified folder:

    latex-cleanup --folder folderPath
    
If no folder is specified, the current folder is cleaned up.

### Nautilus Context Menu Entry
A context menu entry "Clenup Temporary Latex Files" is added which cleans up either the current or the selected folder.

## Temporary Files
To get a list of extensions that are trashed, run

    latex-cleanup --extensions
