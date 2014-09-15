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
"decl "+db_dir+" "+cur_dir+"/main.cpp 4 5", #VAL0_0
"def "+db_dir+" "+cur_dir+"/main.cpp 4 5", #VAL0_0
"ref "+db_dir+" "+cur_dir+"/main.cpp 4 5", #VAL0_0

"decl "+db_dir+" "+cur_dir+"/main.cpp 5 5", #VAL0_1
"def "+db_dir+" "+cur_dir+"/main.cpp 5 5", #VAL0_1
"ref "+db_dir+" "+cur_dir+"/main.cpp 5 5", #VAL0_1

"decl "+db_dir+" "+cur_dir+"/main.cpp 6 5", #VAL0_2
"def "+db_dir+" "+cur_dir+"/main.cpp 6 5", #VAL0_2
"ref "+db_dir+" "+cur_dir+"/main.cpp 6 5", #VAL0_2

"decl "+db_dir+" "+cur_dir+"/main.cpp 7 5", #VAL0_3
"def "+db_dir+" "+cur_dir+"/main.cpp 7 5", #VAL0_3
"ref "+db_dir+" "+cur_dir+"/main.cpp 7 5", #VAL0_3

"decl "+db_dir+" "+cur_dir+"/main.cpp 11 5", #VAL1_0
"def "+db_dir+" "+cur_dir+"/main.cpp 11 5", #VAL1_0
"ref "+db_dir+" "+cur_dir+"/main.cpp 11 5", #VAL1_0

"decl "+db_dir+" "+cur_dir+"/main.cpp 12 5", #VAL1_1
"def "+db_dir+" "+cur_dir+"/main.cpp 12 5", #VAL1_1
"ref "+db_dir+" "+cur_dir+"/main.cpp 12 5", #VAL1_1

"decl "+db_dir+" "+cur_dir+"/main.cpp 13 5", #VAL1_2
"def "+db_dir+" "+cur_dir+"/main.cpp 13 5", #VAL1_2
"ref "+db_dir+" "+cur_dir+"/main.cpp 13 5", #VAL1_2

"decl "+db_dir+" "+cur_dir+"/main.cpp 14 5", #VAL1_3
"def "+db_dir+" "+cur_dir+"/main.cpp 14 5", #VAL1_3
"ref "+db_dir+" "+cur_dir+"/main.cpp 14 5", #VAL1_3

"decl "+db_dir+" "+cur_dir+"/main.cpp 17 13", #check
"def "+db_dir+" "+cur_dir+"/main.cpp 17 13", #check
"ref "+db_dir+" "+cur_dir+"/main.cpp 17 13", #check

"decl "+db_dir+" "+cur_dir+"/main.cpp 19 35", #VAL0_0
"def "+db_dir+" "+cur_dir+"/main.cpp 19 35", #VAL0_0
"ref "+db_dir+" "+cur_dir+"/main.cpp 19 35", #VAL0_0

"decl "+db_dir+" "+cur_dir+"/main.cpp 19 43", #VAL0_1
"def "+db_dir+" "+cur_dir+"/main.cpp 19 43", #VAL0_1
"ref "+db_dir+" "+cur_dir+"/main.cpp 19 43", #VAL0_1

"decl "+db_dir+" "+cur_dir+"/main.cpp 19 51", #VAL0_2
"def "+db_dir+" "+cur_dir+"/main.cpp 19 51", #VAL0_2
"ref "+db_dir+" "+cur_dir+"/main.cpp 19 51", #VAL0_2

"decl "+db_dir+" "+cur_dir+"/main.cpp 19 59", #VAL0_3
"def "+db_dir+" "+cur_dir+"/main.cpp 19 59", #VAL0_3
"ref "+db_dir+" "+cur_dir+"/main.cpp 19 59", #VAL0_3

"decl "+db_dir+" "+cur_dir+"/main.cpp 22 11", #NS0
"def "+db_dir+" "+cur_dir+"/main.cpp 22 11", #NS0
"ref "+db_dir+" "+cur_dir+"/main.cpp 22 11", #NS0

"decl "+db_dir+" "+cur_dir+"/main.cpp 24 9", #VAL0_0
"def "+db_dir+" "+cur_dir+"/main.cpp 24 9", #VAL0_0
"ref "+db_dir+" "+cur_dir+"/main.cpp 24 9", #VAL0_0

"decl "+db_dir+" "+cur_dir+"/main.cpp 25 9", #VAL0_1
"def "+db_dir+" "+cur_dir+"/main.cpp 25 9", #VAL0_1
"ref "+db_dir+" "+cur_dir+"/main.cpp 25 9", #VAL0_1

"decl "+db_dir+" "+cur_dir+"/main.cpp 26 9", #VAL0_2
"def "+db_dir+" "+cur_dir+"/main.cpp 26 9", #VAL0_2
"ref "+db_dir+" "+cur_dir+"/main.cpp 26 9", #VAL0_2

"decl "+db_dir+" "+cur_dir+"/main.cpp 27 9", #VAL0_3
"def "+db_dir+" "+cur_dir+"/main.cpp 27 9", #VAL0_3
"ref "+db_dir+" "+cur_dir+"/main.cpp 27 9", #VAL0_3

"decl "+db_dir+" "+cur_dir+"/main.cpp 29 17", #check
"def "+db_dir+" "+cur_dir+"/main.cpp 29 17", #check
"ref "+db_dir+" "+cur_dir+"/main.cpp 29 17", #check

"decl "+db_dir+" "+cur_dir+"/main.cpp 31 42", #VAL0_0
"def "+db_dir+" "+cur_dir+"/main.cpp 31 42", #VAL0_0
"ref "+db_dir+" "+cur_dir+"/main.cpp 31 42", #VAL0_0

"decl "+db_dir+" "+cur_dir+"/main.cpp 31 50", #VAL0_1
"def "+db_dir+" "+cur_dir+"/main.cpp 31 50", #VAL0_1
"ref "+db_dir+" "+cur_dir+"/main.cpp 31 50", #VAL0_1

