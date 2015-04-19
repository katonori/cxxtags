cmake_minimum_required(VERSION 2.8)

project(cxxtags)

if(NOT LLVM_CONFIG)
    set(LLVM_CONFIG "llvm-config")
endif()
if(NOT LEVELDB_HOME)
    set(LEVELDB_HOME "/usr")
endif()

execute_process(
        COMMAND ${LLVM_CONFIG} --cxxflags
        COMMAND tr -d '\n'
        OUTPUT_VARIABLE LLVM_CXXFLAGS
        ERROR_VARIABLE ERROR_MSG
        )
if(LLVM_CXXFLAGS STREQUAL "")
    message(FATAL_ERROR "ERROR: command execution faild: \"${LLVM_CONFIG}\". Set variable LLVM_CONFIG correctly.")
endif()
execute_process(
        COMMAND ${LLVM_CONFIG} --ldflags
        COMMAND tr -d '\n'
        OUTPUT_VARIABLE LLVM_LDFLAGS
        )
set(CMAKE_CXX_FLAGS "-g -O3 -Wall -std=gnu++11 ${LLVM_CXXFLAGS} -fexceptions")
add_definitions(-UNDEBUG)
#add_definitions(-DTIMER)
set(CMAKE_EXE_LINKER_FLAGS "${LLVM_LDFLAGS}")

FIND_PACKAGE(Boost COMPONENTS filesystem system timer REQUIRED)

include_directories(
    ${LEVELDB_HOME}/include
    ${Boost_INCLUDE_DIRS}
)
link_directories(${LEVELDB_HOME}/lib)

add_executable(cxxtags_core cxxtags_core.cpp DbImplLevelDb.cpp)
target_link_libraries(cxxtags_core clang stdc++ leveldb snappy
    ${Boost_FILESYSTEM_LIBRARY}
    ${Boost_SYSTEM_LIBRARY}
    ${Boost_TIMER_LIBRARY}
)
add_dependencies(cxxtags_core configFile)
add_custom_target(
    configFile
    COMMAND ${PROJECT_SOURCE_DIR}/cxxtags_query genconfig ${PROJECT_SOURCE_DIR}/config.h
)
if(CYGWIN)
    set(EXTENSION ".exe")
endif(CYGWIN)

install(FILES
    ${PROJECT_BINARY_DIR}/cxxtags_core${EXTENSION}
    ${PROJECT_SOURCE_DIR}/cxxtags
    ${PROJECT_SOURCE_DIR}/cxxtags_query
    ${PROJECT_SOURCE_DIR}/cxxtags_util.py
    ${PROJECT_SOURCE_DIR}/cxxtags_run_proj
    DESTINATION ${PROJECT_SOURCE_DIR}/../bin
    PERMISSIONS OWNER_READ OWNER_EXECUTE OWNER_WRITE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE
)
