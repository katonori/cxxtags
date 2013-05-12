PROJ_ROOT = ../../
include ../util/common.mk

MERGER_OUT = db
.PHONY: clean
.SUFFIXES: .db .cpp

DB_FILES = inhe.db

$(MERGER_OUT): $(DB_FILES)
	$(MERGER) add $@ $^
test: $(MERGER_OUT)
	./test.py $(MERGER_OUT)
html: $(MERGER_OUT)
	$(DUMPER) $(MERGER_OUT)
prog: inhe.cpp
	g++ inhe.cpp -o prog
clean:
	rm -rf html $(MERGER_OUT) $(DB_FILES)
.cpp.db:
	$(CXXTAGS) $< -o $*.db
