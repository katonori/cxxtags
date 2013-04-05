CXXTAGS = ../../src/cxxtags -e /usr/include
MERGER = ../../src/cxxtags_merger
DUMPER = ../../src/cxxtags_html_dumper
.PHONY: dump clean
index:
	$(CXXTAGS) main.cpp
merge: 
	$(MERGER) index.db main.cpp.db
test: index merge
	./test.py index.db
html: index merge
	$(DUMPER) index.db
dump:
	sqlite3 index.db ".dump"
prog: main.cpp
	g++ -c main.cpp
	g++ main.o -o prog
clean:
	rm -rf html index.db main.cpp.db
