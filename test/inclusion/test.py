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
# a.cpp
"include " + db_dir + " " + cur_dir + "/a/a.cpp 1",
"include " + db_dir + " " + cur_dir + "/a/a.cpp 2",
"include " + db_dir + " " + cur_dir + "/a/a.cpp 3",
# a.h
"include " + db_dir + " " + cur_dir + "/a/a.h 1",
"include " + db_dir + " " + cur_dir + "/a/a.h 2",
# b.h
"include " + db_dir + " " + cur_dir + "/b.h 1",
]

a_list = [
# a.cpp
[
"/usr/include/stdio.h",
],
[
"/usr/include/c++/4.8/iostream",
],
[
"/home/norito/devel/cxxtags/test/inclusion/a/a.h",
],
# a.h
[
"/usr/include/c++/4.8/string",
],
[
"/home/norito/devel/cxxtags/test/inclusion/b.h",
],
# b.h
[
"/usr/include/c++/4.8/vector",
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
