CXX=g++
LLVM_HOME=/vol/0/pkg/llvm-3.4
INCLUDES=-I${LLVM_HOME}/include/
CXXTAGS_INCLUDES=-I${LLVM_HOME}/include/ -I${LLVM_HOME}/lib/clang/3.4/include
LIBS=-L${LLVM_HOME}/lib/ -L/usr/lib/ -lsqlite3 -lclang -lstdc++ 
CXXFLAGS=-Wall -g -O2
CXXTAGS = env LD_LIBRARY_PATH=${LLVM_HOME}/lib:${LD_LIBRARY_PATH} ./cxxtags
CXXTAGS_DB_MANAGER = ./cxxtags_db_manager

all: cxxtags_core.cpp db.cpp
	$(CXX) $(CXXFLAGS) cxxtags_core.cpp -c $(INCLUDES)
	$(CXX) $(CXXFLAGS) db.cpp -c $(INCLUDES)
	$(CXX) cxxtags_core.o db.o $(LIBS) -o cxxtags_core
	mkdir -p ../bin
	cp cxxtags_core cxxtags cxxtags_db_manager cxxtags_html_dumper cxxtags_util.py cxxtags_query ../bin
	chmod +x cxxtags cxxtags_db_manager cxxtags_html_dumper cxxtags_util.py cxxtags_query ../bin
	strip ../bin/cxxtags_core
index:
	$(CXXTAGS) $(CXXTAGS_INCLUDES) cxxtags_core.cpp
	$(CXXTAGS) $(CXXTAGS_INCLUDES) db.cpp
	$(CXXTAGS_DB_MANAGER) add db cxxtags_core.cpp.db db.cpp.db
clean:
	rm -f cxxtags_core.o db.o cxxtags_core
