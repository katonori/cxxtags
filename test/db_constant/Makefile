CXXTAGS = ../../src/cxxtags -e /usr/include
MERGER = ../../src/cxxtags_merger
DUMPER = ../../src/cxxtags_html_dumper
.PHONY: dump clean

test: index merge
	cp index.db index.db.back
	make html
	diff -sq index.db index.db.back
index:
	env PYTHONPATH=/Users/norito/python_module/ $(CXXTAGS) ../enum/main.cpp
merge: 
	env PYTHONPATH=/Users/norito/python_module/ $(MERGER) index.db main.cpp.db
html: index merge
	$(DUMPER) index.db
dump:
	sqlite3 index.db ".dump"
prog: main.cpp
	g++ -c main.cpp
	g++ main.o -o prog
clean:
	rm -rf html index.db main.cpp.db
