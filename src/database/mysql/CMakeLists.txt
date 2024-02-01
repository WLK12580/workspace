aux_source_directory(. SRC_DIR )
message("mysql=${SRC_DIR}")


message("Singleton_path=${SingletonLib}")

add_executable(mysql ${SRC_DIR})
target_link_libraries(mysql mysqlclient)

target_include_directories(mysql PRIVATE ${SingletonLib})
