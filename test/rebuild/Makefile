PROJ_ROOT = ../../
include ../util/common.mk

MERGER_OUT = db
.PHONY: clean
.SUFFIXES: .db .cpp

$(MERGER_OUT): $(DB_FILES)
	cp main.0.cpp main.cpp
	$(CXXTAGS) db main.cpp
test: clean $(MERGER_OUT)
	./test.0.py $(MERGER_OUT)
	cp main.1.cpp main.cpp
	$(CXXTAGS_QUERY) rebuild $(MERGER_OUT) main.cpp
	./test.1.py $(MERGER_OUT)
prog: inhe.cpp
	g++ inhe.cpp -o prog
clean:
	rm -rf $(MERGER_OUT) $(DB_FILES)
include ../util/common_rule.mk
