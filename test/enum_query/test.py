#!/usr/bin/python

import sys
import os
import sqlite3
import commands
sys.path.append("../../src/")
import cxxtags_util as cxxtags
sys.path.append("../util/")
import clang.cindex # for kind types
import common as test_util

#test_util.DebugOn()

err = 0

if len(sys.argv) != 2:
    print "usage: cmd db_file"
    exit(1)

db_dir = sys.argv[1]

cur_dir = os.getcwd()
cur_dir = os.path.abspath(cur_dir + "/../enum")

test_data_list_decl = [
('c:main.cpp@20@Ea@VAL0_0','VAL0_0',cur_dir+'/main.cpp',4,5,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,0,1,-1),
('c:main.cpp@20@Ea@VAL0_1','VAL0_1',cur_dir+'/main.cpp',5,5,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,1,1,-1),
('c:main.cpp@20@Ea@VAL0_2','VAL0_2',cur_dir+'/main.cpp',6,5,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,2,1,-1),
('c:main.cpp@20@Ea@VAL0_3','VAL0_3',cur_dir+'/main.cpp',7,5,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,3,1,-1),
('c:main.cpp@79@Ea@VAL1_0','VAL1_0',cur_dir+'/main.cpp',11,5,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,0,1,-1),
('c:main.cpp@79@Ea@VAL1_1','VAL1_1',cur_dir+'/main.cpp',12,5,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,1,1,-1),
('c:main.cpp@79@Ea@VAL1_2','VAL1_2',cur_dir+'/main.cpp',13,5,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,2,1,-1),
('c:main.cpp@79@Ea@VAL1_3','VAL1_3',cur_dir+'/main.cpp',14,5,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,3,1,-1),
('c:main.cpp@138@F@check#','check',cur_dir+'/main.cpp',17,13,clang.cindex.CursorKind.FUNCTION_DECL.value,0,1,-1),
('c:@N@NS0','NS0',cur_dir+'/main.cpp',22,11,clang.cindex.CursorKind.NAMESPACE.value,0,1,-1),
('c:main.cpp@250@N@NS0@Ea@VAL0_0','VAL0_0',cur_dir+'/main.cpp',24,9,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,10,1,-1),
('c:main.cpp@250@N@NS0@Ea@VAL0_1','VAL0_1',cur_dir+'/main.cpp',25,9,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,11,1,-1),
('c:main.cpp@250@N@NS0@Ea@VAL0_2','VAL0_2',cur_dir+'/main.cpp',26,9,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,12,1,-1),
('c:main.cpp@250@N@NS0@Ea@VAL0_3','VAL0_3',cur_dir+'/main.cpp',27,9,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,13,1,-1),
('c:main.cpp@335@N@NS0@F@check#','check',cur_dir+'/main.cpp',29,17,clang.cindex.CursorKind.FUNCTION_DECL.value,0,1,-1),
('c:@N@NS0@C@C0','C0',cur_dir+'/main.cpp',33,11,clang.cindex.CursorKind.CLASS_DECL.value,0,1,-1),
('c:main.cpp@480@N@NS0@C@C0@Ea@VAL0_0','VAL0_0',cur_dir+'/main.cpp',36,13,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,20,1,-1),
('c:main.cpp@480@N@NS0@C@C0@Ea@VAL0_1','VAL0_1',cur_dir+'/main.cpp',37,13,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,21,1,-1),
('c:main.cpp@480@N@NS0@C@C0@Ea@VAL0_2','VAL0_2',cur_dir+'/main.cpp',38,13,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,22,1,-1),
('c:main.cpp@480@N@NS0@C@C0@Ea@VAL0_3','VAL0_3',cur_dir+'/main.cpp',39,13,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,23,1,-1),
('c:@N@NS0@C@C0@F@check#','check',cur_dir+'/main.cpp',41,14,clang.cindex.CursorKind.CXX_METHOD.value,0,1,-1),
('c:@N@NS0@C@C1','C1',cur_dir+'/main.cpp',46,11,clang.cindex.CursorKind.CLASS_DECL.value,0,1,-1),
('c:main.cpp@768@N@NS0@C@C1@Ea@VAL0_0','VAL0_0',cur_dir+'/main.cpp',50,13,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,30,1,-1),
('c:main.cpp@768@N@NS0@C@C1@Ea@VAL0_1','VAL0_1',cur_dir+'/main.cpp',51,13,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,31,1,-1),
('c:main.cpp@768@N@NS0@C@C1@Ea@VAL0_2','VAL0_2',cur_dir+'/main.cpp',52,13,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,32,1,-1),
('c:main.cpp@768@N@NS0@C@C1@Ea@VAL0_3','VAL0_3',cur_dir+'/main.cpp',53,13,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,33,1,-1),
('c:@N@NS0@C@C1@F@check#','check',cur_dir+'/main.cpp',55,14,clang.cindex.CursorKind.CXX_METHOD.value,0,1,-1),
('c:@N@NS1','NS1',cur_dir+'/main.cpp',62,11,clang.cindex.CursorKind.NAMESPACE.value,0,1,-1),
('c:main.cpp@1025@N@NS1@Ea@VAL0_0','VAL0_0',cur_dir+'/main.cpp',64,9,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,40,1,-1),
('c:main.cpp@1025@N@NS1@Ea@VAL0_1','VAL0_1',cur_dir+'/main.cpp',65,9,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,41,1,-1),
('c:main.cpp@1025@N@NS1@Ea@VAL0_2','VAL0_2',cur_dir+'/main.cpp',66,9,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,42,1,-1),
('c:main.cpp@1025@N@NS1@Ea@VAL0_3','VAL0_3',cur_dir+'/main.cpp',67,9,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,43,1,-1),
('c:main.cpp@1112@N@NS1@F@check#','check',cur_dir+'/main.cpp',69,17,clang.cindex.CursorKind.FUNCTION_DECL.value,0,1,-1),
('c:@N@NS1@C@C0','C0',cur_dir+'/main.cpp',73,11,clang.cindex.CursorKind.CLASS_DECL.value,0,1,-1),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_0','VAL0_0',cur_dir+'/main.cpp',76,13,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,50,1,-1),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_1','VAL0_1',cur_dir+'/main.cpp',77,13,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,51,1,-1),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_2','VAL0_2',cur_dir+'/main.cpp',78,13,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,52,1,-1),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_3','VAL0_3',cur_dir+'/main.cpp',79,13,clang.cindex.CursorKind.ENUM_CONSTANT_DECL.value,53,1,-1),
('c:@N@NS1@C@C0@F@check#','check',cur_dir+'/main.cpp',81,14,clang.cindex.CursorKind.CXX_METHOD.value,0,1,-1),
('c:@N@NS1@C@C1','C1',cur_dir+'/main.cpp',86,11,clang.cindex.CursorKind.CLASS_DECL.value,0,1,-1),
('c:@N@NS1@C@C1@F@check#','check',cur_dir+'/main.cpp',89,14,clang.cindex.CursorKind.CXX_METHOD.value,0,1,-1),
('c:@F@main','main',cur_dir+'/main.cpp',96,5,clang.cindex.CursorKind.FUNCTION_DECL.value,0,1,-1),
('c:main.cpp@1688@F@main@c00','c00',cur_dir+'/main.cpp',98,13,clang.cindex.CursorKind.VAR_DECL.value,0,1,-1),
('c:main.cpp@1705@F@main@c01','c01',cur_dir+'/main.cpp',99,13,clang.cindex.CursorKind.VAR_DECL.value,0,1,-1),
('c:main.cpp@1722@F@main@c10','c10',cur_dir+'/main.cpp',100,13,clang.cindex.CursorKind.VAR_DECL.value,0,1,-1),
('c:main.cpp@1739@F@main@c11','c11',cur_dir+'/main.cpp',101,13,clang.cindex.CursorKind.VAR_DECL.value,0,1,-1),
]