"decl "+db_dir+" "+cur_dir+"/main.cpp 31 58", #VAL0_2
"def "+db_dir+" "+cur_dir+"/main.cpp 31 58", #VAL0_2
"ref "+db_dir+" "+cur_dir+"/main.cpp 31 58", #VAL0_2

"decl "+db_dir+" "+cur_dir+"/main.cpp 31 66", #VAL0_3
"def "+db_dir+" "+cur_dir+"/main.cpp 31 66", #VAL0_3
"ref "+db_dir+" "+cur_dir+"/main.cpp 31 66", #VAL0_3

"decl "+db_dir+" "+cur_dir+"/main.cpp 33 11", #C0
"def "+db_dir+" "+cur_dir+"/main.cpp 33 11", #C0
"ref "+db_dir+" "+cur_dir+"/main.cpp 33 11", #C0

"decl "+db_dir+" "+cur_dir+"/main.cpp 36 13", #VAL0_0
"def "+db_dir+" "+cur_dir+"/main.cpp 36 13", #VAL0_0
"ref "+db_dir+" "+cur_dir+"/main.cpp 36 13", #VAL0_0

"decl "+db_dir+" "+cur_dir+"/main.cpp 37 13", #VAL0_1
"def "+db_dir+" "+cur_dir+"/main.cpp 37 13", #VAL0_1
"ref "+db_dir+" "+cur_dir+"/main.cpp 37 13", #VAL0_1

"decl "+db_dir+" "+cur_dir+"/main.cpp 38 13", #VAL0_2
"def "+db_dir+" "+cur_dir+"/main.cpp 38 13", #VAL0_2
"ref "+db_dir+" "+cur_dir+"/main.cpp 38 13", #VAL0_2

"decl "+db_dir+" "+cur_dir+"/main.cpp 39 13", #VAL0_3
"def "+db_dir+" "+cur_dir+"/main.cpp 39 13", #VAL0_3
"ref "+db_dir+" "+cur_dir+"/main.cpp 39 13", #VAL0_3

"decl "+db_dir+" "+cur_dir+"/main.cpp 41 14", #check
"def "+db_dir+" "+cur_dir+"/main.cpp 41 14", #check
"ref "+db_dir+" "+cur_dir+"/main.cpp 41 14", #check

"decl "+db_dir+" "+cur_dir+"/main.cpp 43 50", #VAL0_0
"def "+db_dir+" "+cur_dir+"/main.cpp 43 50", #VAL0_0
"ref "+db_dir+" "+cur_dir+"/main.cpp 43 50", #VAL0_0

"decl "+db_dir+" "+cur_dir+"/main.cpp 43 58", #VAL0_1
"def "+db_dir+" "+cur_dir+"/main.cpp 43 58", #VAL0_1
"ref "+db_dir+" "+cur_dir+"/main.cpp 43 58", #VAL0_1

"decl "+db_dir+" "+cur_dir+"/main.cpp 43 66", #VAL0_2
"def "+db_dir+" "+cur_dir+"/main.cpp 43 66", #VAL0_2
"ref "+db_dir+" "+cur_dir+"/main.cpp 43 66", #VAL0_2

"decl "+db_dir+" "+cur_dir+"/main.cpp 43 74", #VAL0_3
"def "+db_dir+" "+cur_dir+"/main.cpp 43 74", #VAL0_3
"ref "+db_dir+" "+cur_dir+"/main.cpp 43 74", #VAL0_3

#"decl "+db_dir+" "+cur_dir+"/main.cpp 46 11", #C1
#"decl "+db_dir+" "+cur_dir+"/main.cpp 46 23", #C0

"decl "+db_dir+" "+cur_dir+"/main.cpp 50 13", #VAL0_0
"def "+db_dir+" "+cur_dir+"/main.cpp 50 13", #VAL0_0
"ref "+db_dir+" "+cur_dir+"/main.cpp 50 13", #VAL0_0

"decl "+db_dir+" "+cur_dir+"/main.cpp 51 13", #VAL0_1
"def "+db_dir+" "+cur_dir+"/main.cpp 51 13", #VAL0_1
"ref "+db_dir+" "+cur_dir+"/main.cpp 51 13", #VAL0_1

"decl "+db_dir+" "+cur_dir+"/main.cpp 52 13", #VAL0_2
"def "+db_dir+" "+cur_dir+"/main.cpp 52 13", #VAL0_2
"ref "+db_dir+" "+cur_dir+"/main.cpp 52 13", #VAL0_2

"decl "+db_dir+" "+cur_dir+"/main.cpp 53 13", #VAL0_3
"def "+db_dir+" "+cur_dir+"/main.cpp 53 13", #VAL0_3
"ref "+db_dir+" "+cur_dir+"/main.cpp 53 13", #VAL0_3

"decl "+db_dir+" "+cur_dir+"/main.cpp 55 14", #check
"def "+db_dir+" "+cur_dir+"/main.cpp 55 14", #check
"ref "+db_dir+" "+cur_dir+"/main.cpp 55 14", #check

"decl "+db_dir+" "+cur_dir+"/main.cpp 57 50", #VAL0_0
"def "+db_dir+" "+cur_dir+"/main.cpp 57 50", #VAL0_0
"ref "+db_dir+" "+cur_dir+"/main.cpp 57 50", #VAL0_0

"decl "+db_dir+" "+cur_dir+"/main.cpp 57 58", #VAL0_1
"def "+db_dir+" "+cur_dir+"/main.cpp 57 58", #VAL0_1
"ref "+db_dir+" "+cur_dir+"/main.cpp 57 58", #VAL0_1

"decl "+db_dir+" "+cur_dir+"/main.cpp 57 66", #VAL0_2
"def "+db_dir+" "+cur_dir+"/main.cpp 57 66", #VAL0_2
"ref "+db_dir+" "+cur_dir+"/main.cpp 57 66", #VAL0_2

"decl "+db_dir+" "+cur_dir+"/main.cpp 57 74", #VAL0_3
"def "+db_dir+" "+cur_dir+"/main.cpp 57 74", #VAL0_3
"ref "+db_dir+" "+cur_dir+"/main.cpp 57 74", #VAL0_3

