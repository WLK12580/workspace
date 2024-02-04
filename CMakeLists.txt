cmake_minimum_required(VERSION 3.20)
project(autocar)
# set(SingletonLib ${CMAKE_SOURCE_DIR}/internal_deps/Singleton CACHE STRING INTERNAL)
include(Config.cmake)
include(CMakeCommon.cmake)
add_subdirectory(internal_deps)

add_subdirectory(src)