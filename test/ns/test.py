#!/usr/bin/python

import sys
import os
import sqlite3
sys.path.append("../../src/")
import cxxtags_util as cxxtags
sys.path.append("../util/")
import clang.cindex # for kind types

err = 0

def test_one(db, q, a):
    global err
    res = list(db.execute(q).fetchall())
    if len(res) != 1:
        print "ERROR: result num: %d"%(len(res))
        print "    q = ", q
        for i in res:
            print "    ", i
        err += 1
    else:
        if res[0] != a:
            print "DIFFER:"
            print "    ", res[0]
            print "    ", a
            err += 1
        #else:
        #    print "OK"

if len(sys.argv) != 2:
    print "usage: cmd db_file"
    exit(1)

cur_dir = os.getcwd()

decl_col = "decl.usr, decl.name, file_list.name, decl.line, decl.col, decl.kind, decl.val, decl.is_virtual, decl.is_def"
ref_col = " ref.usr, ref.name, file_list.name, ref.line, ref.col, ref.kind, ref_file_list.name, ref.ref_line, ref.ref_col"

q_list = [
# main.cpp
[
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=5 AND col=9 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=6 AND col=6 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=6 AND col=10 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=7 AND col=5 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=9 AND col=23 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=10 AND col=5 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=11 AND col=5 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=12 AND col=5 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=13 AND col=5 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=13 AND col=10 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=13 AND col=13 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=14 AND col=5 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=14 AND col=10 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=14 AND col=13 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=15 AND col=5 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=15 AND col=10 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=15 AND col=13 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=16 AND col=5 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=16 AND col=10 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=16 AND col=13 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=17 AND col=5 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=17 AND col=9 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=18 AND col=5 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=18 AND col=9 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=19 AND col=5 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=19 AND col=9 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=20 AND col=5 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=20 AND col=9 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=21 AND col=25 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=22 AND col=37 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=22 AND col=41 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=23 AND col=5 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=25 AND col=25 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
# ns0.h
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=2 AND col=11 AND file_list.name=\"%s/subdir/ns0.h\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=3 AND col=17 AND file_list.name=\"%s/subdir/ns0.h\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=4 AND col=11 AND file_list.name=\"%s/subdir/ns0.h\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=6 AND col=9 AND file_list.name=\"%s/subdir/ns0.h\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=6 AND col=16 AND file_list.name=\"%s/subdir/ns0.h\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=6 AND col=21 AND file_list.name=\"%s/subdir/ns0.h\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=6 AND col=27 AND file_list.name=\"%s/subdir/ns0.h\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=7 AND col=13 AND file_list.name=\"%s/subdir/ns0.h\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=9 AND col=13 AND file_list.name=\"%s/subdir/ns0.h\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=11 AND col=11 AND file_list.name=\"%s/subdir/ns0.h\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=13 AND col=9 AND file_list.name=\"%s/subdir/ns0.h\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=13 AND col=16 AND file_list.name=\"%s/subdir/ns0.h\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=13 AND col=21 AND file_list.name=\"%s/subdir/ns0.h\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=13 AND col=27 AND file_list.name=\"%s/subdir/ns0.h\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=14 AND col=9 AND file_list.name=\"%s/subdir/ns0.h\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=14 AND col=15 AND file_list.name=\"%s/subdir/ns0.h\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=15 AND col=9 AND file_list.name=\"%s/subdir/ns0.h\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=15 AND col=12 AND file_list.name=\"%s/subdir/ns0.h\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=17 AND col=13 AND file_list.name=\"%s/subdir/ns0.h\""%(cur_dir),
# ns1.h
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=2 AND col=11 AND file_list.name=\"%s/ns1.h\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=3 AND col=11 AND file_list.name=\"%s/ns1.h\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=5 AND col=9 AND file_list.name=\"%s/ns1.h\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=5 AND col=16 AND file_list.name=\"%s/ns1.h\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=5 AND col=21 AND file_list.name=\"%s/ns1.h\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=5 AND col=27 AND file_list.name=\"%s/ns1.h\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=6 AND col=14 AND file_list.name=\"%s/ns1.h\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=8 AND col=13 AND file_list.name=\"%s/ns1.h\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=10 AND col=11 AND file_list.name=\"%s/ns1.h\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=12 AND col=9 AND file_list.name=\"%s/ns1.h\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=12 AND col=16 AND file_list.name=\"%s/ns1.h\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=12 AND col=21 AND file_list.name=\"%s/ns1.h\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=12 AND col=27 AND file_list.name=\"%s/ns1.h\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=13 AND col=14 AND file_list.name=\"%s/ns1.h\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=15 AND col=13 AND file_list.name=\"%s/ns1.h\""%(cur_dir),
],
# ns0.cpp
[
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=2 AND col=11 AND file_list.name=\"%s/ns0.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=3 AND col=9 AND file_list.name=\"%s/ns0.cpp\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=3 AND col=13 AND file_list.name=\"%s/ns0.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=5 AND col=35 AND file_list.name=\"%s/ns0.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=6 AND col=16 AND file_list.name=\"%s/ns0.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=8 AND col=5 AND file_list.name=\"%s/ns0.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=8 AND col=11 AND file_list.name=\"%s/ns0.cpp\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=8 AND col=15 AND file_list.name=\"%s/ns0.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=10 AND col=35 AND file_list.name=\"%s/ns0.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=11 AND col=16 AND file_list.name=\"%s/ns0.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=13 AND col=5 AND file_list.name=\"%s/ns0.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=13 AND col=8 AND file_list.name=\"%s/ns0.cpp\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=13 AND col=12 AND file_list.name=\"%s/ns0.cpp\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=17 AND col=10 AND file_list.name=\"%s/ns0.cpp\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=20 AND col=19 AND file_list.name=\"%s/ns0.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=21 AND col=30 AND file_list.name=\"%s/ns0.cpp\""%(cur_dir),
],
# ns1.cpp
[
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=2 AND col=11 AND file_list.name=\"%s/subdir/ns1.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=3 AND col=10 AND file_list.name=\"%s/subdir/ns1.cpp\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=3 AND col=14 AND file_list.name=\"%s/subdir/ns1.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=5 AND col=35 AND file_list.name=\"%s/subdir/ns1.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=7 AND col=10 AND file_list.name=\"%s/subdir/ns1.cpp\""%(cur_dir),
"SELECT "+decl_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_DECL+" WHERE line=7 AND col=14 AND file_list.name=\"%s/subdir/ns1.cpp\""%(cur_dir),
"SELECT "+ref_col+" FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=9 AND col=35 AND file_list.name=\"%s/subdir/ns1.cpp\""%(cur_dir),
]
]

