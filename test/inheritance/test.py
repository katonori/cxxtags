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

decl_col = "decl.usr, decl.name, file_list.name, decl.line, decl.col, decl.kind, decl.val, decl.is_virtual, decl.is_def FROM " + cxxtags.QUERY_JOINED_TABLE_DECL
ref_col = "ref.usr, ref.name, file_list.name, ref.line, ref.col, ref.kind, ref_file_list.name, ref.ref_line, ref.ref_col FROM " + cxxtags.QUERY_JOINED_TABLE_REF
overriden_col = "overriden.usr, overriden.name, file_list.name, overriden.line, overriden.col, overriden.kind, overriden.usr_overrider, overriden.is_def FROM " + cxxtags.QUERY_JOINED_TABLE_OVERRIDEN

q_list = [
# main.cpp
"SELECT "+decl_col+" WHERE line=3 AND col=7 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #CParent0
"SELECT "+decl_col+" WHERE line=6 AND col=5 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #CParent0
"SELECT "+decl_col+" WHERE line=7 AND col=5 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #~CParent0
"SELECT "+decl_col+" WHERE line=8 AND col=18 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #response
"SELECT "+ref_col+" WHERE line=11 AND col=6 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #CParent0
"SELECT "+decl_col+" WHERE line=11 AND col=16 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #response
"SELECT "+decl_col+" WHERE line=15 AND col=7 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #CParent1
"SELECT "+decl_col+" WHERE line=18 AND col=5 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #CParent1
"SELECT "+decl_col+" WHERE line=19 AND col=5 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #~CParent1
"SELECT "+decl_col+" WHERE line=20 AND col=18 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #response
"SELECT "+ref_col+" WHERE line=23 AND col=6 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #CParent1
"SELECT "+decl_col+" WHERE line=23 AND col=16 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #response
"SELECT "+decl_col+" WHERE line=27 AND col=7 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #CChild
"SELECT "+ref_col+" WHERE line=28 AND col=10 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #CParent0
"SELECT "+decl_col+" WHERE line=31 AND col=5 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #CChild
"SELECT "+decl_col+" WHERE line=32 AND col=5 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #~CChild
"SELECT "+decl_col+" WHERE line=33 AND col=18 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #response
"SELECT "+ref_col+" WHERE line=36 AND col=6 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #CChild
"SELECT "+decl_col+" WHERE line=36 AND col=14 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #response
"SELECT "+decl_col+" WHERE line=40 AND col=7 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #CGChild
"SELECT "+ref_col+" WHERE line=41 AND col=10 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #CChild
"SELECT "+decl_col+" WHERE line=44 AND col=5 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #CGChild
"SELECT "+decl_col+" WHERE line=45 AND col=5 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #~CGChild
"SELECT "+decl_col+" WHERE line=46 AND col=18 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #response
"SELECT "+ref_col+" WHERE line=49 AND col=6 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #CGChild
"SELECT "+decl_col+" WHERE line=49 AND col=15 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #response
"SELECT "+decl_col+" WHERE line=53 AND col=7 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #COther
"SELECT "+ref_col+" WHERE line=54 AND col=10 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #CParent0
"SELECT "+ref_col+" WHERE line=54 AND col=27 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #CParent1
"SELECT "+decl_col+" WHERE line=57 AND col=5 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #COther
"SELECT "+decl_col+" WHERE line=58 AND col=5 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #~COther
"SELECT "+decl_col+" WHERE line=59 AND col=18 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #response
"SELECT "+ref_col+" WHERE line=62 AND col=6 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #COther
"SELECT "+decl_col+" WHERE line=62 AND col=14 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #response
"SELECT "+decl_col+" WHERE line=66 AND col=13 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #test
"SELECT "+ref_col+" WHERE line=66 AND col=24 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #CParent0
"SELECT "+decl_col+" WHERE line=66 AND col=34 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #a
"SELECT "+ref_col+" WHERE line=68 AND col=5 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #a
"SELECT "+ref_col+" WHERE line=68 AND col=8 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #response
"SELECT "+decl_col+" WHERE line=71 AND col=5 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #main
"SELECT "+ref_col+" WHERE line=73 AND col=5 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #CParent0
"SELECT "+decl_col+" WHERE line=73 AND col=14 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #parent
"SELECT "+ref_col+" WHERE line=74 AND col=5 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #CChild
"SELECT "+decl_col+" WHERE line=74 AND col=12 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #child
"SELECT "+ref_col+" WHERE line=75 AND col=5 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #CGChild
"SELECT "+decl_col+" WHERE line=75 AND col=13 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #gchild
"SELECT "+ref_col+" WHERE line=76 AND col=5 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #COther
"SELECT "+decl_col+" WHERE line=76 AND col=12 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #other
"SELECT "+ref_col+" WHERE line=77 AND col=5 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #parent
"SELECT "+ref_col+" WHERE line=77 AND col=12 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #response
"SELECT "+ref_col+" WHERE line=78 AND col=5 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #child
"SELECT "+ref_col+" WHERE line=78 AND col=11 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #response
"SELECT "+ref_col+" WHERE line=79 AND col=5 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #gchild
"SELECT "+ref_col+" WHERE line=79 AND col=12 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #response
"SELECT "+ref_col+" WHERE line=80 AND col=5 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #other
"SELECT "+ref_col+" WHERE line=80 AND col=11 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #response
"SELECT "+ref_col+" WHERE line=81 AND col=5 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #test
"SELECT "+ref_col+" WHERE line=81 AND col=11 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #parent
"SELECT "+ref_col+" WHERE line=82 AND col=5 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #test
"SELECT "+ref_col+" WHERE line=82 AND col=11 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #child
"SELECT "+ref_col+" WHERE line=83 AND col=5 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #test
"SELECT "+ref_col+" WHERE line=83 AND col=11 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #gchild
"SELECT "+ref_col+" WHERE line=84 AND col=5 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #test
"SELECT "+ref_col+" WHERE line=84 AND col=11 AND file_list.name=\""+cur_dir+"/inhe.cpp\"", #other
# overriden
"SELECT "+overriden_col+" WHERE line=33 AND col=18 AND file_list.name=\""+cur_dir+"/inhe.cpp\"",
"SELECT "+overriden_col+" WHERE line=36 AND col=14 AND file_list.name=\""+cur_dir+"/inhe.cpp\"",
"SELECT "+overriden_col+" WHERE line=46 AND col=18 AND file_list.name=\""+cur_dir+"/inhe.cpp\"",
"SELECT "+overriden_col+" WHERE line=49 AND col=15 AND file_list.name=\""+cur_dir+"/inhe.cpp\"",
"SELECT "+overriden_col+" WHERE line=59 AND col=18 AND file_list.name=\""+cur_dir+"/inhe.cpp\"",
"SELECT "+overriden_col+" WHERE line=62 AND col=14 AND file_list.name=\""+cur_dir+"/inhe.cpp\"",
]

