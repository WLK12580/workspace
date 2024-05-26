cmake_minimum_required(VERSION 3.14)
project(project)

find_package(VTK REQUIRED)
include_directories(${VTK_INCLUDE_DIRE})

add_executable(${PROJECT_NAME} ./firstvtk.cpp)
target_link_libraries(${PROJECT_NAME} LINK_PRIVATE ${VTK_LIBRARIES})