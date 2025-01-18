# version

## About

Python sript to Handle SW version build information for C/C++ projects.
The script does not update version numbers, but saves information about the version and the current build.


## Features
- requires Python v3
- conforms to Semantic Versioning 2.0.0 https://semver.org/
- saves information into C/C++ source files
- avoids unnecessary updates of source files when the version information remains the same
- saves version information
- saves current sources version (support: HG) 
- saves current build date


## Usage
- get vesion.py
- adjust VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH, VERSION_PRERELEASE as needed
- run script when it is necessary to remember vesion information

### manual use
> python3 version.py

### CMake integration
``` Cmake
find_package(Python3 COMPONENTS Interpreter REQUIRED)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# generate_version
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
add_custom_target(generate_version 
  COMMAND ${Python3_EXECUTABLE} version.py
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  DEPENDS version.py)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# END OF generate_version
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


add_executable(FOOEXE ...)
add_dependencies(FOOEXE generate_version)
...
