#!/usr/bin/python

import sys
import os
import sqlite3

err = 0

def test_one(q, a):
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

cur_dir = os.getcwd()

decl_col = "usr, name, file_name, line, col, kind, val, is_def from decl"
ref_col = " usr, name, file_name, line, col, kind, ref_file_name, ref_line, ref_col from ref"

q_list = [
# main.cpp
"select "+decl_col+" where line=4 and col=5 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_0
"select "+decl_col+" where line=5 and col=5 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_1
"select "+decl_col+" where line=6 and col=5 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_2
"select "+decl_col+" where line=7 and col=5 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_3
"select "+decl_col+" where line=11 and col=5 and file_name=\""+cur_dir+"/main.cpp\"", #VAL1_0
"select "+decl_col+" where line=12 and col=5 and file_name=\""+cur_dir+"/main.cpp\"", #VAL1_1
"select "+decl_col+" where line=13 and col=5 and file_name=\""+cur_dir+"/main.cpp\"", #VAL1_2
"select "+decl_col+" where line=14 and col=5 and file_name=\""+cur_dir+"/main.cpp\"", #VAL1_3
"select "+decl_col+" where line=17 and col=13 and file_name=\""+cur_dir+"/main.cpp\"", #check
"select * from ref where line=19 and col=35 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_0
"select * from ref where line=19 and col=43 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_1
"select * from ref where line=19 and col=51 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_2
"select * from ref where line=19 and col=59 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_3
"select "+decl_col+" where line=22 and col=11 and file_name=\""+cur_dir+"/main.cpp\"", #NS0
"select "+decl_col+" where line=24 and col=9 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_0
"select "+decl_col+" where line=25 and col=9 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_1
"select "+decl_col+" where line=26 and col=9 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_2
"select "+decl_col+" where line=27 and col=9 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_3
"select "+decl_col+" where line=29 and col=17 and file_name=\""+cur_dir+"/main.cpp\"", #check
"select * from ref where line=31 and col=42 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_0
"select * from ref where line=31 and col=50 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_1
"select * from ref where line=31 and col=58 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_2
"select * from ref where line=31 and col=66 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_3
"select "+decl_col+" where line=33 and col=11 and file_name=\""+cur_dir+"/main.cpp\"", #C0
"select "+decl_col+" where line=36 and col=13 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_0
"select "+decl_col+" where line=37 and col=13 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_1
"select "+decl_col+" where line=38 and col=13 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_2
"select "+decl_col+" where line=39 and col=13 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_3
"select "+decl_col+" where line=41 and col=14 and file_name=\""+cur_dir+"/main.cpp\"", #check
"select * from ref where line=43 and col=50 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_0
"select * from ref where line=43 and col=58 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_1
"select * from ref where line=43 and col=66 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_2
"select * from ref where line=43 and col=74 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_3
"select "+decl_col+" where line=46 and col=11 and file_name=\""+cur_dir+"/main.cpp\"", #C1
"select * from ref where line=46 and col=23 and file_name=\""+cur_dir+"/main.cpp\"", #C0
"select "+decl_col+" where line=50 and col=13 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_0
"select "+decl_col+" where line=51 and col=13 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_1
"select "+decl_col+" where line=52 and col=13 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_2
"select "+decl_col+" where line=53 and col=13 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_3
"select "+decl_col+" where line=55 and col=14 and file_name=\""+cur_dir+"/main.cpp\"", #check
"select * from ref where line=57 and col=50 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_0
"select * from ref where line=57 and col=58 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_1
"select * from ref where line=57 and col=66 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_2
"select * from ref where line=57 and col=74 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_3
"select "+decl_col+" where line=62 and col=11 and file_name=\""+cur_dir+"/main.cpp\"", #NS1
"select "+decl_col+" where line=64 and col=9 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_0
"select "+decl_col+" where line=65 and col=9 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_1
"select "+decl_col+" where line=66 and col=9 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_2
"select "+decl_col+" where line=67 and col=9 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_3
"select "+decl_col+" where line=69 and col=17 and file_name=\""+cur_dir+"/main.cpp\"", #check
"select * from ref where line=71 and col=42 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_0
"select * from ref where line=71 and col=50 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_1
"select * from ref where line=71 and col=58 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_2
"select * from ref where line=71 and col=66 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_3
"select "+decl_col+" where line=73 and col=11 and file_name=\""+cur_dir+"/main.cpp\"", #C0
"select "+decl_col+" where line=76 and col=13 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_0
"select "+decl_col+" where line=77 and col=13 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_1
"select "+decl_col+" where line=78 and col=13 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_2
"select "+decl_col+" where line=79 and col=13 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_3
"select "+decl_col+" where line=81 and col=14 and file_name=\""+cur_dir+"/main.cpp\"", #check
"select * from ref where line=83 and col=50 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_0
"select * from ref where line=83 and col=58 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_1
"select * from ref where line=83 and col=66 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_2
"select * from ref where line=83 and col=74 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_3
"select "+decl_col+" where line=86 and col=11 and file_name=\""+cur_dir+"/main.cpp\"", #C1
"select * from ref where line=86 and col=23 and file_name=\""+cur_dir+"/main.cpp\"", #C0
"select "+decl_col+" where line=89 and col=14 and file_name=\""+cur_dir+"/main.cpp\"", #check
"select * from ref where line=91 and col=50 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_0
"select * from ref where line=91 and col=58 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_1
"select * from ref where line=91 and col=66 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_2
"select * from ref where line=91 and col=74 and file_name=\""+cur_dir+"/main.cpp\"", #VAL0_3
"select "+decl_col+" where line=96 and col=5 and file_name=\""+cur_dir+"/main.cpp\"", #main
"select * from ref where line=98 and col=5 and file_name=\""+cur_dir+"/main.cpp\"", #NS0
"select * from ref where line=98 and col=10 and file_name=\""+cur_dir+"/main.cpp\"", #C0
"select "+decl_col+" where line=98 and col=13 and file_name=\""+cur_dir+"/main.cpp\"", #c00
"select * from ref where line=99 and col=5 and file_name=\""+cur_dir+"/main.cpp\"", #NS0
"select * from ref where line=99 and col=10 and file_name=\""+cur_dir+"/main.cpp\"", #C1
"select "+decl_col+" where line=99 and col=13 and file_name=\""+cur_dir+"/main.cpp\"", #c01
"select * from ref where line=100 and col=5 and file_name=\""+cur_dir+"/main.cpp\"", #NS1
"select * from ref where line=100 and col=10 and file_name=\""+cur_dir+"/main.cpp\"", #C0
"select "+decl_col+" where line=100 and col=13 and file_name=\""+cur_dir+"/main.cpp\"", #c10
"select * from ref where line=101 and col=5 and file_name=\""+cur_dir+"/main.cpp\"", #NS1
"select * from ref where line=101 and col=10 and file_name=\""+cur_dir+"/main.cpp\"", #C1
"select "+decl_col+" where line=101 and col=13 and file_name=\""+cur_dir+"/main.cpp\"", #c11
"select * from ref where line=102 and col=7 and file_name=\""+cur_dir+"/main.cpp\"", #check
"select * from ref where line=103 and col=5 and file_name=\""+cur_dir+"/main.cpp\"", #NS0
"select * from ref where line=103 and col=10 and file_name=\""+cur_dir+"/main.cpp\"", #check
"select * from ref where line=104 and col=5 and file_name=\""+cur_dir+"/main.cpp\"", #NS1
"select * from ref where line=104 and col=10 and file_name=\""+cur_dir+"/main.cpp\"", #check
"select * from ref where line=105 and col=5 and file_name=\""+cur_dir+"/main.cpp\"", #c00
"select * from ref where line=105 and col=9 and file_name=\""+cur_dir+"/main.cpp\"", #check
"select * from ref where line=106 and col=5 and file_name=\""+cur_dir+"/main.cpp\"", #c01
"select * from ref where line=106 and col=9 and file_name=\""+cur_dir+"/main.cpp\"", #check
"select * from ref where line=107 and col=5 and file_name=\""+cur_dir+"/main.cpp\"", #c10
"select * from ref where line=107 and col=9 and file_name=\""+cur_dir+"/main.cpp\"", #check
"select * from ref where line=108 and col=5 and file_name=\""+cur_dir+"/main.cpp\"", #c11
"select * from ref where line=108 and col=9 and file_name=\""+cur_dir+"/main.cpp\"", #check
]

