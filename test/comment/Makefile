PROJ_ROOT = ../../
include ../util/common.mk

.PHONY: clean
.SUFFIXES: .db .cpp

GATHER_OUT = db
DB_FILES = main.db

$(GATHER_OUT): $(DB_FILES)
	$(GATHER) $@ $^
test: $(GATHER_OUT)
	./test.py $<
html: $(GATHER_OUT)
	$(DUMPER) $(GATHER_OUT)
prog: main.cpp
	$(CXX) main.cpp -o prog
clean:
	rm -rf html$(GATHER_OUT)  $(DB_FILES) prog
.cpp.db:
	$(CXXTAGS) $< -o $*.db
