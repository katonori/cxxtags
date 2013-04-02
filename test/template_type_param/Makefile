CXXTAGS = ../../src/cxxtags -e /usr/include
MERGER = ../../src/cxxtags_merger
DUMPER = ../../src/cxxtags_html_dumper

.PHONY: dump clean html

clean:
	rm -rf main.cpp.db html
test: html
	(grep "<a name=\"a_loc_16\" id=\"line_16\">" html/main.cpp.1.html) | (grep "<a href=\"ref/main.cpp@232@FT@>1.Tfunc_test.t0.0.@val.9.html\">val</a>") > html/out.txt
main.cpp.db:
	$(CXXTAGS) main.cpp -o $@
html: main.cpp.db 
	$(DUMPER) $<
