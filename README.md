# Nautilus LaTex extension
This is a simple Nautilus extension for basic LaTex usage such as compiling and deleting temporary files.

![](https://github.com/MaxSchambach/github-binaries/blob/master/nautilus-latex.gif)


## Installation

To install the extension run

    mkdir build
    cd build
    cmake ..
    make
    make install
    
If needed, adapt the installation paths in the `CMakeLists.txt` file.
By default, the extension is installed to ``~/.local/share/nautilus-python/extensions``
and the supporting files to ``~/.local/share/nautilus-latex``.

### Dependencies
The Python bindings for the Nautilus extension uses the ``python-nautilus`` package of the GNOME project.

### Command Line Interface
Additional to the Nautilus extension, there is a simple CLI for
cleaning up temporary LaTex files. To install, simply run

    sudo ./install_cli
    
from within the repository folder. For usage, see

    latex-cleanup --help


## Uninstallation

To uninstall, run

    make uninstall
   
from within the ``build`` folder.
