# Nautilus LaTex extension

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
