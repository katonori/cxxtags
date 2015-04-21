PROJ_ROOT = ../../
include ../util/common.mk

.PHONY: clean
.SUFFIXES: .db .cpp

MERGER_OUT = db
DB_FILES = main.db

$(MERGER_OUT): $(DB_FILES)
	$(CXXTAGS_DB_MANAGER) $@ $^
test: $(MERGER_OUT)
	./test.py $<
prog: main.cpp
	$(CXX) main.cpp -o prog
clean:
	rm -rf $(DB_FILES) prog
.cpp.db:
	$(CXXTAGS) $< -o $*.db
