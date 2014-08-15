PROJ_ROOT = ../../
include ../util/common.mk

MERGER_OUT = db
.PHONY: clean check

$(MERGER_OUT):
	$(CXXTAGS) db inhe.cpp
test: check $(MERGER_OUT)
	./test.py $(MERGER_OUT)
html: $(MERGER_OUT)
	$(DUMPER) $(MERGER_OUT)
prog: inhe.cpp
	g++ inhe.cpp -o prog
clean:
	rm -rf html $(MERGER_OUT)
include ../util/common_rule.mk
