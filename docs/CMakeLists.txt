cmake_minimum_required(VERSION 3.18 FATAL_ERROR)

project(docs LANGUAGES NONE)

find_program(PANDOC_EXECUTABLE NAMES pandoc pandoc.exe)
if(NOT PANDOC_EXECUTABLE)
    message(FATAL_ERROR "Pandoc not found")
endif()

SET(SRC
    ${CMAKE_CURRENT_SOURCE_DIR}/index.md
)
set(SITE_DIR "${CMAKE_CURRENT_BINARY_DIR}/_site")

add_custom_command(
    OUTPUT "${SITE_DIR}"
    COMMAND ${CMAKE_COMMAND} -E make_directory "${SITE_DIR}"
    COMMENT "Creating output directory: ${SITE_DIR}"
)
if (SRC)
    foreach(md_file ${SRC})
        get_filename_component(filename_we_ext "${md_file}" NAME_WE)
        set(output_html_name "${filename_we_ext}.html")
        set(output_path "${SITE_DIR}/${output_html_name}")

        add_custom_command(
            OUTPUT "${output_path}"
            COMMAND ${PANDOC_EXECUTABLE} -s ${md_file} -o "${output_path}"
            DEPENDS ${md_file} ${SITE_DIR}
            COMMENT "Rendering ${md_file} to ${output_path}"
        )
        list(APPEND HTML_FILES "${output_path}")
    endforeach()
    add_custom_target(${PROJECT_NAME} ALL
        DEPENDS ${HTML_FILES}
    )
endif()