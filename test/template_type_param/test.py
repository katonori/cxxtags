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

decl_col = "usr_list.name, name_list.name, file_list.name, decl.line, decl.col, decl.kind, decl.val, decl.is_virtual, decl.is_def FROM " + cxxtags.QUERY_JOINED_TABLE_DECL
ref_col = "usr_list.name, name_list.name, file_list.name, ref.line, ref.col, ref.kind, ref_file_list.name, ref.ref_line, ref.ref_col FROM " + cxxtags.QUERY_JOINED_TABLE_REF
overriden_col = "usr_list.name, name_list.name, file_list.name, overriden.line, overriden.col, overriden.kind, usr_list_overrider.name, overriden.is_def FROM " + cxxtags.QUERY_JOINED_TABLE_OVERRIDEN

q_list = [
# main.cpp
"SELECT "+decl_col+" WHERE line=4 and col=7 and file_list.name='"+cur_dir+"/main.cpp'", #C0
"SELECT "+decl_col+" WHERE line=6 and col=5 and file_list.name='"+cur_dir+"/main.cpp'", #C0
"SELECT "+decl_col+" WHERE line=6 and col=12 and file_list.name='"+cur_dir+"/main.cpp'", #a
"SELECT "+ref_col+" WHERE line=6 and col=17 and file_list.name='"+cur_dir+"/main.cpp'", #mVal
"SELECT "+ref_col+" WHERE line=6 and col=22 and file_list.name='"+cur_dir+"/main.cpp'", #a
"SELECT "+decl_col+" WHERE line=7 and col=10 and file_list.name='"+cur_dir+"/main.cpp'", #check
"SELECT "+ref_col+" WHERE line=9 and col=9 and file_list.name='"+cur_dir+"/main.cpp'", #printf
"SELECT "+ref_col+" WHERE line=9 and col=31 and file_list.name='"+cur_dir+"/main.cpp'", #mVal
"SELECT "+decl_col+" WHERE line=12 and col=9 and file_list.name='"+cur_dir+"/main.cpp'", #mVal
"SELECT "+decl_col+" WHERE line=15 and col=20 and file_list.name='"+cur_dir+"/main.cpp'", #in_type
"SELECT "+decl_col+" WHERE line=16 and col=6 and file_list.name='"+cur_dir+"/main.cpp'", #func_test
"SELECT "+ref_col+" WHERE line=16 and col=16 and file_list.name='"+cur_dir+"/main.cpp'", #in_type
"SELECT "+decl_col+" WHERE line=16 and col=24 and file_list.name='"+cur_dir+"/main.cpp'", #val
"SELECT "+ref_col+" WHERE line=18 and col=5 and file_list.name='"+cur_dir+"/main.cpp'", #std
"SELECT "+ref_col+" WHERE line=18 and col=10 and file_list.name='"+cur_dir+"/main.cpp'", #cout
"SELECT "+ref_col+" WHERE line=18 and col=29 and file_list.name='"+cur_dir+"/main.cpp'", #val
"SELECT "+ref_col+" WHERE line=18 and col=36 and file_list.name='"+cur_dir+"/main.cpp'", #std
"SELECT "+ref_col+" WHERE line=18 and col=41 and file_list.name='"+cur_dir+"/main.cpp'", #endl
"SELECT "+decl_col+" WHERE line=21 and col=5 and file_list.name='"+cur_dir+"/main.cpp'", #main
"SELECT "+ref_col+" WHERE line=23 and col=5 and file_list.name='"+cur_dir+"/main.cpp'", #func_test
"SELECT "+ref_col+" WHERE line=24 and col=5 and file_list.name='"+cur_dir+"/main.cpp'", #func_test
"SELECT "+ref_col+" WHERE line=25 and col=5 and file_list.name='"+cur_dir+"/main.cpp'", #std
"SELECT "+ref_col+" WHERE line=25 and col=10 and file_list.name='"+cur_dir+"/main.cpp'", #vector
"SELECT "+ref_col+" WHERE line=25 and col=17 and file_list.name='"+cur_dir+"/main.cpp'", #C0
"SELECT "+decl_col+" WHERE line=25 and col=22 and file_list.name='"+cur_dir+"/main.cpp'", #vecTest
"SELECT "+decl_col+" WHERE line=26 and col=13 and file_list.name='"+cur_dir+"/main.cpp'", #i
"SELECT "+ref_col+" WHERE line=26 and col=20 and file_list.name='"+cur_dir+"/main.cpp'", #i
"SELECT "+ref_col+" WHERE line=26 and col=27 and file_list.name='"+cur_dir+"/main.cpp'", #i
"SELECT "+ref_col+" WHERE line=27 and col=9 and file_list.name='"+cur_dir+"/main.cpp'", #vecTest
"SELECT "+ref_col+" WHERE line=27 and col=17 and file_list.name='"+cur_dir+"/main.cpp'", #push_back
"SELECT "+ref_col+" WHERE line=27 and col=27 and file_list.name='"+cur_dir+"/main.cpp'", #C0
"SELECT "+ref_col+" WHERE line=27 and col=30 and file_list.name='"+cur_dir+"/main.cpp'", #i
"SELECT "+ref_col+" WHERE line=29 and col=9 and file_list.name='"+cur_dir+"/main.cpp'", #std
"SELECT "+ref_col+" WHERE line=29 and col=14 and file_list.name='"+cur_dir+"/main.cpp'", #vector
"SELECT "+ref_col+" WHERE line=29 and col=21 and file_list.name='"+cur_dir+"/main.cpp'", #C0
"SELECT "+ref_col+" WHERE line=29 and col=27 and file_list.name='"+cur_dir+"/main.cpp'", #iterator
"SELECT "+decl_col+" WHERE line=29 and col=36 and file_list.name='"+cur_dir+"/main.cpp'", #itr
"SELECT "+ref_col+" WHERE line=29 and col=42 and file_list.name='"+cur_dir+"/main.cpp'", #vecTest
"SELECT "+ref_col+" WHERE line=29 and col=50 and file_list.name='"+cur_dir+"/main.cpp'", #begin
"SELECT "+ref_col+" WHERE line=30 and col=9 and file_list.name='"+cur_dir+"/main.cpp'", #itr
"SELECT "+ref_col+" WHERE line=30 and col=16 and file_list.name='"+cur_dir+"/main.cpp'", #vecTest
"SELECT "+ref_col+" WHERE line=30 and col=24 and file_list.name='"+cur_dir+"/main.cpp'", #end
"SELECT "+ref_col+" WHERE line=31 and col=9 and file_list.name='"+cur_dir+"/main.cpp'", #itr
"SELECT "+ref_col+" WHERE line=32 and col=9 and file_list.name='"+cur_dir+"/main.cpp'", #itr
"SELECT "+ref_col+" WHERE line=32 and col=14 and file_list.name='"+cur_dir+"/main.cpp'", #check
]

