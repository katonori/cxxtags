PROJ_ROOT = ../../
include ../util/common.mk
CXXTAGS = ../../bin/cxxtags 
MERGER_OUT = db
.PHONY: clean html check
.SUFFIXES: .db .cpp

DB_FILES = main.db
test: check $(MERGER_OUT)
	./test.py db
$(MERGER_OUT): $(DB_FILES)
	$(CXXTAGS_DB_MANAGER) add $@ $^
html: $(MERGER_OUT)
	$(DUMPER) $<
clean:
	rm -rf main.cpp.db html $(MERGER_OUT)
include ../util/common_rule.mk
