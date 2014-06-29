#!/usr/bin/python

import sys
import os
import sqlite3
sys.path.append("../../src/")
import cxxtags_util as cxxtags
sys.path.append("../util/")
import clang.cindex # for kind types

err = 0
ans_idx = 0

def test_one(db, q):
    global err
    global ans_idx
    res = list(db.execute(q).fetchall())
    if len(res) == 0:
        print "ERROR: no result: %d"%(len(res))
        print "    q = ", q
        err += 1
    for row in res:
        if row != ans_list[ans_idx]:
            print "DIFFER:"
            print "    ", row
            print "    ", ans_list[ans_idx]
            err += 1
        ans_idx += 1

if len(sys.argv) != 2:
    print "usage: cmd db_file"
    exit(1)

cur_dir = os.getcwd()

decl_col = "name_list.name, file_list.name, decl.line, decl.col, decl.kind, decl.val, decl.is_virtual, decl.is_def FROM " + cxxtags.QUERY_JOINED_TABLE_DECL
ref_col = "name_list.name, file_list.name, ref.line, ref.col, ref.kind, ref_file_list.name, ref.ref_line, ref.ref_col FROM " + cxxtags.QUERY_JOINED_TABLE_REF
overriden_col = "name_list.name, file_list.name, overriden.line, overriden.col, overriden.kind, usr_list_overrider.name, overriden.is_def FROM " + cxxtags.QUERY_JOINED_TABLE_OVERRIDEN

q_list = [
# main.cpp
"SELECT "+decl_col+" WHERE line=5 and col=7 and file_list.name='"+cur_dir+"/main.cpp'", #C0
"SELECT "+decl_col+" WHERE line=7 and col=5 and file_list.name='"+cur_dir+"/main.cpp'", #C0
"SELECT "+decl_col+" WHERE line=7 and col=12 and file_list.name='"+cur_dir+"/main.cpp'", #a
"SELECT "+ref_col+" WHERE line=7 and col=17 and file_list.name='"+cur_dir+"/main.cpp'", #mVal
"SELECT "+ref_col+" WHERE line=7 and col=22 and file_list.name='"+cur_dir+"/main.cpp'", #a
"SELECT "+decl_col+" WHERE line=8 and col=10 and file_list.name='"+cur_dir+"/main.cpp'", #check
"SELECT "+ref_col+" WHERE line=10 and col=31 and file_list.name='"+cur_dir+"/main.cpp'", #mVal
"SELECT "+decl_col+" WHERE line=13 and col=9 and file_list.name='"+cur_dir+"/main.cpp'", #mVal
"SELECT "+decl_col+" WHERE line=16 and col=20 and file_list.name='"+cur_dir+"/main.cpp'", #in_type
"SELECT "+decl_col+" WHERE line=17 and col=6 and file_list.name='"+cur_dir+"/main.cpp'", #func_test
"SELECT "+ref_col+" WHERE line=17 and col=16 and file_list.name='"+cur_dir+"/main.cpp'", #in_type
"SELECT "+decl_col+" WHERE line=17 and col=24 and file_list.name='"+cur_dir+"/main.cpp'", #val
"SELECT "+ref_col+" WHERE line=19 and col=29 and file_list.name='"+cur_dir+"/main.cpp'", #val
"SELECT "+ref_col+" WHERE line=19 and col=41 and file_list.name='"+cur_dir+"/main.cpp'", #endl
"SELECT "+decl_col+" WHERE line=22 and col=5 and file_list.name='"+cur_dir+"/main.cpp'", #main
"SELECT "+ref_col+" WHERE line=24 and col=5 and file_list.name='"+cur_dir+"/main.cpp'", #func_test
"SELECT "+ref_col+" WHERE line=25 and col=5 and file_list.name='"+cur_dir+"/main.cpp'", #func_test
"SELECT "+ref_col+" WHERE line=26 and col=17 and file_list.name='"+cur_dir+"/main.cpp'", #C0
"SELECT "+decl_col+" WHERE line=26 and col=22 and file_list.name='"+cur_dir+"/main.cpp'", #vecTest
"SELECT "+decl_col+" WHERE line=27 and col=13 and file_list.name='"+cur_dir+"/main.cpp'", #i
"SELECT "+ref_col+" WHERE line=27 and col=20 and file_list.name='"+cur_dir+"/main.cpp'", #i
"SELECT "+ref_col+" WHERE line=27 and col=27 and file_list.name='"+cur_dir+"/main.cpp'", #i
"SELECT "+ref_col+" WHERE line=28 and col=9 and file_list.name='"+cur_dir+"/main.cpp'", #vecTest
"SELECT "+ref_col+" WHERE line=28 and col=27 and file_list.name='"+cur_dir+"/main.cpp'", #C0
"SELECT "+ref_col+" WHERE line=28 and col=30 and file_list.name='"+cur_dir+"/main.cpp'", #i
"SELECT "+ref_col+" WHERE line=30 and col=21 and file_list.name='"+cur_dir+"/main.cpp'", #C0
"SELECT "+decl_col+" WHERE line=30 and col=36 and file_list.name='"+cur_dir+"/main.cpp'", #itr
"SELECT "+ref_col+" WHERE line=30 and col=42 and file_list.name='"+cur_dir+"/main.cpp'", #vecTest
"SELECT "+ref_col+" WHERE line=31 and col=9 and file_list.name='"+cur_dir+"/main.cpp'", #itr
"SELECT "+ref_col+" WHERE line=31 and col=16 and file_list.name='"+cur_dir+"/main.cpp'", #vecTest
"SELECT "+ref_col+" WHERE line=32 and col=9 and file_list.name='"+cur_dir+"/main.cpp'", #itr
"SELECT "+ref_col+" WHERE line=33 and col=9 and file_list.name='"+cur_dir+"/main.cpp'", #itr
"SELECT "+ref_col+" WHERE line=33 and col=14 and file_list.name='"+cur_dir+"/main.cpp'", #check
]

