project(cxxtags)

set(LLVM_HOME "" CACHE PATH "")
set(LEVELDB_HOME "" CACHE PATH "")
set(CMAKE_CXX_FLAGS "-g -O2 -Wall" CACHE STRING "")
set(CMAKE_EXE_LINKER_FLAGS "" CACHE STRING "")

FIND_PACKAGE(Boost COMPONENTS filesystem system timer REQUIRED)

include_directories(
    ${LLVM_HOME}/include
    ${LEVELDB_HOME}/include
    ${Boost_INCLUDE_DIRS}
)
link_directories(${LLVM_HOME}/lib ${LEVELDB_HOME}/lib)

add_executable(cxxtags_core cxxtags_core.cpp DbImplLevelDb.cpp)
target_link_libraries(cxxtags_core clang stdc++ leveldb snappy
    ${Boost_FILESYSTEM_LIBRARY}
    ${Boost_SYSTEM_LIBRARY}
    ${Boost_TIMER_LIBRARY}
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