#"decl "+db_dir+" "+cur_dir+"/main.cpp 62 11", #NS1

"decl "+db_dir+" "+cur_dir+"/main.cpp 64 9", #VAL0_0
"def "+db_dir+" "+cur_dir+"/main.cpp 64 9", #VAL0_0
"ref "+db_dir+" "+cur_dir+"/main.cpp 64 9", #VAL0_0

"decl "+db_dir+" "+cur_dir+"/main.cpp 65 9", #VAL0_1
"def "+db_dir+" "+cur_dir+"/main.cpp 65 9", #VAL0_1
"ref "+db_dir+" "+cur_dir+"/main.cpp 65 9", #VAL0_1

"decl "+db_dir+" "+cur_dir+"/main.cpp 66 9", #VAL0_2
"def "+db_dir+" "+cur_dir+"/main.cpp 66 9", #VAL0_2
"ref "+db_dir+" "+cur_dir+"/main.cpp 66 9", #VAL0_2

"decl "+db_dir+" "+cur_dir+"/main.cpp 67 9", #VAL0_3
"def "+db_dir+" "+cur_dir+"/main.cpp 67 9", #VAL0_3
"ref "+db_dir+" "+cur_dir+"/main.cpp 67 9", #VAL0_3

"decl "+db_dir+" "+cur_dir+"/main.cpp 69 17", #check
"def "+db_dir+" "+cur_dir+"/main.cpp 69 17", #check
"ref "+db_dir+" "+cur_dir+"/main.cpp 69 17", #check

"decl "+db_dir+" "+cur_dir+"/main.cpp 71 42", #VAL0_0
"def "+db_dir+" "+cur_dir+"/main.cpp 71 42", #VAL0_0
"ref "+db_dir+" "+cur_dir+"/main.cpp 71 42", #VAL0_0

"decl "+db_dir+" "+cur_dir+"/main.cpp 71 50", #VAL0_1
"def "+db_dir+" "+cur_dir+"/main.cpp 71 50", #VAL0_1
"ref "+db_dir+" "+cur_dir+"/main.cpp 71 50", #VAL0_1

"decl "+db_dir+" "+cur_dir+"/main.cpp 71 58", #VAL0_2
"def "+db_dir+" "+cur_dir+"/main.cpp 71 58", #VAL0_2
"ref "+db_dir+" "+cur_dir+"/main.cpp 71 58", #VAL0_2

"decl "+db_dir+" "+cur_dir+"/main.cpp 71 66", #VAL0_3
"def "+db_dir+" "+cur_dir+"/main.cpp 71 66", #VAL0_3
"ref "+db_dir+" "+cur_dir+"/main.cpp 71 66", #VAL0_3

#"decl "+db_dir+" "+cur_dir+"/main.cpp 73 11", #C0

"decl "+db_dir+" "+cur_dir+"/main.cpp 76 13", #VAL0_0
"def "+db_dir+" "+cur_dir+"/main.cpp 76 13", #VAL0_0
"ref "+db_dir+" "+cur_dir+"/main.cpp 76 13", #VAL0_0

"decl "+db_dir+" "+cur_dir+"/main.cpp 77 13", #VAL0_1
"def "+db_dir+" "+cur_dir+"/main.cpp 77 13", #VAL0_1
"ref "+db_dir+" "+cur_dir+"/main.cpp 77 13", #VAL0_1

"decl "+db_dir+" "+cur_dir+"/main.cpp 78 13", #VAL0_2
"def "+db_dir+" "+cur_dir+"/main.cpp 78 13", #VAL0_2
"ref "+db_dir+" "+cur_dir+"/main.cpp 78 13", #VAL0_2

"decl "+db_dir+" "+cur_dir+"/main.cpp 79 13", #VAL0_3
"def "+db_dir+" "+cur_dir+"/main.cpp 79 13", #VAL0_3
"ref "+db_dir+" "+cur_dir+"/main.cpp 79 13", #VAL0_3

"decl "+db_dir+" "+cur_dir+"/main.cpp 81 14", #check
"def "+db_dir+" "+cur_dir+"/main.cpp 81 14", #check
"ref "+db_dir+" "+cur_dir+"/main.cpp 81 14", #check

"decl "+db_dir+" "+cur_dir+"/main.cpp 83 50", #VAL0_0
"def "+db_dir+" "+cur_dir+"/main.cpp 83 50", #VAL0_0
"ref "+db_dir+" "+cur_dir+"/main.cpp 83 50", #VAL0_0

"decl "+db_dir+" "+cur_dir+"/main.cpp 83 58", #VAL0_1
"def "+db_dir+" "+cur_dir+"/main.cpp 83 58", #VAL0_1
"ref "+db_dir+" "+cur_dir+"/main.cpp 83 58", #VAL0_1

"decl "+db_dir+" "+cur_dir+"/main.cpp 83 66", #VAL0_2
"def "+db_dir+" "+cur_dir+"/main.cpp 83 66", #VAL0_2
"ref "+db_dir+" "+cur_dir+"/main.cpp 83 66", #VAL0_2

"decl "+db_dir+" "+cur_dir+"/main.cpp 83 74", #VAL0_3
"def "+db_dir+" "+cur_dir+"/main.cpp 83 74", #VAL0_3
"ref "+db_dir+" "+cur_dir+"/main.cpp 83 74", #VAL0_3

#"decl "+db_dir+" "+cur_dir+"/main.cpp 86 11", #C1
#"decl "+db_dir+" "+cur_dir+"/main.cpp 86 23", #C0

"decl "+db_dir+" "+cur_dir+"/main.cpp 89 14", #check
"def "+db_dir+" "+cur_dir+"/main.cpp 89 14", #check
"ref "+db_dir+" "+cur_dir+"/main.cpp 89 14", #check

"decl "+db_dir+" "+cur_dir+"/main.cpp 91 50", #VAL0_0
"def "+db_dir+" "+cur_dir+"/main.cpp 91 50", #VAL0_0
"ref "+db_dir+" "+cur_dir+"/main.cpp 91 50", #VAL0_0