test_data_list_ref = [
('c:main.cpp@20@Ea@VAL0_0','VAL0_0',cur_dir+'/main.cpp',19,35,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',4,5),
('c:main.cpp@20@Ea@VAL0_1','VAL0_1',cur_dir+'/main.cpp',19,43,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',5,5),
('c:main.cpp@20@Ea@VAL0_2','VAL0_2',cur_dir+'/main.cpp',19,51,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',6,5),
('c:main.cpp@20@Ea@VAL0_3','VAL0_3',cur_dir+'/main.cpp',19,59,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',7,5),
('c:main.cpp@250@N@NS0@Ea@VAL0_0','VAL0_0',cur_dir+'/main.cpp',31,42,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',24,9),
('c:main.cpp@250@N@NS0@Ea@VAL0_1','VAL0_1',cur_dir+'/main.cpp',31,50,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',25,9),
('c:main.cpp@250@N@NS0@Ea@VAL0_2','VAL0_2',cur_dir+'/main.cpp',31,58,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',26,9),
('c:main.cpp@250@N@NS0@Ea@VAL0_3','VAL0_3',cur_dir+'/main.cpp',31,66,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',27,9),
('c:main.cpp@480@N@NS0@C@C0@Ea@VAL0_0','VAL0_0',cur_dir+'/main.cpp',43,50,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',36,13),
('c:main.cpp@480@N@NS0@C@C0@Ea@VAL0_1','VAL0_1',cur_dir+'/main.cpp',43,58,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',37,13),
('c:main.cpp@480@N@NS0@C@C0@Ea@VAL0_2','VAL0_2',cur_dir+'/main.cpp',43,66,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',38,13),
('c:main.cpp@480@N@NS0@C@C0@Ea@VAL0_3','VAL0_3',cur_dir+'/main.cpp',43,74,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',39,13),
('c:@N@NS0@C@C0','C0',cur_dir+'/main.cpp',46,23,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/main.cpp',33,11),
('c:main.cpp@768@N@NS0@C@C1@Ea@VAL0_0','VAL0_0',cur_dir+'/main.cpp',57,50,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',50,13),
('c:main.cpp@768@N@NS0@C@C1@Ea@VAL0_1','VAL0_1',cur_dir+'/main.cpp',57,58,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',51,13),
('c:main.cpp@768@N@NS0@C@C1@Ea@VAL0_2','VAL0_2',cur_dir+'/main.cpp',57,66,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',52,13),
('c:main.cpp@768@N@NS0@C@C1@Ea@VAL0_3','VAL0_3',cur_dir+'/main.cpp',57,74,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',53,13),
('c:main.cpp@1025@N@NS1@Ea@VAL0_0','VAL0_0',cur_dir+'/main.cpp',71,42,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',64,9),
('c:main.cpp@1025@N@NS1@Ea@VAL0_1','VAL0_1',cur_dir+'/main.cpp',71,50,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',65,9),
('c:main.cpp@1025@N@NS1@Ea@VAL0_2','VAL0_2',cur_dir+'/main.cpp',71,58,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',66,9),
('c:main.cpp@1025@N@NS1@Ea@VAL0_3','VAL0_3',cur_dir+'/main.cpp',71,66,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',67,9),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_0','VAL0_0',cur_dir+'/main.cpp',83,50,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',76,13),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_1','VAL0_1',cur_dir+'/main.cpp',83,58,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',77,13),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_2','VAL0_2',cur_dir+'/main.cpp',83,66,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',78,13),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_3','VAL0_3',cur_dir+'/main.cpp',83,74,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',79,13),
('c:@N@NS1@C@C0','C0',cur_dir+'/main.cpp',86,23,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/main.cpp',73,11),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_0','VAL0_0',cur_dir+'/main.cpp',91,50,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',76,13),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_1','VAL0_1',cur_dir+'/main.cpp',91,58,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',77,13),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_2','VAL0_2',cur_dir+'/main.cpp',91,66,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',78,13),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_3','VAL0_3',cur_dir+'/main.cpp',91,74,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',79,13),
('c:@N@NS0','NS0',cur_dir+'/main.cpp',98,5,clang.cindex.CursorKind.NAMESPACE_REF.value,cur_dir+'/main.cpp',22,11),
('c:@N@NS0@C@C0','C0',cur_dir+'/main.cpp',98,10,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/main.cpp',33,11),
('c:@N@NS0','NS0',cur_dir+'/main.cpp',99,5,clang.cindex.CursorKind.NAMESPACE_REF.value,cur_dir+'/main.cpp',22,11),
('c:@N@NS0@C@C1','C1',cur_dir+'/main.cpp',99,10,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/main.cpp',46,11),
('c:@N@NS1','NS1',cur_dir+'/main.cpp',100,5,clang.cindex.CursorKind.NAMESPACE_REF.value,cur_dir+'/main.cpp',62,11),
('c:@N@NS1@C@C0','C0',cur_dir+'/main.cpp',100,10,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/main.cpp',73,11),
('c:@N@NS1','NS1',cur_dir+'/main.cpp',101,5,clang.cindex.CursorKind.NAMESPACE_REF.value,cur_dir+'/main.cpp',62,11),
('c:@N@NS1@C@C1','C1',cur_dir+'/main.cpp',101,10,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/main.cpp',86,11),
('c:main.cpp@138@F@check#','check',cur_dir+'/main.cpp',102,7,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',17,13),
('c:@N@NS0','NS0',cur_dir+'/main.cpp',103,5,clang.cindex.CursorKind.NAMESPACE_REF.value,cur_dir+'/main.cpp',22,11),
('c:main.cpp@335@N@NS0@F@check#','check',cur_dir+'/main.cpp',103,10,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',29,17),
('c:@N@NS1','NS1',cur_dir+'/main.cpp',104,5,clang.cindex.CursorKind.NAMESPACE_REF.value,cur_dir+'/main.cpp',62,11),
('c:main.cpp@1112@N@NS1@F@check#','check',cur_dir+'/main.cpp',104,10,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',69,17),
('c:main.cpp@1688@F@main@c00','c00',cur_dir+'/main.cpp',105,5,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',98,13),
('c:@N@NS0@C@C0@F@check#','check',cur_dir+'/main.cpp',105,9,clang.cindex.CursorKind.MEMBER_REF_EXPR.value,cur_dir+'/main.cpp',41,14),
('c:main.cpp@1705@F@main@c01','c01',cur_dir+'/main.cpp',106,5,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',99,13),
('c:@N@NS0@C@C1@F@check#','check',cur_dir+'/main.cpp',106,9,clang.cindex.CursorKind.MEMBER_REF_EXPR.value,cur_dir+'/main.cpp',55,14),
('c:main.cpp@1722@F@main@c10','c10',cur_dir+'/main.cpp',107,5,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',100,13),
('c:@N@NS1@C@C0@F@check#','check',cur_dir+'/main.cpp',107,9,clang.cindex.CursorKind.MEMBER_REF_EXPR.value,cur_dir+'/main.cpp',81,14),
('c:main.cpp@1739@F@main@c11','c11',cur_dir+'/main.cpp',108,5,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/main.cpp',101,13),
('c:@N@NS1@C@C1@F@check#','check',cur_dir+'/main.cpp',108,9,clang.cindex.CursorKind.MEMBER_REF_EXPR.value,cur_dir+'/main.cpp',89,14),
]

err += test_util.DoDeclTest(test_data_list_decl, test_data_list_ref)
err += test_util.DoRefTest(test_data_list_ref, test_data_list_decl)

if err == 0:
    print "OK"
else:
    print "ERR: %d"%(err)
sys.exit(err)
