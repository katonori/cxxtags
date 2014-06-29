CXX=g++
LLVM_HOME=/usr/lib/llvm-3.5/
INCLUDES=-I${LLVM_HOME}/include/
LIBS=-L${LLVM_HOME}/lib/ -L/usr/lib/ -lsqlite3 -lclang -lstdc++ 
#CXXFLAGS=-Wall -g -O2 -grecord-gcc-switches -frecord-gcc-switches 
CXXFLAGS=-Wall -O2 -g
CXXTAGS = ./cxxtags
CXXTAGS_DB_MANAGER = ./cxxtags_db_manager

all: cxxtags_core.cpp db.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) cxxtags_core.cpp -c
	$(CXX) $(CXXFLAGS) -I. db.cpp -c $(INCLUDES)
	$(CXX) cxxtags_core.o db.o $(LIBS) -o cxxtags_core
	mkdir -p ../bin
	cp cxxtags_core cxxtags cxxtags_db_manager cxxtags_html_dumper cxxtags_util.py cxxtags_query ../bin
	chmod +x cxxtags cxxtags_db_manager cxxtags_html_dumper cxxtags_util.py cxxtags_query ../bin
	strip ../bin/cxxtags_core
index: cxxtags_core.o db.o
	$(CXXTAGS) -g cxxtags_core.o
	$(CXXTAGS) -g db.o
	$(CXXTAGS_DB_MANAGER) add db cxxtags_core.o.db db.o.db
clean:
	rm -f cxxtags_core.o db.o cxxtags_core
