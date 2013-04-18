#!/usr/bin/python

import sys
import os
import sqlite3
sys.path.append("../../src/")
import cxxtags_util as cxxtags

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

decl_col = "usr, name, file_name, line, col, kind, val, is_virtual, is_def"
ref_col = " usr, name, file_name, line, col, kind, ref_file_name, ref_line, ref_col"

q_list = [
# main.cpp
"select "+decl_col+" from decl where line=3 and col=7 and file_name=\""+cur_dir+"/inhe.cpp\"", #CParent0
"select "+decl_col+" from decl where line=6 and col=5 and file_name=\""+cur_dir+"/inhe.cpp\"", #CParent0
"select "+decl_col+" from decl where line=7 and col=5 and file_name=\""+cur_dir+"/inhe.cpp\"", #~CParent0
"select "+decl_col+" from decl where line=8 and col=18 and file_name=\""+cur_dir+"/inhe.cpp\"", #response
"select "+ref_col+" from ref where line=11 and col=6 and file_name=\""+cur_dir+"/inhe.cpp\"", #CParent0
"select "+decl_col+" from decl where line=11 and col=16 and file_name=\""+cur_dir+"/inhe.cpp\"", #response
"select "+decl_col+" from decl where line=15 and col=7 and file_name=\""+cur_dir+"/inhe.cpp\"", #CParent1
"select "+decl_col+" from decl where line=18 and col=5 and file_name=\""+cur_dir+"/inhe.cpp\"", #CParent1
"select "+decl_col+" from decl where line=19 and col=5 and file_name=\""+cur_dir+"/inhe.cpp\"", #~CParent1
"select "+decl_col+" from decl where line=20 and col=18 and file_name=\""+cur_dir+"/inhe.cpp\"", #response
"select "+ref_col+" from ref where line=23 and col=6 and file_name=\""+cur_dir+"/inhe.cpp\"", #CParent1
"select "+decl_col+" from decl where line=23 and col=16 and file_name=\""+cur_dir+"/inhe.cpp\"", #response
"select "+decl_col+" from decl where line=27 and col=7 and file_name=\""+cur_dir+"/inhe.cpp\"", #CChild
"select "+ref_col+" from ref where line=28 and col=10 and file_name=\""+cur_dir+"/inhe.cpp\"", #CParent0
"select "+decl_col+" from decl where line=31 and col=5 and file_name=\""+cur_dir+"/inhe.cpp\"", #CChild
"select "+decl_col+" from decl where line=32 and col=5 and file_name=\""+cur_dir+"/inhe.cpp\"", #~CChild
"select "+decl_col+" from decl where line=33 and col=18 and file_name=\""+cur_dir+"/inhe.cpp\"", #response
"select "+ref_col+" from ref where line=36 and col=6 and file_name=\""+cur_dir+"/inhe.cpp\"", #CChild
"select "+decl_col+" from decl where line=36 and col=14 and file_name=\""+cur_dir+"/inhe.cpp\"", #response
"select "+decl_col+" from decl where line=40 and col=7 and file_name=\""+cur_dir+"/inhe.cpp\"", #CGChild
"select "+ref_col+" from ref where line=41 and col=10 and file_name=\""+cur_dir+"/inhe.cpp\"", #CChild
"select "+decl_col+" from decl where line=44 and col=5 and file_name=\""+cur_dir+"/inhe.cpp\"", #CGChild
"select "+decl_col+" from decl where line=45 and col=5 and file_name=\""+cur_dir+"/inhe.cpp\"", #~CGChild
"select "+decl_col+" from decl where line=46 and col=18 and file_name=\""+cur_dir+"/inhe.cpp\"", #response
"select "+ref_col+" from ref where line=49 and col=6 and file_name=\""+cur_dir+"/inhe.cpp\"", #CGChild
"select "+decl_col+" from decl where line=49 and col=15 and file_name=\""+cur_dir+"/inhe.cpp\"", #response
"select "+decl_col+" from decl where line=53 and col=7 and file_name=\""+cur_dir+"/inhe.cpp\"", #COther
"select "+ref_col+" from ref where line=54 and col=10 and file_name=\""+cur_dir+"/inhe.cpp\"", #CParent0
"select "+ref_col+" from ref where line=54 and col=27 and file_name=\""+cur_dir+"/inhe.cpp\"", #CParent1
"select "+decl_col+" from decl where line=57 and col=5 and file_name=\""+cur_dir+"/inhe.cpp\"", #COther
"select "+decl_col+" from decl where line=58 and col=5 and file_name=\""+cur_dir+"/inhe.cpp\"", #~COther
"select "+decl_col+" from decl where line=59 and col=18 and file_name=\""+cur_dir+"/inhe.cpp\"", #response
"select "+ref_col+" from ref where line=62 and col=6 and file_name=\""+cur_dir+"/inhe.cpp\"", #COther
"select "+decl_col+" from decl where line=62 and col=14 and file_name=\""+cur_dir+"/inhe.cpp\"", #response
"select "+decl_col+" from decl where line=66 and col=13 and file_name=\""+cur_dir+"/inhe.cpp\"", #test
"select "+ref_col+" from ref where line=66 and col=24 and file_name=\""+cur_dir+"/inhe.cpp\"", #CParent0
"select "+decl_col+" from decl where line=66 and col=34 and file_name=\""+cur_dir+"/inhe.cpp\"", #a
"select "+ref_col+" from ref where line=68 and col=5 and file_name=\""+cur_dir+"/inhe.cpp\"", #a
"select "+ref_col+" from ref where line=68 and col=8 and file_name=\""+cur_dir+"/inhe.cpp\"", #response
"select "+decl_col+" from decl where line=71 and col=5 and file_name=\""+cur_dir+"/inhe.cpp\"", #main
"select "+ref_col+" from ref where line=73 and col=5 and file_name=\""+cur_dir+"/inhe.cpp\"", #CParent0
"select "+decl_col+" from decl where line=73 and col=14 and file_name=\""+cur_dir+"/inhe.cpp\"", #parent
"select "+ref_col+" from ref where line=74 and col=5 and file_name=\""+cur_dir+"/inhe.cpp\"", #CChild
"select "+decl_col+" from decl where line=74 and col=12 and file_name=\""+cur_dir+"/inhe.cpp\"", #child
"select "+ref_col+" from ref where line=75 and col=5 and file_name=\""+cur_dir+"/inhe.cpp\"", #CGChild
"select "+decl_col+" from decl where line=75 and col=13 and file_name=\""+cur_dir+"/inhe.cpp\"", #gchild
"select "+ref_col+" from ref where line=76 and col=5 and file_name=\""+cur_dir+"/inhe.cpp\"", #COther
"select "+decl_col+" from decl where line=76 and col=12 and file_name=\""+cur_dir+"/inhe.cpp\"", #other
"select "+ref_col+" from ref where line=77 and col=5 and file_name=\""+cur_dir+"/inhe.cpp\"", #parent
"select "+ref_col+" from ref where line=77 and col=12 and file_name=\""+cur_dir+"/inhe.cpp\"", #response
"select "+ref_col+" from ref where line=78 and col=5 and file_name=\""+cur_dir+"/inhe.cpp\"", #child
"select "+ref_col+" from ref where line=78 and col=11 and file_name=\""+cur_dir+"/inhe.cpp\"", #response
"select "+ref_col+" from ref where line=79 and col=5 and file_name=\""+cur_dir+"/inhe.cpp\"", #gchild
"select "+ref_col+" from ref where line=79 and col=12 and file_name=\""+cur_dir+"/inhe.cpp\"", #response
"select "+ref_col+" from ref where line=80 and col=5 and file_name=\""+cur_dir+"/inhe.cpp\"", #other
"select "+ref_col+" from ref where line=80 and col=11 and file_name=\""+cur_dir+"/inhe.cpp\"", #response
"select "+ref_col+" from ref where line=81 and col=5 and file_name=\""+cur_dir+"/inhe.cpp\"", #test
"select "+ref_col+" from ref where line=81 and col=11 and file_name=\""+cur_dir+"/inhe.cpp\"", #parent
"select "+ref_col+" from ref where line=82 and col=5 and file_name=\""+cur_dir+"/inhe.cpp\"", #test
"select "+ref_col+" from ref where line=82 and col=11 and file_name=\""+cur_dir+"/inhe.cpp\"", #child
"select "+ref_col+" from ref where line=83 and col=5 and file_name=\""+cur_dir+"/inhe.cpp\"", #test
"select "+ref_col+" from ref where line=83 and col=11 and file_name=\""+cur_dir+"/inhe.cpp\"", #gchild
"select "+ref_col+" from ref where line=84 and col=5 and file_name=\""+cur_dir+"/inhe.cpp\"", #test
"select "+ref_col+" from ref where line=84 and col=11 and file_name=\""+cur_dir+"/inhe.cpp\"", #other
]

