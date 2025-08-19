cmake_minimum_required(VERSION 3.18 FATAL_ERROR)

project(pyadmt LANGUAGES CXX)

if(PYTHON3_EXACT_VERSION)
    set(PYTHON3_EXACT_VERSION_ARG ${PYTHON3_EXACT_VERSION} EXACT)
endif()
find_package(Python3 ${PYTHON3_EXACT_VERSION_ARG} REQUIRED COMPONENTS Interpreter Development.Module)
message(STATUS "Python ${Python3_VERSION} found at " ${Python3_EXECUTABLE})

SET(SRC
    ${CMAKE_CURRENT_SOURCE_DIR}/main.cpp
)
add_executable(${PROJECT_NAME} ${SRC})

target_compile_definitions(${PROJECT_NAME} PUBLIC "PYTHON_VERSION_MAJOR=${Python3_VERSION_MAJOR}")
target_compile_definitions(${PROJECT_NAME} PUBLIC "PYTHON_VERSION_MINOR=${Python3_VERSION_MINOR}")

target_link_libraries(${PROJECT_NAME} admt)
target_include_directories(${PROJECT_NAME} PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}")

if(ADMT_BUILD_TESTS)
    enable_testing()
    add_test(
        NAME ${PROJECT_NAME} 
        COMMAND "${PROJECT_NAME}"
        WORKING_DIRECTORY ${PROJECT_DIR}
    )
endif()