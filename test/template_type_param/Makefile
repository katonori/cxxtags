PROJ_ROOT = ../../
include ../util/common.mk
CXXTAGS = ../../bin/cxxtags 
GATHER_OUT = db
.PHONY: clean html
.SUFFIXES: .db .cpp

DB_FILES = main.db
test: $(GATHER_OUT)
	./test.py db
main.cpp.db:
	$(CXXTAGS) main.cpp -o $@
$(GATHER_OUT): $(DB_FILES)
	$(GATHER) $@ $^
html: $(GATHER_OUT)
	$(DUMPER) $<
clean:
	rm -rf main.cpp.db html $(GATHER_OUT)
.cpp.db:
	$(CXXTAGS) $< -o $*.db
