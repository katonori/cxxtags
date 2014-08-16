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
# TODO: add def test
"decl " + db_dir + " " + cur_dir + "/main.cpp 5 9",
"def " + db_dir + " " + cur_dir + "/main.cpp 5 9",
"ref " + db_dir + " " + cur_dir + "/main.cpp 5 9",

"decl " + db_dir + " " + cur_dir+"/main.cpp 6 6",
"def " + db_dir + " " + cur_dir+"/main.cpp 6 6",
"ref " + db_dir + " " + cur_dir+"/main.cpp 6 6",

"decl " + db_dir + " " + cur_dir+"/main.cpp 6 10",
"def " + db_dir + " " + cur_dir+"/main.cpp 6 10",
"ref " + db_dir + " " + cur_dir+"/main.cpp 6 10",

"decl " + db_dir + " " + cur_dir+"/main.cpp 7 5",
"def " + db_dir + " " + cur_dir+"/main.cpp 7 5",
"ref " + db_dir + " " + cur_dir+"/main.cpp 7 5",

"decl " + db_dir + " " + cur_dir+"/main.cpp 9 23",
"def " + db_dir + " " + cur_dir+"/main.cpp 9 23",
"ref " + db_dir + " " + cur_dir+"/main.cpp 9 23",

"decl " + db_dir + " " + cur_dir+"/main.cpp 10 5",
"def " + db_dir + " " + cur_dir+"/main.cpp 10 5",
"ref " + db_dir + " " + cur_dir+"/main.cpp 10 5",

"decl " + db_dir + " " + cur_dir+"/main.cpp 11 5",
"def " + db_dir + " " + cur_dir+"/main.cpp 11 5",
"ref " + db_dir + " " + cur_dir+"/main.cpp 11 5",

"decl " + db_dir + " " + cur_dir+"/main.cpp 12 5",
"def " + db_dir + " " + cur_dir+"/main.cpp 12 5",
"ref " + db_dir + " " + cur_dir+"/main.cpp 12 5",

"decl " + db_dir + " " + cur_dir+"/main.cpp 13 5",
"def " + db_dir + " " + cur_dir+"/main.cpp 13 5",
"ref " + db_dir + " " + cur_dir+"/main.cpp 13 5",

"decl " + db_dir + " " + cur_dir+"/main.cpp 13 10",
"def " + db_dir + " " + cur_dir+"/main.cpp 13 10",
"ref " + db_dir + " " + cur_dir+"/main.cpp 13 10",

"decl " + db_dir + " " + cur_dir+"/main.cpp 13 13",
"def " + db_dir + " " + cur_dir+"/main.cpp 13 13",
"ref " + db_dir + " " + cur_dir+"/main.cpp 13 13",

"decl " + db_dir + " " + cur_dir+"/main.cpp 14 5",
"def " + db_dir + " " + cur_dir+"/main.cpp 14 5",
"ref " + db_dir + " " + cur_dir+"/main.cpp 14 5",

"decl " + db_dir + " " + cur_dir+"/main.cpp 14 10",
"def " + db_dir + " " + cur_dir+"/main.cpp 14 10",
"ref " + db_dir + " " + cur_dir+"/main.cpp 14 10",

"decl " + db_dir + " " + cur_dir+"/main.cpp 14 13",
"def " + db_dir + " " + cur_dir+"/main.cpp 14 13",
"ref " + db_dir + " " + cur_dir+"/main.cpp 14 13",

"decl " + db_dir + " " + cur_dir+"/main.cpp 15 5",
"def " + db_dir + " " + cur_dir+"/main.cpp 15 5",
"ref " + db_dir + " " + cur_dir+"/main.cpp 15 5",

"decl " + db_dir + " " + cur_dir+"/main.cpp 15 10",
"def " + db_dir + " " + cur_dir+"/main.cpp 15 10",
"ref " + db_dir + " " + cur_dir+"/main.cpp 15 10",

"decl " + db_dir + " " + cur_dir+"/main.cpp 15 13",
"def " + db_dir + " " + cur_dir+"/main.cpp 15 13",
"ref " + db_dir + " " + cur_dir+"/main.cpp 15 13",

"decl " + db_dir + " " + cur_dir+"/main.cpp 16 5",
"def " + db_dir + " " + cur_dir+"/main.cpp 16 5",
"ref " + db_dir + " " + cur_dir+"/main.cpp 16 5",

"decl " + db_dir + " " + cur_dir+"/main.cpp 16 10",
"def " + db_dir + " " + cur_dir+"/main.cpp 16 10",
"ref " + db_dir + " " + cur_dir+"/main.cpp 16 10",

"decl " + db_dir + " " + cur_dir+"/main.cpp 16 13",
"def " + db_dir + " " + cur_dir+"/main.cpp 16 13",
"ref " + db_dir + " " + cur_dir+"/main.cpp 16 13",

"decl " + db_dir + " " + cur_dir+"/main.cpp 17 5",
"def " + db_dir + " " + cur_dir+"/main.cpp 17 5",
"ref " + db_dir + " " + cur_dir+"/main.cpp 17 5",

"decl " + db_dir + " " + cur_dir+"/main.cpp 17 9",
"def " + db_dir + " " + cur_dir+"/main.cpp 17 9",
"ref " + db_dir + " " + cur_dir+"/main.cpp 17 9",

"decl " + db_dir + " " + cur_dir+"/main.cpp 18 5",
"def " + db_dir + " " + cur_dir+"/main.cpp 18 5",
"ref " + db_dir + " " + cur_dir+"/main.cpp 18 5",

"decl " + db_dir + " " + cur_dir+"/main.cpp 18 9",
"def " + db_dir + " " + cur_dir+"/main.cpp 18 9",
"ref " + db_dir + " " + cur_dir+"/main.cpp 18 9",

"decl " + db_dir + " " + cur_dir+"/main.cpp 19 5",
"def " + db_dir + " " + cur_dir+"/main.cpp 19 5",
"ref " + db_dir + " " + cur_dir+"/main.cpp 19 5",

"decl " + db_dir + " " + cur_dir+"/main.cpp 19 9",
"def " + db_dir + " " + cur_dir+"/main.cpp 19 9",
"ref " + db_dir + " " + cur_dir+"/main.cpp 19 9",

"decl " + db_dir + " " + cur_dir+"/main.cpp 20 5",
"def " + db_dir + " " + cur_dir+"/main.cpp 20 5",
"ref " + db_dir + " " + cur_dir+"/main.cpp 20 5",

