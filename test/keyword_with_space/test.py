#!/usr/bin/python

import sys
import os
sys.path.append("../../src/")
sys.path.append("../util/")
import common
import commands

CXXTAGS_QUERY = "../../bin/cxxtags_query"

if len(sys.argv) != 2:
    print "usage: cmd db_file"
    exit(1)

db_dir = sys.argv[1]
cur_dir = os.getcwd()

q_list = [
# main.cpp
"decl "+db_dir+" "+cur_dir+"/main.cpp 3 8",
"def "+db_dir+" "+cur_dir+"/main.cpp 3 8",
"ref "+db_dir+" "+cur_dir+"/main.cpp 3 8",

"decl "+db_dir+" "+cur_dir+"/main.cpp 4 9",
"def "+db_dir+" "+cur_dir+"/main.cpp  4 9",
"ref "+db_dir+" "+cur_dir+"/main.cpp  4 9",

"decl "+db_dir+" "+cur_dir+"/main.cpp 5 9",
"def "+db_dir+" "+cur_dir+"/main.cpp  5 9",
"ref "+db_dir+" "+cur_dir+"/main.cpp  5 9",

"decl "+db_dir+" "+cur_dir+"/main.cpp 6 9",
"def "+db_dir+" "+cur_dir+"/main.cpp  6 9",
"ref "+db_dir+" "+cur_dir+"/main.cpp  6 9",

"decl "+db_dir+" "+cur_dir+"/main.cpp 8 7",
"def "+db_dir+" "+cur_dir+"/main.cpp  8 7",
"ref "+db_dir+" "+cur_dir+"/main.cpp  8 7",

"decl "+db_dir+" "+cur_dir+"/main.cpp 9 11",
"def "+db_dir+" "+cur_dir+"/main.cpp  9 11",
"ref "+db_dir+" "+cur_dir+"/main.cpp  9 11",

"decl "+db_dir+" "+cur_dir+"/main.cpp 10 11",
"def "+db_dir+" "+cur_dir+"/main.cpp  10 11",
"ref "+db_dir+" "+cur_dir+"/main.cpp  10 11",

"decl "+db_dir+" "+cur_dir+"/main.cpp 11 11",
"def "+db_dir+" "+cur_dir+"/main.cpp  11 11",
"ref "+db_dir+" "+cur_dir+"/main.cpp  11 11",

"decl "+db_dir+" "+cur_dir+"/main.cpp 22 5",
"def "+db_dir+" "+cur_dir+"/main.cpp  22 5",
"ref "+db_dir+" "+cur_dir+"/main.cpp  22 5",

"decl "+db_dir+" "+cur_dir+"/main.cpp 26 5",
"def "+db_dir+" "+cur_dir+"/main.cpp  26 5",
"ref "+db_dir+" "+cur_dir+"/main.cpp  26 5",

"decl "+db_dir+" "+cur_dir+"/main.cpp 30 5",
"def "+db_dir+" "+cur_dir+"/main.cpp  30 5",
"ref "+db_dir+" "+cur_dir+"/main.cpp  30 5",

"decl "+db_dir+" "+cur_dir+"/main.cpp 31 11",
"def "+db_dir+" "+cur_dir+"/main.cpp  31 11",
"ref "+db_dir+" "+cur_dir+"/main.cpp  31 11",
]

a_list = [
# 3 8
["S0|"+cur_dir+"/main.cpp|3|8|struct S0 {"],
["S0|"+cur_dir+"/main.cpp|3|8|struct S0 {"],
[
'S0|'+cur_dir+r'/main.cpp|22|5|    S0 a;',
],
# 4 9
["a|"+cur_dir+"/main.cpp|4|9|    int a;"],
["a|"+cur_dir+"/main.cpp|4|9|    int a;"],
[
'a|'+cur_dir+r'/main.cpp|23|7|    a.a = 0;',
],
# 5 9
["b|"+cur_dir+"/main.cpp|5|9|    int b;"],
["b|"+cur_dir+"/main.cpp|5|9|    int b;"],
[
'b|'+cur_dir+r'/main.cpp|24|7|    a.b = 1;',
],
# 6 9
["c|"+cur_dir+"/main.cpp|6|9|    int c;"],
["c|"+cur_dir+"/main.cpp|6|9|    int c;"],
[
'c|'+cur_dir+r'/main.cpp|25|7|    a.c = 2;',
],
# 8 7
["U0|"+cur_dir+"/main.cpp|8|7|union U0 {"],
["U0|"+cur_dir+"/main.cpp|8|7|union U0 {"],
[
'U0|'+cur_dir+r'/main.cpp|26|5|    U0 b;',
],
# 9 11
["a|"+cur_dir+"/main.cpp|9|11|    int   a;"],
["a|"+cur_dir+"/main.cpp|9|11|    int   a;"],
[
'a|'+cur_dir+r'/main.cpp|27|7|    b.a = 0;',
],
# 10 11
["b|"+cur_dir+"/main.cpp|10|11|    short b;"],
["b|"+cur_dir+"/main.cpp|10|11|    short b;"],
[
'b|'+cur_dir+r'/main.cpp|28|7|    b.b = 1;',
],
# 11 11
["c|"+cur_dir+"/main.cpp|11|11|    float c;"],
["c|"+cur_dir+"/main.cpp|11|11|    float c;"],
[
'c|'+cur_dir+r'/main.cpp|29|7|    b.c = 1.0;',
],
# 22 5
["S0|"+cur_dir+"/main.cpp|3|8|struct S0 {"],
["S0|"+cur_dir+"/main.cpp|3|8|struct S0 {"],
[
'S0|'+cur_dir+r'/main.cpp|22|5|    S0 a;',
],
# 26 5
["U0|"+cur_dir+"/main.cpp|8|7|union U0 {"],
["U0|"+cur_dir+"/main.cpp|8|7|union U0 {"],
[
'U0|'+cur_dir+r'/main.cpp|26|5|    U0 b;',
],
# 30 5
["C0|"+cur_dir+"/main.cpp|13|7|class C0 {"],
["C0|"+cur_dir+"/main.cpp|13|7|class C0 {"],
[
'C0|'+cur_dir+r'/main.cpp|30|5|    C0 c;',
],
# 31 11
["EVAL|"+cur_dir+"/main.cpp|17|5|    EVAL,"],
["EVAL|"+cur_dir+"/main.cpp|17|5|    EVAL,"],
[
'EVAL|'+cur_dir+r'/main.cpp|31|11|    c.a = EVAL;',
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
