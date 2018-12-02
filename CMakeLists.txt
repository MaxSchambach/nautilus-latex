cmake_minimum_required(VERSION 2.6)
project(NautilusLatex NONE)

set (NautilusLatex_VERSION_MAJOR 0)
set (NautilusLatex_VERSION_MINOR 1)

# Configurable paths
set(EXT_PATH "~/.local/share/nautilus-python/extensions" CACHE FILEPATH "Path to Nautilus extension.")
set(SRC_PATH "~/.local/share/nautilus-latex" CACHE FILEPATH "Path to extension support files.")

# Configure files
configure_file(nautilus-latex.py nautilus-latex.py)
configure_file(src/latex_cleanup.py src/latex_cleanup.py)
configure_file(src/support.py src/support.py)
configure_file(src/config.ini src/config.ini)

# Extensions files
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/nautilus-latex.py"
        PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ GROUP_EXECUTE GROUP_READ WORLD_EXECUTE WORLD_READ
        DESTINATION ${EXT_PATH})

install(FILES "${CMAKE_CURRENT_BINARY_DIR}/src/support.py"
        PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ GROUP_EXECUTE GROUP_READ WORLD_EXECUTE WORLD_READ
        DESTINATION ${SRC_PATH})

install(FILES "${CMAKE_CURRENT_BINARY_DIR}/src/latex_cleanup.py"
        PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ GROUP_EXECUTE GROUP_READ WORLD_EXECUTE WORLD_READ
        DESTINATION ${SRC_PATH})

install(FILES "${CMAKE_CURRENT_BINARY_DIR}/src/config.ini"
        PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ GROUP_EXECUTE GROUP_READ WORLD_EXECUTE WORLD_READ
        DESTINATION ${SRC_PATH})


# Uninstall target
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/cmake/cmake_uninstall.cmake.in"
               "${CMAKE_CURRENT_BINARY_DIR}/cmake/cmake_uninstall.cmake" IMMEDIATE @ONLY)
add_custom_target(uninstall COMMAND ${CMAKE_COMMAND}
                  -P ${CMAKE_CURRENT_BINARY_DIR}/cmake/cmake_uninstall.cmake)
