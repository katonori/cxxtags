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

err = 0
#test_util.DebugOn()

if len(sys.argv) != 2:
    print "usage: cmd db_file"
    exit(1)

db_dir = sys.argv[1]

cur_dir = os.getcwd()
cur_dir = os.path.abspath(cur_dir + "/../inheritance")

test_data_list_ref = [
('c:@C@CParent0','CParent0',cur_dir+'/inhe.cpp',11,6,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/inhe.cpp',3,7),
('c:@C@CParent1','CParent1',cur_dir+'/inhe.cpp',23,6,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/inhe.cpp',15,7),
('c:@C@CParent0','CParent0',cur_dir+'/inhe.cpp',28,10,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/inhe.cpp',3,7),
('c:@C@CChild','CChild',cur_dir+'/inhe.cpp',36,6,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/inhe.cpp',27,7),
('c:@C@CChild','CChild',cur_dir+'/inhe.cpp',41,10,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/inhe.cpp',27,7),
('c:@C@CGChild','CGChild',cur_dir+'/inhe.cpp',49,6,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/inhe.cpp',40,7),
('c:@C@CParent0','CParent0',cur_dir+'/inhe.cpp',54,10,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/inhe.cpp',3,7),
('c:@C@CParent1','CParent1',cur_dir+'/inhe.cpp',54,27,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/inhe.cpp',15,7),
('c:@C@COther','COther',cur_dir+'/inhe.cpp',62,6,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/inhe.cpp',53,7),
('c:@C@CParent0','CParent0',cur_dir+'/inhe.cpp',66,24,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/inhe.cpp',3,7),
('c:inhe.cpp@886@F@test#*$@C@CParent0#@a','a',cur_dir+'/inhe.cpp',68,5,clang.cindex.CursorKind.DECL_REF_EXPR.value,cur_dir+'/inhe.cpp',66,34),
('c:@C@CParent0@F@response#','response',cur_dir+'/inhe.cpp',68,8,clang.cindex.CursorKind.MEMBER_REF_EXPR.value,cur_dir+'/inhe.cpp',11,16),
('c:@C@CParent0','CParent0',cur_dir+'/inhe.cpp',73,5,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/inhe.cpp',3,7),
('c:@C@CChild','CChild',cur_dir+'/inhe.cpp',74,5,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/inhe.cpp',27,7),
('c:@C@CGChild','CGChild',cur_dir+'/inhe.cpp',75,5,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/inhe.cpp',40,7),
('c:@C@COther','COther',cur_dir+'/inhe.cpp',76,5,clang.cindex.CursorKind.TYPE_REF.value,cur_dir+'/inhe.cpp',53,7),
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
]

test_data_list_decl = [
('c:@C@CParent0','CParent0',cur_dir+'/inhe.cpp',3,7,clang.cindex.CursorKind.CLASS_DECL.value,0,0,1),
('c:@C@CParent0@F@CParent0#','CParent0',cur_dir+'/inhe.cpp',6,5,clang.cindex.CursorKind.CONSTRUCTOR.value,0,0,1),
('c:@C@CParent0@F@~CParent0#','~CParent0',cur_dir+'/inhe.cpp',7,5,clang.cindex.CursorKind.DESTRUCTOR.value,0,0,1),
('c:@C@CParent0@F@response#','response',cur_dir+'/inhe.cpp',8,18,clang.cindex.CursorKind.CXX_METHOD.value,0,1,0),
('c:@C@CParent0@F@response#','response',cur_dir+'/inhe.cpp',11,16,clang.cindex.CursorKind.CXX_METHOD.value,0,1,1),
('c:@C@CParent1','CParent1',cur_dir+'/inhe.cpp',15,7,clang.cindex.CursorKind.CLASS_DECL.value,0,0,1),
('c:@C@CParent1@F@CParent1#','CParent1',cur_dir+'/inhe.cpp',18,5,clang.cindex.CursorKind.CONSTRUCTOR.value,0,0,1),
('c:@C@CParent1@F@~CParent1#','~CParent1',cur_dir+'/inhe.cpp',19,5,clang.cindex.CursorKind.DESTRUCTOR.value,0,0,1),
('c:@C@CParent1@F@response#','response',cur_dir+'/inhe.cpp',20,18,clang.cindex.CursorKind.CXX_METHOD.value,0,1,0),
('c:@C@CParent1@F@response#','response',cur_dir+'/inhe.cpp',23,16,clang.cindex.CursorKind.CXX_METHOD.value,0,1,1),
('c:@C@CChild','CChild',cur_dir+'/inhe.cpp',27,7,clang.cindex.CursorKind.CLASS_DECL.value,0,0,1),
('c:@C@CChild@F@CChild#','CChild',cur_dir+'/inhe.cpp',31,5,clang.cindex.CursorKind.CONSTRUCTOR.value,0,0,1),
('c:@C@CChild@F@~CChild#','~CChild',cur_dir+'/inhe.cpp',32,5,clang.cindex.CursorKind.DESTRUCTOR.value,0,0,1),
('c:@C@CChild@F@response#','response',cur_dir+'/inhe.cpp',33,18,clang.cindex.CursorKind.CXX_METHOD.value,0,1,0),
('c:@C@CChild@F@response#','response',cur_dir+'/inhe.cpp',36,14,clang.cindex.CursorKind.CXX_METHOD.value,0,1,1),
('c:@C@CGChild','CGChild',cur_dir+'/inhe.cpp',40,7,clang.cindex.CursorKind.CLASS_DECL.value,0,0,1),
('c:@C@CGChild@F@CGChild#','CGChild',cur_dir+'/inhe.cpp',44,5,clang.cindex.CursorKind.CONSTRUCTOR.value,0,0,1),
('c:@C@CGChild@F@~CGChild#','~CGChild',cur_dir+'/inhe.cpp',45,5,clang.cindex.CursorKind.DESTRUCTOR.value,0,0,1),
('c:@C@CGChild@F@response#','response',cur_dir+'/inhe.cpp',46,18,clang.cindex.CursorKind.CXX_METHOD.value,0,1,0),
('c:@C@CGChild@F@response#','response',cur_dir+'/inhe.cpp',49,15,clang.cindex.CursorKind.CXX_METHOD.value,0,1,1),
('c:@C@COther','COther',cur_dir+'/inhe.cpp',53,7,clang.cindex.CursorKind.CLASS_DECL.value,0,0,1),
('c:@C@COther@F@COther#','COther',cur_dir+'/inhe.cpp',57,5,clang.cindex.CursorKind.CONSTRUCTOR.value,0,0,1),
('c:@C@COther@F@~COther#','~COther',cur_dir+'/inhe.cpp',58,5,clang.cindex.CursorKind.DESTRUCTOR.value,0,0,1),
('c:@C@COther@F@response#','response',cur_dir+'/inhe.cpp',59,18,clang.cindex.CursorKind.CXX_METHOD.value,0,1,0),
('c:@C@COther@F@response#','response',cur_dir+'/inhe.cpp',62,14,clang.cindex.CursorKind.CXX_METHOD.value,0,1,1),
('c:inhe.cpp@869@F@test#*$@C@CParent0#','test',cur_dir+'/inhe.cpp',66,13,clang.cindex.CursorKind.FUNCTION_DECL.value,0,0,1),
('c:inhe.cpp@886@F@test#*$@C@CParent0#@a','a',cur_dir+'/inhe.cpp',66,34,clang.cindex.CursorKind.PARM_DECL.value,0,0,1),
('c:@F@main','main',cur_dir+'/inhe.cpp',71,5,clang.cindex.CursorKind.FUNCTION_DECL.value,0,0,1),
('c:inhe.cpp@946@F@main@parent','parent',cur_dir+'/inhe.cpp',73,14,clang.cindex.CursorKind.VAR_DECL.value,0,0,1),
('c:inhe.cpp@967@F@main@child','child',cur_dir+'/inhe.cpp',74,12,clang.cindex.CursorKind.VAR_DECL.value,0,0,1),
('c:inhe.cpp@985@F@main@gchild','gchild',cur_dir+'/inhe.cpp',75,13,clang.cindex.CursorKind.VAR_DECL.value,0,0,1),
('c:inhe.cpp@1005@F@main@other','other',cur_dir+'/inhe.cpp',76,12,clang.cindex.CursorKind.VAR_DECL.value,0,0,1),
]


test_data_list_overriden = [
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

err += test_util.DoDeclTest(test_data_list_decl, test_data_list_ref)
err += test_util.DoRefTest(test_data_list_ref, test_data_list_decl)

# build test list
usr_list = []
for test in test_data_list_overriden:
    usr_list.append(test[6])
usr_list = set(usr_list)
test_list = []
for usr in usr_list:
    for test in test_data_list_decl:
        if usr == test[0]:
            test_list.append(test)

for test in test_list:
    resultList = []
    test_util.DbgPrint("override test")
    #print test
    usr, dummy, fileName, line, col, dummy, dummy, dummy, is_def = test
    # search overrider
    for i in test_data_list_overriden:
        i_usr, dummy, i_fileName, i_line, i_col, dummy, i_usr_overrider, i_isDef = i
        if usr == i_usr_overrider:
            for declRow in test_data_list_decl:
                declUsr, declName, declFileName, declLine, declCol, dummy, dummy, dummy, declIsDef = declRow
                if i_usr == declUsr and i_isDef == declIsDef:
                    resultList.append((declLine, declCol, declFileName ))

    if len(resultList) == 0:
        continue

    # exec command
    cmdResult = test_util.QueryTestExecCommand("override", fileName, line, col)
    test_util.DbgPrint(cmdResult)
    test_util.DbgPrint(resultList)
    cmdResult = sorted(cmdResult)
    resultList = sorted(resultList)

    # check result
    i  = 0
    for row in cmdResult:
        if row != resultList[i]:
            print "DIFFER: " 
            print row
            print resultList[i]
            err += 1
        i+=1

# build test list
usr_list = []
for test in test_data_list_overriden:
    usr_list.append(test[0])
usr_list = set(usr_list)
test_list = []
for usr in usr_list:
    for test in test_data_list_decl:
        if usr == test[0]:
            test_list.append(test)

for test in test_list:
    resultList = []
    test_util.DbgPrint("overriden test")
    #print test
    usr, dummy, fileName, line, col, dummy, dummy, dummy, is_def = test
    # get decl location
    for i in test_data_list_overriden:
        i_usr, dummy, i_fileName, i_line, i_col, dummy, i_usr_overrider, i_isDef = i
        if i_usr == usr:
            resultList.append((i_line, i_col, i_fileName ))

    if len(resultList) == 0:
        continue

    # exec command
    cmdResult = test_util.QueryTestExecCommand("overriden", fileName, line, col)
    test_util.DbgPrint(cmdResult)
    test_util.DbgPrint(resultList)
    cmdResult = sorted(cmdResult)
    resultList = sorted(resultList)

    # check result
    i  = 0
    for row in cmdResult:
        if row != resultList[i]:
            print "DIFFER: " 
            print row
            print resultList[i]
            err += 1
        i+=1

if err == 0:
    print "OK"
else:
    print "ERR: %d"%(err)
sys.exit(err)
