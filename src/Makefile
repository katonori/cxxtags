CC=clang
LLVM_HOME=/pkg/llvm-3.2
INCLUDES=-I${LLVM_HOME}/include/ -I/usr/include/libxml2/
LIBS=-L${LLVM_HOME}/lib/ -L/usr/lib/ -lsqlite3 -lclang -lxml2 -lstdc++
CFLAGS=-Wall

all: cxxtags_core.cpp db.cpp
	$(CC) $(CFLAGS) cxxtags_core.cpp -c $(INCLUDES)
	$(CC) $(CFLAGS) db.cpp -c $(INCLUDES)
	$(CC) $(LIBS) cxxtags_core.o db.o -o cxxtags_core
	mkdir -p ../bin
	cp cxxtags_core cxxtags cxxtags_gather cxxtags_html_dumper cxxtags_util.py ../bin
