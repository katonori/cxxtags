LLVM_HOME=/pkg/llvm-3.2/

CXX=g++
LD=g++
INCLUDES=-I${LLVM_HOME}/include/
LIBS=-L${LLVM_HOME}/lib/ -L/usr/lib/ -lsqlite3 -lclang -lstdc++ 
CXXFLAGS=-Wall -O2 -g
#CXXTAGS = ../bin/cxxtags -e /usr/include/c++:/usr/include/sys/
CXXTAGS = ../bin/cxxtags
CXXTAGS_DB_MANAGER = ../bin/cxxtags_db_manager
LDFLAGS = 
BINS = cxxtags_core cxxtags cxxtags_db_manager cxxtags_html_dumper cxxtags_util.py cxxtags_query g++.py gcc.py

all: cxxtags_core.cpp db.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) cxxtags_core.cpp -c
	$(CXX) $(CXXFLAGS) -I. db.cpp -c $(INCLUDES)
	$(LD) $(LDFLAGS) cxxtags_core.o db.o $(LIBS) -o cxxtags_core
	mkdir -p ../bin
	chmod +x $(BINS)
	cp $(BINS) ../bin
	strip ../bin/cxxtags_core
index: 
	$(CXXTAGS) $(INCLUDES) cxxtags_core.cpp -o cxxtags_core.cpp.db
	$(CXXTAGS) $(INCLUDES) db.cpp -o db.cpp.db
	$(CXXTAGS_DB_MANAGER) add db cxxtags_core.cpp.db db.cpp.db
clean:
	rm -rf db cxxtags_core.o db.o cxxtags_core
