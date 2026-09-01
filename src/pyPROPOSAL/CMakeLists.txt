project(pyPROPOSAL LANGUAGES CXX)

set(PYBIND11_FINDPYTHON ON)
find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)
find_package(pybind11 CONFIG REQUIRED)


file(GLOB_RECURSE PYTHON_SRC_FILES ${CMAKE_CURRENT_SOURCE_DIR}/*.cxx)
pybind11_add_module(pyPROPOSAL MODULE
    ${PYTHON_SRC_FILES})

set_target_properties(pyPROPOSAL PROPERTIES
    OUTPUT_NAME proposal)

target_include_directories(pyPROPOSAL PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR})

target_link_libraries(pyPROPOSAL PRIVATE PROPOSAL::PROPOSAL)

# The wheel has no Python package, so the module goes at its root and
# `import proposal` binds straight to it.
install(TARGETS pyPROPOSAL DESTINATION .)
