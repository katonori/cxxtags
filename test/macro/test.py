#!/usr/bin/python

import sys
import os
sys.path.append("../../src/")
sys.path.append("../util/")
import commands
import common

CXXTAGS_QUERY = "../../bin/cxxtags_query"

if len(sys.argv) != 2:
    print "usage: cmd db_file"
    exit(1)

cur_dir = os.getcwd()
db_dir = sys.argv[1]

q_list = [
# main.cpp
"decl " + db_dir + " " + cur_dir + "/main.cpp 11 5",
"def " + db_dir + " " + cur_dir + "/main.cpp 11 5",
"ref " + db_dir + " " + cur_dir + "/main.cpp 11 5",
]

a_list = [
# main.cpp
[
"FUNC|"+cur_dir+"/main.cpp|7|9|#define FUNC func",
"func|"+cur_dir+"/main.cpp|1|6|void func();",
],
["func|"+cur_dir+"/main.cpp|2|6|void func()"],
[
"FUNC|"+cur_dir+"/main.cpp|11|5|    FUNC();",
"func|"+cur_dir+"/main.cpp|12|5|    func();",
],
]

err = 0

i = 0
for q in q_list:
    err += common.test_one(q, a_list[i])
    i+=1
if err == 0:
    print "OK"
else:
    print "ERR: %d"%(err)

exit(err)
