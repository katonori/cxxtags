PROJ_ROOT = ../../
include ../util/common.mk

MERGER_OUT = db
.PHONY: clean db
.SUFFIXES: .db .cpp

DB_FILES = ns0.db ns1.db main.db

$(MERGER_OUT):
	$(CXXTAGS) -I./subdir db ns0.cpp
	$(CXXTAGS) -I. -I./subdir db subdir/ns1.cpp
	$(CXXTAGS) -I./subdir db main.cpp
test: check clean $(MERGER_OUT)
	./test.py $(MERGER_OUT)
	#$(CXXTAGS_DB_MANAGER) rebuild $(MERGER_OUT) ns0.h
	#./test.py $(MERGER_OUT)
ns1.db:
	$(CXXTAGS) $(CXXTAGS_INCLUDES) $(MERGER_OUT) ./subdir/ns1.cpp -I. 
html: $(MERGER_OUT)
	$(DUMPER) $(MERGER_OUT)
prog:
	$(CXX) -I./subdir -c ns0.cpp
	$(CXX) -I./subdir -c subdir/ns1.cpp
	$(CXX) -I./subdir -c main.cpp
	$(CXX) ns0.o ns1.o main.o -o prog
clean:
	rm -rf $(MERGER_OUT) html $(DB_FILES)
include ../util/common_rule.mk
