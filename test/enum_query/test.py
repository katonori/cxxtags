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
('c:main.cpp@20@Ea@VAL0_0','VAL0_0',cur_dir+'/main.cpp',4,5,0,1,-1),
('c:main.cpp@20@Ea@VAL0_1','VAL0_1',cur_dir+'/main.cpp',5,5,1,1,-1),
('c:main.cpp@20@Ea@VAL0_2','VAL0_2',cur_dir+'/main.cpp',6,5,2,1,-1),
('c:main.cpp@20@Ea@VAL0_3','VAL0_3',cur_dir+'/main.cpp',7,5,3,1,-1),
('c:main.cpp@79@Ea@VAL1_0','VAL1_0',cur_dir+'/main.cpp',11,5,0,1,-1),
('c:main.cpp@79@Ea@VAL1_1','VAL1_1',cur_dir+'/main.cpp',12,5,1,1,-1),
('c:main.cpp@79@Ea@VAL1_2','VAL1_2',cur_dir+'/main.cpp',13,5,2,1,-1),
('c:main.cpp@79@Ea@VAL1_3','VAL1_3',cur_dir+'/main.cpp',14,5,3,1,-1),
('c:main.cpp@138@F@check#','check',cur_dir+'/main.cpp',17,13,0,1,-1),
('c:@N@NS0','NS0',cur_dir+'/main.cpp',22,11,0,1,-1),
('c:main.cpp@250@N@NS0@Ea@VAL0_0','VAL0_0',cur_dir+'/main.cpp',24,9,10,1,-1),
('c:main.cpp@250@N@NS0@Ea@VAL0_1','VAL0_1',cur_dir+'/main.cpp',25,9,11,1,-1),
('c:main.cpp@250@N@NS0@Ea@VAL0_2','VAL0_2',cur_dir+'/main.cpp',26,9,12,1,-1),
('c:main.cpp@250@N@NS0@Ea@VAL0_3','VAL0_3',cur_dir+'/main.cpp',27,9,13,1,-1),
('c:main.cpp@335@N@NS0@F@check#','check',cur_dir+'/main.cpp',29,17,0,1,-1),
('c:@N@NS0@C@C0','C0',cur_dir+'/main.cpp',33,11,0,1,-1),
('c:main.cpp@480@N@NS0@C@C0@Ea@VAL0_0','VAL0_0',cur_dir+'/main.cpp',36,13,20,1,-1),
('c:main.cpp@480@N@NS0@C@C0@Ea@VAL0_1','VAL0_1',cur_dir+'/main.cpp',37,13,21,1,-1),
('c:main.cpp@480@N@NS0@C@C0@Ea@VAL0_2','VAL0_2',cur_dir+'/main.cpp',38,13,22,1,-1),
('c:main.cpp@480@N@NS0@C@C0@Ea@VAL0_3','VAL0_3',cur_dir+'/main.cpp',39,13,23,1,-1),
('c:@N@NS0@C@C0@F@check#','check',cur_dir+'/main.cpp',41,14,0,1,-1),
('c:@N@NS0@C@C1','C1',cur_dir+'/main.cpp',46,11,0,1,-1),
('c:main.cpp@768@N@NS0@C@C1@Ea@VAL0_0','VAL0_0',cur_dir+'/main.cpp',50,13,30,1,-1),
('c:main.cpp@768@N@NS0@C@C1@Ea@VAL0_1','VAL0_1',cur_dir+'/main.cpp',51,13,31,1,-1),
('c:main.cpp@768@N@NS0@C@C1@Ea@VAL0_2','VAL0_2',cur_dir+'/main.cpp',52,13,32,1,-1),
('c:main.cpp@768@N@NS0@C@C1@Ea@VAL0_3','VAL0_3',cur_dir+'/main.cpp',53,13,33,1,-1),
('c:@N@NS0@C@C1@F@check#','check',cur_dir+'/main.cpp',55,14,0,1,-1),
('c:@N@NS1','NS1',cur_dir+'/main.cpp',62,11,0,1,-1),
('c:main.cpp@1025@N@NS1@Ea@VAL0_0','VAL0_0',cur_dir+'/main.cpp',64,9,40,1,-1),
('c:main.cpp@1025@N@NS1@Ea@VAL0_1','VAL0_1',cur_dir+'/main.cpp',65,9,41,1,-1),
('c:main.cpp@1025@N@NS1@Ea@VAL0_2','VAL0_2',cur_dir+'/main.cpp',66,9,42,1,-1),
('c:main.cpp@1025@N@NS1@Ea@VAL0_3','VAL0_3',cur_dir+'/main.cpp',67,9,43,1,-1),
('c:main.cpp@1112@N@NS1@F@check#','check',cur_dir+'/main.cpp',69,17,0,1,-1),
('c:@N@NS1@C@C0','C0',cur_dir+'/main.cpp',73,11,0,1,-1),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_0','VAL0_0',cur_dir+'/main.cpp',76,13,50,1,-1),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_1','VAL0_1',cur_dir+'/main.cpp',77,13,51,1,-1),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_2','VAL0_2',cur_dir+'/main.cpp',78,13,52,1,-1),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_3','VAL0_3',cur_dir+'/main.cpp',79,13,53,1,-1),
('c:@N@NS1@C@C0@F@check#','check',cur_dir+'/main.cpp',81,14,0,1,-1),
('c:@N@NS1@C@C1','C1',cur_dir+'/main.cpp',86,11,0,1,-1),
('c:@N@NS1@C@C1@F@check#','check',cur_dir+'/main.cpp',89,14,0,1,-1),
('c:@F@main','main',cur_dir+'/main.cpp',96,5,0,1,-1),
('c:main.cpp@1688@F@main@c00','c00',cur_dir+'/main.cpp',98,13,0,1,-1),
('c:main.cpp@1705@F@main@c01','c01',cur_dir+'/main.cpp',99,13,0,1,-1),
('c:main.cpp@1722@F@main@c10','c10',cur_dir+'/main.cpp',100,13,0,1,-1),
('c:main.cpp@1739@F@main@c11','c11',cur_dir+'/main.cpp',101,13,0,1,-1),
]

