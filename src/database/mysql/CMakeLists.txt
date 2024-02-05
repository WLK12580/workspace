aux_source_directory(. SRC_DIR )

include_directories(${SingletonInclude})
add_executable(mysql ${SRC_DIR})
target_link_libraries(mysql mysqlclient)

target_include_directories(mysql PRIVATE ${SingletonInclude})
