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
"override  " + db_dir + " " + cur_dir + "/Interface.h 3 17",
"override  " + db_dir + " " + cur_dir + "/Impl0.cpp 4 9",
"override  " + db_dir + " " + cur_dir + "/Impl1.cpp 4 9",
"override  " + db_dir + " " + cur_dir + "/Impl2.cpp 4 9",
"override  " + db_dir + " " + cur_dir + "/Impl3.cpp 4 9",
]

a_list = [
# main.cpp
[
"func|"+cur_dir+"/Impl0.cpp|4|9|    int func() { return 0; }",
"func|"+cur_dir+"/Impl1.cpp|4|9|    int func() { return 1; }",
"func|"+cur_dir+"/Impl2.cpp|4|9|    int func() { return 2; }",
"func|"+cur_dir+"/Impl3.cpp|4|9|    int func() { return 3; }",
],
[
"func|"+cur_dir+"/Interface.h|3|17|    virtual int func() = 0;",
],
[
"func|"+cur_dir+"/Interface.h|3|17|    virtual int func() = 0;",
],
[
"func|"+cur_dir+"/Interface.h|3|17|    virtual int func() = 0;",
],
[
"func|"+cur_dir+"/Interface.h|3|17|    virtual int func() = 0;",
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
