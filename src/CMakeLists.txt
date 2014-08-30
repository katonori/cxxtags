project(cxxtags)

set(LLVM_HOME "" CACHE PATH "")
set(LEVELDB_HOME "" CACHE PATH "")
set(BOOST_HOME "" CACHE PATH "")
set(CMAKE_CXX_FLAGS "-g -O2 -Wall" CACHE STRING "")
set(CMAKE_EXE_LINKER_FLAGS "" CACHE STRING "")

include_directories(${LLVM_HOME}/include ${LEVELDB_HOME}/include ${BOOST_HOME}/include)
link_directories(${LLVM_HOME}/lib ${LEVELDB_HOME}/lib ${BOOST_HOME}/lib)

add_executable(cxxtags_core cxxtags_core.cpp DbImplLevelDb.cpp)
target_link_libraries(cxxtags_core clang stdc++ leveldb snappy boost_filesystem-mt boost_system-mt boost_timer-mt)

install(FILES
    ${PROJECT_BINARY_DIR}/cxxtags_core
    ${PROJECT_SOURCE_DIR}/cxxtags
    ${PROJECT_SOURCE_DIR}/cxxtags_db_manager
    ${PROJECT_SOURCE_DIR}/cxxtags_query
    ${PROJECT_SOURCE_DIR}/cxxtags_util.py
    ${PROJECT_SOURCE_DIR}/cxxtags_run_proj
    ${PROJECT_SOURCE_DIR}/g++.py
    ${PROJECT_SOURCE_DIR}/gcc.py
    DESTINATION ${PROJECT_SOURCE_DIR}/../bin
    PERMISSIONS OWNER_READ OWNER_EXECUTE OWNER_WRITE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE
   )