"decl " + db_dir + " " + cur_dir+"/main.cpp 20 9",
"def " + db_dir + " " + cur_dir+"/main.cpp 20 9",
"ref " + db_dir + " " + cur_dir+"/main.cpp 20 9",

"decl " + db_dir + " " + cur_dir+"/main.cpp 21 25",
"def " + db_dir + " " + cur_dir+"/main.cpp 21 25",
"ref " + db_dir + " " + cur_dir+"/main.cpp 21 25",

"decl " + db_dir + " " + cur_dir+"/main.cpp 22 37",
"def " + db_dir + " " + cur_dir+"/main.cpp 22 37",
"ref " + db_dir + " " + cur_dir+"/main.cpp 22 37",

# ns0.h
"decl " + db_dir + " " + cur_dir+"/subdir/ns0.h 2 11",
"def " + db_dir + " " + cur_dir+"/subdir/ns0.h 2 11",
"ref " + db_dir + " " + cur_dir+"/subdir/ns0.h 2 11",

"decl " + db_dir + " " + cur_dir+"/subdir/ns0.h 3 17",
"def " + db_dir + " " + cur_dir+"/subdir/ns0.h 3 17",
"ref " + db_dir + " " + cur_dir+"/subdir/ns0.h 3 17",

"decl " + db_dir + " " + cur_dir+"/subdir/ns0.h 4 11",
"def " + db_dir + " " + cur_dir+"/subdir/ns0.h 4 11",
"ref " + db_dir + " " + cur_dir+"/subdir/ns0.h 4 11",

"decl " + db_dir + " " + cur_dir+"/subdir/ns0.h 6 9",
"def " + db_dir + " " + cur_dir+"/subdir/ns0.h 6 9",
"ref " + db_dir + " " + cur_dir+"/subdir/ns0.h 6 9",

"decl " + db_dir + " " + cur_dir+"/subdir/ns0.h 7 13",
"def " + db_dir + " " + cur_dir+"/subdir/ns0.h 7 13",
"ref " + db_dir + " " + cur_dir+"/subdir/ns0.h 7 13",

"decl " + db_dir + " " + cur_dir+"/subdir/ns0.h 9 13",
"def " + db_dir + " " + cur_dir+"/subdir/ns0.h 9 13",
"ref " + db_dir + " " + cur_dir+"/subdir/ns0.h 9 13",

"decl " + db_dir + " " + cur_dir+"/subdir/ns0.h 11 11",
"def " + db_dir + " " + cur_dir+"/subdir/ns0.h 11 11",
"ref " + db_dir + " " + cur_dir+"/subdir/ns0.h 11 11",

"decl " + db_dir + " " + cur_dir+"/subdir/ns0.h 13 9",
"def " + db_dir + " " + cur_dir+"/subdir/ns0.h 13 9",
"ref " + db_dir + " " + cur_dir+"/subdir/ns0.h 13 9",

"decl " + db_dir + " " + cur_dir+"/subdir/ns0.h 14 9",
"def " + db_dir + " " + cur_dir+"/subdir/ns0.h 14 9",
"ref " + db_dir + " " + cur_dir+"/subdir/ns0.h 14 9",

"decl " + db_dir + " " + cur_dir+"/subdir/ns0.h 14 15",
"def " + db_dir + " " + cur_dir+"/subdir/ns0.h 14 15",
"ref " + db_dir + " " + cur_dir+"/subdir/ns0.h 14 15",

"decl " + db_dir + " " + cur_dir+"/subdir/ns0.h 15 9",
"def " + db_dir + " " + cur_dir+"/subdir/ns0.h 15 9",
"ref " + db_dir + " " + cur_dir+"/subdir/ns0.h 15 9",

"decl " + db_dir + " " + cur_dir+"/subdir/ns0.h 15 12",
"def " + db_dir + " " + cur_dir+"/subdir/ns0.h 15 12",
"ref " + db_dir + " " + cur_dir+"/subdir/ns0.h 15 12",

"decl " + db_dir + " " + cur_dir+"/subdir/ns0.h 17 13",
"def " + db_dir + " " + cur_dir+"/subdir/ns0.h 17 13",
"ref " + db_dir + " " + cur_dir+"/subdir/ns0.h 17 13",

# ns1.h
"decl " + db_dir + " " + cur_dir+"/ns1.h 2 11",
"def " + db_dir + " " + cur_dir+"/ns1.h 2 11",
"ref " + db_dir + " " + cur_dir+"/ns1.h 2 11",

"decl " + db_dir + " " + cur_dir+"/ns1.h 3 11",
"def " + db_dir + " " + cur_dir+"/ns1.h 3 11",
"ref " + db_dir + " " + cur_dir+"/ns1.h 3 11",

"decl " + db_dir + " " + cur_dir+"/ns1.h 5 9",
"def " + db_dir + " " + cur_dir+"/ns1.h 5 9",
"ref " + db_dir + " " + cur_dir+"/ns1.h 5 9",

"decl " + db_dir + " " + cur_dir+"/ns1.h 5 21",
"def " + db_dir + " " + cur_dir+"/ns1.h 5 21",
"ref " + db_dir + " " + cur_dir+"/ns1.h 5 21",

"decl " + db_dir + " " + cur_dir+"/ns1.h 6 14",
"def " + db_dir + " " + cur_dir+"/ns1.h 6 14",
"ref " + db_dir + " " + cur_dir+"/ns1.h 6 14",

"decl " + db_dir + " " + cur_dir+"/ns1.h 8 13",
"def " + db_dir + " " + cur_dir+"/ns1.h 8 13",
"ref " + db_dir + " " + cur_dir+"/ns1.h 8 13",

"decl " + db_dir + " " + cur_dir+"/ns1.h 10 11",
"def " + db_dir + " " + cur_dir+"/ns1.h 10 11",
"ref " + db_dir + " " + cur_dir+"/ns1.h 10 11",

"decl " + db_dir + " " + cur_dir+"/ns1.h 12 9",
"def " + db_dir + " " + cur_dir+"/ns1.h 12 9",
"ref " + db_dir + " " + cur_dir+"/ns1.h 12 9",

"decl " + db_dir + " " + cur_dir+"/ns1.h 13 14",
"def " + db_dir + " " + cur_dir+"/ns1.h 13 14",
"ref " + db_dir + " " + cur_dir+"/ns1.h 13 14",

