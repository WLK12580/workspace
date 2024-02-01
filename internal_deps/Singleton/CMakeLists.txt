project(SingletonTest)


aux_source_directory(. SRCS)


# add_library(${PROJECT_NAME} SHARED ${SRCS})
add_executable(${PROJECT_NAME} ${SRCS})