a_list = [
('c:@C@CParent0','CParent0',cur_dir+'/inhe.cpp',3,7,'ClassDecl',0,0,1),
('c:@C@CParent0@F@CParent0#','CParent0',cur_dir+'/inhe.cpp',6,5,'CXXConstructor',0,0,1),
('c:@C@CParent0@F@~CParent0#','~CParent0',cur_dir+'/inhe.cpp',7,5,'CXXDestructor',0,0,1),
('c:@C@CParent0@F@response#','response',cur_dir+'/inhe.cpp',8,18,'CXXMethod',0,1,0),
('c:@C@CParent0','CParent0',cur_dir+'/inhe.cpp',11,6,'TypeRef',cur_dir+'/inhe.cpp',3,7),
('c:@C@CParent0@F@response#','response',cur_dir+'/inhe.cpp',11,16,'CXXMethod',0,1,1),
('c:@C@CParent1','CParent1',cur_dir+'/inhe.cpp',15,7,'ClassDecl',0,0,1),
('c:@C@CParent1@F@CParent1#','CParent1',cur_dir+'/inhe.cpp',18,5,'CXXConstructor',0,0,1),
('c:@C@CParent1@F@~CParent1#','~CParent1',cur_dir+'/inhe.cpp',19,5,'CXXDestructor',0,0,1),
('c:@C@CParent1@F@response#','response',cur_dir+'/inhe.cpp',20,18,'CXXMethod',0,1,0),
('c:@C@CParent1','CParent1',cur_dir+'/inhe.cpp',23,6,'TypeRef',cur_dir+'/inhe.cpp',15,7),
('c:@C@CParent1@F@response#','response',cur_dir+'/inhe.cpp',23,16,'CXXMethod',0,1,1),
('c:@C@CChild','CChild',cur_dir+'/inhe.cpp',27,7,'ClassDecl',0,0,1),
('c:@C@CParent0','CParent0',cur_dir+'/inhe.cpp',28,10,'TypeRef',cur_dir+'/inhe.cpp',3,7),
('c:@C@CChild@F@CChild#','CChild',cur_dir+'/inhe.cpp',31,5,'CXXConstructor',0,0,1),
('c:@C@CChild@F@~CChild#','~CChild',cur_dir+'/inhe.cpp',32,5,'CXXDestructor',0,0,1),
('c:@C@CChild@F@response#','response',cur_dir+'/inhe.cpp',33,18,'CXXMethod',0,1,0),
('c:@C@CChild','CChild',cur_dir+'/inhe.cpp',36,6,'TypeRef',cur_dir+'/inhe.cpp',27,7),
('c:@C@CChild@F@response#','response',cur_dir+'/inhe.cpp',36,14,'CXXMethod',0,1,1),
('c:@C@CGChild','CGChild',cur_dir+'/inhe.cpp',40,7,'ClassDecl',0,0,1),
('c:@C@CChild','CChild',cur_dir+'/inhe.cpp',41,10,'TypeRef',cur_dir+'/inhe.cpp',27,7),
('c:@C@CGChild@F@CGChild#','CGChild',cur_dir+'/inhe.cpp',44,5,'CXXConstructor',0,0,1),
('c:@C@CGChild@F@~CGChild#','~CGChild',cur_dir+'/inhe.cpp',45,5,'CXXDestructor',0,0,1),
('c:@C@CGChild@F@response#','response',cur_dir+'/inhe.cpp',46,18,'CXXMethod',0,1,0),
('c:@C@CGChild','CGChild',cur_dir+'/inhe.cpp',49,6,'TypeRef',cur_dir+'/inhe.cpp',40,7),
('c:@C@CGChild@F@response#','response',cur_dir+'/inhe.cpp',49,15,'CXXMethod',0,1,1),
('c:@C@COther','COther',cur_dir+'/inhe.cpp',53,7,'ClassDecl',0,0,1),
('c:@C@CParent0','CParent0',cur_dir+'/inhe.cpp',54,10,'TypeRef',cur_dir+'/inhe.cpp',3,7),
('c:@C@CParent1','CParent1',cur_dir+'/inhe.cpp',54,27,'TypeRef',cur_dir+'/inhe.cpp',15,7),
('c:@C@COther@F@COther#','COther',cur_dir+'/inhe.cpp',57,5,'CXXConstructor',0,0,1),
('c:@C@COther@F@~COther#','~COther',cur_dir+'/inhe.cpp',58,5,'CXXDestructor',0,0,1),
('c:@C@COther@F@response#','response',cur_dir+'/inhe.cpp',59,18,'CXXMethod',0,1,0),
('c:@C@COther','COther',cur_dir+'/inhe.cpp',62,6,'TypeRef',cur_dir+'/inhe.cpp',53,7),
('c:@C@COther@F@response#','response',cur_dir+'/inhe.cpp',62,14,'CXXMethod',0,1,1),
('c:inhe.cpp@869@F@test#*$@C@CParent0#','test',cur_dir+'/inhe.cpp',66,13,'FunctionDecl',0,0,1),
('c:@C@CParent0','CParent0',cur_dir+'/inhe.cpp',66,24,'TypeRef',cur_dir+'/inhe.cpp',3,7),
('c:inhe.cpp@886@F@test#*$@C@CParent0#@a','a',cur_dir+'/inhe.cpp',66,34,'ParmDecl',0,0,1),
('c:inhe.cpp@886@F@test#*$@C@CParent0#@a','a',cur_dir+'/inhe.cpp',68,5,'DeclRefExpr',cur_dir+'/inhe.cpp',66,34),
('c:@C@CParent0@F@response#','response',cur_dir+'/inhe.cpp',68,8,'MemberRefExpr',cur_dir+'/inhe.cpp',11,16),
('c:@F@main','main',cur_dir+'/inhe.cpp',71,5,'FunctionDecl',0,0,1),
('c:@C@CParent0','CParent0',cur_dir+'/inhe.cpp',73,5,'TypeRef',cur_dir+'/inhe.cpp',3,7),
('c:inhe.cpp@946@F@main@parent','parent',cur_dir+'/inhe.cpp',73,14,'VarDecl',0,0,1),
('c:@C@CChild','CChild',cur_dir+'/inhe.cpp',74,5,'TypeRef',cur_dir+'/inhe.cpp',27,7),
('c:inhe.cpp@967@F@main@child','child',cur_dir+'/inhe.cpp',74,12,'VarDecl',0,0,1),
('c:@C@CGChild','CGChild',cur_dir+'/inhe.cpp',75,5,'TypeRef',cur_dir+'/inhe.cpp',40,7),
('c:inhe.cpp@985@F@main@gchild','gchild',cur_dir+'/inhe.cpp',75,13,'VarDecl',0,0,1),
('c:@C@COther','COther',cur_dir+'/inhe.cpp',76,5,'TypeRef',cur_dir+'/inhe.cpp',53,7),
('c:inhe.cpp@1005@F@main@other','other',cur_dir+'/inhe.cpp',76,12,'VarDecl',0,0,1),
('c:inhe.cpp@946@F@main@parent','parent',cur_dir+'/inhe.cpp',77,5,'DeclRefExpr',cur_dir+'/inhe.cpp',73,14),
('c:@C@CParent0@F@response#','response',cur_dir+'/inhe.cpp',77,12,'MemberRefExpr',cur_dir+'/inhe.cpp',11,16),
('c:inhe.cpp@967@F@main@child','child',cur_dir+'/inhe.cpp',78,5,'DeclRefExpr',cur_dir+'/inhe.cpp',74,12),
('c:@C@CChild@F@response#','response',cur_dir+'/inhe.cpp',78,11,'MemberRefExpr',cur_dir+'/inhe.cpp',36,14),
('c:inhe.cpp@985@F@main@gchild','gchild',cur_dir+'/inhe.cpp',79,5,'DeclRefExpr',cur_dir+'/inhe.cpp',75,13),
('c:@C@CGChild@F@response#','response',cur_dir+'/inhe.cpp',79,12,'MemberRefExpr',cur_dir+'/inhe.cpp',49,15),
('c:inhe.cpp@1005@F@main@other','other',cur_dir+'/inhe.cpp',80,5,'DeclRefExpr',cur_dir+'/inhe.cpp',76,12),
('c:@C@COther@F@response#','response',cur_dir+'/inhe.cpp',80,11,'MemberRefExpr',cur_dir+'/inhe.cpp',62,14),
('c:inhe.cpp@869@F@test#*$@C@CParent0#','test',cur_dir+'/inhe.cpp',81,5,'DeclRefExpr',cur_dir+'/inhe.cpp',66,13),
('c:inhe.cpp@946@F@main@parent','parent',cur_dir+'/inhe.cpp',81,11,'DeclRefExpr',cur_dir+'/inhe.cpp',73,14),
('c:inhe.cpp@869@F@test#*$@C@CParent0#','test',cur_dir+'/inhe.cpp',82,5,'DeclRefExpr',cur_dir+'/inhe.cpp',66,13),
('c:inhe.cpp@967@F@main@child','child',cur_dir+'/inhe.cpp',82,11,'DeclRefExpr',cur_dir+'/inhe.cpp',74,12),
('c:inhe.cpp@869@F@test#*$@C@CParent0#','test',cur_dir+'/inhe.cpp',83,5,'DeclRefExpr',cur_dir+'/inhe.cpp',66,13),
('c:inhe.cpp@985@F@main@gchild','gchild',cur_dir+'/inhe.cpp',83,11,'DeclRefExpr',cur_dir+'/inhe.cpp',75,13),
('c:inhe.cpp@869@F@test#*$@C@CParent0#','test',cur_dir+'/inhe.cpp',84,5,'DeclRefExpr',cur_dir+'/inhe.cpp',66,13),
('c:inhe.cpp@1005@F@main@other','other',cur_dir+'/inhe.cpp',84,11,'DeclRefExpr',cur_dir+'/inhe.cpp',76,12),
# overriden
('c:@C@CParent0@F@response#','response',cur_dir+'/inhe.cpp',33,18,'CXXMethod','c:@C@CChild@F@response#',0),
('c:@C@CParent0@F@response#','response',cur_dir+'/inhe.cpp',36,14,'CXXMethod','c:@C@CChild@F@response#',1),
('c:@C@CChild@F@response#','response',cur_dir+'/inhe.cpp',46,18,'CXXMethod','c:@C@CGChild@F@response#',0),
('c:@C@CChild@F@response#','response',cur_dir+'/inhe.cpp',49,15,'CXXMethod','c:@C@CGChild@F@response#',1),
('c:@C@CParent0@F@response#','response',cur_dir+'/inhe.cpp',59,18,'CXXMethod','c:@C@COther@F@response#',0),
('c:@C@CParent1@F@response#','response',cur_dir+'/inhe.cpp',59,18,'CXXMethod','c:@C@COther@F@response#',0),
('c:@C@CParent0@F@response#','response',cur_dir+'/inhe.cpp',62,14,'CXXMethod','c:@C@COther@F@response#',1),
('c:@C@CParent1@F@response#','response',cur_dir+'/inhe.cpp',62,14,'CXXMethod','c:@C@COther@F@response#',1),
]

db_dir = sys.argv[1]
fn = cur_dir + "/" + "inhe.cpp"
db = cxxtags.get_db_by_file_name(db_dir, fn)

i = 0
for q in q_list:
    test_one(db, q, a_list[i])
    i+=1
if err == 0:
    print "OK"
else:
    print "ERR: %d"%(err)
exit(err)