"decl "+db_dir+" "+cur_dir+"/main.cpp 91 58", #VAL0_1
"def "+db_dir+" "+cur_dir+"/main.cpp 91 58", #VAL0_1
"ref "+db_dir+" "+cur_dir+"/main.cpp 91 58", #VAL0_1

"decl "+db_dir+" "+cur_dir+"/main.cpp 91 66", #VAL0_2
"def "+db_dir+" "+cur_dir+"/main.cpp 91 66", #VAL0_2
"ref "+db_dir+" "+cur_dir+"/main.cpp 91 66", #VAL0_2

"decl "+db_dir+" "+cur_dir+"/main.cpp 91 74", #VAL0_3
"def "+db_dir+" "+cur_dir+"/main.cpp 91 74", #VAL0_3
"ref "+db_dir+" "+cur_dir+"/main.cpp 91 74", #VAL0_3

#"decl "+db_dir+" "+cur_dir+"/main.cpp 96 5", #main
#"decl "+db_dir+" "+cur_dir+"/main.cpp 98 5", #NS0
#"decl "+db_dir+" "+cur_dir+"/main.cpp 98 10", #C0
#"decl "+db_dir+" "+cur_dir+"/main.cpp 98 13", #c00
#"decl "+db_dir+" "+cur_dir+"/main.cpp 99 5", #NS0
#"decl "+db_dir+" "+cur_dir+"/main.cpp 99 10", #C1
#"decl "+db_dir+" "+cur_dir+"/main.cpp 99 13", #c01
#"decl "+db_dir+" "+cur_dir+"/main.cpp 100 5", #NS1
#"decl "+db_dir+" "+cur_dir+"/main.cpp 100 10", #C0
#"decl "+db_dir+" "+cur_dir+"/main.cpp 100 13", #c10
#"decl "+db_dir+" "+cur_dir+"/main.cpp 101 5", #NS1
#"decl "+db_dir+" "+cur_dir+"/main.cpp 101 10", #C1
#"decl "+db_dir+" "+cur_dir+"/main.cpp 101 13", #c11

"decl "+db_dir+" "+cur_dir+"/main.cpp 102 7", #check
"def "+db_dir+" "+cur_dir+"/main.cpp 102 7", #check
"ref "+db_dir+" "+cur_dir+"/main.cpp 102 7", #check

#"decl "+db_dir+" "+cur_dir+"/main.cpp 103 5", #NS0

"decl "+db_dir+" "+cur_dir+"/main.cpp 103 10", #check
"def "+db_dir+" "+cur_dir+"/main.cpp 103 10", #check
"ref "+db_dir+" "+cur_dir+"/main.cpp 103 10", #check

#"decl "+db_dir+" "+cur_dir+"/main.cpp 104 5", #NS1

"decl "+db_dir+" "+cur_dir+"/main.cpp 104 10", #check
"def "+db_dir+" "+cur_dir+"/main.cpp 104 10", #check
"ref "+db_dir+" "+cur_dir+"/main.cpp 104 10", #check

#"decl "+db_dir+" "+cur_dir+"/main.cpp 105 5", #c00

"decl "+db_dir+" "+cur_dir+"/main.cpp 105 9", #check
"def "+db_dir+" "+cur_dir+"/main.cpp 105 9", #check
"ref "+db_dir+" "+cur_dir+"/main.cpp 105 9", #check

#"decl "+db_dir+" "+cur_dir+"/main.cpp 106 5", #c01

"decl "+db_dir+" "+cur_dir+"/main.cpp 106 9", #check
"def "+db_dir+" "+cur_dir+"/main.cpp 106 9", #check
"ref "+db_dir+" "+cur_dir+"/main.cpp 106 9", #check

#"decl "+db_dir+" "+cur_dir+"/main.cpp 107 5", #c10

"decl "+db_dir+" "+cur_dir+"/main.cpp 107 9", #check
"def "+db_dir+" "+cur_dir+"/main.cpp 107 9", #check
"ref "+db_dir+" "+cur_dir+"/main.cpp 107 9", #check

#"decl "+db_dir+" "+cur_dir+"/main.cpp 108 5", #c11

"decl "+db_dir+" "+cur_dir+"/main.cpp 108 9", #check
"def "+db_dir+" "+cur_dir+"/main.cpp 108 9", #check
"ref "+db_dir+" "+cur_dir+"/main.cpp 108 9", #check

"decl "+db_dir+" "+cur_dir+"/main.cpp 111 6", #namedEnum
"def "+db_dir+" "+cur_dir+"/main.cpp 111 6", #namedEnum
"ref "+db_dir+" "+cur_dir+"/main.cpp 111 6", #namedEnum

"decl "+db_dir+" "+cur_dir+"/main.cpp 112 5", #VAL2_0
"def "+db_dir+" "+cur_dir+"/main.cpp 112 5", #VAL2_0
"ref "+db_dir+" "+cur_dir+"/main.cpp 112 5", #VAL2_0

"decl "+db_dir+" "+cur_dir+"/main.cpp 113 5", #VAL2_1
"def "+db_dir+" "+cur_dir+"/main.cpp 113 5", #VAL2_1
"ref "+db_dir+" "+cur_dir+"/main.cpp 113 5", #VAL2_1

"decl "+db_dir+" "+cur_dir+"/main.cpp 115 1", #namedEnum
"def "+db_dir+" "+cur_dir+"/main.cpp 115 1", #namedEnum
"ref "+db_dir+" "+cur_dir+"/main.cpp 115 1", #namedEnum

"decl "+db_dir+" "+cur_dir+"/main.cpp 115 15", #VAL2_1
"def "+db_dir+" "+cur_dir+"/main.cpp 115 15", #VAL2_1
"ref "+db_dir+" "+cur_dir+"/main.cpp 115 15", #VAL2_1
]

