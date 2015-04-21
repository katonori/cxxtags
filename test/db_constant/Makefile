include ../utils/common.mk
CXXTAGS = ../../src/cxxtags -e /usr/include
DUMPER = ../../src/cxxtags_html_dumper
.PHONY: dump clean

test: index merge
	cp index.db index.db.back
	diff -sq index.db index.db.back
index:
	$(CXXTAGS) ../enum/main.cpp
merge: 
	$(CXXTAGS_DB_MANAGER) index.db main.cpp.db
dump:
	sqlite3 index.db ".dump"
prog: main.cpp
	g++ -c main.cpp
	g++ main.o -o prog
clean:
	rm -rf index.db main.cpp.db
