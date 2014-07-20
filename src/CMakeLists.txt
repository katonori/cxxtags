project(cxxtags)

set(LLVM_HOME "" CACHE PATH "")
set(CMAKE_CXX_FLAGS "-g -O2")

include_directories(${LLVM_HOME}/include)
link_directories(${LLVM_HOME}/lib)

add_executable(cxxtags_core cxxtags_core.cpp db.cpp)
target_link_libraries(cxxtags_core sqlite3 clang stdc++)

install(FILES
    ${PROJECT_BINARY_DIR}/cxxtags_core
    ${PROJECT_SOURCE_DIR}/cxxtags
    ${PROJECT_SOURCE_DIR}/cxxtags_db_manager
    ${PROJECT_SOURCE_DIR}/cxxtags_query
    ${PROJECT_SOURCE_DIR}/cxxtags_util.py
    ${PROJECT_SOURCE_DIR}/g++.py
    ${PROJECT_SOURCE_DIR}/gcc.py
    DESTINATION ${PROJECT_SOURCE_DIR}/../bin
    PERMISSIONS OWNER_READ OWNER_EXECUTE OWNER_WRITE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE
   )
