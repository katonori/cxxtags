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
"select "+decl_col+" from decl where line=5 and col=9 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+decl_col+" from decl where line=6 and col=6 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=6 and col=10 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+decl_col+" from decl where line=7 and col=5 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+decl_col+" from decl where line=9 and col=23 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=10 and col=5 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=11 and col=5 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=12 and col=5 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=13 and col=5 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=13 and col=10 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+decl_col+" from decl where line=13 and col=13 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=14 and col=5 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=14 and col=10 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+decl_col+" from decl where line=14 and col=13 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=15 and col=5 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=15 and col=10 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+decl_col+" from decl where line=15 and col=13 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=16 and col=5 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=16 and col=10 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+decl_col+" from decl where line=16 and col=13 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=17 and col=5 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=17 and col=9 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=18 and col=5 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=18 and col=9 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=19 and col=5 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=19 and col=9 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=20 and col=5 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=20 and col=9 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=21 and col=25 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+decl_col+" from decl where line=22 and col=37 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=22 and col=41 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=23 and col=5 and file_name=\"%s/main.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=25 and col=25 and file_name=\"%s/main.cpp\""%(cur_dir),
# ns0.cpp
"select "+decl_col+" from decl where line=2 and col=11 and file_name=\"%s/ns0.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=3 and col=9 and file_name=\"%s/ns0.cpp\""%(cur_dir),
"select "+decl_col+" from decl where line=3 and col=13 and file_name=\"%s/ns0.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=5 and col=35 and file_name=\"%s/ns0.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=6 and col=16 and file_name=\"%s/ns0.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=8 and col=5 and file_name=\"%s/ns0.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=8 and col=11 and file_name=\"%s/ns0.cpp\""%(cur_dir),
"select "+decl_col+" from decl where line=8 and col=15 and file_name=\"%s/ns0.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=10 and col=35 and file_name=\"%s/ns0.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=11 and col=16 and file_name=\"%s/ns0.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=13 and col=5 and file_name=\"%s/ns0.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=13 and col=8 and file_name=\"%s/ns0.cpp\""%(cur_dir),
"select "+decl_col+" from decl where line=13 and col=12 and file_name=\"%s/ns0.cpp\""%(cur_dir),
"select "+decl_col+" from decl where line=17 and col=10 and file_name=\"%s/ns0.cpp\""%(cur_dir),
"select "+decl_col+" from decl where line=20 and col=19 and file_name=\"%s/ns0.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=21 and col=30 and file_name=\"%s/ns0.cpp\""%(cur_dir),
# ns1.cpp
"select "+decl_col+" from decl where line=2 and col=11 and file_name=\"%s/subdir/ns1.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=3 and col=10 and file_name=\"%s/subdir/ns1.cpp\""%(cur_dir),
"select "+decl_col+" from decl where line=3 and col=14 and file_name=\"%s/subdir/ns1.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=5 and col=35 and file_name=\"%s/subdir/ns1.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=7 and col=10 and file_name=\"%s/subdir/ns1.cpp\""%(cur_dir),
"select "+decl_col+" from decl where line=7 and col=14 and file_name=\"%s/subdir/ns1.cpp\""%(cur_dir),
"select "+ref_col+" from ref where line=9 and col=35 and file_name=\"%s/subdir/ns1.cpp\""%(cur_dir),
# ns0.h
"select "+decl_col+" from decl where line=2 and col=11 and file_name=\"%s/subdir/ns0.h\""%(cur_dir),
"select "+decl_col+" from decl where line=3 and col=17 and file_name=\"%s/subdir/ns0.h\""%(cur_dir),
"select "+decl_col+" from decl where line=4 and col=11 and file_name=\"%s/subdir/ns0.h\""%(cur_dir),
"select "+decl_col+" from decl where line=6 and col=9 and file_name=\"%s/subdir/ns0.h\""%(cur_dir),
"select "+decl_col+" from decl where line=6 and col=16 and file_name=\"%s/subdir/ns0.h\""%(cur_dir),
"select "+ref_col+" from ref where line=6 and col=21 and file_name=\"%s/subdir/ns0.h\""%(cur_dir),
"select "+ref_col+" from ref where line=6 and col=27 and file_name=\"%s/subdir/ns0.h\""%(cur_dir),
"select "+decl_col+" from decl where line=7 and col=13 and file_name=\"%s/subdir/ns0.h\""%(cur_dir),
"select "+decl_col+" from decl where line=9 and col=13 and file_name=\"%s/subdir/ns0.h\""%(cur_dir),
"select "+decl_col+" from decl where line=11 and col=11 and file_name=\"%s/subdir/ns0.h\""%(cur_dir),
"select "+decl_col+" from decl where line=13 and col=9 and file_name=\"%s/subdir/ns0.h\""%(cur_dir),
"select "+decl_col+" from decl where line=13 and col=16 and file_name=\"%s/subdir/ns0.h\""%(cur_dir),
"select "+ref_col+" from ref where line=13 and col=21 and file_name=\"%s/subdir/ns0.h\""%(cur_dir),
"select "+ref_col+" from ref where line=13 and col=27 and file_name=\"%s/subdir/ns0.h\""%(cur_dir),
"select "+ref_col+" from ref where line=14 and col=9 and file_name=\"%s/subdir/ns0.h\""%(cur_dir),
"select "+decl_col+" from decl where line=14 and col=15 and file_name=\"%s/subdir/ns0.h\""%(cur_dir),
"select "+ref_col+" from ref where line=15 and col=9 and file_name=\"%s/subdir/ns0.h\""%(cur_dir),
"select "+decl_col+" from decl where line=15 and col=12 and file_name=\"%s/subdir/ns0.h\""%(cur_dir),
"select "+decl_col+" from decl where line=17 and col=13 and file_name=\"%s/subdir/ns0.h\""%(cur_dir),
# ns1.h
"select "+decl_col+" from decl where line=2 and col=11 and file_name=\"%s/ns1.h\""%(cur_dir),
"select "+decl_col+" from decl where line=3 and col=11 and file_name=\"%s/ns1.h\""%(cur_dir),
"select "+decl_col+" from decl where line=5 and col=9 and file_name=\"%s/ns1.h\""%(cur_dir),
"select "+decl_col+" from decl where line=5 and col=16 and file_name=\"%s/ns1.h\""%(cur_dir),
"select "+ref_col+" from ref where line=5 and col=21 and file_name=\"%s/ns1.h\""%(cur_dir),
"select "+ref_col+" from ref where line=5 and col=27 and file_name=\"%s/ns1.h\""%(cur_dir),
"select "+decl_col+" from decl where line=6 and col=14 and file_name=\"%s/ns1.h\""%(cur_dir),
"select "+decl_col+" from decl where line=8 and col=13 and file_name=\"%s/ns1.h\""%(cur_dir),
"select "+decl_col+" from decl where line=10 and col=11 and file_name=\"%s/ns1.h\""%(cur_dir),
"select "+decl_col+" from decl where line=12 and col=9 and file_name=\"%s/ns1.h\""%(cur_dir),
"select "+decl_col+" from decl where line=12 and col=16 and file_name=\"%s/ns1.h\""%(cur_dir),
"select "+ref_col+" from ref where line=12 and col=21 and file_name=\"%s/ns1.h\""%(cur_dir),
"select "+ref_col+" from ref where line=12 and col=27 and file_name=\"%s/ns1.h\""%(cur_dir),
"select "+decl_col+" from decl where line=13 and col=14 and file_name=\"%s/ns1.h\""%(cur_dir),
"select "+decl_col+" from decl where line=15 and col=13 and file_name=\"%s/ns1.h\""%(cur_dir),
]

