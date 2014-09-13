PROJ_ROOT = ../../
include ../util/common.mk

DB_DIR = db
.PHONY: clean check

$(DB_DIR):
	$(CXXTAGS) db inhe.cpp
test: check clean $(DB_DIR)
	./test.py $(DB_DIR)
html: $(DB_DIR)
	$(DUMPER) $(DB_DIR)
prog: inhe.cpp
	g++ inhe.cpp -o prog
clean:
	rm -rf html $(DB_DIR)
include ../util/common_rule.mk