a_list = [
('c:main.cpp@20@Ea@VAL0_0','VAL0_0','/Users/norito/devel/cxxtags/test/enum/main.cpp',4,5,'EnumConstantDecl',0,1),
('c:main.cpp@20@Ea@VAL0_1','VAL0_1','/Users/norito/devel/cxxtags/test/enum/main.cpp',5,5,'EnumConstantDecl',1,1),
('c:main.cpp@20@Ea@VAL0_2','VAL0_2','/Users/norito/devel/cxxtags/test/enum/main.cpp',6,5,'EnumConstantDecl',2,1),
('c:main.cpp@20@Ea@VAL0_3','VAL0_3','/Users/norito/devel/cxxtags/test/enum/main.cpp',7,5,'EnumConstantDecl',3,1),
('c:main.cpp@79@Ea@VAL1_0','VAL1_0','/Users/norito/devel/cxxtags/test/enum/main.cpp',11,5,'EnumConstantDecl',0,1),
('c:main.cpp@79@Ea@VAL1_1','VAL1_1','/Users/norito/devel/cxxtags/test/enum/main.cpp',12,5,'EnumConstantDecl',1,1),
('c:main.cpp@79@Ea@VAL1_2','VAL1_2','/Users/norito/devel/cxxtags/test/enum/main.cpp',13,5,'EnumConstantDecl',2,1),
('c:main.cpp@79@Ea@VAL1_3','VAL1_3','/Users/norito/devel/cxxtags/test/enum/main.cpp',14,5,'EnumConstantDecl',3,1),
('c:main.cpp@138@F@check#','check','/Users/norito/devel/cxxtags/test/enum/main.cpp',17,13,'FunctionDecl',0,1),
('c:main.cpp@20@Ea@VAL0_0','VAL0_0','/Users/norito/devel/cxxtags/test/enum/main.cpp',19,35,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',4,5),
('c:main.cpp@20@Ea@VAL0_1','VAL0_1','/Users/norito/devel/cxxtags/test/enum/main.cpp',19,43,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',5,5),
('c:main.cpp@20@Ea@VAL0_2','VAL0_2','/Users/norito/devel/cxxtags/test/enum/main.cpp',19,51,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',6,5),
('c:main.cpp@20@Ea@VAL0_3','VAL0_3','/Users/norito/devel/cxxtags/test/enum/main.cpp',19,59,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',7,5),
('c:@N@NS0','NS0','/Users/norito/devel/cxxtags/test/enum/main.cpp',22,11,'Namespace',0,1),
('c:main.cpp@250@N@NS0@Ea@VAL0_0','VAL0_0','/Users/norito/devel/cxxtags/test/enum/main.cpp',24,9,'EnumConstantDecl',10,1),
('c:main.cpp@250@N@NS0@Ea@VAL0_1','VAL0_1','/Users/norito/devel/cxxtags/test/enum/main.cpp',25,9,'EnumConstantDecl',11,1),
('c:main.cpp@250@N@NS0@Ea@VAL0_2','VAL0_2','/Users/norito/devel/cxxtags/test/enum/main.cpp',26,9,'EnumConstantDecl',12,1),
('c:main.cpp@250@N@NS0@Ea@VAL0_3','VAL0_3','/Users/norito/devel/cxxtags/test/enum/main.cpp',27,9,'EnumConstantDecl',13,1),
('c:main.cpp@335@N@NS0@F@check#','check','/Users/norito/devel/cxxtags/test/enum/main.cpp',29,17,'FunctionDecl',0,1),
('c:main.cpp@250@N@NS0@Ea@VAL0_0','VAL0_0','/Users/norito/devel/cxxtags/test/enum/main.cpp',31,42,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',24,9),
('c:main.cpp@250@N@NS0@Ea@VAL0_1','VAL0_1','/Users/norito/devel/cxxtags/test/enum/main.cpp',31,50,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',25,9),
('c:main.cpp@250@N@NS0@Ea@VAL0_2','VAL0_2','/Users/norito/devel/cxxtags/test/enum/main.cpp',31,58,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',26,9),
('c:main.cpp@250@N@NS0@Ea@VAL0_3','VAL0_3','/Users/norito/devel/cxxtags/test/enum/main.cpp',31,66,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',27,9),
('c:@N@NS0@C@C0','C0','/Users/norito/devel/cxxtags/test/enum/main.cpp',33,11,'ClassDecl',0,1),
('c:main.cpp@480@N@NS0@C@C0@Ea@VAL0_0','VAL0_0','/Users/norito/devel/cxxtags/test/enum/main.cpp',36,13,'EnumConstantDecl',20,1),
('c:main.cpp@480@N@NS0@C@C0@Ea@VAL0_1','VAL0_1','/Users/norito/devel/cxxtags/test/enum/main.cpp',37,13,'EnumConstantDecl',21,1),
('c:main.cpp@480@N@NS0@C@C0@Ea@VAL0_2','VAL0_2','/Users/norito/devel/cxxtags/test/enum/main.cpp',38,13,'EnumConstantDecl',22,1),
('c:main.cpp@480@N@NS0@C@C0@Ea@VAL0_3','VAL0_3','/Users/norito/devel/cxxtags/test/enum/main.cpp',39,13,'EnumConstantDecl',23,1),
('c:@N@NS0@C@C0@F@check#','check','/Users/norito/devel/cxxtags/test/enum/main.cpp',41,14,'CXXMethod',0,1),
('c:main.cpp@480@N@NS0@C@C0@Ea@VAL0_0','VAL0_0','/Users/norito/devel/cxxtags/test/enum/main.cpp',43,50,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',36,13),
('c:main.cpp@480@N@NS0@C@C0@Ea@VAL0_1','VAL0_1','/Users/norito/devel/cxxtags/test/enum/main.cpp',43,58,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',37,13),
('c:main.cpp@480@N@NS0@C@C0@Ea@VAL0_2','VAL0_2','/Users/norito/devel/cxxtags/test/enum/main.cpp',43,66,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',38,13),
('c:main.cpp@480@N@NS0@C@C0@Ea@VAL0_3','VAL0_3','/Users/norito/devel/cxxtags/test/enum/main.cpp',43,74,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',39,13),
('c:@N@NS0@C@C1','C1','/Users/norito/devel/cxxtags/test/enum/main.cpp',46,11,'ClassDecl',0,1),
('c:@N@NS0@C@C0','C0','/Users/norito/devel/cxxtags/test/enum/main.cpp',46,23,'TypeRef','/Users/norito/devel/cxxtags/test/enum/main.cpp',33,11),
('c:main.cpp@768@N@NS0@C@C1@Ea@VAL0_0','VAL0_0','/Users/norito/devel/cxxtags/test/enum/main.cpp',50,13,'EnumConstantDecl',30,1),
('c:main.cpp@768@N@NS0@C@C1@Ea@VAL0_1','VAL0_1','/Users/norito/devel/cxxtags/test/enum/main.cpp',51,13,'EnumConstantDecl',31,1),
('c:main.cpp@768@N@NS0@C@C1@Ea@VAL0_2','VAL0_2','/Users/norito/devel/cxxtags/test/enum/main.cpp',52,13,'EnumConstantDecl',32,1),
('c:main.cpp@768@N@NS0@C@C1@Ea@VAL0_3','VAL0_3','/Users/norito/devel/cxxtags/test/enum/main.cpp',53,13,'EnumConstantDecl',33,1),
('c:@N@NS0@C@C1@F@check#','check','/Users/norito/devel/cxxtags/test/enum/main.cpp',55,14,'CXXMethod',0,1),
('c:main.cpp@768@N@NS0@C@C1@Ea@VAL0_0','VAL0_0','/Users/norito/devel/cxxtags/test/enum/main.cpp',57,50,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',50,13),
('c:main.cpp@768@N@NS0@C@C1@Ea@VAL0_1','VAL0_1','/Users/norito/devel/cxxtags/test/enum/main.cpp',57,58,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',51,13),
('c:main.cpp@768@N@NS0@C@C1@Ea@VAL0_2','VAL0_2','/Users/norito/devel/cxxtags/test/enum/main.cpp',57,66,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',52,13),
('c:main.cpp@768@N@NS0@C@C1@Ea@VAL0_3','VAL0_3','/Users/norito/devel/cxxtags/test/enum/main.cpp',57,74,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',53,13),
('c:@N@NS1','NS1','/Users/norito/devel/cxxtags/test/enum/main.cpp',62,11,'Namespace',0,1),
('c:main.cpp@1025@N@NS1@Ea@VAL0_0','VAL0_0','/Users/norito/devel/cxxtags/test/enum/main.cpp',64,9,'EnumConstantDecl',40,1),
('c:main.cpp@1025@N@NS1@Ea@VAL0_1','VAL0_1','/Users/norito/devel/cxxtags/test/enum/main.cpp',65,9,'EnumConstantDecl',41,1),
('c:main.cpp@1025@N@NS1@Ea@VAL0_2','VAL0_2','/Users/norito/devel/cxxtags/test/enum/main.cpp',66,9,'EnumConstantDecl',42,1),
('c:main.cpp@1025@N@NS1@Ea@VAL0_3','VAL0_3','/Users/norito/devel/cxxtags/test/enum/main.cpp',67,9,'EnumConstantDecl',43,1),
('c:main.cpp@1112@N@NS1@F@check#','check','/Users/norito/devel/cxxtags/test/enum/main.cpp',69,17,'FunctionDecl',0,1),
('c:main.cpp@1025@N@NS1@Ea@VAL0_0','VAL0_0','/Users/norito/devel/cxxtags/test/enum/main.cpp',71,42,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',64,9),
('c:main.cpp@1025@N@NS1@Ea@VAL0_1','VAL0_1','/Users/norito/devel/cxxtags/test/enum/main.cpp',71,50,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',65,9),
('c:main.cpp@1025@N@NS1@Ea@VAL0_2','VAL0_2','/Users/norito/devel/cxxtags/test/enum/main.cpp',71,58,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',66,9),
('c:main.cpp@1025@N@NS1@Ea@VAL0_3','VAL0_3','/Users/norito/devel/cxxtags/test/enum/main.cpp',71,66,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',67,9),
('c:@N@NS1@C@C0','C0','/Users/norito/devel/cxxtags/test/enum/main.cpp',73,11,'ClassDecl',0,1),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_0','VAL0_0','/Users/norito/devel/cxxtags/test/enum/main.cpp',76,13,'EnumConstantDecl',50,1),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_1','VAL0_1','/Users/norito/devel/cxxtags/test/enum/main.cpp',77,13,'EnumConstantDecl',51,1),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_2','VAL0_2','/Users/norito/devel/cxxtags/test/enum/main.cpp',78,13,'EnumConstantDecl',52,1),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_3','VAL0_3','/Users/norito/devel/cxxtags/test/enum/main.cpp',79,13,'EnumConstantDecl',53,1),
('c:@N@NS1@C@C0@F@check#','check','/Users/norito/devel/cxxtags/test/enum/main.cpp',81,14,'CXXMethod',0,1),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_0','VAL0_0','/Users/norito/devel/cxxtags/test/enum/main.cpp',83,50,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',76,13),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_1','VAL0_1','/Users/norito/devel/cxxtags/test/enum/main.cpp',83,58,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',77,13),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_2','VAL0_2','/Users/norito/devel/cxxtags/test/enum/main.cpp',83,66,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',78,13),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_3','VAL0_3','/Users/norito/devel/cxxtags/test/enum/main.cpp',83,74,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',79,13),
('c:@N@NS1@C@C1','C1','/Users/norito/devel/cxxtags/test/enum/main.cpp',86,11,'ClassDecl',0,1),
('c:@N@NS1@C@C0','C0','/Users/norito/devel/cxxtags/test/enum/main.cpp',86,23,'TypeRef','/Users/norito/devel/cxxtags/test/enum/main.cpp',73,11),
('c:@N@NS1@C@C1@F@check#','check','/Users/norito/devel/cxxtags/test/enum/main.cpp',89,14,'CXXMethod',0,1),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_0','VAL0_0','/Users/norito/devel/cxxtags/test/enum/main.cpp',91,50,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',76,13),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_1','VAL0_1','/Users/norito/devel/cxxtags/test/enum/main.cpp',91,58,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',77,13),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_2','VAL0_2','/Users/norito/devel/cxxtags/test/enum/main.cpp',91,66,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',78,13),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_3','VAL0_3','/Users/norito/devel/cxxtags/test/enum/main.cpp',91,74,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',79,13),
('c:@F@main','main','/Users/norito/devel/cxxtags/test/enum/main.cpp',96,5,'FunctionDecl',0,1),
('c:@N@NS0','NS0','/Users/norito/devel/cxxtags/test/enum/main.cpp',98,5,'NamespaceRef','/Users/norito/devel/cxxtags/test/enum/main.cpp',22,11),
('c:@N@NS0@C@C0','C0','/Users/norito/devel/cxxtags/test/enum/main.cpp',98,10,'TypeRef','/Users/norito/devel/cxxtags/test/enum/main.cpp',33,11),
('c:main.cpp@1688@F@main@c00','c00','/Users/norito/devel/cxxtags/test/enum/main.cpp',98,13,'VarDecl',0,1),
('c:@N@NS0','NS0','/Users/norito/devel/cxxtags/test/enum/main.cpp',99,5,'NamespaceRef','/Users/norito/devel/cxxtags/test/enum/main.cpp',22,11),
('c:@N@NS0@C@C1','C1','/Users/norito/devel/cxxtags/test/enum/main.cpp',99,10,'TypeRef','/Users/norito/devel/cxxtags/test/enum/main.cpp',46,11),
('c:main.cpp@1705@F@main@c01','c01','/Users/norito/devel/cxxtags/test/enum/main.cpp',99,13,'VarDecl',0,1),
('c:@N@NS1','NS1','/Users/norito/devel/cxxtags/test/enum/main.cpp',100,5,'NamespaceRef','/Users/norito/devel/cxxtags/test/enum/main.cpp',62,11),
('c:@N@NS1@C@C0','C0','/Users/norito/devel/cxxtags/test/enum/main.cpp',100,10,'TypeRef','/Users/norito/devel/cxxtags/test/enum/main.cpp',73,11),
('c:main.cpp@1722@F@main@c10','c10','/Users/norito/devel/cxxtags/test/enum/main.cpp',100,13,'VarDecl',0,1),
('c:@N@NS1','NS1','/Users/norito/devel/cxxtags/test/enum/main.cpp',101,5,'NamespaceRef','/Users/norito/devel/cxxtags/test/enum/main.cpp',62,11),
('c:@N@NS1@C@C1','C1','/Users/norito/devel/cxxtags/test/enum/main.cpp',101,10,'TypeRef','/Users/norito/devel/cxxtags/test/enum/main.cpp',86,11),
('c:main.cpp@1739@F@main@c11','c11','/Users/norito/devel/cxxtags/test/enum/main.cpp',101,13,'VarDecl',0,1),
('c:main.cpp@138@F@check#','check','/Users/norito/devel/cxxtags/test/enum/main.cpp',102,7,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',17,13),
('c:@N@NS0','NS0','/Users/norito/devel/cxxtags/test/enum/main.cpp',103,5,'NamespaceRef','/Users/norito/devel/cxxtags/test/enum/main.cpp',22,11),
('c:main.cpp@335@N@NS0@F@check#','check','/Users/norito/devel/cxxtags/test/enum/main.cpp',103,10,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',29,17),
('c:@N@NS1','NS1','/Users/norito/devel/cxxtags/test/enum/main.cpp',104,5,'NamespaceRef','/Users/norito/devel/cxxtags/test/enum/main.cpp',62,11),
('c:main.cpp@1112@N@NS1@F@check#','check','/Users/norito/devel/cxxtags/test/enum/main.cpp',104,10,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',69,17),
('c:main.cpp@1688@F@main@c00','c00','/Users/norito/devel/cxxtags/test/enum/main.cpp',105,5,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',98,13),
('c:@N@NS0@C@C0@F@check#','check','/Users/norito/devel/cxxtags/test/enum/main.cpp',105,9,'MemberRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',41,14),
('c:main.cpp@1705@F@main@c01','c01','/Users/norito/devel/cxxtags/test/enum/main.cpp',106,5,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',99,13),
('c:@N@NS0@C@C1@F@check#','check','/Users/norito/devel/cxxtags/test/enum/main.cpp',106,9,'MemberRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',55,14),
('c:main.cpp@1722@F@main@c10','c10','/Users/norito/devel/cxxtags/test/enum/main.cpp',107,5,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',100,13),
('c:@N@NS1@C@C0@F@check#','check','/Users/norito/devel/cxxtags/test/enum/main.cpp',107,9,'MemberRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',81,14),
('c:main.cpp@1739@F@main@c11','c11','/Users/norito/devel/cxxtags/test/enum/main.cpp',108,5,'DeclRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',101,13),
('c:@N@NS1@C@C1@F@check#','check','/Users/norito/devel/cxxtags/test/enum/main.cpp',108,9,'MemberRefExpr','/Users/norito/devel/cxxtags/test/enum/main.cpp',89,14),
]

db = sqlite3.connect(sys.argv[1])

i = 0
for q in q_list:
    test_one(q, a_list[i])
    i+=1
if err == 0:
    print "OK"
else:
    print "ERR: %d"%(err)
exit(err)
