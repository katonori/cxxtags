PROJ_ROOT = ../../
include ../util/common.mk

MERGER_OUT = db
.PHONY: clean check test
.SUFFIXES: .db .cpp

DB_FILES = main.db

$(MERGER_OUT): $(DB_FILES)
	$(CXXTAGS_DB_MANAGER) add $@ $^
test: check clean $(MERGER_OUT)
	./test.py $(MERGER_OUT)
html: $(MERGER_OUT)
	$(DUMPER) $(MERGER_OUT)
prog: main.cpp
	$(CXX) main.cpp -o prog
clean:
	rm -rf html $(MERGER_OUT) $(DB_FILES)
include ../util/common_rule.mk
