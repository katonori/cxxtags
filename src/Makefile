CXX=g++
LLVM_HOME=/pkg/llvm-3.2
INCLUDES=-I${LLVM_HOME}/include/
LIBS=-L${LLVM_HOME}/lib/ -L/usr/lib/ -lsqlite3 -lclang -lstdc++ -lpthread
CXXFLAGS=-Wall -g -O2

all: cxxtags_core.cpp db.cpp
	$(CXX) $(CXXFLAGS) cxxtags_core.cpp -c $(INCLUDES)
	$(CXX) $(CXXFLAGS) db.cpp -c $(INCLUDES)
	$(CXX) cxxtags_core.o db.o $(LIBS) -o cxxtags_core
	mkdir -p ../bin
	cp cxxtags_core cxxtags cxxtags_gather cxxtags_html_dumper cxxtags_util.py ../bin
	strip ../bin/cxxtags_core
clean:
	rm -f cxxtags_core.o db.o cxxtags_core
