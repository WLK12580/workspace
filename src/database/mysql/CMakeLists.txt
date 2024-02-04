aux_source_directory(. SRC_DIR )
message("mysql=${SRC_DIR}")

add_executable(mysql ${SRC_DIR})
target_link_libraries(mysql mysqlclient)

# target_include_directories(mysql PRIVATE)
