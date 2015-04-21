PROJ_ROOT = ../../
include ../util/common.mk
CXXTAGS = ../../bin/cxxtags 
MERGER_OUT = db
.PHONY: clean
.SUFFIXES: .db .cpp

DB_FILES = main.db
test: $(MERGER_OUT)
	./test.py db
$(MERGER_OUT): $(DB_FILES)
	$(CXXTAGS_DB_MANAGER) add $@ $^
clean:
	rm -rf main.db $(MERGER_OUT)
include ../util/common_rule.mk
