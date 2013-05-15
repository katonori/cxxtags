#!/usr/bin/python
import sys
import os
import commands
sys.path.append("../util/")
import common as test_util

cur_dir = os.getcwd()

testList = [
(1,5, cur_dir+"/main.cpp"), #a
(2,5, cur_dir+"/main.cpp"), #main
(4,9, cur_dir+"/main.cpp"), #b
(4,13, cur_dir+"/main.cpp"), #a
(5,12, cur_dir+"/main.cpp"), #b
]

refListPartial = [
[('a', 1, 5, cur_dir+'/main.cpp','int a = 5;')],
[('main', 2, 5, cur_dir+'/main.cpp','int main()')],
[],
[('a', 1, 5, cur_dir+'/main.cpp','int a = 5;')],
[],
]

refListFull = [
[('a', 1, 5, cur_dir+'/main.cpp','int a = 5;')],
[('main', 2, 5, cur_dir+'/main.cpp','int main()')],
[('b', 4, 9, cur_dir+'/main.cpp','    int b = a + 1;')],
[('a', 1, 5, cur_dir+'/main.cpp','int a = 5;')],
[('b', 4, 9, cur_dir+'/main.cpp','    int b = a + 1;')],
]

def doTest(testList, refList):
    err = 0
    i = 0
    while i < len(testList):
        line, col, fn = testList[i]
        result = test_util.QueryTestExecCommand("decl", fn, line, col)
        if result != refList[i]:
            print "ERROR: ", result
            print "ERROR: ", refList[i]
            err+=1
        i+=1
    return err

err = 0

CXXTAGS = "../../bin/cxxtags"
CXXTAGS_DB_MANAGER = "../../bin/cxxtags_db_manager"
DB_DIR = "db"
QUERY_CMD = 'sqlite3 db/main.db "select contained_part from db_info"'

# test partial
if os.system(CXXTAGS + ' -p main.cpp -o main.db'):
    sys.exit(1)
if os.system(CXXTAGS_DB_MANAGER + " add " + DB_DIR + ' main.db'):
    sys.exit(1)
rv = commands.getoutput(QUERY_CMD)
if rv != "1":
    print "ERROR:contained_part:", rv
    err+=1
err += doTest(testList, refListPartial)

# rebuild: full
if os.system(CXXTAGS_DB_MANAGER + " rebuild " + DB_DIR + ' main.cpp'):
    sys.exit(1)
rv = commands.getoutput(QUERY_CMD)
if rv != "0":
    print "ERROR:contained_part:", rv
    err+=1
# test full
err += doTest(testList, refListFull)

# rebuild: partial
if os.system(CXXTAGS_DB_MANAGER + " rebuild --partial " + DB_DIR + ' main.cpp'):
    sys.exit(1)
rv = commands.getoutput(QUERY_CMD)
if rv != "1":
    print "ERROR:contained_part:", rv
    err+=1
# test partial again
err += doTest(testList, refListPartial)

if err == 0:
    print "OK"
else:
    print "NG"
