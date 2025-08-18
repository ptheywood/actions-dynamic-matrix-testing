cmake_minimum_required(VERSION 3.18 FATAL_ERROR)

# Main project name wiht no languages
project(admt LANGUAGES NONE)

# Enable CXX 
include(CheckLanguage)
check_language(CXX)
if(CMAKE_CXX_COMPILER)
    enable_language(CXX)
endif()

# Not enabling CUDA to keep CI time down for prototyping
# check_language(CUDA)
# if(CMAKE_CUDA_COMPILER)
    # enable_language(CUDA)
# endif()


# Define some cmake options to control building of certain parts. This is a simplified version that is just enough to check CI behaviour.

option(ADMT_BUILD_DOCS "Enable building docs" OFF)
option(ADMT_BUILD_TESTS "Enable building tests" OFF)
option(ADMT_BUILD_PYTHON "Enable python target" OFF)

# Add other CMakeLists.txt files based on the settings passed in.

add_subdirectory(src "${PROJECT_BINARY_DIR}/admt")

if(ADMT_BUILD_DOCS)
    enable_testing()
    add_subdirectory(docs)
endif()

if(ADMT_BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()

if(ADMT_BUILD_PYTHON)
    add_subdirectory(python)
endif()


# find cpplint, if it's enabled make a target lint.
find_file(CPPLINT_EXECUTABLE NAMES cpplint cpplint.exe)

if(CPPLINT_EXECUTABLE)
    message(STATUS "found cpplint at ${CPPLINT_EXECUTABLE}")

    if(NOT CMAKE_SOURCE_DIR STREQUAL CMAKE_CURRENT_SOURCE_DIR)
        # Use find the repository root via git, to pass to cpplint.
        execute_process(COMMAND git rev-parse --show-toplevel
        WORKING_DIRECTORY "${CMAKE_CURRENT_LIST_DIR}"
        RESULT_VARIABLE git_repo_found
        OUTPUT_VARIABLE abs_repo_root
        OUTPUT_STRIP_TRAILING_WHITESPACE)
        if(git_repo_found EQUAL 0)
            LIST(APPEND CPPLINT_ARGS "--repository=${abs_repo_root}")
        endif()
    endif()

    if(CPPLINT_EXECUTABLE AND NOT TARGET lint)
        add_custom_target(lint COMMAND ${CPPLINT_EXECUTABLE} --recursive ${CMAKE_CURRENT_SOURCE_DIR}/include/ ${CMAKE_CURRENT_SOURCE_DIR}/src/ ${CMAKE_CURRENT_SOURCE_DIR}/python/ ${CMAKE_CURRENT_SOURCE_DIR}/tests/)
        set_target_properties(lint PROPERTIES EXCLUDE_FROM_ALL TRUE)
    endif()
endif()
