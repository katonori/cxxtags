PROJ_ROOT = ../../
include ../util/common.mk

DB_DIR = db
.PHONY: clean

$(DB_DIR):
	$(CXXTAGS) db main.cpp
test: clean $(DB_DIR)
	./test.py $(DB_DIR)
clean:
	rm -rf $(DB_DIR)
include ../util/common_rule.mk
