cmake_minimum_required(VERSION 3.18 FATAL_ERROR)

project(tests LANGUAGES CXX)

enable_testing()

SET(SRC
    ${CMAKE_CURRENT_SOURCE_DIR}/main.cpp
)
add_executable(${PROJECT_NAME} ${SRC})

target_link_libraries(${PROJECT_NAME} admt)
target_include_directories(${PROJECT_NAME} PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}")

add_test(
    NAME ${PROJECT_NAME} 
    COMMAND "${PROJECT_NAME}"
    WORKING_DIRECTORY ${PROJECT_DIR}
)