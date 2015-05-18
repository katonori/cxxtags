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
"ref  " + db_dir + " " + cur_dir + "/main.cpp 3 11",
"decl  " + db_dir + " " + cur_dir + "/main.cpp 7 5",
]

a_list = [
# main.cpp
[
"test|"+cur_dir+"/main.cpp|7|5|    test::cout << \"TEST\\n\";",
],
[
"test|"+cur_dir+"/main.cpp|3|11|namespace test = std;",
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
