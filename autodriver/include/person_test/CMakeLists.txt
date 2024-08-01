project(Singleton)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(LIBRARY_OUTPUT_PATH ${CMAKE_BINARY_DIR}/lib)
message("bindir=${PROJECT_SOURCE_DIR}/lib")
aux_source_directory(. SRCS)

add_executable(${PROJECT_NAME} ${SRCS} )