LLVM_HOME=/pkg/llvm-3.2/

#CXX=g++
CXX=sh g++.sh
LD=g++
INCLUDES=-I${LLVM_HOME}/include/
LIBS=-L${LLVM_HOME}/lib/ -L/usr/lib/ -lsqlite3 -lclang -lstdc++ 
#CXXFLAGS=-Wall -g -O2 -grecord-gcc-switches -frecord-gcc-switches 
CXXFLAGS=-Wall -O2 -g
#CXXFLAGS=-Wall -O2 -g -fprofile-arcs -ftest-coverage 
CXXTAGS = ./cxxtags
CXXTAGS_DB_MANAGER = ./cxxtags_db_manager
#LDFLAGS = -lprofile_rt
LDFLAGS = 
BINS = cxxtags_core cxxtags cxxtags_db_manager cxxtags_html_dumper cxxtags_util.py cxxtags_query g++.sh gcc.sh

all: cxxtags_core.cpp db.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) cxxtags_core.cpp -c
	$(CXX) $(CXXFLAGS) -I. db.cpp -c $(INCLUDES)
	$(LD) $(LDFLAGS) cxxtags_core.o db.o $(LIBS) -o cxxtags_core
	mkdir -p ../bin
	chmod +x $(BINS)
	cp $(BINS) ../bin
	strip ../bin/cxxtags_core
index: 
	$(CXXTAGS) $(INCLUDES) cxxtags_core.cpp
	$(CXXTAGS) $(INCLUDES) db.cpp
	$(CXXTAGS_DB_MANAGER) add db cxxtags_core.cpp.db db.cpp.db
clean:
	rm -rf db cxxtags_core.o db.o cxxtags_core
