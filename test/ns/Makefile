PROJ_ROOT = ../../
include ../util/common.mk

DB_DIR = db
.PHONY: clean db
.SUFFIXES: .db .cpp

CXXTAGS = $(PROJ_ROOT)/bin/cxxtags 

$(DB_DIR):
	$(CXXTAGS) db ns0.cpp -- -I./subdir 
	$(CXXTAGS) db subdir/ns1.cpp -- -I. -I./subdir
	$(CXXTAGS) db main.cpp -- -I./subdir 
test: check clean $(DB_DIR)
	./test.py $(DB_DIR)
	#$(CXXTAGS_DB_MANAGER) rebuild $(DB_DIR) ns0.h
	#./test.py $(DB_DIR)
ns1.db:
	$(CXXTAGS) $(DB_DIR) ./subdir/ns1.cpp -- $(CXXTAGS_INCLUDES) -I. 
html: $(DB_DIR)
	$(DUMPER) $(DB_DIR)
prog:
	$(CXX) -I./subdir -c ns0.cpp
	$(CXX) -I./subdir -c subdir/ns1.cpp
	$(CXX) -I./subdir -c main.cpp
	$(CXX) ns0.o ns1.o main.o -o prog
clean:
	rm -rf $(DB_DIR) html
include ../util/common_rule.mk
