PROJ_ROOT = ../../
include ../util/common.mk

MERGER_OUT = db
.PHONY: clean check
.SUFFIXES: .db .cpp

DB_FILES = inhe.db

$(MERGER_OUT): $(DB_FILES)
	$(CXXTAGS_DB_MANAGER) add $@ $^
test: check $(MERGER_OUT)
	./test.py $(MERGER_OUT)
html: $(MERGER_OUT)
	$(DUMPER) $(MERGER_OUT)
prog: inhe.cpp
	g++ inhe.cpp -o prog
clean:
	rm -rf html $(MERGER_OUT) $(DB_FILES)
.cpp.db:
	$(CXXTAGS) $(CXXTAGS_INCLUDES) $< -o $*.db
include ../util/common_rule.mk
