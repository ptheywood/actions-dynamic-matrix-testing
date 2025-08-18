cmake_minimum_required(VERSION 3.18 FATAL_ERROR)

project(admt LANGUAGES NONE)

include(CheckLanguage)
check_language(CXX)
enable_language(CXX)


set(SRC_INCLUDE
    ${CMAKE_CURRENT_SOURCE_DIR}/../include/admt/admt.h
)
set(SRC_SRC
    ${CMAKE_CURRENT_SOURCE_DIR}/../src/admt/admt.cpp
)
set(ALL_SRC
    ${SRC_INCLUDE}
    ${SRC_SRC}
)

add_library(${PROJECT_NAME} STATIC "${ALL_SRC}")


target_compile_features(${PROJECT_NAME} PUBLIC cxx_std_17)
target_compile_features(${PROJECT_NAME} PUBLIC cuda_std_17)
set_property(TARGET ${PROJECT_NAME} PROPERTY CXX_EXTENSIONS OFF)
set_property(TARGET ${PROJECT_NAME} PROPERTY CUDA_EXTENSIONS OFF)
set_property(TARGET ${PROJECT_NAME} PROPERTY CXX_STANDARD_REQUIRED ON)
set_property(TARGET ${PROJECT_NAME} PROPERTY CUDA_STANDARD_REQUIRED ON)

target_include_directories(${PROJECT_NAME} PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/../include")
target_include_directories(${PROJECT_NAME} PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/../src")