"decl " + db_dir + " " + cur_dir+"/ns1.h 15 13",
"def " + db_dir + " " + cur_dir+"/ns1.h 15 13",
"ref " + db_dir + " " + cur_dir+"/ns1.h 15 13",

# ns1.cpp
"decl " + db_dir + " " + cur_dir+"/subdir/ns1.cpp 2 11",
"def " + db_dir + " " + cur_dir+"/subdir/ns1.cpp 2 11",
"ref " + db_dir + " " + cur_dir+"/subdir/ns1.cpp 2 11",

"decl " + db_dir + " " + cur_dir+"/subdir/ns1.cpp 3 10",
"def " + db_dir + " " + cur_dir+"/subdir/ns1.cpp 3 10",
"ref " + db_dir + " " + cur_dir+"/subdir/ns1.cpp 3 10",

"decl " + db_dir + " " + cur_dir+"/subdir/ns1.cpp 3 14",
"def " + db_dir + " " + cur_dir+"/subdir/ns1.cpp 3 14",
"ref " + db_dir + " " + cur_dir+"/subdir/ns1.cpp 3 14",

"decl " + db_dir + " " + cur_dir+"/subdir/ns1.cpp 5 35",
"def " + db_dir + " " + cur_dir+"/subdir/ns1.cpp 5 35",
"ref " + db_dir + " " + cur_dir+"/subdir/ns1.cpp 5 35",

"decl " + db_dir + " " + cur_dir+"/subdir/ns1.cpp 7 10",
"def " + db_dir + " " + cur_dir+"/subdir/ns1.cpp 7 10",
"ref " + db_dir + " " + cur_dir+"/subdir/ns1.cpp 7 10",

"decl " + db_dir + " " + cur_dir+"/subdir/ns1.cpp 7 14",
"def " + db_dir + " " + cur_dir+"/subdir/ns1.cpp 7 14",
"ref " + db_dir + " " + cur_dir+"/subdir/ns1.cpp 7 14",

"decl " + db_dir + " " + cur_dir+"/subdir/ns1.cpp 9 35",
"def " + db_dir + " " + cur_dir+"/subdir/ns1.cpp 9 35",
"ref " + db_dir + " " + cur_dir+"/subdir/ns1.cpp 9 35",

# ns0.cpp
"decl " + db_dir + " " + cur_dir+"/ns0.cpp 2 11",
"def " + db_dir + " " + cur_dir+"/ns0.cpp 2 11",
"ref " + db_dir + " " + cur_dir+"/ns0.cpp 2 11",

"decl " + db_dir + " " + cur_dir+"/ns0.cpp 3 9",
"def " + db_dir + " " + cur_dir+"/ns0.cpp 3 9",
"ref " + db_dir + " " + cur_dir+"/ns0.cpp 3 9",

"decl " + db_dir + " " + cur_dir+"/ns0.cpp 3 13",
"def " + db_dir + " " + cur_dir+"/ns0.cpp 3 13",
"ref " + db_dir + " " + cur_dir+"/ns0.cpp 3 13",

"decl " + db_dir + " " + cur_dir+"/ns0.cpp 5 35",
"def " + db_dir + " " + cur_dir+"/ns0.cpp 5 35",
"ref " + db_dir + " " + cur_dir+"/ns0.cpp 5 35",

"decl " + db_dir + " " + cur_dir+"/ns0.cpp 6 16",
"def " + db_dir + " " + cur_dir+"/ns0.cpp 6 16",
"ref " + db_dir + " " + cur_dir+"/ns0.cpp 6 16",

"decl " + db_dir + " " + cur_dir+"/ns0.cpp 8 5",
"def " + db_dir + " " + cur_dir+"/ns0.cpp 8 5",
"ref " + db_dir + " " + cur_dir+"/ns0.cpp 8 5",

"decl " + db_dir + " " + cur_dir+"/ns0.cpp 8 11",
"def " + db_dir + " " + cur_dir+"/ns0.cpp 8 11",
"ref " + db_dir + " " + cur_dir+"/ns0.cpp 8 11",

"decl " + db_dir + " " + cur_dir+"/ns0.cpp 8 15",
"def " + db_dir + " " + cur_dir+"/ns0.cpp 8 15",
"ref " + db_dir + " " + cur_dir+"/ns0.cpp 8 15",

"decl " + db_dir + " " + cur_dir+"/ns0.cpp 10 35",
"def " + db_dir + " " + cur_dir+"/ns0.cpp 10 35",
"ref " + db_dir + " " + cur_dir+"/ns0.cpp 10 35",

"decl " + db_dir + " " + cur_dir+"/ns0.cpp 11 16",
"def " + db_dir + " " + cur_dir+"/ns0.cpp 11 16",
"ref " + db_dir + " " + cur_dir+"/ns0.cpp 11 16",

"decl " + db_dir + " " + cur_dir+"/ns0.cpp 13 5",
"def " + db_dir + " " + cur_dir+"/ns0.cpp 13 5",
"ref " + db_dir + " " + cur_dir+"/ns0.cpp 13 5",

"decl " + db_dir + " " + cur_dir+"/ns0.cpp 13 8",
"def " + db_dir + " " + cur_dir+"/ns0.cpp 13 8",
"ref " + db_dir + " " + cur_dir+"/ns0.cpp 13 8",

"decl " + db_dir + " " + cur_dir+"/ns0.cpp 13 12",
"def " + db_dir + " " + cur_dir+"/ns0.cpp 13 12",
"ref " + db_dir + " " + cur_dir+"/ns0.cpp 13 12",

"decl " + db_dir + " " + cur_dir+"/ns0.cpp 17 10",
"def " + db_dir + " " + cur_dir+"/ns0.cpp 17 10",
"ref " + db_dir + " " + cur_dir+"/ns0.cpp 17 10",

"decl " + db_dir + " " + cur_dir+"/ns0.cpp 20 10",
"def " + db_dir + " " + cur_dir+"/ns0.cpp 20 10",
"ref " + db_dir + " " + cur_dir+"/ns0.cpp 20 10",

"decl " + db_dir + " " + cur_dir+"/ns0.cpp 20 19",
"def " + db_dir + " " + cur_dir+"/ns0.cpp 20 19",
"ref " + db_dir + " " + cur_dir+"/ns0.cpp 20 19",
]

