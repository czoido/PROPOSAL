project(pyPROPOSAL LANGUAGES CXX)

set(PYBIND11_FINDPYTHON ON)
find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)
find_package(pybind11 CONFIG REQUIRED)


file(GLOB_RECURSE PYTHON_SRC_FILES ${CMAKE_CURRENT_SOURCE_DIR}/*.cxx)
pybind11_add_module(pyPROPOSAL MODULE
    ${PYTHON_SRC_FILES})

# The extension is imported as proposal._proposal, re-exported by
# python/proposal/__init__.py
set_target_properties(pyPROPOSAL PROPERTIES
    OUTPUT_NAME _proposal)

target_include_directories(pyPROPOSAL PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR})

target_link_libraries(pyPROPOSAL PRIVATE PROPOSAL::PROPOSAL)

# Must match the Python package name so the module lands next to __init__.py
# in the wheel.
install(TARGETS pyPROPOSAL DESTINATION proposal)
