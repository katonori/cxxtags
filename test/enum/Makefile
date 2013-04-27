PROJ_ROOT = ../../
include ../util/common.mk

GATHER_OUT = db
.PHONY: clean
.SUFFIXES: .db .cpp

DB_FILES = main.db

$(GATHER_OUT): $(DB_FILES)
	$(GATHER) $@ $^
test: clean $(GATHER_OUT)
	./test.py $(GATHER_OUT)
html: $(GATHER_OUT)
	$(DUMPER) $(GATHER_OUT)
prog: main.cpp
	$(CXX) main.cpp -o prog
clean:
	rm -rf html $(GATHER_OUT) $(DB_FILES)

.cpp.db:
	$(CXXTAGS) $< -o $*.db
