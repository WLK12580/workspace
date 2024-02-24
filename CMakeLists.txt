cmake_minimum_required(VERSION 3.20)
project(autocar)
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)  #强制要求c++23版本 防止编译器回退
set(CMAKE_CXX_FLAGS"-Wall -Wextra")
set(CMAKE_CXX_FLAGS_DEBUG"-g")
set(CMAKE_CXX_FLAGS_RELEASE"-O3")
# set(SingletonLib ${CMAKE_SOURCE_DIR}/internal_deps/Singleton CACHE STRING INTERNAL)
include(Config.cmake)
include(CMakeCommon.cmake)

add_subdirectory(internal_deps)
add_subdirectory(src)