aux_source_directory(. SRC_DIR )

include_directories(${SingletonInclude})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
add_executable(mysql ${SRC_DIR})
target_link_libraries(mysql mysqlclient)

target_include_directories(mysql PRIVATE ${SingletonInclude})
