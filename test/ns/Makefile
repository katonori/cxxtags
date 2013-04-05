CXXTAGS = ../../src/cxxtags -e /usr/include
MERGER = ../../src/cxxtags_merger
DUMPER = ../../src/cxxtags_html_dumper
.PHONY: clean dump
index:
	$(CXXTAGS) ns0.cpp -I./subdir
	$(CXXTAGS) ./subdir/ns1.cpp -I.
	$(CXXTAGS) main.cpp -I./subdir
merge: 
	$(MERGER) index.db main.cpp.db ns0.cpp.db ns1.cpp.db

check: index merge
	sqlite3 ns0.cpp.db ".dump" > ns0.cpp.db.out
	sqlite3 ns1.cpp.db ".dump" > ns1.cpp.db.out
	sqlite3 main.cpp.db ".dump" > main.cpp.db.out
	sqlite3 index.db ".dump" > index.db.out
	diff -q ns0.cpp.db.out ns0.cpp.db.ref
	diff -q ns1.cpp.db.out ns1.cpp.db.ref
	diff -q main.cpp.db.out main.cpp.db.ref
	diff -q index.db.out index.db.ref
test: index merge
	./test.py index.db
html: index merge
	$(DUMPER) index.db
dump:
	sqlite3 index.db ".dump"

prog:
	g++ -c ns0.cpp
	g++ -c ns1.cpp
	g++ -c main.cpp
	g++ ns0.o ns1.o main.o -o prog
clean:
	rm -rf index.db html main.cpp.db ns0.cpp.db ns1.cpp.db