q_list_sys = [
"select * from ref where line=9 and col=5 and file_name=\"%s/main.cpp\""%(cur_dir),
"select * from ref where line=9 and col=10 and file_name=\"%s/main.cpp\""%(cur_dir),
"select * from ref where line=10 and col=9 and file_name=\"%s/main.cpp\""%(cur_dir),
"select * from ref where line=11 and col=9 and file_name=\"%s/main.cpp\""%(cur_dir),
"select * from ref where line=12 and col=9 and file_name=\"%s/main.cpp\""%(cur_dir),
"select * from ref where line=21 and col=5 and file_name=\"%s/main.cpp\""%(cur_dir),
"select * from ref where line=22 and col=9 and file_name=\"%s/main.cpp\""%(cur_dir),
"select * from ref where line=22 and col=14 and file_name=\"%s/main.cpp\""%(cur_dir),
"select * from ref where line=22 and col=28 and file_name=\"%s/main.cpp\""%(cur_dir),
"select * from ref where line=22 and col=45 and file_name=\"%s/main.cpp\""%(cur_dir),
"select * from ref where line=25 and col=9 and file_name=\"%s/main.cpp\""%(cur_dir),
]

a_list = [
('c:macro@BUFF_SIZE','BUFF_SIZE','%s/main.cpp'%(cur_dir),5,9,'macro definition',0,0,0),
('c:@msg','msg','%s/main.cpp'%(cur_dir),6,6,'VarDecl',0,0,1),
('c:macro@BUFF_SIZE','BUFF_SIZE','%s/main.cpp'%(cur_dir),6,10,'macro expansion','%s/main.cpp'%(cur_dir),5,9),
('c:@F@main', 'main', '%s/main.cpp'%(cur_dir), 7, 5, 'FunctionDecl', 0,0,1),
('c:main.cpp@127@F@main@vec','vec','%s/main.cpp'%(cur_dir),9,23,'VarDecl',0,0,1),
('c:main.cpp@127@F@main@vec','vec','%s/main.cpp'%(cur_dir),10,5,'DeclRefExpr','%s/main.cpp'%(cur_dir),9,23),
('c:main.cpp@127@F@main@vec','vec','%s/main.cpp'%(cur_dir),11,5,'DeclRefExpr','%s/main.cpp'%(cur_dir),9,23),
('c:main.cpp@127@F@main@vec','vec','%s/main.cpp'%(cur_dir),12,5,'DeclRefExpr','%s/main.cpp'%(cur_dir),9,23),
('c:@N@NS0','NS0','%s/main.cpp'%(cur_dir),13,5,'NamespaceRef','%s/subdir/ns0.h'%(cur_dir),2,11),
('c:@N@NS0@C@C0','C0','%s/main.cpp'%(cur_dir),13,10,'TypeRef','%s/subdir/ns0.h'%(cur_dir),4,11),
('c:main.cpp@220@F@main@c00','c00','%s/main.cpp'%(cur_dir),13,13,'VarDecl',0,0,1),
('c:@N@NS1','NS1','%s/main.cpp'%(cur_dir),14,5,'NamespaceRef','%s/ns1.h'%(cur_dir),2,11),
('c:@N@NS1@C@C0','C0','%s/main.cpp'%(cur_dir),14,10,'TypeRef','%s/ns1.h'%(cur_dir),3,11),
('c:main.cpp@240@F@main@c10','c10','%s/main.cpp'%(cur_dir),14,13,'VarDecl',0,0,1),
('c:@N@NS0','NS0','%s/main.cpp'%(cur_dir),15,5,'NamespaceRef','%s/subdir/ns0.h'%(cur_dir),2,11),
('c:@N@NS0@C@C1','C1','%s/main.cpp'%(cur_dir),15,10,'TypeRef','%s/subdir/ns0.h'%(cur_dir),11,11),
('c:main.cpp@260@F@main@c01','c01','%s/main.cpp'%(cur_dir),15,13,'VarDecl',0,0,1),
('c:@N@NS1','NS1','%s/main.cpp'%(cur_dir),16,5,'NamespaceRef','%s/ns1.h'%(cur_dir),2,11),
('c:@N@NS1@C@C1','C1','%s/main.cpp'%(cur_dir),16,10,'TypeRef','%s/ns1.h'%(cur_dir),10,11),
('c:main.cpp@280@F@main@c11','c11','%s/main.cpp'%(cur_dir),16,13,'VarDecl',0,0,1),
('c:main.cpp@220@F@main@c00','c00','%s/main.cpp'%(cur_dir),17,5,'DeclRefExpr','%s/main.cpp'%(cur_dir),13,13),
('c:@N@NS0@C@C0@F@check#','check','%s/main.cpp'%(cur_dir),17,9,'MemberRefExpr','%s/subdir/ns0.h'%(cur_dir),7,13),
('c:main.cpp@240@F@main@c10','c10','%s/main.cpp'%(cur_dir),18,5,'DeclRefExpr','%s/main.cpp'%(cur_dir),14,13),
('c:@N@NS1@C@C0@F@check#','check','%s/main.cpp'%(cur_dir),18,9,'MemberRefExpr','%s/ns1.h'%(cur_dir),6,14),
('c:main.cpp@260@F@main@c01','c01','%s/main.cpp'%(cur_dir),19,5,'DeclRefExpr','%s/main.cpp'%(cur_dir),15,13),
('c:@N@NS0@C@C1@F@check#1','check','%s/main.cpp'%(cur_dir),19,9,'MemberRefExpr','%s/subdir/ns0.h'%(cur_dir),14,15),
('c:main.cpp@280@F@main@c11','c11','%s/main.cpp'%(cur_dir),20,5,'DeclRefExpr','%s/main.cpp'%(cur_dir),16,13),
('c:@N@NS1@C@C1@F@check#','check','%s/main.cpp'%(cur_dir),20,9,'MemberRefExpr','%s/ns1.h'%(cur_dir),13,14),
('c:@msg','msg','%s/main.cpp'%(cur_dir),21,25,'DeclRefExpr','%s/main.cpp'%(cur_dir),6,6),
('c:main.cpp@402@F@main@i','i','%s/main.cpp'%(cur_dir),22,37,'VarDecl',0,0,1),
('c:main.cpp@127@F@main@vec','vec','%s/main.cpp'%(cur_dir),22,41,'DeclRefExpr','%s/main.cpp'%(cur_dir),9,23),
('c:main.cpp@402@F@main@i','i','%s/main.cpp'%(cur_dir),23,5,'DeclRefExpr','%s/main.cpp'%(cur_dir),22,37),
('c:main.cpp@402@F@main@i','i','%s/main.cpp'%(cur_dir),25,25,'DeclRefExpr','%s/main.cpp'%(cur_dir),22,37),
# ns0.cpp
('c:@N@NS0','NS0',cur_dir+'/ns0.cpp',2,11,'Namespace',0,0,1),
('c:@N@NS0@C@C0','C0',cur_dir+'/ns0.cpp',3,9,'TypeRef',cur_dir+'/subdir/ns0.h',4,11),
('c:@N@NS0@C@C0@F@check#','check',cur_dir+'/ns0.cpp',3,13,'CXXMethod',0,0,1),
('c:@N@NS0@C@C0@FI@m_val','m_val',cur_dir+'/ns0.cpp',5,35,'MemberRefExpr',cur_dir+'/subdir/ns0.h',9,13),
('c:@N@NS0@C@C0@FI@m_val','m_val',cur_dir+'/ns0.cpp',6,16,'MemberRefExpr',cur_dir+'/subdir/ns0.h',9,13),
('c:ns0.h@39@N@NS0@T@MYINT','MYINT',cur_dir+'/ns0.cpp',8,5,'TypeRef',cur_dir+'/subdir/ns0.h',3,17),
('c:@N@NS0@C@C1','C1',cur_dir+'/ns0.cpp',8,11,'TypeRef',cur_dir+'/subdir/ns0.h',11,11),
('c:@N@NS0@C@C1@F@check#1','check',cur_dir+'/ns0.cpp',8,15,'CXXMethod',0,0,1),
('c:@N@NS0@C@C1@FI@m_val','m_val',cur_dir+'/ns0.cpp',10,35,'MemberRefExpr',cur_dir+'/subdir/ns0.h',17,13),
('c:@N@NS0@C@C1@FI@m_val','m_val',cur_dir+'/ns0.cpp',11,16,'MemberRefExpr',cur_dir+'/subdir/ns0.h',17,13),
('c:@N@NS0@C@C1','C1',cur_dir+'/ns0.cpp',13,5,'TypeRef',cur_dir+'/subdir/ns0.h',11,11),
('c:@N@NS0@C@C1','C1',cur_dir+'/ns0.cpp',13,8,'TypeRef',cur_dir+'/subdir/ns0.h',11,11),
('c:@N@NS0@C@C1@F@check2#','check2',cur_dir+'/ns0.cpp',13,12,'CXXMethod',0,0,1),
('c:@N@NS0@F@asdf#','asdf',cur_dir+'/ns0.cpp',17,10,'FunctionDecl',0,0,1),
('c:ns0.cpp@356@N@NS0@F@asdf#I#@a','a',cur_dir+'/ns0.cpp',20,19,'ParmDecl',0,0,1),
('c:ns0.cpp@356@N@NS0@F@asdf#I#@a','a',cur_dir+'/ns0.cpp',21,30,'DeclRefExpr',cur_dir+'/ns0.cpp',20,19),
# ns1.cpp
('c:@N@NS1','NS1',cur_dir+'/subdir/ns1.cpp',2,11,'Namespace',0,0,1),
('c:@N@NS1@C@C0','C0',cur_dir+'/subdir/ns1.cpp',3,10,'TypeRef',cur_dir+'/ns1.h',3,11),
('c:@N@NS1@C@C0@F@check#','check',cur_dir+'/subdir/ns1.cpp',3,14,'CXXMethod',0,0,1),
('c:@N@NS1@C@C0@FI@m_val','m_val',cur_dir+'/subdir/ns1.cpp',5,35,'MemberRefExpr',cur_dir+'/ns1.h',8,13),
('c:@N@NS1@C@C1','C1',cur_dir+'/subdir/ns1.cpp',7,10,'TypeRef',cur_dir+'/ns1.h',10,11),
('c:@N@NS1@C@C1@F@check#','check',cur_dir+'/subdir/ns1.cpp',7,14,'CXXMethod',0,0,1),
('c:@N@NS1@C@C1@FI@m_val','m_val',cur_dir+'/subdir/ns1.cpp',9,35,'MemberRefExpr',cur_dir+'/ns1.h',15,13),
# ns0.h
('c:@N@NS0','NS0',cur_dir+'/subdir/ns0.h',2,11,'Namespace',0,0,1),
('c:ns0.h@39@N@NS0@T@MYINT','MYINT',cur_dir+'/subdir/ns0.h',3,17,'TypedefDecl',0,0,1),
('c:@N@NS0@C@C0','C0',cur_dir+'/subdir/ns0.h',4,11,'ClassDecl',0,0,1),
('c:@N@NS0@C@C0@F@C0#I#','C0',cur_dir+'/subdir/ns0.h',6,9,'CXXConstructor',0,0,1),
('c:ns0.h@101@N@NS0@C@C0@F@C0#I#@a','a',cur_dir+'/subdir/ns0.h',6,16,'ParmDecl',0,0,1),
('c:@N@NS0@C@C0@FI@m_val','m_val',cur_dir+'/subdir/ns0.h',6,21,'MemberRef',cur_dir+'/subdir/ns0.h',9,13),
('c:ns0.h@101@N@NS0@C@C0@F@C0#I#@a','a',cur_dir+'/subdir/ns0.h',6,27,'DeclRefExpr',cur_dir+'/subdir/ns0.h',6,16),
('c:@N@NS0@C@C0@F@check#','check',cur_dir+'/subdir/ns0.h',7,13,'CXXMethod',0,0,0),
('c:@N@NS0@C@C0@FI@m_val','m_val',cur_dir+'/subdir/ns0.h',9,13,'FieldDecl',0,0,1),
('c:@N@NS0@C@C1','C1',cur_dir+'/subdir/ns0.h',11,11,'ClassDecl',0,0,1),
('c:@N@NS0@C@C1@F@C1#I#','C1',cur_dir+'/subdir/ns0.h',13,9,'CXXConstructor',0,0,1),
('c:ns0.h@228@N@NS0@C@C1@F@C1#I#@a','a',cur_dir+'/subdir/ns0.h',13,16,'ParmDecl',0,0,1),
('c:@N@NS0@C@C1@FI@m_val','m_val',cur_dir+'/subdir/ns0.h',13,21,'MemberRef',cur_dir+'/subdir/ns0.h',17,13),
('c:ns0.h@228@N@NS0@C@C1@F@C1#I#@a','a',cur_dir+'/subdir/ns0.h',13,27,'DeclRefExpr',cur_dir+'/subdir/ns0.h',13,16),
('c:ns0.h@39@N@NS0@T@MYINT','MYINT',cur_dir+'/subdir/ns0.h',14,9,'TypeRef',cur_dir+'/subdir/ns0.h',3,17),
('c:@N@NS0@C@C1@F@check#1','check',cur_dir+'/subdir/ns0.h',14,15,'CXXMethod',0,0,0),
('c:@N@NS0@C@C1','C1',cur_dir+'/subdir/ns0.h',15,9,'TypeRef',cur_dir+'/subdir/ns0.h',11,11),
('c:@N@NS0@C@C1@F@check2#','check2',cur_dir+'/subdir/ns0.h',15,12,'CXXMethod',0,0,0),
('c:@N@NS0@C@C1@FI@m_val','m_val',cur_dir+'/subdir/ns0.h',17,13,'FieldDecl',0,0,1),
# ns1.h
('c:@N@NS1','NS1',cur_dir+'/ns1.h',2,11,'Namespace',0,0,1),
('c:@N@NS1@C@C0','C0',cur_dir+'/ns1.h',3,11,'ClassDecl',0,0,1),
('c:@N@NS1@C@C0@F@C0#I#','C0',cur_dir+'/ns1.h',5,9,'CXXConstructor',0,0,1),
('c:ns1.h@77@N@NS1@C@C0@F@C0#I#@a','a',cur_dir+'/ns1.h',5,16,'ParmDecl',0,0,1),
('c:@N@NS1@C@C0@FI@m_val','m_val',cur_dir+'/ns1.h',5,21,'MemberRef',cur_dir+'/ns1.h',8,13),
('c:ns1.h@77@N@NS1@C@C0@F@C0#I#@a','a',cur_dir+'/ns1.h',5,27,'DeclRefExpr',cur_dir+'/ns1.h',5,16),
('c:@N@NS1@C@C0@F@check#','check',cur_dir+'/ns1.h',6,14,'CXXMethod',0,0,0),
('c:@N@NS1@C@C0@FI@m_val','m_val',cur_dir+'/ns1.h',8,13,'FieldDecl',0,0,1),
('c:@N@NS1@C@C1','C1',cur_dir+'/ns1.h',10,11,'ClassDecl',0,0,1),
('c:@N@NS1@C@C1@F@C1#I#','C1',cur_dir+'/ns1.h',12,9,'CXXConstructor',0,0,1),
('c:ns1.h@205@N@NS1@C@C1@F@C1#I#@a','a',cur_dir+'/ns1.h',12,16,'ParmDecl',0,0,1),
('c:@N@NS1@C@C1@FI@m_val','m_val',cur_dir+'/ns1.h',12,21,'MemberRef',cur_dir+'/ns1.h',15,13),
('c:ns1.h@205@N@NS1@C@C1@F@C1#I#@a','a',cur_dir+'/ns1.h',12,27,'DeclRefExpr',cur_dir+'/ns1.h',12,16),
('c:@N@NS1@C@C1@F@check#','check',cur_dir+'/ns1.h',13,14,'CXXMethod',0,0,0),
('c:@N@NS1@C@C1@FI@m_val','m_val',cur_dir+'/ns1.h',15,13,'FieldDecl',0,0,1),
]