a_list = [
# 4 5
["VAL0_0|"+cur_dir+"/main.cpp|4|5|    VAL0_0,"],
["VAL0_0|"+cur_dir+"/main.cpp|4|5|    VAL0_0,"],
['VAL0_0|'+cur_dir+r'/main.cpp|19|35|    printf(":: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 5 5
["VAL0_1|"+cur_dir+"/main.cpp|5|5|    VAL0_1,"],
["VAL0_1|"+cur_dir+"/main.cpp|5|5|    VAL0_1,"],
['VAL0_1|'+cur_dir+r'/main.cpp|19|43|    printf(":: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 6 5
["VAL0_2|"+cur_dir+"/main.cpp|6|5|    VAL0_2,"],
["VAL0_2|"+cur_dir+"/main.cpp|6|5|    VAL0_2,"],
['VAL0_2|'+cur_dir+r'/main.cpp|19|51|    printf(":: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 7 5
["VAL0_3|"+cur_dir+"/main.cpp|7|5|    VAL0_3,"],
["VAL0_3|"+cur_dir+"/main.cpp|7|5|    VAL0_3,"],
['VAL0_3|'+cur_dir+r'/main.cpp|19|59|    printf(":: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 11 5
["VAL1_0|"+cur_dir+"/main.cpp|11|5|    VAL1_0,"],
["VAL1_0|"+cur_dir+"/main.cpp|11|5|    VAL1_0,"],
[''],
# 12 5
["VAL1_1|"+cur_dir+"/main.cpp|12|5|    VAL1_1,"],
["VAL1_1|"+cur_dir+"/main.cpp|12|5|    VAL1_1,"],
[''],
# 13 5
["VAL1_2|"+cur_dir+"/main.cpp|13|5|    VAL1_2,"],
["VAL1_2|"+cur_dir+"/main.cpp|13|5|    VAL1_2,"],
[''],
# 14 5
["VAL1_3|"+cur_dir+"/main.cpp|14|5|    VAL1_3,"],
["VAL1_3|"+cur_dir+"/main.cpp|14|5|    VAL1_3,"],
[''],
# 17 3
["check|"+cur_dir+"/main.cpp|17|13|static void check()"],
["check|"+cur_dir+"/main.cpp|17|13|static void check()"],
["check|"+cur_dir+"/main.cpp|102|7|    ::check();"],
# 19 35
["VAL0_0|"+cur_dir+"/main.cpp|4|5|    VAL0_0,"],
["VAL0_0|"+cur_dir+"/main.cpp|4|5|    VAL0_0,"],
['VAL0_0|'+cur_dir+r'/main.cpp|19|35|    printf(":: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 19 43
["VAL0_1|"+cur_dir+"/main.cpp|5|5|    VAL0_1,"],
["VAL0_1|"+cur_dir+"/main.cpp|5|5|    VAL0_1,"],
['VAL0_1|'+cur_dir+r'/main.cpp|19|43|    printf(":: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 19 51
["VAL0_2|"+cur_dir+"/main.cpp|6|5|    VAL0_2,"],
["VAL0_2|"+cur_dir+"/main.cpp|6|5|    VAL0_2,"],
['VAL0_2|'+cur_dir+r'/main.cpp|19|51|    printf(":: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 19 59
["VAL0_3|"+cur_dir+"/main.cpp|7|5|    VAL0_3,"],
["VAL0_3|"+cur_dir+"/main.cpp|7|5|    VAL0_3,"],
['VAL0_3|'+cur_dir+r'/main.cpp|19|59|    printf(":: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 22 11
["NS0|"+cur_dir+"/main.cpp|22|11|namespace NS0 {"],
["NS0|"+cur_dir+"/main.cpp|22|11|namespace NS0 {"],
[
'NS0|'+cur_dir+r'/main.cpp|98|5|    NS0::C0 c00;',
'NS0|'+cur_dir+r'/main.cpp|99|5|    NS0::C1 c01;',
'NS0|'+cur_dir+r'/main.cpp|103|5|    NS0::check();',
],
# 24 9
["VAL0_0|"+cur_dir+"/main.cpp|24|9|        VAL0_0=10,"],
["VAL0_0|"+cur_dir+"/main.cpp|24|9|        VAL0_0=10,"],
['VAL0_0|'+cur_dir+r'/main.cpp|31|42|        printf("NS0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 25 9
["VAL0_1|"+cur_dir+"/main.cpp|25|9|        VAL0_1,"],
["VAL0_1|"+cur_dir+"/main.cpp|25|9|        VAL0_1,"],
['VAL0_1|'+cur_dir+r'/main.cpp|31|50|        printf("NS0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 26 9
["VAL0_2|"+cur_dir+"/main.cpp|26|9|        VAL0_2,"],
["VAL0_2|"+cur_dir+"/main.cpp|26|9|        VAL0_2,"],
['VAL0_2|'+cur_dir+r'/main.cpp|31|58|        printf("NS0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 27 9
["VAL0_3|"+cur_dir+"/main.cpp|27|9|        VAL0_3,"],
["VAL0_3|"+cur_dir+"/main.cpp|27|9|        VAL0_3,"],
['VAL0_3|'+cur_dir+r'/main.cpp|31|66|        printf("NS0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 29 17
["check|"+cur_dir+"/main.cpp|29|17|    static void check()"],
["check|"+cur_dir+"/main.cpp|29|17|    static void check()"],
['check|'+cur_dir+r'/main.cpp|103|10|    NS0::check();'],
# 31 42
["VAL0_0|"+cur_dir+"/main.cpp|24|9|        VAL0_0=10,"],
["VAL0_0|"+cur_dir+"/main.cpp|24|9|        VAL0_0=10,"],
['VAL0_0|'+cur_dir+r'/main.cpp|31|42|        printf("NS0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 31 50
["VAL0_1|"+cur_dir+"/main.cpp|25|9|        VAL0_1,"],
["VAL0_1|"+cur_dir+"/main.cpp|25|9|        VAL0_1,"],
['VAL0_1|'+cur_dir+r'/main.cpp|31|50|        printf("NS0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 31 58
["VAL0_2|"+cur_dir+"/main.cpp|26|9|        VAL0_2,"],
["VAL0_2|"+cur_dir+"/main.cpp|26|9|        VAL0_2,"],
['VAL0_2|'+cur_dir+r'/main.cpp|31|58|        printf("NS0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 31 66
["VAL0_3|"+cur_dir+"/main.cpp|27|9|        VAL0_3,"],
["VAL0_3|"+cur_dir+"/main.cpp|27|9|        VAL0_3,"],
['VAL0_3|'+cur_dir+r'/main.cpp|31|66|        printf("NS0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 33 11
["C0|"+cur_dir+"/main.cpp|33|11|    class C0 {"],
["C0|"+cur_dir+"/main.cpp|33|11|    class C0 {"],
[
'C0|'+cur_dir+r'/main.cpp|46|23|    class C1 : public C0',
'C0|'+cur_dir+r'/main.cpp|98|10|    NS0::C0 c00;',
],
# 36 13
["VAL0_0|"+cur_dir+"/main.cpp|36|13|            VAL0_0 = 20,"],
["VAL0_0|"+cur_dir+"/main.cpp|36|13|            VAL0_0 = 20,"],
['VAL0_0|'+cur_dir+r'/main.cpp|43|50|            printf("NS0::C0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 37 13
["VAL0_1|"+cur_dir+"/main.cpp|37|13|            VAL0_1,"],
["VAL0_1|"+cur_dir+"/main.cpp|37|13|            VAL0_1,"],
['VAL0_1|'+cur_dir+r'/main.cpp|43|58|            printf("NS0::C0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 38 13
["VAL0_2|"+cur_dir+"/main.cpp|38|13|            VAL0_2,"],
["VAL0_2|"+cur_dir+"/main.cpp|38|13|            VAL0_2,"],
['VAL0_2|'+cur_dir+r'/main.cpp|43|66|            printf("NS0::C0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 39 13
["VAL0_3|"+cur_dir+"/main.cpp|39|13|            VAL0_3,"],
["VAL0_3|"+cur_dir+"/main.cpp|39|13|            VAL0_3,"],
['VAL0_3|'+cur_dir+r'/main.cpp|43|74|            printf("NS0::C0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 41 14
["check|"+cur_dir+"/main.cpp|41|14|        void check()"],
["check|"+cur_dir+"/main.cpp|41|14|        void check()"],
['check|'+cur_dir+r'/main.cpp|105|9|    c00.check();'],
# 43 50
["VAL0_0|"+cur_dir+"/main.cpp|36|13|            VAL0_0 = 20,"],
["VAL0_0|"+cur_dir+"/main.cpp|36|13|            VAL0_0 = 20,"],
['VAL0_0|'+cur_dir+r'/main.cpp|43|50|            printf("NS0::C0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 43 58
["VAL0_1|"+cur_dir+"/main.cpp|37|13|            VAL0_1,"],
["VAL0_1|"+cur_dir+"/main.cpp|37|13|            VAL0_1,"],
['VAL0_1|'+cur_dir+r'/main.cpp|43|58|            printf("NS0::C0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 43 66
["VAL0_2|"+cur_dir+"/main.cpp|38|13|            VAL0_2,"],
["VAL0_2|"+cur_dir+"/main.cpp|38|13|            VAL0_2,"],
['VAL0_2|'+cur_dir+r'/main.cpp|43|66|            printf("NS0::C0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 43 74
["VAL0_3|"+cur_dir+"/main.cpp|39|13|            VAL0_3,"],
["VAL0_3|"+cur_dir+"/main.cpp|39|13|            VAL0_3,"],
['VAL0_3|'+cur_dir+r'/main.cpp|43|74|            printf("NS0::C0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 50 13
["VAL0_0|"+cur_dir+"/main.cpp|50|13|            VAL0_0 = 30,"],
["VAL0_0|"+cur_dir+"/main.cpp|50|13|            VAL0_0 = 30,"],
['VAL0_0|'+cur_dir+r'/main.cpp|57|50|            printf("NS0::C1:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 51 13
["VAL0_1|"+cur_dir+"/main.cpp|51|13|            VAL0_1,"],
["VAL0_1|"+cur_dir+"/main.cpp|51|13|            VAL0_1,"],
['VAL0_1|'+cur_dir+r'/main.cpp|57|58|            printf("NS0::C1:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 52 13
["VAL0_2|"+cur_dir+"/main.cpp|52|13|            VAL0_2,"],
["VAL0_2|"+cur_dir+"/main.cpp|52|13|            VAL0_2,"],
['VAL0_2|'+cur_dir+r'/main.cpp|57|66|            printf("NS0::C1:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 53 13
["VAL0_3|"+cur_dir+"/main.cpp|53|13|            VAL0_3,"],
["VAL0_3|"+cur_dir+"/main.cpp|53|13|            VAL0_3,"],
['VAL0_3|'+cur_dir+r'/main.cpp|57|74|            printf("NS0::C1:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 55 14
["check|"+cur_dir+"/main.cpp|55|14|        void check()"],
["check|"+cur_dir+"/main.cpp|55|14|        void check()"],
['check|'+cur_dir+r'/main.cpp|106|9|    c01.check();'],
# 57 50
["VAL0_0|"+cur_dir+"/main.cpp|50|13|            VAL0_0 = 30,"],
["VAL0_0|"+cur_dir+"/main.cpp|50|13|            VAL0_0 = 30,"],
['VAL0_0|'+cur_dir+r'/main.cpp|57|50|            printf("NS0::C1:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 57 58
["VAL0_1|"+cur_dir+"/main.cpp|51|13|            VAL0_1,"],
["VAL0_1|"+cur_dir+"/main.cpp|51|13|            VAL0_1,"],
['VAL0_1|'+cur_dir+r'/main.cpp|57|58|            printf("NS0::C1:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 57 66
["VAL0_2|"+cur_dir+"/main.cpp|52|13|            VAL0_2,"],
["VAL0_2|"+cur_dir+"/main.cpp|52|13|            VAL0_2,"],
['VAL0_2|'+cur_dir+r'/main.cpp|57|66|            printf("NS0::C1:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 57 74
["VAL0_3|"+cur_dir+"/main.cpp|53|13|            VAL0_3,"],
["VAL0_3|"+cur_dir+"/main.cpp|53|13|            VAL0_3,"],
['VAL0_3|'+cur_dir+r'/main.cpp|57|74|            printf("NS0::C1:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 64 9
["VAL0_0|"+cur_dir+"/main.cpp|64|9|        VAL0_0 = 40,"],
["VAL0_0|"+cur_dir+"/main.cpp|64|9|        VAL0_0 = 40,"],
['VAL0_0|'+cur_dir+r'/main.cpp|71|42|        printf("NS0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 65 9
["VAL0_1|"+cur_dir+"/main.cpp|65|9|        VAL0_1,"],
["VAL0_1|"+cur_dir+"/main.cpp|65|9|        VAL0_1,"],
['VAL0_1|'+cur_dir+r'/main.cpp|71|50|        printf("NS0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 66 9
["VAL0_2|"+cur_dir+"/main.cpp|66|9|        VAL0_2,"],
["VAL0_2|"+cur_dir+"/main.cpp|66|9|        VAL0_2,"],
['VAL0_2|'+cur_dir+r'/main.cpp|71|58|        printf("NS0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 67 9
["VAL0_3|"+cur_dir+"/main.cpp|67|9|        VAL0_3,"],
["VAL0_3|"+cur_dir+"/main.cpp|67|9|        VAL0_3,"],
['VAL0_3|'+cur_dir+r'/main.cpp|71|66|        printf("NS0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 69 17
["check|"+cur_dir+"/main.cpp|69|17|    static void check()"],
["check|"+cur_dir+"/main.cpp|69|17|    static void check()"],
['check|'+cur_dir+r'/main.cpp|104|10|    NS1::check();'],
# 71 42
["VAL0_0|"+cur_dir+"/main.cpp|64|9|        VAL0_0 = 40,"],
["VAL0_0|"+cur_dir+"/main.cpp|64|9|        VAL0_0 = 40,"],
['VAL0_0|'+cur_dir+r'/main.cpp|71|42|        printf("NS0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 71 50
["VAL0_1|"+cur_dir+"/main.cpp|65|9|        VAL0_1,"],
["VAL0_1|"+cur_dir+"/main.cpp|65|9|        VAL0_1,"],
['VAL0_1|'+cur_dir+r'/main.cpp|71|50|        printf("NS0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 71 58
["VAL0_2|"+cur_dir+"/main.cpp|66|9|        VAL0_2,"],
["VAL0_2|"+cur_dir+"/main.cpp|66|9|        VAL0_2,"],
['VAL0_2|'+cur_dir+r'/main.cpp|71|58|        printf("NS0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 71 66
["VAL0_3|"+cur_dir+"/main.cpp|67|9|        VAL0_3,"],
["VAL0_3|"+cur_dir+"/main.cpp|67|9|        VAL0_3,"],
['VAL0_3|'+cur_dir+r'/main.cpp|71|66|        printf("NS0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);'],
# 76 13
["VAL0_0|"+cur_dir+"/main.cpp|76|13|            VAL0_0 = 50,"],
["VAL0_0|"+cur_dir+"/main.cpp|76|13|            VAL0_0 = 50,"],
[
'VAL0_0|'+cur_dir+r'/main.cpp|83|50|            printf("NS0::C0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);',
'VAL0_0|'+cur_dir+r'/main.cpp|91|50|            printf("NS1::C1:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);',
],
# 77 13
["VAL0_1|"+cur_dir+"/main.cpp|77|13|            VAL0_1,"],
["VAL0_1|"+cur_dir+"/main.cpp|77|13|            VAL0_1,"],
[
'VAL0_1|'+cur_dir+r'/main.cpp|83|58|            printf("NS0::C0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);',
'VAL0_1|'+cur_dir+r'/main.cpp|91|58|            printf("NS1::C1:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);',
],
# 78 13
["VAL0_2|"+cur_dir+"/main.cpp|78|13|            VAL0_2,"],
["VAL0_2|"+cur_dir+"/main.cpp|78|13|            VAL0_2,"],
[
'VAL0_2|'+cur_dir+r'/main.cpp|83|66|            printf("NS0::C0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);',
'VAL0_2|'+cur_dir+r'/main.cpp|91|66|            printf("NS1::C1:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);',
],
# 79 13
["VAL0_3|"+cur_dir+"/main.cpp|79|13|            VAL0_3,"],
["VAL0_3|"+cur_dir+"/main.cpp|79|13|            VAL0_3,"],
[
'VAL0_3|'+cur_dir+r'/main.cpp|83|74|            printf("NS0::C0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);',
'VAL0_3|'+cur_dir+r'/main.cpp|91|74|            printf("NS1::C1:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);',
],
# 81 14
["check|"+cur_dir+"/main.cpp|81|14|        void check()"],
["check|"+cur_dir+"/main.cpp|81|14|        void check()"],
['check|'+cur_dir+r'/main.cpp|107|9|    c10.check();'],
# 83 50
["VAL0_0|"+cur_dir+"/main.cpp|76|13|            VAL0_0 = 50,"],
["VAL0_0|"+cur_dir+"/main.cpp|76|13|            VAL0_0 = 50,"],
[
'VAL0_0|'+cur_dir+r'/main.cpp|83|50|            printf("NS0::C0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);',
'VAL0_0|'+cur_dir+r'/main.cpp|91|50|            printf("NS1::C1:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);',
],
# 83 58
["VAL0_1|"+cur_dir+"/main.cpp|77|13|            VAL0_1,"],
["VAL0_1|"+cur_dir+"/main.cpp|77|13|            VAL0_1,"],
[
'VAL0_1|'+cur_dir+r'/main.cpp|83|58|            printf("NS0::C0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);',
'VAL0_1|'+cur_dir+r'/main.cpp|91|58|            printf("NS1::C1:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);',
],
# 83 66
["VAL0_2|"+cur_dir+"/main.cpp|78|13|            VAL0_2,"],
["VAL0_2|"+cur_dir+"/main.cpp|78|13|            VAL0_2,"],
[
'VAL0_2|'+cur_dir+r'/main.cpp|83|66|            printf("NS0::C0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);',
'VAL0_2|'+cur_dir+r'/main.cpp|91|66|            printf("NS1::C1:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);',
],
# 83 74
["VAL0_3|"+cur_dir+"/main.cpp|79|13|            VAL0_3,"],
["VAL0_3|"+cur_dir+"/main.cpp|79|13|            VAL0_3,"],
[
'VAL0_3|'+cur_dir+r'/main.cpp|83|74|            printf("NS0::C0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);',
'VAL0_3|'+cur_dir+r'/main.cpp|91|74|            printf("NS1::C1:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);',
],
# 89 14
["check|"+cur_dir+"/main.cpp|89|14|        void check()"],
["check|"+cur_dir+"/main.cpp|89|14|        void check()"],
['check|'+cur_dir+r'/main.cpp|108|9|    c11.check();'],
# 91 50
["VAL0_0|"+cur_dir+"/main.cpp|76|13|            VAL0_0 = 50,"],
["VAL0_0|"+cur_dir+"/main.cpp|76|13|            VAL0_0 = 50,"],
[
'VAL0_0|'+cur_dir+r'/main.cpp|83|50|            printf("NS0::C0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);',
'VAL0_0|'+cur_dir+r'/main.cpp|91|50|            printf("NS1::C1:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);',
],
# 91 58
["VAL0_1|"+cur_dir+"/main.cpp|77|13|            VAL0_1,"],
["VAL0_1|"+cur_dir+"/main.cpp|77|13|            VAL0_1,"],
[
'VAL0_1|'+cur_dir+r'/main.cpp|83|58|            printf("NS0::C0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);',
'VAL0_1|'+cur_dir+r'/main.cpp|91|58|            printf("NS1::C1:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);',
],
# 91 66
["VAL0_2|"+cur_dir+"/main.cpp|78|13|            VAL0_2,"],
["VAL0_2|"+cur_dir+"/main.cpp|78|13|            VAL0_2,"],
[
'VAL0_2|'+cur_dir+r'/main.cpp|83|66|            printf("NS0::C0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);',
'VAL0_2|'+cur_dir+r'/main.cpp|91|66|            printf("NS1::C1:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);',
],
# 91 74
["VAL0_3|"+cur_dir+"/main.cpp|79|13|            VAL0_3,"],
["VAL0_3|"+cur_dir+"/main.cpp|79|13|            VAL0_3,"],
[
'VAL0_3|'+cur_dir+r'/main.cpp|83|74|            printf("NS0::C0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);',
'VAL0_3|'+cur_dir+r'/main.cpp|91|74|            printf("NS1::C1:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);',
],
# 102 7
["check|"+cur_dir+"/main.cpp|17|13|static void check()"],
["check|"+cur_dir+"/main.cpp|17|13|static void check()"],
["check|"+cur_dir+"/main.cpp|102|7|    ::check();"],
# 103 10
["check|"+cur_dir+"/main.cpp|29|17|    static void check()"],
["check|"+cur_dir+"/main.cpp|29|17|    static void check()"],
['check|'+cur_dir+r'/main.cpp|103|10|    NS0::check();'],
# 104 10
["check|"+cur_dir+"/main.cpp|69|17|    static void check()"],
["check|"+cur_dir+"/main.cpp|69|17|    static void check()"],
['check|'+cur_dir+r'/main.cpp|104|10|    NS1::check();'],
# 105 9
["check|"+cur_dir+"/main.cpp|41|14|        void check()"],
["check|"+cur_dir+"/main.cpp|41|14|        void check()"],
['check|'+cur_dir+r'/main.cpp|105|9|    c00.check();'],
# 106 9
["check|"+cur_dir+"/main.cpp|55|14|        void check()"],
["check|"+cur_dir+"/main.cpp|55|14|        void check()"],
['check|'+cur_dir+r'/main.cpp|106|9|    c01.check();'],
# 107 9
["check|"+cur_dir+"/main.cpp|81|14|        void check()"],
["check|"+cur_dir+"/main.cpp|81|14|        void check()"],
['check|'+cur_dir+r'/main.cpp|107|9|    c10.check();'],
# 108 9
["check|"+cur_dir+"/main.cpp|89|14|        void check()"],
["check|"+cur_dir+"/main.cpp|89|14|        void check()"],
['check|'+cur_dir+r'/main.cpp|108|9|    c11.check();'],
# 111 6
["namedEnum|"+cur_dir+"/main.cpp|111|6|enum namedEnum {"],
["namedEnum|"+cur_dir+"/main.cpp|111|6|enum namedEnum {"],
["namedEnum|"+cur_dir+"/main.cpp|115|1|namedEnum e = VAL2_1;"],
# 112 5
["VAL2_0|"+cur_dir+"/main.cpp|112|5|    VAL2_0,"],
["VAL2_0|"+cur_dir+"/main.cpp|112|5|    VAL2_0,"],
[""],
# 113 5
["VAL2_1|"+cur_dir+"/main.cpp|113|5|    VAL2_1,"],
["VAL2_1|"+cur_dir+"/main.cpp|113|5|    VAL2_1,"],
["VAL2_1|"+cur_dir+"/main.cpp|115|15|namedEnum e = VAL2_1;"],
# 115 5
["namedEnum|"+cur_dir+"/main.cpp|111|6|enum namedEnum {"],
["namedEnum|"+cur_dir+"/main.cpp|111|6|enum namedEnum {"],
["namedEnum|"+cur_dir+"/main.cpp|115|1|namedEnum e = VAL2_1;"],
# 115 15
["VAL2_1|"+cur_dir+"/main.cpp|113|5|    VAL2_1,"],
["VAL2_1|"+cur_dir+"/main.cpp|113|5|    VAL2_1,"],
["VAL2_1|"+cur_dir+"/main.cpp|115|15|namedEnum e = VAL2_1;"],
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