ans_list = [
('c:@C@CParent0','CParent0',cur_dir+'/inhe.cpp',3,7,clang.cindex.CursorKind.CLASS_DECL.value,0,0,1),
('c:@C@CParent0@F@CParent0#','CParent0',cur_dir+'/inhe.cpp',6,5,clang.cindex.CursorKind.CONSTRUCTOR.value,0,0,1),
('c:@C@CParent0@F@~CParent0#','~CParent0',cur_dir+'/inhe.cpp',7,5,clang.cindex.CursorKind.DESTRUCTOR.value,0,0,1),
('c:@C@CParent0@F@response#','response',cur_dir+'/inhe.cpp',8,18,clang.cindex.CursorKind.CXX_METHOD.value,0,1,0),
('c:@C@CParent0','CParent0',cur_dir+'/inhe.cpp',11,6,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/inhe.cpp',3,7),
('c:@C@CParent0@F@response#','response',cur_dir+'/inhe.cpp',11,16,clang.cindex.CursorKind.CXX_METHOD.value,0,1,1),
('c:@C@CParent1','CParent1',cur_dir+'/inhe.cpp',15,7,clang.cindex.CursorKind.CLASS_DECL.value,0,0,1),
('c:@C@CParent1@F@CParent1#','CParent1',cur_dir+'/inhe.cpp',18,5,clang.cindex.CursorKind.CONSTRUCTOR.value,0,0,1),
('c:@C@CParent1@F@~CParent1#','~CParent1',cur_dir+'/inhe.cpp',19,5,clang.cindex.CursorKind.DESTRUCTOR.value,0,0,1),
('c:@C@CParent1@F@response#','response',cur_dir+'/inhe.cpp',20,18,clang.cindex.CursorKind.CXX_METHOD.value,0,1,0),
('c:@C@CParent1','CParent1',cur_dir+'/inhe.cpp',23,6,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/inhe.cpp',15,7),
('c:@C@CParent1@F@response#','response',cur_dir+'/inhe.cpp',23,16,clang.cindex.CursorKind.CXX_METHOD.value,0,1,1),
('c:@C@CChild','CChild',cur_dir+'/inhe.cpp',27,7,clang.cindex.CursorKind.CLASS_DECL.value,0,0,1),
('c:@C@CParent0','CParent0',cur_dir+'/inhe.cpp',28,10,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/inhe.cpp',3,7),
('c:@C@CChild@F@CChild#','CChild',cur_dir+'/inhe.cpp',31,5,clang.cindex.CursorKind.CONSTRUCTOR.value,0,0,1),
('c:@C@CChild@F@~CChild#','~CChild',cur_dir+'/inhe.cpp',32,5,clang.cindex.CursorKind.DESTRUCTOR.value,0,0,1),
('c:@C@CChild@F@response#','response',cur_dir+'/inhe.cpp',33,18,clang.cindex.CursorKind.CXX_METHOD.value,0,1,0),
('c:@C@CChild','CChild',cur_dir+'/inhe.cpp',36,6,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/inhe.cpp',27,7),
('c:@C@CChild@F@response#','response',cur_dir+'/inhe.cpp',36,14,clang.cindex.CursorKind.CXX_METHOD.value,0,1,1),
('c:@C@CGChild','CGChild',cur_dir+'/inhe.cpp',40,7,clang.cindex.CursorKind.CLASS_DECL.value,0,0,1),
('c:@C@CChild','CChild',cur_dir+'/inhe.cpp',41,10,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/inhe.cpp',27,7),
('c:@C@CGChild@F@CGChild#','CGChild',cur_dir+'/inhe.cpp',44,5,clang.cindex.CursorKind.CONSTRUCTOR.value,0,0,1),
('c:@C@CGChild@F@~CGChild#','~CGChild',cur_dir+'/inhe.cpp',45,5,clang.cindex.CursorKind.DESTRUCTOR.value,0,0,1),
('c:@C@CGChild@F@response#','response',cur_dir+'/inhe.cpp',46,18,clang.cindex.CursorKind.CXX_METHOD.value,0,1,0),
('c:@C@CGChild','CGChild',cur_dir+'/inhe.cpp',49,6,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/inhe.cpp',40,7),
('c:@C@CGChild@F@response#','response',cur_dir+'/inhe.cpp',49,15,clang.cindex.CursorKind.CXX_METHOD.value,0,1,1),
('c:@C@COther','COther',cur_dir+'/inhe.cpp',53,7,clang.cindex.CursorKind.CLASS_DECL.value,0,0,1),
('c:@C@CParent0','CParent0',cur_dir+'/inhe.cpp',54,10,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/inhe.cpp',3,7),
('c:@C@CParent1','CParent1',cur_dir+'/inhe.cpp',54,27,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/inhe.cpp',15,7),
('c:@C@COther@F@COther#','COther',cur_dir+'/inhe.cpp',57,5,clang.cindex.CursorKind.CONSTRUCTOR.value,0,0,1),
('c:@C@COther@F@~COther#','~COther',cur_dir+'/inhe.cpp',58,5,clang.cindex.CursorKind.DESTRUCTOR.value,0,0,1),
('c:@C@COther@F@response#','response',cur_dir+'/inhe.cpp',59,18,clang.cindex.CursorKind.CXX_METHOD.value,0,1,0),
('c:@C@COther','COther',cur_dir+'/inhe.cpp',62,6,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/inhe.cpp',53,7),
('c:@C@COther@F@response#','response',cur_dir+'/inhe.cpp',62,14,clang.cindex.CursorKind.CXX_METHOD.value,0,1,1),
('c:inhe.cpp@869@F@test#*$@C@CParent0#','test',cur_dir+'/inhe.cpp',66,13,clang.cindex.CursorKind.FUNCTION_DECL.value,0,0,1),
('c:@C@CParent0','CParent0',cur_dir+'/inhe.cpp',66,24,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/inhe.cpp',3,7),
('c:inhe.cpp@886@F@test#*$@C@CParent0#@a','a',cur_dir+'/inhe.cpp',66,34,clang.cindex.CursorKind.PARM_DECL.value,0,0,1),
('c:inhe.cpp@886@F@test#*$@C@CParent0#@a','a',cur_dir+'/inhe.cpp',68,5,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/inhe.cpp',66,34),
('c:@C@CParent0@F@response#','response',cur_dir+'/inhe.cpp',68,8,clang.cindex.CursorKind.MEMBER_REF_EXPR.value,cur_dir+'/inhe.cpp',11,16),
('c:@F@main','main',cur_dir+'/inhe.cpp',71,5,clang.cindex.CursorKind.FUNCTION_DECL.value,0,0,1),
('c:@C@CParent0','CParent0',cur_dir+'/inhe.cpp',73,5,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/inhe.cpp',3,7),
('c:inhe.cpp@946@F@main@parent','parent',cur_dir+'/inhe.cpp',73,14,clang.cindex.CursorKind.VAR_DECL.value,0,0,1),
('c:@C@CChild','CChild',cur_dir+'/inhe.cpp',74,5,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/inhe.cpp',27,7),
('c:inhe.cpp@967@F@main@child','child',cur_dir+'/inhe.cpp',74,12,clang.cindex.CursorKind.VAR_DECL.value,0,0,1),
('c:@C@CGChild','CGChild',cur_dir+'/inhe.cpp',75,5,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/inhe.cpp',40,7),
('c:inhe.cpp@985@F@main@gchild','gchild',cur_dir+'/inhe.cpp',75,13,clang.cindex.CursorKind.VAR_DECL.value,0,0,1),
('c:@C@COther','COther',cur_dir+'/inhe.cpp',76,5,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/inhe.cpp',53,7),
('c:inhe.cpp@1005@F@main@other','other',cur_dir+'/inhe.cpp',76,12,clang.cindex.CursorKind.VAR_DECL.value,0,0,1),
('c:inhe.cpp@946@F@main@parent','parent',cur_dir+'/inhe.cpp',77,5,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/inhe.cpp',73,14),
('c:@C@CParent0@F@response#','response',cur_dir+'/inhe.cpp',77,12,clang.cindex.CursorKind.MEMBER_REF_EXPR.value,cur_dir+'/inhe.cpp',11,16),
('c:inhe.cpp@967@F@main@child','child',cur_dir+'/inhe.cpp',78,5,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/inhe.cpp',74,12),
('c:@C@CChild@F@response#','response',cur_dir+'/inhe.cpp',78,11,clang.cindex.CursorKind.MEMBER_REF_EXPR.value,cur_dir+'/inhe.cpp',36,14),
('c:inhe.cpp@985@F@main@gchild','gchild',cur_dir+'/inhe.cpp',79,5,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/inhe.cpp',75,13),
('c:@C@CGChild@F@response#','response',cur_dir+'/inhe.cpp',79,12,clang.cindex.CursorKind.MEMBER_REF_EXPR.value,cur_dir+'/inhe.cpp',49,15),
('c:inhe.cpp@1005@F@main@other','other',cur_dir+'/inhe.cpp',80,5,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/inhe.cpp',76,12),
('c:@C@COther@F@response#','response',cur_dir+'/inhe.cpp',80,11,clang.cindex.CursorKind.MEMBER_REF_EXPR.value,cur_dir+'/inhe.cpp',62,14),
('c:inhe.cpp@869@F@test#*$@C@CParent0#','test',cur_dir+'/inhe.cpp',81,5,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/inhe.cpp',66,13),
('c:inhe.cpp@946@F@main@parent','parent',cur_dir+'/inhe.cpp',81,11,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/inhe.cpp',73,14),
('c:inhe.cpp@869@F@test#*$@C@CParent0#','test',cur_dir+'/inhe.cpp',82,5,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/inhe.cpp',66,13),
('c:inhe.cpp@967@F@main@child','child',cur_dir+'/inhe.cpp',82,11,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/inhe.cpp',74,12),
('c:inhe.cpp@869@F@test#*$@C@CParent0#','test',cur_dir+'/inhe.cpp',83,5,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/inhe.cpp',66,13),
('c:inhe.cpp@985@F@main@gchild','gchild',cur_dir+'/inhe.cpp',83,11,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/inhe.cpp',75,13),
('c:inhe.cpp@869@F@test#*$@C@CParent0#','test',cur_dir+'/inhe.cpp',84,5,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/inhe.cpp',66,13),
('c:inhe.cpp@1005@F@main@other','other',cur_dir+'/inhe.cpp',84,11,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/inhe.cpp',76,12),
# overriden
('c:@C@CParent0@F@response#','response',cur_dir+'/inhe.cpp',33,18,clang.cindex.CursorKind.CXX_METHOD.value,'c:@C@CChild@F@response#',0),
('c:@C@CParent0@F@response#','response',cur_dir+'/inhe.cpp',36,14,clang.cindex.CursorKind.CXX_METHOD.value,'c:@C@CChild@F@response#',1),
('c:@C@CChild@F@response#','response',cur_dir+'/inhe.cpp',46,18,clang.cindex.CursorKind.CXX_METHOD.value,'c:@C@CGChild@F@response#',0),
('c:@C@CChild@F@response#','response',cur_dir+'/inhe.cpp',49,15,clang.cindex.CursorKind.CXX_METHOD.value,'c:@C@CGChild@F@response#',1),
('c:@C@CParent0@F@response#','response',cur_dir+'/inhe.cpp',59,18,clang.cindex.CursorKind.CXX_METHOD.value,'c:@C@COther@F@response#',0),
('c:@C@CParent1@F@response#','response',cur_dir+'/inhe.cpp',59,18,clang.cindex.CursorKind.CXX_METHOD.value,'c:@C@COther@F@response#',0),
('c:@C@CParent0@F@response#','response',cur_dir+'/inhe.cpp',62,14,clang.cindex.CursorKind.CXX_METHOD.value,'c:@C@COther@F@response#',1),
('c:@C@CParent1@F@response#','response',cur_dir+'/inhe.cpp',62,14,clang.cindex.CursorKind.CXX_METHOD.value,'c:@C@COther@F@response#',1),
]

db_dir = sys.argv[1]
fn = cur_dir + "/" + "inhe.cpp"
db = cxxtags.get_db_by_file_name(db_dir, fn)

for q in q_list:
    test_one(db, q)
if err == 0:
    print "OK"
else:
    print "ERR: %d"%(err)
exit(err)
