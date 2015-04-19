CXXTAGS = $(PROJ_ROOT)/bin/cxxtags -e /usr/include
CXXTAGS_INCLUDES = `llvm-config --cxxflags`
CXXTAGS_DB_MANAGER = $(PROJ_ROOT)/bin/cxxtags_db_manager
CXXTAGS_QUERY = $(PROJ_ROOT)/bin/cxxtags_query
DUMPER = $(PROJ_ROOT)/bin/cxxtags_html_dumper
CXX = g++
