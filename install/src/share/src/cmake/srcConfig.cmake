# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_src_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED src_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(src_FOUND FALSE)
  elseif(NOT src_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(src_FOUND FALSE)
  endif()
  return()
endif()
set(_src_CONFIG_INCLUDED TRUE)

# output package information
if(NOT src_FIND_QUIETLY)
  message(STATUS "Found src: 0.0.0 (${src_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'src' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${src_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(src_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${src_DIR}/${_extra}")
endforeach()
