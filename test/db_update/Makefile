PROJ_ROOT = ../../
include ../util/common.mk

MERGER_OUT = db
.PHONY: clean
.SUFFIXES: .c .db

DB_FILES = test.db

test: clean
        # former
	cp a.c test.c
	$(CXXTAGS) test.c -o test.db
	$(CXXTAGS_DB_MANAGER) add $(MERGER_OUT) test.db
	sqlite3 $(MERGER_OUT)/file_index.db ".dump" > file_index0.txt
	test "1" = `sqlite3 $(MERGER_OUT)/test.db "SELECT * FROM decl,name_list ON decl.name_id=name_list.id WHERE name_list.name='func_a';"|wc -l`
        # latter
        # change the contents of source file "test.c" and update database.
	cp b.c test.c
	$(CXXTAGS) test.c -o test.db
	$(CXXTAGS_DB_MANAGER) add $(MERGER_OUT) test.db
	sqlite3 $(MERGER_OUT)/file_index.db ".dump" > file_index1.txt
	test "1" = `sqlite3 $(MERGER_OUT)/test.db "SELECT * FROM decl,name_list ON decl.name_id=name_list.id WHERE name_list.name='func_b';"|wc -l`
        # check if db/file_index.db is not changed.
	diff file_index0.txt file_index1.txt

prog: main.cpp
	$(CXX) main.cpp -o prog
clean:
	rm -rf $(MERGER_OUT) $(DB_FILES) test.c file_index0.txt file_index1.txt
include ../util/common_rule.mk