a_list_sys = [
('c:@N@std','std','%s/main.cpp'%(cur_dir),9,5,'NamespaceRef','/usr/include/c++/4.2.1/bits/vector.tcc',64,1),
('c:@N@std@CT>2#T#T@vector','vector','%s/main.cpp'%(cur_dir),9,10,'TEMPLATE_REF','/usr/include/c++/4.2.1/bits/stl_vector.h',162,11),
('c:@N@std@C@vector>#I#$@N@std@C@allocator>#I@F@push_back#&1I#','push_back','%s/main.cpp'%(cur_dir),10,9,'MemberRefExpr','/usr/include/c++/4.2.1/bits/stl_vector.h',600,7),
('c:@N@std@C@vector>#I#$@N@std@C@allocator>#I@F@push_back#&1I#','push_back','%s/main.cpp'%(cur_dir),11,9,'MemberRefExpr','/usr/include/c++/4.2.1/bits/stl_vector.h',600,7),
('c:@N@std@C@vector>#I#$@N@std@C@allocator>#I@F@push_back#&1I#','push_back','%s/main.cpp'%(cur_dir),12,9,'MemberRefExpr','/usr/include/c++/4.2.1/bits/stl_vector.h',600,7),
('c:main.cpp@220@F@main@c00','c00','%s/main.cpp'%(cur_dir),13,13,'VarDecl',1),
]

db = sqlite3.connect(sys.argv[1])

i = 0
for q in q_list:
    test_one(q, a_list[i])
    i+=1
"""
i = 0
for q in q_list_sys:
    test_one(q, a_list_sys[i])
    i+=1
"""
if err == 0:
    print "OK"
else:
    print "ERR: %d"%(err)
exit(err)
