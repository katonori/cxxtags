PROJ_ROOT = ../../
include ../util/common.mk

MERGER_OUT = db
.PHONY: clean
.SUFFIXES: .db .cpp
DB_FILES = main.db
vpath %.cpp ./:../enum

$(MERGER_OUT): $(DB_FILES)
	$(CXXTAGS_DB_MANAGER) add $@ $^
test: clean $(MERGER_OUT)
	./test.py $(MERGER_OUT)
prog: main.cpp
	$(CXX) main.cpp -o prog
clean:
	rm -rf $(MERGER_OUT) $(DB_FILES)
include ../util/common_rule.mk