a_list = [
# main.cpp
["BUFF_SIZE|"+cur_dir+"/main.cpp|5|9|#define BUFF_SIZE 256"],
[""],
["BUFF_SIZE|"+cur_dir+"/main.cpp|6|10|char msg[BUFF_SIZE] = \"MESSAGE\\n\";"],

["msg|"+cur_dir+"/main.cpp|6|6|char msg[BUFF_SIZE] = \"MESSAGE\\n\";"],
["msg|"+cur_dir+"/main.cpp|6|6|char msg[BUFF_SIZE] = \"MESSAGE\\n\";"],
["msg|"+cur_dir+"/main.cpp|21|25|    printf(\"AAA: %s\\n\", msg);"],

["BUFF_SIZE|"+cur_dir+"/main.cpp|5|9|#define BUFF_SIZE 256"],
[""],
["BUFF_SIZE|"+cur_dir+"/main.cpp|6|10|char msg[BUFF_SIZE] = \"MESSAGE\\n\";"],

["main|"+cur_dir+"/main.cpp|7|5|int main()"],
["main|"+cur_dir+"/main.cpp|7|5|int main()"],
[""],

["vec|"+cur_dir+"/main.cpp|9|23|    std::vector<int > vec;"],
["vec|"+cur_dir+"/main.cpp|9|23|    std::vector<int > vec;"],
[
"vec|"+cur_dir+"/main.cpp|10|5|    vec.push_back(1);",
"vec|"+cur_dir+"/main.cpp|11|5|    vec.push_back(2);",
"vec|"+cur_dir+"/main.cpp|12|5|    vec.push_back(3);",
"vec|"+cur_dir+"/main.cpp|22|41|    for(std::vector<int >::iterator i = vec.begin();",
"vec|"+cur_dir+"/main.cpp|23|10|    i != vec.end();",
],

["vec|"+cur_dir+"/main.cpp|9|23|    std::vector<int > vec;"],
["vec|"+cur_dir+"/main.cpp|9|23|    std::vector<int > vec;"],
[
"vec|"+cur_dir+"/main.cpp|10|5|    vec.push_back(1);",
"vec|"+cur_dir+"/main.cpp|11|5|    vec.push_back(2);",
"vec|"+cur_dir+"/main.cpp|12|5|    vec.push_back(3);",
"vec|"+cur_dir+"/main.cpp|22|41|    for(std::vector<int >::iterator i = vec.begin();",
"vec|"+cur_dir+"/main.cpp|23|10|    i != vec.end();",
],

["vec|"+cur_dir+"/main.cpp|9|23|    std::vector<int > vec;"],
["vec|"+cur_dir+"/main.cpp|9|23|    std::vector<int > vec;"],
[
"vec|"+cur_dir+"/main.cpp|10|5|    vec.push_back(1);",
"vec|"+cur_dir+"/main.cpp|11|5|    vec.push_back(2);",
"vec|"+cur_dir+"/main.cpp|12|5|    vec.push_back(3);",
"vec|"+cur_dir+"/main.cpp|22|41|    for(std::vector<int >::iterator i = vec.begin();",
"vec|"+cur_dir+"/main.cpp|23|10|    i != vec.end();",
],

["vec|"+cur_dir+"/main.cpp|9|23|    std::vector<int > vec;"],
["vec|"+cur_dir+"/main.cpp|9|23|    std::vector<int > vec;"],
[
"vec|"+cur_dir+"/main.cpp|10|5|    vec.push_back(1);",
"vec|"+cur_dir+"/main.cpp|11|5|    vec.push_back(2);",
"vec|"+cur_dir+"/main.cpp|12|5|    vec.push_back(3);",
"vec|"+cur_dir+"/main.cpp|22|41|    for(std::vector<int >::iterator i = vec.begin();",
"vec|"+cur_dir+"/main.cpp|23|10|    i != vec.end();",
],
# 13 5
[
"NS0|"+cur_dir+"/subdir/ns0.h|2|11|namespace NS0 {",
],
[
"NS0|"+cur_dir+"/subdir/ns0.h|2|11|namespace NS0 {",
"NS0|"+cur_dir+"/ns0.cpp|2|11|namespace NS0 {",
],
[
"NS0|"+cur_dir+"/main.cpp|13|5|    NS0::C0 c00(0);",
"NS0|"+cur_dir+"/main.cpp|15|5|    NS0::C1 c01(2);",
],
# 13 10
["C0|"+cur_dir+"/subdir/ns0.h|4|11|    class C0 {"],
["C0|"+cur_dir+"/subdir/ns0.h|4|11|    class C0 {"],
[
"C0|"+cur_dir+"/main.cpp|13|10|    NS0::C0 c00(0);",
"C0|"+cur_dir+"/ns0.cpp|3|9|    int C0::check()",
],
# 13 13
["c00|"+cur_dir+"/main.cpp|13|13|    NS0::C0 c00(0);"],
["c00|"+cur_dir+"/main.cpp|13|13|    NS0::C0 c00(0);"],
[
"c00|"+cur_dir+"/main.cpp|17|5|    c00.check();",
],
# 14 5
[
"NS1|"+cur_dir+"/ns1.h|2|11|namespace NS1 {",
],
[
"NS1|"+cur_dir+"/ns1.h|2|11|namespace NS1 {",
"NS1|"+cur_dir+"/subdir/ns1.cpp|2|11|namespace NS1 {",
],
[
"NS1|"+cur_dir+"/main.cpp|14|5|    NS1::C0 c10(1);",
"NS1|"+cur_dir+"/main.cpp|16|5|    NS1::C1 c11(3);",
],
# 14 10
["C0|"+cur_dir+"/ns1.h|3|11|    class C0 {"],
["C0|"+cur_dir+"/ns1.h|3|11|    class C0 {"],
[
"C0|"+cur_dir+"/main.cpp|14|10|    NS1::C0 c10(1);",
"C0|"+cur_dir+"/subdir/ns1.cpp|3|10|    void C0::check()",
],
# 14 13
["c10|"+cur_dir+"/main.cpp|14|13|    NS1::C0 c10(1);"],
["c10|"+cur_dir+"/main.cpp|14|13|    NS1::C0 c10(1);"],
["c10|"+cur_dir+"/main.cpp|18|5|    c10.check();"],
# 15 5
[
"NS0|"+cur_dir+"/subdir/ns0.h|2|11|namespace NS0 {",
],
[
"NS0|"+cur_dir+"/subdir/ns0.h|2|11|namespace NS0 {",
"NS0|"+cur_dir+"/ns0.cpp|2|11|namespace NS0 {",
],
[
"NS0|"+cur_dir+"/main.cpp|13|5|    NS0::C0 c00(0);",
"NS0|"+cur_dir+"/main.cpp|15|5|    NS0::C1 c01(2);",
],
# 15 10
["C1|"+cur_dir+"/subdir/ns0.h|11|11|    class C1 {"],
["C1|"+cur_dir+"/subdir/ns0.h|11|11|    class C1 {"],
[
"C1|"+cur_dir+"/main.cpp|15|10|    NS0::C1 c01(2);",
"C1|"+cur_dir+"/ns0.cpp|8|11|    MYINT C1::check() const",
"C1|"+cur_dir+"/ns0.cpp|13|5|    C1 C1::check2()",
"C1|"+cur_dir+"/ns0.cpp|13|8|    C1 C1::check2()",
"C1|"+cur_dir+"/subdir/ns0.h|15|9|        C1 check2();",
],
# 15 13
["c01|"+cur_dir+"/main.cpp|15|13|    NS0::C1 c01(2);"],
["c01|"+cur_dir+"/main.cpp|15|13|    NS0::C1 c01(2);"],
["c01|"+cur_dir+"/main.cpp|19|5|    c01.check();"],
# 16 5
[
"NS1|"+cur_dir+"/ns1.h|2|11|namespace NS1 {",
],
[
"NS1|"+cur_dir+"/ns1.h|2|11|namespace NS1 {",
"NS1|"+cur_dir+"/subdir/ns1.cpp|2|11|namespace NS1 {",
],
[
"NS1|"+cur_dir+"/main.cpp|14|5|    NS1::C0 c10(1);",
"NS1|"+cur_dir+"/main.cpp|16|5|    NS1::C1 c11(3);",
],
# 16 10
["C1|"+cur_dir+"/ns1.h|10|11|    class C1 {"],
["C1|"+cur_dir+"/ns1.h|10|11|    class C1 {"],
[
"C1|"+cur_dir+"/main.cpp|16|10|    NS1::C1 c11(3);",
"C1|"+cur_dir+"/subdir/ns1.cpp|7|10|    void C1::check()",
],
# 16 13
["c11|"+cur_dir+"/main.cpp|16|13|    NS1::C1 c11(3);"],
["c11|"+cur_dir+"/main.cpp|16|13|    NS1::C1 c11(3);"],
["c11|"+cur_dir+"/main.cpp|20|5|    c11.check();"],
# 17 5
["c00|"+cur_dir+"/main.cpp|13|13|    NS0::C0 c00(0);"],
["c00|"+cur_dir+"/main.cpp|13|13|    NS0::C0 c00(0);"],
[
"c00|"+cur_dir+"/main.cpp|17|5|    c00.check();",
],
# 17 9
["check|"+cur_dir+"/subdir/ns0.h|7|13|        int check();"],
["check|"+cur_dir+"/ns0.cpp|3|13|    int C0::check()"],
[
"check|"+cur_dir+"/main.cpp|17|9|    c00.check();",
],
# 18 5
["c10|"+cur_dir+"/main.cpp|14|13|    NS1::C0 c10(1);"],
["c10|"+cur_dir+"/main.cpp|14|13|    NS1::C0 c10(1);"],
[
"c10|"+cur_dir+"/main.cpp|18|5|    c10.check();",
],
# 18 9
["check|"+cur_dir+"/ns1.h|6|14|        void check();"],
["check|"+cur_dir+"/subdir/ns1.cpp|3|14|    void C0::check()"],
[
"check|"+cur_dir+"/main.cpp|18|9|    c10.check();",
],
# 19 5
["c01|"+cur_dir+"/main.cpp|15|13|    NS0::C1 c01(2);"],
["c01|"+cur_dir+"/main.cpp|15|13|    NS0::C1 c01(2);"],
["c01|"+cur_dir+"/main.cpp|19|5|    c01.check();"],
# 19 9
["check|"+cur_dir+"/subdir/ns0.h|14|15|        MYINT check() const;"],
["check|"+cur_dir+"/ns0.cpp|8|15|    MYINT C1::check() const"],
["check|"+cur_dir+"/main.cpp|19|9|    c01.check();"],
# 20 5
["c11|"+cur_dir+"/main.cpp|16|13|    NS1::C1 c11(3);"],
["c11|"+cur_dir+"/main.cpp|16|13|    NS1::C1 c11(3);"],
["c11|"+cur_dir+"/main.cpp|20|5|    c11.check();"],
# 20 9
["check|"+cur_dir+"/ns1.h|13|14|        void check();"],
["check|"+cur_dir+"/subdir/ns1.cpp|7|14|    void C1::check()"],
["check|"+cur_dir+"/main.cpp|20|9|    c11.check();"],
# 21 25
["msg|"+cur_dir+"/main.cpp|6|6|char msg[BUFF_SIZE] = \"MESSAGE\\n\";"],
[r'msg|'+cur_dir+r'/main.cpp|6|6|char msg[BUFF_SIZE] = "MESSAGE\n";'],
["msg|"+cur_dir+"/main.cpp|21|25|    printf(\"AAA: %s\\n\", msg);"],
# 22 37
["i|"+cur_dir+"/main.cpp|22|37|    for(std::vector<int >::iterator i = vec.begin();"],
["i|"+cur_dir+"/main.cpp|22|37|    for(std::vector<int >::iterator i = vec.begin();"],
[
"i|"+cur_dir+"/main.cpp|23|5|    i != vec.end();",
"i|"+cur_dir+"/main.cpp|24|5|    i++){",
"i|"+cur_dir+"/main.cpp|25|25|        printf(\"%d\\n\", *i);",
],

# ns0.h
# 2 11
[
#"NS0|"+cur_dir+"/subdir/ns0.h|2|11|namespace NS0 {",
"NS0|"+cur_dir+"/ns0.cpp|2|11|namespace NS0 {",
],
[
"NS0|"+cur_dir+"/subdir/ns0.h|2|11|namespace NS0 {",
"NS0|"+cur_dir+"/ns0.cpp|2|11|namespace NS0 {",
],
[
"NS0|"+cur_dir+"/main.cpp|13|5|    NS0::C0 c00(0);",
"NS0|"+cur_dir+"/main.cpp|15|5|    NS0::C1 c01(2);",
],
# 3 17
["MYINT|"+cur_dir+"/subdir/ns0.h|3|17|    typedef int MYINT ;"],
["MYINT|"+cur_dir+"/subdir/ns0.h|3|17|    typedef int MYINT ;"],
[
"MYINT|"+cur_dir+"/subdir/ns0.h|14|9|        MYINT check() const;",
"MYINT|"+cur_dir+"/ns0.cpp|8|5|    MYINT C1::check() const",
],
# 4 11
["C0|"+cur_dir+"/subdir/ns0.h|4|11|    class C0 {"],
["C0|"+cur_dir+"/subdir/ns0.h|4|11|    class C0 {"],
[
"C0|"+cur_dir+"/main.cpp|13|10|    NS0::C0 c00(0);",
"C0|"+cur_dir+"/ns0.cpp|3|9|    int C0::check()",
],
# 6 9
["C0|"+cur_dir+"/subdir/ns0.h|6|9|        C0(int a) : m_val(a) {}"],
["C0|"+cur_dir+"/subdir/ns0.h|6|9|        C0(int a) : m_val(a) {}"],
[
""
],
# 7 13
["check|"+cur_dir+"/subdir/ns0.h|7|13|        int check();"],
["check|"+cur_dir+"/ns0.cpp|3|13|    int C0::check()"],
[
"check|"+cur_dir+"/main.cpp|17|9|    c00.check();",
],
# 9 13
["m_val|"+cur_dir+"/subdir/ns0.h|9|13|        int m_val;"],
["m_val|"+cur_dir+"/subdir/ns0.h|9|13|        int m_val;"],
[
"m_val|"+cur_dir+"/subdir/ns0.h|6|21|        C0(int a) : m_val(a) {}",
"m_val|"+cur_dir+"/ns0.cpp|5|35|        printf(\"C0: val is %d\\n\", m_val);",
"m_val|"+cur_dir+"/ns0.cpp|6|16|        return m_val;",
],
# 11 11
["C1|"+cur_dir+"/subdir/ns0.h|11|11|    class C1 {"],
["C1|"+cur_dir+"/subdir/ns0.h|11|11|    class C1 {"],
[
"C1|"+cur_dir+"/main.cpp|15|10|    NS0::C1 c01(2);",
"C1|"+cur_dir+"/ns0.cpp|8|11|    MYINT C1::check() const",
"C1|"+cur_dir+"/ns0.cpp|13|5|    C1 C1::check2()",
"C1|"+cur_dir+"/ns0.cpp|13|8|    C1 C1::check2()",
"C1|"+cur_dir+"/subdir/ns0.h|15|9|        C1 check2();",
],
# 13 9
["C1|"+cur_dir+"/subdir/ns0.h|13|9|        C1(int a) : m_val(a) {}"],
["C1|"+cur_dir+"/subdir/ns0.h|13|9|        C1(int a) : m_val(a) {}"],
[
""
],
# 14 9
["MYINT|"+cur_dir+"/subdir/ns0.h|3|17|    typedef int MYINT ;"],
["MYINT|"+cur_dir+"/subdir/ns0.h|3|17|    typedef int MYINT ;"],
[
"MYINT|"+cur_dir+"/subdir/ns0.h|14|9|        MYINT check() const;",
"MYINT|"+cur_dir+"/ns0.cpp|8|5|    MYINT C1::check() const",
],
# 14 15
["check|"+cur_dir+"/subdir/ns0.h|14|15|        MYINT check() const;"],
["check|"+cur_dir+"/ns0.cpp|8|15|    MYINT C1::check() const"],
["check|"+cur_dir+"/main.cpp|19|9|    c01.check();"],
# 15 9
["C1|"+cur_dir+"/subdir/ns0.h|11|11|    class C1 {"],
["C1|"+cur_dir+"/subdir/ns0.h|11|11|    class C1 {"],
[
"C1|"+cur_dir+"/main.cpp|15|10|    NS0::C1 c01(2);",
"C1|"+cur_dir+"/ns0.cpp|8|11|    MYINT C1::check() const",
"C1|"+cur_dir+"/ns0.cpp|13|5|    C1 C1::check2()",
"C1|"+cur_dir+"/ns0.cpp|13|8|    C1 C1::check2()",
"C1|"+cur_dir+"/subdir/ns0.h|15|9|        C1 check2();",
],
# 15 12
["check2|"+cur_dir+"/subdir/ns0.h|15|12|        C1 check2();"],
["check2|"+cur_dir+"/ns0.cpp|13|12|    C1 C1::check2()"],
[
""
],
# 17 13
["m_val|"+cur_dir+"/subdir/ns0.h|17|13|        int m_val;"],
["m_val|"+cur_dir+"/subdir/ns0.h|17|13|        int m_val;"],
[
"m_val|"+cur_dir+"/subdir/ns0.h|13|21|        C1(int a) : m_val(a) {}",
"m_val|"+cur_dir+"/ns0.cpp|10|35|        printf(\"C1: val is %d\\n\", m_val);",
"m_val|"+cur_dir+"/ns0.cpp|11|16|        return m_val;",
],

# ns1.h
# 2 11
[
#"NS1|"+cur_dir+"/ns1.h|2|11|namespace NS1 {",
"NS1|"+cur_dir+"/subdir/ns1.cpp|2|11|namespace NS1 {",
],
[
"NS1|"+cur_dir+"/ns1.h|2|11|namespace NS1 {",
"NS1|"+cur_dir+"/subdir/ns1.cpp|2|11|namespace NS1 {",
],
[
"NS1|"+cur_dir+"/main.cpp|14|5|    NS1::C0 c10(1);",
"NS1|"+cur_dir+"/main.cpp|16|5|    NS1::C1 c11(3);",
],
# 3 11
["C0|"+cur_dir+"/ns1.h|3|11|    class C0 {"],
["C0|"+cur_dir+"/ns1.h|3|11|    class C0 {"],
[
"C0|"+cur_dir+"/main.cpp|14|10|    NS1::C0 c10(1);",
"C0|"+cur_dir+"/subdir/ns1.cpp|3|10|    void C0::check()",
],
# 5 9
["C0|"+cur_dir+"/ns1.h|5|9|        C0(int a) : m_val(a) {}"],
["C0|"+cur_dir+"/ns1.h|5|9|        C0(int a) : m_val(a) {}"],
[
""
],
# 5 21
["m_val|"+cur_dir+"/ns1.h|8|13|        int m_val;"],
["m_val|"+cur_dir+"/ns1.h|8|13|        int m_val;"],
[
"m_val|"+cur_dir+"/ns1.h|5|21|        C0(int a) : m_val(a) {}",
"m_val|"+cur_dir+"/subdir/ns1.cpp|5|35|        printf(\"C0: val is %d\\n\", m_val);",
],
# 6 14
["check|"+cur_dir+"/ns1.h|6|14|        void check();"],
["check|"+cur_dir+"/subdir/ns1.cpp|3|14|    void C0::check()"],
["check|"+cur_dir+"/main.cpp|18|9|    c10.check();"],
# 8 13
["m_val|"+cur_dir+"/ns1.h|8|13|        int m_val;"],
["m_val|"+cur_dir+"/ns1.h|8|13|        int m_val;"],
[
"m_val|"+cur_dir+"/ns1.h|5|21|        C0(int a) : m_val(a) {}",
"m_val|"+cur_dir+"/subdir/ns1.cpp|5|35|        printf(\"C0: val is %d\\n\", m_val);",
],
# 10 11
["C1|"+cur_dir+"/ns1.h|10|11|    class C1 {"],
["C1|"+cur_dir+"/ns1.h|10|11|    class C1 {"],
[
"C1|"+cur_dir+"/main.cpp|16|10|    NS1::C1 c11(3);",
"C1|"+cur_dir+"/subdir/ns1.cpp|7|10|    void C1::check()",
],
# 12 9
["C1|"+cur_dir+"/ns1.h|12|9|        C1(int a) : m_val(a) {}"],
["C1|"+cur_dir+"/ns1.h|12|9|        C1(int a) : m_val(a) {}"],
[
""
],
# 13 14
["check|"+cur_dir+"/ns1.h|13|14|        void check();"],
["check|"+cur_dir+"/subdir/ns1.cpp|7|14|    void C1::check()"],
["check|"+cur_dir+"/main.cpp|20|9|    c11.check();"],
# 15 13
["m_val|"+cur_dir+"/ns1.h|15|13|        int m_val;"],
["m_val|"+cur_dir+"/ns1.h|15|13|        int m_val;"],
[
"m_val|"+cur_dir+"/ns1.h|12|21|        C1(int a) : m_val(a) {}",
"m_val|"+cur_dir+"/subdir/ns1.cpp|9|35|        printf(\"C1: val is %d\\n\", m_val);",
],

# ns1.cpp
# 2 11
[
#"NS1|"+cur_dir+"/ns1.h|2|11|namespace NS1 {",
"NS1|"+cur_dir+"/subdir/ns1.cpp|2|11|namespace NS1 {",
],
[
"NS1|"+cur_dir+"/ns1.h|2|11|namespace NS1 {",
"NS1|"+cur_dir+"/subdir/ns1.cpp|2|11|namespace NS1 {",
],
[
"NS1|"+cur_dir+"/main.cpp|14|5|    NS1::C0 c10(1);",
"NS1|"+cur_dir+"/main.cpp|16|5|    NS1::C1 c11(3);",
],
# 3 10
["C0|"+cur_dir+"/ns1.h|3|11|    class C0 {"],
["C0|"+cur_dir+"/ns1.h|3|11|    class C0 {"],
[
"C0|"+cur_dir+"/main.cpp|14|10|    NS1::C0 c10(1);",
"C0|"+cur_dir+"/subdir/ns1.cpp|3|10|    void C0::check()",
],
# 3 14
["check|"+cur_dir+"/ns1.h|6|14|        void check();"],
["check|"+cur_dir+"/subdir/ns1.cpp|3|14|    void C0::check()"],
[
"check|"+cur_dir+"/main.cpp|18|9|    c10.check();",
],
# 5 35
["m_val|"+cur_dir+"/ns1.h|8|13|        int m_val;"],
["m_val|"+cur_dir+"/ns1.h|8|13|        int m_val;"],
[
"m_val|"+cur_dir+"/ns1.h|5|21|        C0(int a) : m_val(a) {}",
"m_val|"+cur_dir+"/subdir/ns1.cpp|5|35|        printf(\"C0: val is %d\\n\", m_val);",
],
# 7 10
["C1|"+cur_dir+"/ns1.h|10|11|    class C1 {"],
["C1|"+cur_dir+"/ns1.h|10|11|    class C1 {"],
[
"C1|"+cur_dir+"/main.cpp|16|10|    NS1::C1 c11(3);",
"C1|"+cur_dir+"/subdir/ns1.cpp|7|10|    void C1::check()",
],
# 7 14
["check|"+cur_dir+"/ns1.h|13|14|        void check();"],
["check|"+cur_dir+"/subdir/ns1.cpp|7|14|    void C1::check()"],
["check|"+cur_dir+"/main.cpp|20|9|    c11.check();"],
# 9 35
["m_val|"+cur_dir+"/ns1.h|15|13|        int m_val;"],
["m_val|"+cur_dir+"/ns1.h|15|13|        int m_val;"],
[
"m_val|"+cur_dir+"/ns1.h|12|21|        C1(int a) : m_val(a) {}",
"m_val|"+cur_dir+"/subdir/ns1.cpp|9|35|        printf(\"C1: val is %d\\n\", m_val);",
],
# ns0.cpp
# 2 11
[
#"NS0|"+cur_dir+"/subdir/ns0.h|2|11|namespace NS0 {",
"NS0|"+cur_dir+"/ns0.cpp|2|11|namespace NS0 {",
],
[
"NS0|"+cur_dir+"/subdir/ns0.h|2|11|namespace NS0 {",
"NS0|"+cur_dir+"/ns0.cpp|2|11|namespace NS0 {",
],
[
"NS0|"+cur_dir+"/main.cpp|13|5|    NS0::C0 c00(0);",
"NS0|"+cur_dir+"/main.cpp|15|5|    NS0::C1 c01(2);",
],
# 3 9
["C0|"+cur_dir+"/subdir/ns0.h|4|11|    class C0 {"],
["C0|"+cur_dir+"/subdir/ns0.h|4|11|    class C0 {"],
[
"C0|"+cur_dir+"/main.cpp|13|10|    NS0::C0 c00(0);",
"C0|"+cur_dir+"/ns0.cpp|3|9|    int C0::check()",
],
# 3 13
["check|"+cur_dir+"/subdir/ns0.h|7|13|        int check();"],
["check|"+cur_dir+"/ns0.cpp|3|13|    int C0::check()"],
[
"check|"+cur_dir+"/main.cpp|17|9|    c00.check();",
],
# 5 35
["m_val|"+cur_dir+"/subdir/ns0.h|9|13|        int m_val;"],
["m_val|"+cur_dir+"/subdir/ns0.h|9|13|        int m_val;"],
[
"m_val|"+cur_dir+"/subdir/ns0.h|6|21|        C0(int a) : m_val(a) {}",
"m_val|"+cur_dir+"/ns0.cpp|5|35|        printf(\"C0: val is %d\\n\", m_val);",
"m_val|"+cur_dir+"/ns0.cpp|6|16|        return m_val;",
],
# 6 16
["m_val|"+cur_dir+"/subdir/ns0.h|9|13|        int m_val;"],
["m_val|"+cur_dir+"/subdir/ns0.h|9|13|        int m_val;"],
[
"m_val|"+cur_dir+"/subdir/ns0.h|6|21|        C0(int a) : m_val(a) {}",
"m_val|"+cur_dir+"/ns0.cpp|5|35|        printf(\"C0: val is %d\\n\", m_val);",
"m_val|"+cur_dir+"/ns0.cpp|6|16|        return m_val;",
],
# 8 5
["MYINT|"+cur_dir+"/subdir/ns0.h|3|17|    typedef int MYINT ;"],
["MYINT|"+cur_dir+"/subdir/ns0.h|3|17|    typedef int MYINT ;"],
[
"MYINT|"+cur_dir+"/subdir/ns0.h|14|9|        MYINT check() const;",
"MYINT|"+cur_dir+"/ns0.cpp|8|5|    MYINT C1::check() const",
],
# 8 11
["C1|"+cur_dir+"/subdir/ns0.h|11|11|    class C1 {"],
["C1|"+cur_dir+"/subdir/ns0.h|11|11|    class C1 {"],
[
"C1|"+cur_dir+"/main.cpp|15|10|    NS0::C1 c01(2);",
"C1|"+cur_dir+"/ns0.cpp|8|11|    MYINT C1::check() const",
"C1|"+cur_dir+"/ns0.cpp|13|5|    C1 C1::check2()",
"C1|"+cur_dir+"/ns0.cpp|13|8|    C1 C1::check2()",
"C1|"+cur_dir+"/subdir/ns0.h|15|9|        C1 check2();",
],
# 8 15
["check|"+cur_dir+"/subdir/ns0.h|14|15|        MYINT check() const;"],
["check|"+cur_dir+"/ns0.cpp|8|15|    MYINT C1::check() const"],
["check|"+cur_dir+"/main.cpp|19|9|    c01.check();"],
# 10 35
["m_val|"+cur_dir+"/subdir/ns0.h|17|13|        int m_val;"],
["m_val|"+cur_dir+"/subdir/ns0.h|17|13|        int m_val;"],
[
"m_val|"+cur_dir+"/subdir/ns0.h|13|21|        C1(int a) : m_val(a) {}",
"m_val|"+cur_dir+"/ns0.cpp|10|35|        printf(\"C1: val is %d\\n\", m_val);",
"m_val|"+cur_dir+"/ns0.cpp|11|16|        return m_val;",
],
# 11 16
["m_val|"+cur_dir+"/subdir/ns0.h|17|13|        int m_val;"],
["m_val|"+cur_dir+"/subdir/ns0.h|17|13|        int m_val;"],
[
"m_val|"+cur_dir+"/subdir/ns0.h|13|21|        C1(int a) : m_val(a) {}",
"m_val|"+cur_dir+"/ns0.cpp|10|35|        printf(\"C1: val is %d\\n\", m_val);",
"m_val|"+cur_dir+"/ns0.cpp|11|16|        return m_val;",
],
# 13 5
["C1|"+cur_dir+"/subdir/ns0.h|11|11|    class C1 {"],
["C1|"+cur_dir+"/subdir/ns0.h|11|11|    class C1 {"],
[
"C1|"+cur_dir+"/main.cpp|15|10|    NS0::C1 c01(2);",
"C1|"+cur_dir+"/ns0.cpp|8|11|    MYINT C1::check() const",
"C1|"+cur_dir+"/ns0.cpp|13|5|    C1 C1::check2()",
"C1|"+cur_dir+"/ns0.cpp|13|8|    C1 C1::check2()",
"C1|"+cur_dir+"/subdir/ns0.h|15|9|        C1 check2();",
],
# 13 8
["C1|"+cur_dir+"/subdir/ns0.h|11|11|    class C1 {"],
["C1|"+cur_dir+"/subdir/ns0.h|11|11|    class C1 {"],
[
"C1|"+cur_dir+"/main.cpp|15|10|    NS0::C1 c01(2);",
"C1|"+cur_dir+"/ns0.cpp|8|11|    MYINT C1::check() const",
"C1|"+cur_dir+"/ns0.cpp|13|5|    C1 C1::check2()",
"C1|"+cur_dir+"/ns0.cpp|13|8|    C1 C1::check2()",
"C1|"+cur_dir+"/subdir/ns0.h|15|9|        C1 check2();",
],
# 13 12
["check2|"+cur_dir+"/subdir/ns0.h|15|12|        C1 check2();"],
["check2|"+cur_dir+"/ns0.cpp|13|12|    C1 C1::check2()"],
[
""
],
# 17 10
["asdf|"+cur_dir+"/ns0.cpp|17|10|    void asdf(void) {"],
["asdf|"+cur_dir+"/ns0.cpp|17|10|    void asdf(void) {"],
[
""
],
# 20 10
["asdf|"+cur_dir+"/ns0.cpp|20|10|    void asdf(int a) {"],
["asdf|"+cur_dir+"/ns0.cpp|20|10|    void asdf(int a) {"],
[
""
],
# 20 19
["a|"+cur_dir+"/ns0.cpp|20|19|    void asdf(int a) {"],
["a|"+cur_dir+"/ns0.cpp|20|19|    void asdf(int a) {"],
[
"a|"+cur_dir+"/ns0.cpp|21|30|        printf(\"asdf: %d\\n\", a);",
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
