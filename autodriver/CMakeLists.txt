cmake_minimum_required(VERSION 3.22)
project(autodirver)
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)  #强制要求c++23版本 防止编译器回退
set(CMAKE_CXX_FLAGS"-Wall -Wextra")
set(CMAKE_CXX_FLAGS_DEBUG"-g")
set(CMAKE_CXX_FLAGS_RELEASE"-O3")
enable_testing()

MESSAGE(STATUS "可执行程序的目录（绝对路径）：" ${PROJECT_BINARY_DIR})
MESSAGE(STATUS "当前目录（绝对路径）：" ${PROJECT_SOURCE_DIR})
MESSAGE(STATUS "当前文件的绝对路径（含文件名）：" ${CMAKE_CURRENT_LIST_FILE})
MESSAGE(STATUS "当前目录的绝对路径（不含文件名）：" ${CMAKE_CURRENT_SOURCE_DIR})

# 删除末尾的'/'
string(REGEX REPLACE "/$" "" CURRENT_FOLDER_ABSOLUTE ${CMAKE_CURRENT_SOURCE_DIR})
MESSAGE(STATUS "当前目录的绝对路径：" ${CURRENT_FOLDER_ABSOLUTE})

# 获取当前目录的相对路径
string(REGEX REPLACE ".*/(.*)" "\\1" CURRENT_FOLDER ${CURRENT_FOLDER_ABSOLUTE})
MESSAGE(STATUS "当前目录名：" ${CURRENT_FOLDER})


include(${PROJECT_SOURCE_DIR}/cmake/Config.cmake)
include(${PROJECT_SOURCE_DIR}/cmake/CMakeCommon.cmake)

add_subdirectory(include)
add_subdirectory(src)
