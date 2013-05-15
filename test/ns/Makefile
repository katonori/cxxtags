PROJ_ROOT = ../../
include ../util/common.mk

MERGER_OUT = db
.PHONY: clean
.SUFFIXES: .db .cpp

DB_FILES = ns0.db ns1.db main.db

$(MERGER_OUT): $(DB_FILES)
	$(CXXTAGS_DB_MANAGER) add $@ $^
test: check $(MERGER_OUT)
	./test.py $(MERGER_OUT)
ns1.db:
	$(CXXTAGS) $(CXXTAGS_INCLUDES) ./subdir/ns1.cpp -I. -o ns1.db
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
# override rule
.cpp.db:
	$(CXXTAGS) $(CXXTAGS_INCLUDES) -I./subdir $< -o $*.db