ans_list = [
(u'C0',cur_dir+'/main.cpp',5,7,clang.cindex.CursorKind.CLASS_DECL.value,0,0,1),
(u'C0',cur_dir+'/main.cpp',7,5,clang.cindex.CursorKind.CONSTRUCTOR.value,0,0,1),
(u'a',cur_dir+'/main.cpp',7,12,clang.cindex.CursorKind.PARM_DECL.value,0,0,1),
(u'mVal',cur_dir+'/main.cpp',7,17,clang.cindex.CursorKind.MEMBER_REF.value,cur_dir+u'/main.cpp', 13, 9),
(u'a', cur_dir+u'/main.cpp', 7, 22, clang.cindex.CursorKind.DECL_REF_EXPR.value, cur_dir+u'/main.cpp', 7, 12),
(u'check', cur_dir+u'/main.cpp', 8, 10, clang.cindex.CursorKind.CXX_METHOD.value, 0, 0, 1),
(u'mVal', cur_dir+u'/main.cpp', 10, 31, clang.cindex.CursorKind.MEMBER_REF_EXPR.value, cur_dir+u'/main.cpp', 13, 9),
(u'mVal', cur_dir+'/main.cpp',13,9,clang.cindex.CursorKind.FIELD_DECL.value,0,0,1),
(u'in_type', cur_dir+u'/main.cpp', 16, 20, clang.cindex.CursorKind.TEMPLATE_TYPE_PARAMETER.value, 0, 0, 1),
(u'func_test', cur_dir+u'/main.cpp', 17, 6, clang.cindex.CursorKind.FUNCTION_TEMPLATE.value, 0, 0, 1),
(u'in_type', cur_dir+u'/main.cpp', 17, 16, clang.cindex.CursorKind.TYPE_REF.value, cur_dir+u'/main.cpp', 16, 20),
(u'val', cur_dir+u'/main.cpp', 17, 24, clang.cindex.CursorKind.PARM_DECL.value, 0, 0, 1),
(u'val', cur_dir+u'/main.cpp', 19, 29, clang.cindex.CursorKind.DECL_REF_EXPR.value, cur_dir+u'/main.cpp', 17, 24),
(u'endl', cur_dir+u'/main.cpp', 19, 41, clang.cindex.CursorKind.OVERLOADED_DECL_REF.value, cur_dir+u'/main.cpp', 19, 41),
(u'main', cur_dir+u'/main.cpp', 22, 5, clang.cindex.CursorKind.FUNCTION_DECL.value, 0, 0, 1),
(u'func_test', cur_dir+u'/main.cpp', 24, 5, clang.cindex.CursorKind.DECL_REF_EXPR.value, cur_dir+u'/main.cpp', 17, 6),
(u'func_test', cur_dir+u'/main.cpp', 25, 5, clang.cindex.CursorKind.DECL_REF_EXPR.value, cur_dir+u'/main.cpp', 17, 6),
(u'C0', cur_dir+u'/main.cpp', 26, 17, clang.cindex.CursorKind.TYPE_REF.value, cur_dir+u'/main.cpp', 5, 7),
(u'vecTest', cur_dir+u'/main.cpp', 26, 22, clang.cindex.CursorKind.VAR_DECL.value, 0, 0, 1),
(u'i', cur_dir+u'/main.cpp', 27, 13, clang.cindex.CursorKind.VAR_DECL.value, 0, 0, 1),
(u'i', cur_dir+u'/main.cpp', 27, 20, clang.cindex.CursorKind.DECL_REF_EXPR.value, cur_dir+u'/main.cpp', 27, 13),
(u'i', cur_dir+u'/main.cpp', 27, 27, clang.cindex.CursorKind.DECL_REF_EXPR.value, cur_dir+u'/main.cpp', 27, 13),
(u'vecTest', cur_dir+u'/main.cpp', 28, 9, clang.cindex.CursorKind.DECL_REF_EXPR.value, cur_dir+u'/main.cpp', 26, 22),
(u'C0', cur_dir+u'/main.cpp', 28, 27, clang.cindex.CursorKind.TYPE_REF.value, cur_dir+u'/main.cpp', 5, 7),
(u'i', cur_dir+u'/main.cpp', 28, 30, clang.cindex.CursorKind.DECL_REF_EXPR.value, cur_dir+u'/main.cpp', 27, 13),
(u'C0', cur_dir+u'/main.cpp', 30, 21, clang.cindex.CursorKind.TYPE_REF.value, cur_dir+u'/main.cpp', 5, 7),
(u'itr', cur_dir+u'/main.cpp', 30, 36, clang.cindex.CursorKind.VAR_DECL.value, 0, 0, 1),
(u'vecTest', cur_dir+u'/main.cpp', 30, 42, clang.cindex.CursorKind.DECL_REF_EXPR.value, cur_dir+u'/main.cpp', 26, 22),
(u'itr', cur_dir+u'/main.cpp', 31, 9, clang.cindex.CursorKind.DECL_REF_EXPR.value, cur_dir+u'/main.cpp', 30, 36),
(u'vecTest', cur_dir+u'/main.cpp', 31, 16, clang.cindex.CursorKind.DECL_REF_EXPR.value, cur_dir+u'/main.cpp', 26, 22),
(u'itr', cur_dir+u'/main.cpp', 32, 9, clang.cindex.CursorKind.DECL_REF_EXPR.value, cur_dir+u'/main.cpp', 30, 36),
(u'itr', cur_dir+u'/main.cpp', 33, 9, clang.cindex.CursorKind.DECL_REF_EXPR.value, cur_dir+u'/main.cpp', 30, 36),
(u'check', cur_dir+u'/main.cpp', 33, 14, clang.cindex.CursorKind.MEMBER_REF_EXPR.value, cur_dir+u'/main.cpp', 8, 10),
]

db_dir = sys.argv[1]
fn = cur_dir + "/" + "main.cpp"
db = cxxtags.get_db_by_file_name(db_dir, fn)

for q in q_list:
    test_one(db, q)
if err == 0:
    print "OK"
else:
    print "ERR: %d"%(err)
exit(err)
