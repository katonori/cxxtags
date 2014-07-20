PROJ_ROOT = ../../
include ../util/common.mk

MERGER_OUT = db
.PHONY: clean check
.SUFFIXES: .db .cpp

DB_FILES = inhe.db

$(DB_FILES):
	env CXXTAGS_DB_DST=`pwd`/$(MERGER_OUT) g++.py inhe.cpp -o $@
$(MERGER_OUT): $(DB_FILES)
	$(CXXTAGS_DB_MANAGER) rebuild $(MERGER_OUT)
test: check $(MERGER_OUT)
	./test.py $(MERGER_OUT)
	$(CXXTAGS_DB_MANAGER) rebuild $(MERGER_OUT)
	./test.py $(MERGER_OUT)
html: $(MERGER_OUT)
	$(DUMPER) $(MERGER_OUT)
prog: inhe.cpp
	g++ inhe.cpp -o prog
clean:
	rm -rf html $(MERGER_OUT) $(DB_FILES)
include ../util/common_rule.mk
