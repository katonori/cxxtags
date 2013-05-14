PROJ_ROOT = ../../
include ../util/common.mk

MERGER_OUT = db
.PHONY: clean check test
.SUFFIXES: .db .cpp

DB_FILES = main.db

$(MERGER_OUT): $(DB_FILES)
	$(MERGER) add $@ $^
test: check clean $(MERGER_OUT)
	./test.py $(MERGER_OUT)
html: $(MERGER_OUT)
	$(DUMPER) $(MERGER_OUT)
prog: main.cpp
	$(CXX) main.cpp -o prog
clean:
	rm -rf html $(MERGER_OUT) $(DB_FILES)

.cpp.db:
	$(CXXTAGS) $(CXXTAGS_INCLUDES) $< -o $*.db
include ../util/common_rule.mk