test_data_list_ref = [
('c:main.cpp@20@Ea@VAL0_0','VAL0_0',cur_dir+'/main.cpp',19,35,cur_dir+'/main.cpp',4,5),
('c:main.cpp@20@Ea@VAL0_1','VAL0_1',cur_dir+'/main.cpp',19,43,cur_dir+'/main.cpp',5,5),
('c:main.cpp@20@Ea@VAL0_2','VAL0_2',cur_dir+'/main.cpp',19,51,cur_dir+'/main.cpp',6,5),
('c:main.cpp@20@Ea@VAL0_3','VAL0_3',cur_dir+'/main.cpp',19,59,cur_dir+'/main.cpp',7,5),
('c:main.cpp@250@N@NS0@Ea@VAL0_0','VAL0_0',cur_dir+'/main.cpp',31,42,cur_dir+'/main.cpp',24,9),
('c:main.cpp@250@N@NS0@Ea@VAL0_1','VAL0_1',cur_dir+'/main.cpp',31,50,cur_dir+'/main.cpp',25,9),
('c:main.cpp@250@N@NS0@Ea@VAL0_2','VAL0_2',cur_dir+'/main.cpp',31,58,cur_dir+'/main.cpp',26,9),
('c:main.cpp@250@N@NS0@Ea@VAL0_3','VAL0_3',cur_dir+'/main.cpp',31,66,cur_dir+'/main.cpp',27,9),
('c:main.cpp@480@N@NS0@C@C0@Ea@VAL0_0','VAL0_0',cur_dir+'/main.cpp',43,50,cur_dir+'/main.cpp',36,13),
('c:main.cpp@480@N@NS0@C@C0@Ea@VAL0_1','VAL0_1',cur_dir+'/main.cpp',43,58,cur_dir+'/main.cpp',37,13),
('c:main.cpp@480@N@NS0@C@C0@Ea@VAL0_2','VAL0_2',cur_dir+'/main.cpp',43,66,cur_dir+'/main.cpp',38,13),
('c:main.cpp@480@N@NS0@C@C0@Ea@VAL0_3','VAL0_3',cur_dir+'/main.cpp',43,74,cur_dir+'/main.cpp',39,13),
('c:@N@NS0@C@C0','C0',cur_dir+'/main.cpp',46,23,cur_dir+'/main.cpp',33,11),
('c:main.cpp@768@N@NS0@C@C1@Ea@VAL0_0','VAL0_0',cur_dir+'/main.cpp',57,50,cur_dir+'/main.cpp',50,13),
('c:main.cpp@768@N@NS0@C@C1@Ea@VAL0_1','VAL0_1',cur_dir+'/main.cpp',57,58,cur_dir+'/main.cpp',51,13),
('c:main.cpp@768@N@NS0@C@C1@Ea@VAL0_2','VAL0_2',cur_dir+'/main.cpp',57,66,cur_dir+'/main.cpp',52,13),
('c:main.cpp@768@N@NS0@C@C1@Ea@VAL0_3','VAL0_3',cur_dir+'/main.cpp',57,74,cur_dir+'/main.cpp',53,13),
('c:main.cpp@1025@N@NS1@Ea@VAL0_0','VAL0_0',cur_dir+'/main.cpp',71,42,cur_dir+'/main.cpp',64,9),
('c:main.cpp@1025@N@NS1@Ea@VAL0_1','VAL0_1',cur_dir+'/main.cpp',71,50,cur_dir+'/main.cpp',65,9),
('c:main.cpp@1025@N@NS1@Ea@VAL0_2','VAL0_2',cur_dir+'/main.cpp',71,58,cur_dir+'/main.cpp',66,9),
('c:main.cpp@1025@N@NS1@Ea@VAL0_3','VAL0_3',cur_dir+'/main.cpp',71,66,cur_dir+'/main.cpp',67,9),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_0','VAL0_0',cur_dir+'/main.cpp',83,50,cur_dir+'/main.cpp',76,13),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_1','VAL0_1',cur_dir+'/main.cpp',83,58,cur_dir+'/main.cpp',77,13),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_2','VAL0_2',cur_dir+'/main.cpp',83,66,cur_dir+'/main.cpp',78,13),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_3','VAL0_3',cur_dir+'/main.cpp',83,74,cur_dir+'/main.cpp',79,13),
('c:@N@NS1@C@C0','C0',cur_dir+'/main.cpp',86,23,cur_dir+'/main.cpp',73,11),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_0','VAL0_0',cur_dir+'/main.cpp',91,50,cur_dir+'/main.cpp',76,13),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_1','VAL0_1',cur_dir+'/main.cpp',91,58,cur_dir+'/main.cpp',77,13),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_2','VAL0_2',cur_dir+'/main.cpp',91,66,cur_dir+'/main.cpp',78,13),
('c:main.cpp@1257@N@NS1@C@C0@Ea@VAL0_3','VAL0_3',cur_dir+'/main.cpp',91,74,cur_dir+'/main.cpp',79,13),
('c:@N@NS0','NS0',cur_dir+'/main.cpp',98,5,cur_dir+'/main.cpp',22,11),
('c:@N@NS0@C@C0','C0',cur_dir+'/main.cpp',98,10,cur_dir+'/main.cpp',33,11),
('c:@N@NS0','NS0',cur_dir+'/main.cpp',99,5,cur_dir+'/main.cpp',22,11),
('c:@N@NS0@C@C1','C1',cur_dir+'/main.cpp',99,10,cur_dir+'/main.cpp',46,11),
('c:@N@NS1','NS1',cur_dir+'/main.cpp',100,5,cur_dir+'/main.cpp',62,11),
('c:@N@NS1@C@C0','C0',cur_dir+'/main.cpp',100,10,cur_dir+'/main.cpp',73,11),
('c:@N@NS1','NS1',cur_dir+'/main.cpp',101,5,cur_dir+'/main.cpp',62,11),
('c:@N@NS1@C@C1','C1',cur_dir+'/main.cpp',101,10,cur_dir+'/main.cpp',86,11),
('c:main.cpp@138@F@check#','check',cur_dir+'/main.cpp',102,7,cur_dir+'/main.cpp',17,13),
('c:@N@NS0','NS0',cur_dir+'/main.cpp',103,5,cur_dir+'/main.cpp',22,11),
('c:main.cpp@335@N@NS0@F@check#','check',cur_dir+'/main.cpp',103,10,cur_dir+'/main.cpp',29,17),
('c:@N@NS1','NS1',cur_dir+'/main.cpp',104,5,cur_dir+'/main.cpp',62,11),
('c:main.cpp@1112@N@NS1@F@check#','check',cur_dir+'/main.cpp',104,10,cur_dir+'/main.cpp',69,17),
('c:main.cpp@1688@F@main@c00','c00',cur_dir+'/main.cpp',105,5,cur_dir+'/main.cpp',98,13),
('c:@N@NS0@C@C0@F@check#','check',cur_dir+'/main.cpp',105,9,cur_dir+'/main.cpp',41,14),
('c:main.cpp@1705@F@main@c01','c01',cur_dir+'/main.cpp',106,5,cur_dir+'/main.cpp',99,13),
('c:@N@NS0@C@C1@F@check#','check',cur_dir+'/main.cpp',106,9,cur_dir+'/main.cpp',55,14),
('c:main.cpp@1722@F@main@c10','c10',cur_dir+'/main.cpp',107,5,cur_dir+'/main.cpp',100,13),
('c:@N@NS1@C@C0@F@check#','check',cur_dir+'/main.cpp',107,9,cur_dir+'/main.cpp',81,14),
('c:main.cpp@1739@F@main@c11','c11',cur_dir+'/main.cpp',108,5,cur_dir+'/main.cpp',101,13),
('c:@N@NS1@C@C1@F@check#','check',cur_dir+'/main.cpp',108,9,cur_dir+'/main.cpp',89,14),
]

err += test_util.DoDeclTest(test_data_list_decl, test_data_list_ref)
err += test_util.DoRefTest(test_data_list_ref, test_data_list_decl)

if err == 0:
    print "OK"
else:
    print "ERR: %d"%(err)
sys.exit(err)
