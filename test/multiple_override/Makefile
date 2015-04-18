PROJ_ROOT = ../../
include ../util/common.mk

DB_DIR = db
.PHONY: clean check

$(DB_DIR):
	$(CXXTAGS) db Impl0.cpp
	$(CXXTAGS) db Impl1.cpp
	$(CXXTAGS) db Impl2.cpp
	$(CXXTAGS) db Impl3.cpp
test: check clean $(DB_DIR)
	./test.py $(DB_DIR)
clean:
	rm -rf html $(DB_DIR)
include ../util/common_rule.mk
