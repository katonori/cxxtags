CXXTAGS = ../../src/cxxtags -e /usr/include
MERGER = ../../src/cxxtags_merger
DUMPER = ../../src/cxxtags_html_dumper
.PHONY: dump clean

index: inhe.cpp
	env PYTHONPATH=/Users/norito/python_module/ $(CXXTAGS) inhe.cpp
merge: inhe.cpp.db
	env PYTHONPATH=/Users/norito/python_module/ $(MERGER) index.db inhe.cpp.db

test: index merge
	python test.py index.db
html:  index merge
	$(DUMPER) index.db
dump:
	sqlite3 index.db ".dump"

prog: inhe.cpp
	g++ inhe.cpp -o prog
clean:
	rm -rf html index.db inhe.cpp.db
