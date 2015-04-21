PROJ_ROOT = ../../
include ../util/common.mk

DB_DIR = db
.PHONY: clean

$(DB_DIR):
	$(CXXTAGS) db inhe.cpp
test: clean $(DB_DIR)
	./test.py $(DB_DIR)
prog: inhe.cpp
	g++ inhe.cpp -o prog
clean:
	rm -rf $(DB_DIR)
include ../util/common_rule.mk
