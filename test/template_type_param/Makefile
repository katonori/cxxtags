PROJ_ROOT = ../../
include ../util/common.mk
GATHER_OUT = db
.PHONY: clean html
.SUFFIXES: .db .cpp

DB_FILES = main.db
test: html
	(grep "<a name=\"a_loc_16\" id=\"line_16\">" html/main.cpp.3.html) | (grep "<a href=\"ref/main.cpp@232@FT@>1.Tfunc_test.t0.0.@val.9.html\">val</a>") > html/out.txt
main.cpp.db:
	$(CXXTAGS) main.cpp -o $@
$(GATHER_OUT): $(DB_FILES)
	$(GATHER) $@ $^
html: $(GATHER_OUT)
	$(DUMPER) $<
clean:
	rm -rf main.cpp.db html
.cpp.db:
	$(CXXTAGS) $< -o $*.db
