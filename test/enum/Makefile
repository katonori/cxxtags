PROJ_ROOT = ../../
include ../util/common.mk

DB_DIR = db
.PHONY: clean
.SUFFIXES: .db .cpp

$(DB_DIR):
	$(CXXTAGS) $(DB_DIR) main.cpp -- $(CXXTAGS_INCLUDES)
test: clean $(DB_DIR)
	./test.py $(DB_DIR)
prog: main.cpp
	$(CXX) main.cpp -o prog
clean:
	rm -rf $(DB_DIR)
include ../util/common_rule.mk
