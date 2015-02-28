PROJ_ROOT = ../../
include ../util/common.mk

DB_DIR = db
.PHONY: clean check
.SUFFIXES: .db .cpp

$(DB_DIR):
	$(CXXTAGS) $(DB_DIR) main.cpp -- $(CXXTAGS_INCLUDES)
test: check clean $(DB_DIR)
	./test.py $(DB_DIR)
html: $(DB_DIR)
	$(DUMPER) $(DB_DIR)
prog: main.cpp
	$(CXX) main.cpp -o prog
clean:
	rm -rf html $(DB_DIR)
include ../util/common_rule.mk