q_list_sys = [
"SELECT * FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=9 AND col=5 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT * FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=9 AND col=10 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT * FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=10 AND col=9 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT * FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=11 AND col=9 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT * FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=12 AND col=9 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT * FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=21 AND col=5 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT * FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=22 AND col=9 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT * FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=22 AND col=14 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT * FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=22 AND col=28 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT * FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=22 AND col=45 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
"SELECT * FROM "+cxxtags.QUERY_JOINED_TABLE_REF+" WHERE line=25 AND col=9 AND file_list.name=\"%s/main.cpp\""%(cur_dir),
]

a_list = [
# main.cpp
[
('c:macro@BUFF_SIZE','BUFF_SIZE','%s/main.cpp'%(cur_dir),5,9,clang.cindex.CursorKind.MACRO_DEFINITION.value,0,0,0),
('c:@msg','msg','%s/main.cpp'%(cur_dir),6,6,clang.cindex.CursorKind.VAR_DECL.value,0,0,1),
('c:macro@BUFF_SIZE','BUFF_SIZE','%s/main.cpp'%(cur_dir),6,10,clang.cindex.CursorKind.MACRO_INSTANTIATION.value,'%s/main.cpp'%(cur_dir),5,9),
('c:@F@main', 'main', '%s/main.cpp'%(cur_dir), 7, 5, clang.cindex.CursorKind.FUNCTION_DECL.value, 0,0,1),
('c:main.cpp@127@F@main@vec','vec','%s/main.cpp'%(cur_dir),9,23,clang.cindex.CursorKind.VAR_DECL.value,0,0,1),
('c:main.cpp@127@F@main@vec','vec','%s/main.cpp'%(cur_dir),10,5,clang.cindex.CursorKind.DECL_REF_EXPR.value,'%s/main.cpp'%(cur_dir),9,23),
('c:main.cpp@127@F@main@vec','vec','%s/main.cpp'%(cur_dir),11,5,clang.cindex.CursorKind.DECL_REF_EXPR.value,'%s/main.cpp'%(cur_dir),9,23),
('c:main.cpp@127@F@main@vec','vec','%s/main.cpp'%(cur_dir),12,5,clang.cindex.CursorKind.DECL_REF_EXPR.value,'%s/main.cpp'%(cur_dir),9,23),
('c:@N@NS0','NS0','%s/main.cpp'%(cur_dir),13,5,clang.cindex.CursorKind.NAMESPACE_REF.value,'%s/subdir/ns0.h'%(cur_dir),2,11),
('c:@N@NS0@C@C0','C0','%s/main.cpp'%(cur_dir),13,10,clang.cindex.CursorKind.TYPE_REF.value,'%s/subdir/ns0.h'%(cur_dir),4,11),
('c:main.cpp@220@F@main@c00','c00','%s/main.cpp'%(cur_dir),13,13,clang.cindex.CursorKind.VAR_DECL.value,0,0,1),
('c:@N@NS1','NS1','%s/main.cpp'%(cur_dir),14,5,clang.cindex.CursorKind.NAMESPACE_REF.value,'%s/ns1.h'%(cur_dir),2,11),
('c:@N@NS1@C@C0','C0','%s/main.cpp'%(cur_dir),14,10,clang.cindex.CursorKind.TYPE_REF.value,'%s/ns1.h'%(cur_dir),3,11),
('c:main.cpp@240@F@main@c10','c10','%s/main.cpp'%(cur_dir),14,13,clang.cindex.CursorKind.VAR_DECL.value,0,0,1),
('c:@N@NS0','NS0','%s/main.cpp'%(cur_dir),15,5,clang.cindex.CursorKind.NAMESPACE_REF.value,'%s/subdir/ns0.h'%(cur_dir),2,11),
('c:@N@NS0@C@C1','C1','%s/main.cpp'%(cur_dir),15,10,clang.cindex.CursorKind.TYPE_REF.value,'%s/subdir/ns0.h'%(cur_dir),11,11),
('c:main.cpp@260@F@main@c01','c01','%s/main.cpp'%(cur_dir),15,13,clang.cindex.CursorKind.VAR_DECL.value,0,0,1),
('c:@N@NS1','NS1','%s/main.cpp'%(cur_dir),16,5,clang.cindex.CursorKind.NAMESPACE_REF.value,'%s/ns1.h'%(cur_dir),2,11),
('c:@N@NS1@C@C1','C1','%s/main.cpp'%(cur_dir),16,10,clang.cindex.CursorKind.TYPE_REF.value,'%s/ns1.h'%(cur_dir),10,11),
('c:main.cpp@280@F@main@c11','c11','%s/main.cpp'%(cur_dir),16,13,clang.cindex.CursorKind.VAR_DECL.value,0,0,1),
('c:main.cpp@220@F@main@c00','c00','%s/main.cpp'%(cur_dir),17,5,clang.cindex.CursorKind.DECL_REF_EXPR.value,'%s/main.cpp'%(cur_dir),13,13),
('c:@N@NS0@C@C0@F@check#','check','%s/main.cpp'%(cur_dir),17,9,clang.cindex.CursorKind.MEMBER_REF_EXPR.value,'%s/subdir/ns0.h'%(cur_dir),7,13),
('c:main.cpp@240@F@main@c10','c10','%s/main.cpp'%(cur_dir),18,5,clang.cindex.CursorKind.DECL_REF_EXPR.value,'%s/main.cpp'%(cur_dir),14,13),
('c:@N@NS1@C@C0@F@check#','check','%s/main.cpp'%(cur_dir),18,9,clang.cindex.CursorKind.MEMBER_REF_EXPR.value,'%s/ns1.h'%(cur_dir),6,14),
('c:main.cpp@260@F@main@c01','c01','%s/main.cpp'%(cur_dir),19,5,clang.cindex.CursorKind.DECL_REF_EXPR.value,'%s/main.cpp'%(cur_dir),15,13),
('c:@N@NS0@C@C1@F@check#1','check','%s/main.cpp'%(cur_dir),19,9,clang.cindex.CursorKind.MEMBER_REF_EXPR.value,'%s/subdir/ns0.h'%(cur_dir),14,15),
('c:main.cpp@280@F@main@c11','c11','%s/main.cpp'%(cur_dir),20,5,clang.cindex.CursorKind.DECL_REF_EXPR.value,'%s/main.cpp'%(cur_dir),16,13),
('c:@N@NS1@C@C1@F@check#','check','%s/main.cpp'%(cur_dir),20,9,clang.cindex.CursorKind.MEMBER_REF_EXPR.value,'%s/ns1.h'%(cur_dir),13,14),
('c:@msg','msg','%s/main.cpp'%(cur_dir),21,25,clang.cindex.CursorKind.DECL_REF_EXPR.value,'%s/main.cpp'%(cur_dir),6,6),
('c:main.cpp@402@F@main@i','i','%s/main.cpp'%(cur_dir),22,37,clang.cindex.CursorKind.VAR_DECL.value,0,0,1),
('c:main.cpp@127@F@main@vec','vec','%s/main.cpp'%(cur_dir),22,41,clang.cindex.CursorKind.DECL_REF_EXPR.value,'%s/main.cpp'%(cur_dir),9,23),
('c:main.cpp@402@F@main@i','i','%s/main.cpp'%(cur_dir),23,5,clang.cindex.CursorKind.DECL_REF_EXPR.value,'%s/main.cpp'%(cur_dir),22,37),
('c:main.cpp@402@F@main@i','i','%s/main.cpp'%(cur_dir),25,25,clang.cindex.CursorKind.DECL_REF_EXPR.value,'%s/main.cpp'%(cur_dir),22,37),
# ns0.h
('c:@N@NS0','NS0',cur_dir+'/subdir/ns0.h',2,11,clang.cindex.CursorKind.NAMESPACE.value,0,0,1),
('c:ns0.h@39@N@NS0@T@MYINT','MYINT',cur_dir+'/subdir/ns0.h',3,17,clang.cindex.CursorKind.TYPEDEF_DECL.value,0,0,1),
('c:@N@NS0@C@C0','C0',cur_dir+'/subdir/ns0.h',4,11,clang.cindex.CursorKind.CLASS_DECL.value,0,0,1),
('c:@N@NS0@C@C0@F@C0#I#','C0',cur_dir+'/subdir/ns0.h',6,9,clang.cindex.CursorKind.CONSTRUCTOR.value,0,0,1),
('c:ns0.h@101@N@NS0@C@C0@F@C0#I#@a','a',cur_dir+'/subdir/ns0.h',6,16,clang.cindex.CursorKind.PARM_DECL.value,0,0,1),
('c:@N@NS0@C@C0@FI@m_val','m_val',cur_dir+'/subdir/ns0.h',6,21,clang.cindex.CursorKind.MEMBER_REF.value,cur_dir+'/subdir/ns0.h',9,13),
('c:ns0.h@101@N@NS0@C@C0@F@C0#I#@a','a',cur_dir+'/subdir/ns0.h',6,27,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/subdir/ns0.h',6,16),
('c:@N@NS0@C@C0@F@check#','check',cur_dir+'/subdir/ns0.h',7,13,clang.cindex.CursorKind.CXX_METHOD.value,0,0,0),
('c:@N@NS0@C@C0@FI@m_val','m_val',cur_dir+'/subdir/ns0.h',9,13,clang.cindex.CursorKind.FIELD_DECL.value,0,0,1),
('c:@N@NS0@C@C1','C1',cur_dir+'/subdir/ns0.h',11,11,clang.cindex.CursorKind.CLASS_DECL.value,0,0,1),
('c:@N@NS0@C@C1@F@C1#I#','C1',cur_dir+'/subdir/ns0.h',13,9,clang.cindex.CursorKind.CONSTRUCTOR.value,0,0,1),
('c:ns0.h@228@N@NS0@C@C1@F@C1#I#@a','a',cur_dir+'/subdir/ns0.h',13,16,clang.cindex.CursorKind.PARM_DECL.value,0,0,1),
('c:@N@NS0@C@C1@FI@m_val','m_val',cur_dir+'/subdir/ns0.h',13,21,clang.cindex.CursorKind.MEMBER_REF.value,cur_dir+'/subdir/ns0.h',17,13),
('c:ns0.h@228@N@NS0@C@C1@F@C1#I#@a','a',cur_dir+'/subdir/ns0.h',13,27,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/subdir/ns0.h',13,16),
('c:ns0.h@39@N@NS0@T@MYINT','MYINT',cur_dir+'/subdir/ns0.h',14,9,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/subdir/ns0.h',3,17),
('c:@N@NS0@C@C1@F@check#1','check',cur_dir+'/subdir/ns0.h',14,15,clang.cindex.CursorKind.CXX_METHOD.value,0,0,0),
('c:@N@NS0@C@C1','C1',cur_dir+'/subdir/ns0.h',15,9,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/subdir/ns0.h',11,11),
('c:@N@NS0@C@C1@F@check2#','check2',cur_dir+'/subdir/ns0.h',15,12,clang.cindex.CursorKind.CXX_METHOD.value,0,0,0),
('c:@N@NS0@C@C1@FI@m_val','m_val',cur_dir+'/subdir/ns0.h',17,13,clang.cindex.CursorKind.FIELD_DECL.value,0,0,1),
# ns1.h
('c:@N@NS1','NS1',cur_dir+'/ns1.h',2,11,clang.cindex.CursorKind.NAMESPACE.value,0,0,1),
('c:@N@NS1@C@C0','C0',cur_dir+'/ns1.h',3,11,clang.cindex.CursorKind.CLASS_DECL.value,0,0,1),
('c:@N@NS1@C@C0@F@C0#I#','C0',cur_dir+'/ns1.h',5,9,clang.cindex.CursorKind.CONSTRUCTOR.value,0,0,1),
('c:ns1.h@77@N@NS1@C@C0@F@C0#I#@a','a',cur_dir+'/ns1.h',5,16,clang.cindex.CursorKind.PARM_DECL.value,0,0,1),
('c:@N@NS1@C@C0@FI@m_val','m_val',cur_dir+'/ns1.h',5,21,clang.cindex.CursorKind.MEMBER_REF.value,cur_dir+'/ns1.h',8,13),
('c:ns1.h@77@N@NS1@C@C0@F@C0#I#@a','a',cur_dir+'/ns1.h',5,27,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/ns1.h',5,16),
('c:@N@NS1@C@C0@F@check#','check',cur_dir+'/ns1.h',6,14,clang.cindex.CursorKind.CXX_METHOD.value,0,0,0),
('c:@N@NS1@C@C0@FI@m_val','m_val',cur_dir+'/ns1.h',8,13,clang.cindex.CursorKind.FIELD_DECL.value,0,0,1),
('c:@N@NS1@C@C1','C1',cur_dir+'/ns1.h',10,11,clang.cindex.CursorKind.CLASS_DECL.value,0,0,1),
('c:@N@NS1@C@C1@F@C1#I#','C1',cur_dir+'/ns1.h',12,9,clang.cindex.CursorKind.CONSTRUCTOR.value,0,0,1),
('c:ns1.h@205@N@NS1@C@C1@F@C1#I#@a','a',cur_dir+'/ns1.h',12,16,clang.cindex.CursorKind.PARM_DECL.value,0,0,1),
('c:@N@NS1@C@C1@FI@m_val','m_val',cur_dir+'/ns1.h',12,21,clang.cindex.CursorKind.MEMBER_REF.value,cur_dir+'/ns1.h',15,13),
('c:ns1.h@205@N@NS1@C@C1@F@C1#I#@a','a',cur_dir+'/ns1.h',12,27,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/ns1.h',12,16),
('c:@N@NS1@C@C1@F@check#','check',cur_dir+'/ns1.h',13,14,clang.cindex.CursorKind.CXX_METHOD.value,0,0,0),
('c:@N@NS1@C@C1@FI@m_val','m_val',cur_dir+'/ns1.h',15,13,clang.cindex.CursorKind.FIELD_DECL.value,0,0,1),
],
# ns0.cpp
[
('c:@N@NS0','NS0',cur_dir+'/ns0.cpp',2,11,clang.cindex.CursorKind.NAMESPACE.value,0,0,1),
('c:@N@NS0@C@C0','C0',cur_dir+'/ns0.cpp',3,9,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/subdir/ns0.h',4,11),
('c:@N@NS0@C@C0@F@check#','check',cur_dir+'/ns0.cpp',3,13,clang.cindex.CursorKind.CXX_METHOD.value,0,0,1),
('c:@N@NS0@C@C0@FI@m_val','m_val',cur_dir+'/ns0.cpp',5,35,clang.cindex.CursorKind.MEMBER_REF_EXPR.value,cur_dir+'/subdir/ns0.h',9,13),
('c:@N@NS0@C@C0@FI@m_val','m_val',cur_dir+'/ns0.cpp',6,16,clang.cindex.CursorKind.MEMBER_REF_EXPR.value,cur_dir+'/subdir/ns0.h',9,13),
('c:ns0.h@39@N@NS0@T@MYINT','MYINT',cur_dir+'/ns0.cpp',8,5,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/subdir/ns0.h',3,17),
('c:@N@NS0@C@C1','C1',cur_dir+'/ns0.cpp',8,11,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/subdir/ns0.h',11,11),
('c:@N@NS0@C@C1@F@check#1','check',cur_dir+'/ns0.cpp',8,15,clang.cindex.CursorKind.CXX_METHOD.value,0,0,1),
('c:@N@NS0@C@C1@FI@m_val','m_val',cur_dir+'/ns0.cpp',10,35,clang.cindex.CursorKind.MEMBER_REF_EXPR.value,cur_dir+'/subdir/ns0.h',17,13),
('c:@N@NS0@C@C1@FI@m_val','m_val',cur_dir+'/ns0.cpp',11,16,clang.cindex.CursorKind.MEMBER_REF_EXPR.value,cur_dir+'/subdir/ns0.h',17,13),
('c:@N@NS0@C@C1','C1',cur_dir+'/ns0.cpp',13,5,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/subdir/ns0.h',11,11),
('c:@N@NS0@C@C1','C1',cur_dir+'/ns0.cpp',13,8,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/subdir/ns0.h',11,11),
('c:@N@NS0@C@C1@F@check2#','check2',cur_dir+'/ns0.cpp',13,12,clang.cindex.CursorKind.CXX_METHOD.value,0,0,1),
('c:@N@NS0@F@asdf#','asdf',cur_dir+'/ns0.cpp',17,10,clang.cindex.CursorKind.FUNCTION_DECL.value,0,0,1),
('c:ns0.cpp@356@N@NS0@F@asdf#I#@a','a',cur_dir+'/ns0.cpp',20,19,clang.cindex.CursorKind.PARM_DECL.value,0,0,1),
('c:ns0.cpp@356@N@NS0@F@asdf#I#@a','a',cur_dir+'/ns0.cpp',21,30,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/ns0.cpp',20,19),
],
# ns1.cpp
[
('c:@N@NS1','NS1',cur_dir+'/subdir/ns1.cpp',2,11,clang.cindex.CursorKind.NAMESPACE.value,0,0,1),
('c:@N@NS1@C@C0','C0',cur_dir+'/subdir/ns1.cpp',3,10,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/ns1.h',3,11),
('c:@N@NS1@C@C0@F@check#','check',cur_dir+'/subdir/ns1.cpp',3,14,clang.cindex.CursorKind.CXX_METHOD.value,0,0,1),
('c:@N@NS1@C@C0@FI@m_val','m_val',cur_dir+'/subdir/ns1.cpp',5,35,clang.cindex.CursorKind.MEMBER_REF_EXPR.value,cur_dir+'/ns1.h',8,13),
('c:@N@NS1@C@C1','C1',cur_dir+'/subdir/ns1.cpp',7,10,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/ns1.h',10,11),
('c:@N@NS1@C@C1@F@check#','check',cur_dir+'/subdir/ns1.cpp',7,14,clang.cindex.CursorKind.CXX_METHOD.value,0,0,1),
('c:@N@NS1@C@C1@FI@m_val','m_val',cur_dir+'/subdir/ns1.cpp',9,35,clang.cindex.CursorKind.MEMBER_REF_EXPR.value,cur_dir+'/ns1.h',15,13),
]
]

a_list_sys = [
('c:@N@std','std','%s/main.cpp'%(cur_dir),9,5,clang.cindex.CursorKind.NAMESPACE_REF.value,'/usr/include/c++/4.2.1/bits/vector.tcc',64,1),
('c:@N@std@CT>2#T#T@vector','vector','%s/main.cpp'%(cur_dir),9,10,'TEMPLATE_REF','/usr/include/c++/4.2.1/bits/stl_vector.h',162,11),
('c:@N@std@C@vector>#I#$@N@std@C@allocator>#I@F@push_back#&1I#','push_back','%s/main.cpp'%(cur_dir),10,9,clang.cindex.CursorKind.MEMBER_REF_EXPR.value,'/usr/include/c++/4.2.1/bits/stl_vector.h',600,7),
('c:@N@std@C@vector>#I#$@N@std@C@allocator>#I@F@push_back#&1I#','push_back','%s/main.cpp'%(cur_dir),11,9,clang.cindex.CursorKind.MEMBER_REF_EXPR.value,'/usr/include/c++/4.2.1/bits/stl_vector.h',600,7),
('c:@N@std@C@vector>#I#$@N@std@C@allocator>#I@F@push_back#&1I#','push_back','%s/main.cpp'%(cur_dir),12,9,clang.cindex.CursorKind.MEMBER_REF_EXPR.value,'/usr/include/c++/4.2.1/bits/stl_vector.h',600,7),
('c:main.cpp@220@F@main@c00','c00','%s/main.cpp'%(cur_dir),13,13,clang.cindex.CursorKind.VAR_DECL.value,1),
]

db_dir = sys.argv[1]
file_list = [
cur_dir + "/" + "main.cpp",
cur_dir + "/" + "ns0.cpp",
cur_dir + "/" + "subdir/ns1.cpp"
]

f_no = 0
for f in file_list:
    db = cxxtags.get_db_by_file_name(db_dir, f)
    i = 0
    for q in q_list[f_no]:
        test_one(db, q, a_list[f_no][i])
        i+=1
    if err == 0:
        print "OK"
    else:
        print "ERR: %d"%(err)
    f_no += 1

exit(err)
