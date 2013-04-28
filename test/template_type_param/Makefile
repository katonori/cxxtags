PROJ_ROOT = ../../
include ../util/common.mk
CXXTAGS = ../../bin/cxxtags 
MERGER_OUT = db
.PHONY: clean html
.SUFFIXES: .db .cpp

DB_FILES = main.db
test: $(MERGER_OUT)
	./test.py db
main.cpp.db:
	$(CXXTAGS) main.cpp -o $@
$(MERGER_OUT): $(DB_FILES)
	$(MERGER) $@ $^
html: $(MERGER_OUT)
	$(DUMPER) $<
clean:
	rm -rf main.cpp.db html $(MERGER_OUT)
.cpp.db:
	$(CXXTAGS) $< -o $*.db
