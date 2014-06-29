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

if len(sys.argv) != 2:
    print "usage: cmd db_file"
    exit(1)

db_dir = sys.argv[1]

cur_dir = os.getcwd()

decl_col = "name_list.name, file_list.name, decl.line, decl.col, decl.kind, decl.val, decl.is_def, decl.type_kind, decl.is_pointer FROM " + cxxtags.QUERY_JOINED_TABLE_DECL
ref_col = " name_list.name, file_list.name, ref.line, ref.col, ref.kind, ref_file_list.name, ref.ref_line, ref.ref_col FROM " + cxxtags.QUERY_JOINED_TABLE_REF

q_list = [
# main.cpp
"SELECT "+decl_col+" WHERE line=4 AND col=5 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_0
"SELECT "+decl_col+" WHERE line=5 AND col=5 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_1
"SELECT "+decl_col+" WHERE line=6 AND col=5 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_2
"SELECT "+decl_col+" WHERE line=7 AND col=5 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_3
"SELECT "+decl_col+" WHERE line=11 AND col=5 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL1_0
"SELECT "+decl_col+" WHERE line=12 AND col=5 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL1_1
"SELECT "+decl_col+" WHERE line=13 AND col=5 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL1_2
"SELECT "+decl_col+" WHERE line=14 AND col=5 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL1_3
"SELECT "+decl_col+" WHERE line=17 AND col=13 AND file_list.name=\""+cur_dir+"/main.cpp\"", #check
"SELECT "+ref_col+" WHERE line=19 AND col=35 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_0
"SELECT "+ref_col+" WHERE line=19 AND col=43 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_1
"SELECT "+ref_col+" WHERE line=19 AND col=51 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_2
"SELECT "+ref_col+" WHERE line=19 AND col=59 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_3
"SELECT "+decl_col+" WHERE line=22 AND col=11 AND file_list.name=\""+cur_dir+"/main.cpp\"", #NS0
"SELECT "+decl_col+" WHERE line=24 AND col=9 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_0
"SELECT "+decl_col+" WHERE line=25 AND col=9 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_1
"SELECT "+decl_col+" WHERE line=26 AND col=9 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_2
"SELECT "+decl_col+" WHERE line=27 AND col=9 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_3
"SELECT "+decl_col+" WHERE line=29 AND col=17 AND file_list.name=\""+cur_dir+"/main.cpp\"", #check
"SELECT "+ref_col+" WHERE line=31 AND col=42 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_0
"SELECT "+ref_col+" WHERE line=31 AND col=50 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_1
"SELECT "+ref_col+" WHERE line=31 AND col=58 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_2
"SELECT "+ref_col+" WHERE line=31 AND col=66 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_3
"SELECT "+decl_col+" WHERE line=33 AND col=11 AND file_list.name=\""+cur_dir+"/main.cpp\"", #C0
"SELECT "+decl_col+" WHERE line=36 AND col=13 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_0
"SELECT "+decl_col+" WHERE line=37 AND col=13 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_1
"SELECT "+decl_col+" WHERE line=38 AND col=13 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_2
"SELECT "+decl_col+" WHERE line=39 AND col=13 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_3
"SELECT "+decl_col+" WHERE line=41 AND col=14 AND file_list.name=\""+cur_dir+"/main.cpp\"", #check
"SELECT "+ref_col+" WHERE line=43 AND col=50 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_0
"SELECT "+ref_col+" WHERE line=43 AND col=58 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_1
"SELECT "+ref_col+" WHERE line=43 AND col=66 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_2
"SELECT "+ref_col+" WHERE line=43 AND col=74 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_3
"SELECT "+decl_col+" WHERE line=46 AND col=11 AND file_list.name=\""+cur_dir+"/main.cpp\"", #C1
"SELECT "+ref_col+" WHERE line=46 AND col=23 AND file_list.name=\""+cur_dir+"/main.cpp\"", #C0
"SELECT "+decl_col+" WHERE line=50 AND col=13 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_0
"SELECT "+decl_col+" WHERE line=51 AND col=13 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_1
"SELECT "+decl_col+" WHERE line=52 AND col=13 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_2
"SELECT "+decl_col+" WHERE line=53 AND col=13 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_3
"SELECT "+decl_col+" WHERE line=55 AND col=14 AND file_list.name=\""+cur_dir+"/main.cpp\"", #check
"SELECT "+ref_col+" WHERE line=57 AND col=50 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_0
"SELECT "+ref_col+" WHERE line=57 AND col=58 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_1
"SELECT "+ref_col+" WHERE line=57 AND col=66 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_2
"SELECT "+ref_col+" WHERE line=57 AND col=74 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_3
"SELECT "+decl_col+" WHERE line=62 AND col=11 AND file_list.name=\""+cur_dir+"/main.cpp\"", #NS1
"SELECT "+decl_col+" WHERE line=64 AND col=9 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_0
"SELECT "+decl_col+" WHERE line=65 AND col=9 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_1
"SELECT "+decl_col+" WHERE line=66 AND col=9 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_2
"SELECT "+decl_col+" WHERE line=67 AND col=9 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_3
"SELECT "+decl_col+" WHERE line=69 AND col=17 AND file_list.name=\""+cur_dir+"/main.cpp\"", #check
"SELECT "+ref_col+" WHERE line=71 AND col=42 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_0
"SELECT "+ref_col+" WHERE line=71 AND col=50 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_1
"SELECT "+ref_col+" WHERE line=71 AND col=58 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_2
"SELECT "+ref_col+" WHERE line=71 AND col=66 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_3
"SELECT "+decl_col+" WHERE line=73 AND col=11 AND file_list.name=\""+cur_dir+"/main.cpp\"", #C0
"SELECT "+decl_col+" WHERE line=76 AND col=13 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_0
"SELECT "+decl_col+" WHERE line=77 AND col=13 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_1
"SELECT "+decl_col+" WHERE line=78 AND col=13 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_2
"SELECT "+decl_col+" WHERE line=79 AND col=13 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_3
"SELECT "+decl_col+" WHERE line=81 AND col=14 AND file_list.name=\""+cur_dir+"/main.cpp\"", #check
"SELECT "+ref_col+" WHERE line=83 AND col=50 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_0
"SELECT "+ref_col+" WHERE line=83 AND col=58 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_1
"SELECT "+ref_col+" WHERE line=83 AND col=66 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_2
"SELECT "+ref_col+" WHERE line=83 AND col=74 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_3
"SELECT "+decl_col+" WHERE line=86 AND col=11 AND file_list.name=\""+cur_dir+"/main.cpp\"", #C1
"SELECT "+ref_col+" WHERE line=86 AND col=23 AND file_list.name=\""+cur_dir+"/main.cpp\"", #C0
"SELECT "+decl_col+" WHERE line=89 AND col=14 AND file_list.name=\""+cur_dir+"/main.cpp\"", #check
"SELECT "+ref_col+" WHERE line=91 AND col=50 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_0
"SELECT "+ref_col+" WHERE line=91 AND col=58 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_1
"SELECT "+ref_col+" WHERE line=91 AND col=66 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_2
"SELECT "+ref_col+" WHERE line=91 AND col=74 AND file_list.name=\""+cur_dir+"/main.cpp\"", #VAL0_3
"SELECT "+decl_col+" WHERE line=96 AND col=5 AND file_list.name=\""+cur_dir+"/main.cpp\"", #main
"SELECT "+ref_col+" WHERE line=98 AND col=5 AND file_list.name=\""+cur_dir+"/main.cpp\"", #NS0
"SELECT "+ref_col+" WHERE line=98 AND col=10 AND file_list.name=\""+cur_dir+"/main.cpp\"", #C0
"SELECT "+decl_col+" WHERE line=98 AND col=13 AND file_list.name=\""+cur_dir+"/main.cpp\"", #c00
"SELECT "+ref_col+" WHERE line=99 AND col=5 AND file_list.name=\""+cur_dir+"/main.cpp\"", #NS0
"SELECT "+ref_col+" WHERE line=99 AND col=10 AND file_list.name=\""+cur_dir+"/main.cpp\"", #C1
"SELECT "+decl_col+" WHERE line=99 AND col=13 AND file_list.name=\""+cur_dir+"/main.cpp\"", #c01
"SELECT "+ref_col+" WHERE line=100 AND col=5 AND file_list.name=\""+cur_dir+"/main.cpp\"", #NS1
"SELECT "+ref_col+" WHERE line=100 AND col=10 AND file_list.name=\""+cur_dir+"/main.cpp\"", #C0
"SELECT "+decl_col+" WHERE line=100 AND col=13 AND file_list.name=\""+cur_dir+"/main.cpp\"", #c10
"SELECT "+ref_col+" WHERE line=101 AND col=5 AND file_list.name=\""+cur_dir+"/main.cpp\"", #NS1
"SELECT "+ref_col+" WHERE line=101 AND col=10 AND file_list.name=\""+cur_dir+"/main.cpp\"", #C1
"SELECT "+decl_col+" WHERE line=101 AND col=13 AND file_list.name=\""+cur_dir+"/main.cpp\"", #c11
"SELECT "+ref_col+" WHERE line=102 AND col=7 AND file_list.name=\""+cur_dir+"/main.cpp\"", #check
"SELECT "+ref_col+" WHERE line=103 AND col=5 AND file_list.name=\""+cur_dir+"/main.cpp\"", #NS0
"SELECT "+ref_col+" WHERE line=103 AND col=10 AND file_list.name=\""+cur_dir+"/main.cpp\"", #check
"SELECT "+ref_col+" WHERE line=104 AND col=5 AND file_list.name=\""+cur_dir+"/main.cpp\"", #NS1
"SELECT "+ref_col+" WHERE line=104 AND col=10 AND file_list.name=\""+cur_dir+"/main.cpp\"", #check
"SELECT "+ref_col+" WHERE line=105 AND col=5 AND file_list.name=\""+cur_dir+"/main.cpp\"", #c00
"SELECT "+ref_col+" WHERE line=105 AND col=9 AND file_list.name=\""+cur_dir+"/main.cpp\"", #check
"SELECT "+ref_col+" WHERE line=106 AND col=5 AND file_list.name=\""+cur_dir+"/main.cpp\"", #c01
"SELECT "+ref_col+" WHERE line=106 AND col=9 AND file_list.name=\""+cur_dir+"/main.cpp\"", #check
"SELECT "+ref_col+" WHERE line=107 AND col=5 AND file_list.name=\""+cur_dir+"/main.cpp\"", #c10
"SELECT "+ref_col+" WHERE line=107 AND col=9 AND file_list.name=\""+cur_dir+"/main.cpp\"", #check
"SELECT "+ref_col+" WHERE line=108 AND col=5 AND file_list.name=\""+cur_dir+"/main.cpp\"", #c11
"SELECT "+ref_col+" WHERE line=108 AND col=9 AND file_list.name=\""+cur_dir+"/main.cpp\"", #check
]

