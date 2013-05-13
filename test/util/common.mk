CXXTAGS = $(PROJ_ROOT)/src/cxxtags -e /usr/include
CXXTAGS_INCLUDES = -I${LLVM_HOME}/lib/clang/3.2/include
MERGER = $(PROJ_ROOT)/src/cxxtags_merger
DUMPER = $(PROJ_ROOT)/src/cxxtags_html_dumper
CXX = g++
