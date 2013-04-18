PROJ_ROOT = ../../
include ../util/common.mk

GATHER_OUT = db
.PHONY: clean
.SUFFIXES: .db .cpp

DB_FILES = ns0.db ns1.db main.db

$(GATHER_OUT): $(DB_FILES)
	$(GATHER) $@ $^

test: $(GATHER_OUT)
	./test.py $<

ns1.db:
	$(CXXTAGS) ./subdir/ns1.cpp -I. -o ns1.db
index:
	$(CXXTAGS) ns0.cpp -I./subdir
	$(CXXTAGS) main.cpp -I./subdir
html: $(GATHER_OUT)
	$(DUMPER) $(GATHER_OUT)
prog:
	$(CXX) -I./subdir -c ns0.cpp
	$(CXX) -I./subdir -c subdir/ns1.cpp
	$(CXX) -I./subdir -c main.cpp
	$(CXX) ns0.o ns1.o main.o -o prog
clean:
	rm -rf $(GATHER_OUT) html $(DB_FILES)
.cpp.db:
	$(CXXTAGS) -I./subdir $< -o $*.db