a_list = [

('VAL0_0',cur_dir+'/main.cpp',4,5,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,0,1,106,0),
('VAL0_1',cur_dir+'/main.cpp',5,5,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,1,1,106,0),
('VAL0_2',cur_dir+'/main.cpp',6,5,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,2,1,106,0),
('VAL0_3',cur_dir+'/main.cpp',7,5,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,3,1,106,0),
('VAL1_0',cur_dir+'/main.cpp',11,5,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,0,1,106,0),
('VAL1_1',cur_dir+'/main.cpp',12,5,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,1,1,106,0),
('VAL1_2',cur_dir+'/main.cpp',13,5,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,2,1,106,0),
('VAL1_3',cur_dir+'/main.cpp',14,5,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,3,1,106,0),
('check',cur_dir+'/main.cpp',17,13,clang.cindex.CursorKind.FUNCTION_DECL.value,0,1, 2, 0),
('VAL0_0',cur_dir+'/main.cpp',19,35,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',4,5),
('VAL0_1',cur_dir+'/main.cpp',19,43,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',5,5),
('VAL0_2',cur_dir+'/main.cpp',19,51,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',6,5),
('VAL0_3',cur_dir+'/main.cpp',19,59,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',7,5),
('NS0',cur_dir+'/main.cpp',22,11,clang.cindex.CursorKind.NAMESPACE.value,0,1,0,0),
('VAL0_0',cur_dir+'/main.cpp',24,9,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,10,1,106,0),
('VAL0_1',cur_dir+'/main.cpp',25,9,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,11,1,106,0),
('VAL0_2',cur_dir+'/main.cpp',26,9,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,12,1,106,0),
('VAL0_3',cur_dir+'/main.cpp',27,9,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,13,1,106,0),
('check',cur_dir+'/main.cpp',29,17,clang.cindex.CursorKind.FUNCTION_DECL.value,0,1,2,0),
('VAL0_0',cur_dir+'/main.cpp',31,42,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',24,9),
('VAL0_1',cur_dir+'/main.cpp',31,50,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',25,9),
('VAL0_2',cur_dir+'/main.cpp',31,58,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',26,9),
('VAL0_3',cur_dir+'/main.cpp',31,66,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',27,9),
('C0',cur_dir+'/main.cpp',33,11,clang.cindex.CursorKind.CLASS_DECL.value,0,1, 105, 0),
('VAL0_0',cur_dir+'/main.cpp',36,13,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,20,1, 106, 0),
('VAL0_1',cur_dir+'/main.cpp',37,13,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,21,1, 106, 0),
('VAL0_2',cur_dir+'/main.cpp',38,13,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,22,1, 106, 0),
('VAL0_3',cur_dir+'/main.cpp',39,13,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,23,1, 106, 0),
('check',cur_dir+'/main.cpp',41,14,clang.cindex.CursorKind.CXX_METHOD.value,0,1, 2, 0),
('VAL0_0',cur_dir+'/main.cpp',43,50,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',36,13),
('VAL0_1',cur_dir+'/main.cpp',43,58,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',37,13),
('VAL0_2',cur_dir+'/main.cpp',43,66,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',38,13),
('VAL0_3',cur_dir+'/main.cpp',43,74,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',39,13),
('C1',cur_dir+'/main.cpp',46,11,clang.cindex.CursorKind.CLASS_DECL.value,0,1, 105, 0),
('C0',cur_dir+'/main.cpp',46,23,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/main.cpp',33,11),
('VAL0_0',cur_dir+'/main.cpp',50,13,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,30,1, 106, 0),
('VAL0_1',cur_dir+'/main.cpp',51,13,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,31,1, 106, 0),
('VAL0_2',cur_dir+'/main.cpp',52,13,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,32,1, 106, 0),
('VAL0_3',cur_dir+'/main.cpp',53,13,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,33,1, 106, 0),
('check',cur_dir+'/main.cpp',55,14,clang.cindex.CursorKind.CXX_METHOD.value,0,1, 2, 0),
('VAL0_0',cur_dir+'/main.cpp',57,50,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',50,13),
('VAL0_1',cur_dir+'/main.cpp',57,58,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',51,13),
('VAL0_2',cur_dir+'/main.cpp',57,66,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',52,13),
('VAL0_3',cur_dir+'/main.cpp',57,74,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',53,13),
('NS1',cur_dir+'/main.cpp',62,11,clang.cindex.CursorKind.NAMESPACE.value,0,1,  0, 0),
('VAL0_0',cur_dir+'/main.cpp',64,9,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,40,1, 106, 0),
('VAL0_1',cur_dir+'/main.cpp',65,9,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,41,1, 106, 0),
('VAL0_2',cur_dir+'/main.cpp',66,9,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,42,1, 106, 0),
('VAL0_3',cur_dir+'/main.cpp',67,9,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,43,1, 106, 0),
('check',cur_dir+'/main.cpp',69,17,clang.cindex.CursorKind.FUNCTION_DECL.value,0,1, 2, 0),
('VAL0_0',cur_dir+'/main.cpp',71,42,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',64,9),
('VAL0_1',cur_dir+'/main.cpp',71,50,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',65,9),
('VAL0_2',cur_dir+'/main.cpp',71,58,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',66,9),
('VAL0_3',cur_dir+'/main.cpp',71,66,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',67,9),
('C0',cur_dir+'/main.cpp',73,11,clang.cindex.CursorKind.CLASS_DECL.value,0,1, 105, 0),
('VAL0_0',cur_dir+'/main.cpp',76,13,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,50,1, 106, 0),
('VAL0_1',cur_dir+'/main.cpp',77,13,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,51,1, 106, 0),
('VAL0_2',cur_dir+'/main.cpp',78,13,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,52,1, 106, 0),
('VAL0_3',cur_dir+'/main.cpp',79,13,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,53,1, 106, 0),
('check',cur_dir+'/main.cpp',81,14,clang.cindex.CursorKind.CXX_METHOD.value,0,1, 2, 0),
('VAL0_0',cur_dir+'/main.cpp',83,50,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',76,13),
('VAL0_1',cur_dir+'/main.cpp',83,58,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',77,13),
('VAL0_2',cur_dir+'/main.cpp',83,66,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',78,13),
('VAL0_3',cur_dir+'/main.cpp',83,74,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',79,13),
('C1',cur_dir+'/main.cpp',86,11,clang.cindex.CursorKind.CLASS_DECL.value,0,1, 105, 0),
('C0',cur_dir+'/main.cpp',86,23,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/main.cpp',73,11),
('check',cur_dir+'/main.cpp',89,14,clang.cindex.CursorKind.CXX_METHOD.value,0,1, 2, 0),
('VAL0_0',cur_dir+'/main.cpp',91,50,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',76,13),
('VAL0_1',cur_dir+'/main.cpp',91,58,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',77,13),
('VAL0_2',cur_dir+'/main.cpp',91,66,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',78,13),
('VAL0_3',cur_dir+'/main.cpp',91,74,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',79,13),
('main',cur_dir+'/main.cpp',96,5,clang.cindex.CursorKind.FUNCTION_DECL.value,0,1,  17, 0),
('NS0',cur_dir+'/main.cpp',98,5,clang.cindex.CursorKind.NAMESPACE_REF.value,cur_dir+'/main.cpp',22,11),
('C0',cur_dir+'/main.cpp',98,10,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/main.cpp',33,11),
('c00',cur_dir+'/main.cpp',98,13,clang.cindex.CursorKind.VAR_DECL.value,0,1, 105, 0),
('NS0',cur_dir+'/main.cpp',99,5,clang.cindex.CursorKind.NAMESPACE_REF.value,cur_dir+'/main.cpp',22,11),
('C1',cur_dir+'/main.cpp',99,10,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/main.cpp',46,11),
('c01',cur_dir+'/main.cpp',99,13,clang.cindex.CursorKind.VAR_DECL.value,0,1, 105, 0),
('NS1',cur_dir+'/main.cpp',100,5,clang.cindex.CursorKind.NAMESPACE_REF.value,cur_dir+'/main.cpp',62,11),
('C0',cur_dir+'/main.cpp',100,10,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/main.cpp',73,11),
('c10',cur_dir+'/main.cpp',100,13,clang.cindex.CursorKind.VAR_DECL.value,0,1, 105, 0),
('NS1',cur_dir+'/main.cpp',101,5,clang.cindex.CursorKind.NAMESPACE_REF.value,cur_dir+'/main.cpp',62,11),
('C1',cur_dir+'/main.cpp',101,10,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/main.cpp',86,11),
('c11',cur_dir+'/main.cpp',101,13,clang.cindex.CursorKind.VAR_DECL.value,0,1, 105, 0),
('check',cur_dir+'/main.cpp',102,7,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',17,13),
('NS0',cur_dir+'/main.cpp',103,5,clang.cindex.CursorKind.NAMESPACE_REF.value,cur_dir+'/main.cpp',22,11),
('check',cur_dir+'/main.cpp',103,10,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',29,17),
('NS1',cur_dir+'/main.cpp',104,5,clang.cindex.CursorKind.NAMESPACE_REF.value,cur_dir+'/main.cpp',62,11),
('check',cur_dir+'/main.cpp',104,10,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',69,17),
('c00',cur_dir+'/main.cpp',105,5,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',98,13),
('check',cur_dir+'/main.cpp',105,9,clang.cindex.CursorKind.MEMBER_REF_EXPR.value,cur_dir+'/main.cpp',41,14),
('c01',cur_dir+'/main.cpp',106,5,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',99,13),
('check',cur_dir+'/main.cpp',106,9,clang.cindex.CursorKind.MEMBER_REF_EXPR.value,cur_dir+'/main.cpp',55,14),
('c10',cur_dir+'/main.cpp',107,5,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',100,13),
('check',cur_dir+'/main.cpp',107,9,clang.cindex.CursorKind.MEMBER_REF_EXPR.value,cur_dir+'/main.cpp',81,14),
('c11',cur_dir+'/main.cpp',108,5,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',101,13),
('check',cur_dir+'/main.cpp',108,9,clang.cindex.CursorKind.MEMBER_REF_EXPR.value,cur_dir+'/main.cpp',89,14),
]

db = cxxtags.get_db_by_file_name(db_dir, "main.cpp")

i = 0
for q in q_list:
    test_one(db, q, a_list[i])
    i+=1
if err == 0:
    print "OK"
else:
    print "ERR: %d"%(err)
exit(err)