ans_list = [
(u'c:@C@C0', u'C0',cur_dir+'/main.cpp',4,7,clang.cindex.CursorKind.CLASS_DECL.value,0,0,1),
(u'c:@C@C0@F@C0#I#', u'C0',cur_dir+'/main.cpp',6,5,clang.cindex.CursorKind.CONSTRUCTOR.value,0,0,1),
(u'c:main.cpp@65@C@C0@F@C0#I#@a', u'a',cur_dir+'/main.cpp',6,12,clang.cindex.CursorKind.PARM_DECL.value,0,0,1),
(u'c:@C@C0@FI@mVal', u'mVal',cur_dir+'/main.cpp',6,17,clang.cindex.CursorKind.MEMBER_REF.value,cur_dir+u'/main.cpp', 12, 9),
(u'c:main.cpp@65@C@C0@F@C0#I#@a', u'a', cur_dir+u'/main.cpp', 6, 22, clang.cindex.CursorKind.DECL_REF_EXPR.value, cur_dir+u'/main.cpp', 6, 12),
(u'c:@C@C0@F@check#1', u'check', cur_dir+u'/main.cpp', 7, 10, clang.cindex.CursorKind.CXX_METHOD.value, 0, 0, 1),
(u'c:@F@printf', u'printf', cur_dir+u'/main.cpp', 9, 9, clang.cindex.CursorKind.DECL_REF_EXPR.value, u'/usr/include/stdio.h', 267, 6),
(u'c:@C@C0@FI@mVal', u'mVal', cur_dir+u'/main.cpp', 9, 31, clang.cindex.CursorKind.MEMBER_REF_EXPR.value, cur_dir+u'/main.cpp', 12, 9),
(u'c:@C@C0@FI@mVal', u'mVal', cur_dir+'/main.cpp',12,9,clang.cindex.CursorKind.FIELD_DECL.value,0,0,1),
(u'c:main.cpp@198', u'in_type', cur_dir+u'/main.cpp', 15, 20, clang.cindex.CursorKind.TEMPLATE_TYPE_PARAMETER.value, 0, 0, 1),
 (u'c:@FT@>1#Tfunc_test#t0.0#', u'func_test', cur_dir+u'/main.cpp', 16, 6, clang.cindex.CursorKind.FUNCTION_TEMPLATE.value, 0, 0, 1),
(u'c:main.cpp@198', u'in_type', cur_dir+u'/main.cpp', 16, 16, clang.cindex.CursorKind.TYPE_REF.value, cur_dir+u'/main.cpp', 15, 20),
(u'c:main.cpp@232@FT@>1#Tfunc_test#t0.0#@val', u'val', cur_dir+u'/main.cpp', 16, 24, clang.cindex.CursorKind.PARM_DECL.value, 0, 0, 1),
(u'c:@N@std', u'std', cur_dir+u'/main.cpp', 18, 5, clang.cindex.CursorKind.NAMESPACE_REF.value, u'/usr/include/c++/4.2.1/iostream', 48, 26),
(u'c:@N@std@cout', u'cout', cur_dir+u'/main.cpp', 18, 10, clang.cindex.CursorKind.DECL_REF_EXPR.value, u'/usr/include/c++/4.2.1/iostream', 64, 18),
(u'c:main.cpp@232@FT@>1#Tfunc_test#t0.0#@val', u'val', cur_dir+u'/main.cpp', 18, 29, clang.cindex.CursorKind.DECL_REF_EXPR.value, cur_dir+u'/main.cpp', 16, 24),
(u'c:@N@std', u'std', cur_dir+u'/main.cpp', 18, 36, clang.cindex.CursorKind.NAMESPACE_REF.value, u'/usr/include/c++/4.2.1/iostream', 48, 26),
(u'', u'endl', cur_dir+u'/main.cpp', 18, 41, clang.cindex.CursorKind.OVERLOADED_DECL_REF.value, cur_dir+u'/main.cpp', 18, 41),
(u'c:@F@main', u'main', cur_dir+u'/main.cpp', 21, 5, clang.cindex.CursorKind.FUNCTION_DECL.value, 0, 0, 1),
(u'c:@F@func_test<#I>#I#', u'func_test', cur_dir+u'/main.cpp', 23, 5, clang.cindex.CursorKind.DECL_REF_EXPR.value, cur_dir+u'/main.cpp', 16, 6),
(u'c:@F@func_test<#d>#d#', u'func_test', cur_dir+u'/main.cpp', 24, 5, clang.cindex.CursorKind.DECL_REF_EXPR.value, cur_dir+u'/main.cpp', 16, 6),
(u'c:@N@std', u'std', cur_dir+u'/main.cpp', 25, 5, clang.cindex.CursorKind.NAMESPACE_REF.value, u'/usr/include/c++/4.2.1/iostream', 48, 26),
(u'c:@N@std@CT>2#T#T@vector', u'vector', cur_dir+u'/main.cpp', 25, 10, clang.cindex.CursorKind.TEMPLATE_REF.value, u'/usr/include/c++/4.2.1/bits/stl_vector.h', 162, 11),
(u'c:@C@C0', u'C0', cur_dir+u'/main.cpp', 25, 17, clang.cindex.CursorKind.TYPE_REF.value, cur_dir+u'/main.cpp', 4, 7),
(u'c:main.cpp@351@F@main@vecTest', u'vecTest', cur_dir+u'/main.cpp', 25, 22, clang.cindex.CursorKind.VAR_DECL.value, 0, 0, 1),
(u'c:main.cpp@385@F@main@i', u'i', cur_dir+u'/main.cpp', 26, 13, clang.cindex.CursorKind.VAR_DECL.value, 0, 0, 1),
(u'c:main.cpp@385@F@main@i', u'i', cur_dir+u'/main.cpp', 26, 20, clang.cindex.CursorKind.DECL_REF_EXPR.value, cur_dir+u'/main.cpp', 26, 13),
(u'c:main.cpp@385@F@main@i', u'i', cur_dir+u'/main.cpp', 26, 27, clang.cindex.CursorKind.DECL_REF_EXPR.value, cur_dir+u'/main.cpp', 26, 13),
(u'c:main.cpp@351@F@main@vecTest', u'vecTest', cur_dir+u'/main.cpp', 27, 9, clang.cindex.CursorKind.DECL_REF_EXPR.value, cur_dir+u'/main.cpp', 25, 22),
(u'c:@N@std@C@vector>#$@C@C0#$@N@std@C@allocator>#S0_@F@push_back#&1S0_#', u'push_back', cur_dir+u'/main.cpp', 27, 17, clang.cindex.CursorKind.MEMBER_REF_EXPR.value, u'/usr/include/c++/4.2.1/bits/stl_vector.h', 600, 7),
(u'c:@C@C0', u'C0', cur_dir+u'/main.cpp', 27, 27, clang.cindex.CursorKind.TYPE_REF.value, cur_dir+u'/main.cpp', 4, 7),
(u'c:main.cpp@385@F@main@i', u'i', cur_dir+u'/main.cpp', 27, 30, clang.cindex.CursorKind.DECL_REF_EXPR.value, cur_dir+u'/main.cpp', 26, 13),
(u'c:@N@std', u'std', cur_dir+u'/main.cpp', 29, 9, clang.cindex.CursorKind.NAMESPACE_REF.value, u'/usr/include/c++/4.2.1/iostream', 48, 26),
(u'c:@N@std@CT>2#T#T@vector', u'vector', cur_dir+u'/main.cpp', 29, 14, clang.cindex.CursorKind.TEMPLATE_REF.value, u'/usr/include/c++/4.2.1/bits/stl_vector.h', 162, 11),
(u'c:@C@C0', u'C0', cur_dir+u'/main.cpp', 29, 21, clang.cindex.CursorKind.TYPE_REF.value, cur_dir+u'/main.cpp', 4, 7),
(u'c:stl_vector.h@6289@N@std@C@vector>#$@C@C0#$@N@std@C@allocator>#S0_@T@iterator', u'iterator', cur_dir+u'/main.cpp', 29, 27, clang.cindex.CursorKind.TYPE_REF.value, u'/usr/include/c++/4.2.1/bits/stl_vector.h', 179, 66),
(u'c:main.cpp@458@F@main@itr', u'itr', cur_dir+u'/main.cpp', 29, 36, clang.cindex.CursorKind.VAR_DECL.value, 0, 0, 1),
(u'c:main.cpp@351@F@main@vecTest', u'vecTest', cur_dir+u'/main.cpp', 29, 42, clang.cindex.CursorKind.DECL_REF_EXPR.value, cur_dir+u'/main.cpp', 25, 22),
(u'c:@N@std@C@vector>#$@C@C0#$@N@std@C@allocator>#S0_@F@begin#', u'begin', cur_dir+u'/main.cpp', 29, 50, clang.cindex.CursorKind.MEMBER_REF_EXPR.value, u'/usr/include/c++/4.2.1/bits/stl_vector.h', 330, 7),
(u'c:main.cpp@458@F@main@itr', u'itr', cur_dir+u'/main.cpp', 30, 9, clang.cindex.CursorKind.DECL_REF_EXPR.value, cur_dir+u'/main.cpp', 29, 36),
(u'c:main.cpp@351@F@main@vecTest', u'vecTest', cur_dir+u'/main.cpp', 30, 16, clang.cindex.CursorKind.DECL_REF_EXPR.value, cur_dir+u'/main.cpp', 25, 22),
(u'c:@N@std@C@vector>#$@C@C0#$@N@std@C@allocator>#S0_@F@end#', u'end', cur_dir+u'/main.cpp', 30, 24, clang.cindex.CursorKind.MEMBER_REF_EXPR.value, u'/usr/include/c++/4.2.1/bits/stl_vector.h', 348, 7),
(u'c:main.cpp@458@F@main@itr', u'itr', cur_dir+u'/main.cpp', 31, 9, clang.cindex.CursorKind.DECL_REF_EXPR.value, cur_dir+u'/main.cpp', 29, 36),
(u'c:main.cpp@458@F@main@itr', u'itr', cur_dir+u'/main.cpp', 32, 9, clang.cindex.CursorKind.DECL_REF_EXPR.value, cur_dir+u'/main.cpp', 29, 36),
(u'c:@C@C0@F@check#1', u'check', cur_dir+u'/main.cpp', 32, 14, clang.cindex.CursorKind.MEMBER_REF_EXPR.value, cur_dir+u'/main.cpp', 7, 10),
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
