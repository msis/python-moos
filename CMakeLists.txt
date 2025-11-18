cmake_minimum_required(VERSION 3.11)
project (python-moos)

find_package(MOOS 10 REQUIRED)

add_subdirectory(pybind11)
pybind11_add_module(pymoos src/pyMOOS.cpp)
include_directories(${MOOS_INCLUDE_DIRS})
target_link_libraries(pymoos PRIVATE ${MOOS_LIBRARIES})
