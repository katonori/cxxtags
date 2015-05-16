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
"decl "+db_dir+" "+cur_dir+"/inhe.cpp 3 7", #CParent0
"def "+db_dir+" "+cur_dir+"/inhe.cpp 3 7", #CParent0
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 3 7", #CParent0
"override "+db_dir+" "+cur_dir+"/inhe.cpp 3 7", #CParent0

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 6 5", #CParent0
"def "+db_dir+" "+cur_dir+"/inhe.cpp 6 5", #CParent0
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 6 5", #CParent0
"override "+db_dir+" "+cur_dir+"/inhe.cpp 6 5", #CParent0

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 7 5", #~CParent0
"def "+db_dir+" "+cur_dir+"/inhe.cpp 7 5", #~CParent0
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 7 5", #~CParent0
"override "+db_dir+" "+cur_dir+"/inhe.cpp 7 5", #~CParent0

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 8 18", #response
"def "+db_dir+" "+cur_dir+"/inhe.cpp 8 18", #response
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 8 18", #response
"override "+db_dir+" "+cur_dir+"/inhe.cpp 8 18", #response

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 11 6", #CParent0
"def "+db_dir+" "+cur_dir+"/inhe.cpp 11 6", #CParent0
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 11 6", #CParent0
"override "+db_dir+" "+cur_dir+"/inhe.cpp 11 6", #CParent0

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 11 16", #response
"def "+db_dir+" "+cur_dir+"/inhe.cpp 11 16", #response
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 11 16", #response
"override "+db_dir+" "+cur_dir+"/inhe.cpp 11 16", #response

#"decl "+db_dir+" "+cur_dir+"/inhe.cpp 12 5", #printf

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 15 7", #CParent1
"def "+db_dir+" "+cur_dir+"/inhe.cpp 15 7", #CParent1
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 15 7", #CParent1
"override "+db_dir+" "+cur_dir+"/inhe.cpp 15 7", #CParent1

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 18 5", #CParent1
"def "+db_dir+" "+cur_dir+"/inhe.cpp 18 5", #CParent1
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 18 5", #CParent1
"override "+db_dir+" "+cur_dir+"/inhe.cpp 18 5", #CParent1

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 19 5", #~CParent1
"def "+db_dir+" "+cur_dir+"/inhe.cpp 19 5", #~CParent1
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 19 5", #~CParent1
"override "+db_dir+" "+cur_dir+"/inhe.cpp 19 5", #~CParent1

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 20 18", #response
"def "+db_dir+" "+cur_dir+"/inhe.cpp 20 18", #response
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 20 18", #response
"override "+db_dir+" "+cur_dir+"/inhe.cpp 20 18", #response

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 23 6", #CParent1
"def "+db_dir+" "+cur_dir+"/inhe.cpp 23 6", #CParent1
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 23 6", #CParent1
"override "+db_dir+" "+cur_dir+"/inhe.cpp 23 6", #CParent1

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 23 16", #response
"def "+db_dir+" "+cur_dir+"/inhe.cpp 23 16", #response
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 23 16", #response
"override "+db_dir+" "+cur_dir+"/inhe.cpp 23 16", #response

#"decl "+db_dir+" "+cur_dir+"/inhe.cpp 24 5", #printf

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 27 7", #CChild
"def "+db_dir+" "+cur_dir+"/inhe.cpp 27 7", #CChild
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 27 7", #CChild
"override "+db_dir+" "+cur_dir+"/inhe.cpp 27 7", #CChild

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 28 10", #CParent0
"def "+db_dir+" "+cur_dir+"/inhe.cpp 28 10", #CParent0
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 28 10", #CParent0
"override "+db_dir+" "+cur_dir+"/inhe.cpp 28 10", #CParent0

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 31 5", #CChild
"def "+db_dir+" "+cur_dir+"/inhe.cpp 31 5", #CChild
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 31 5", #CChild
"override "+db_dir+" "+cur_dir+"/inhe.cpp 31 5", #CChild

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 32 5", #~CChild
"def "+db_dir+" "+cur_dir+"/inhe.cpp 32 5", #~CChild
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 32 5", #~CChild
"override "+db_dir+" "+cur_dir+"/inhe.cpp 32 5", #~CChild

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 33 18", #response
"def "+db_dir+" "+cur_dir+"/inhe.cpp 33 18", #response
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 33 18", #response
"override "+db_dir+" "+cur_dir+"/inhe.cpp 33 18", #response

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 36 6", #CChild
"def "+db_dir+" "+cur_dir+"/inhe.cpp 36 6", #CChild
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 36 6", #CChild
"override "+db_dir+" "+cur_dir+"/inhe.cpp 36 6", #CChild

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 36 14", #response
"def "+db_dir+" "+cur_dir+"/inhe.cpp 36 14", #response
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 36 14", #response
"override "+db_dir+" "+cur_dir+"/inhe.cpp 36 14", #response

#"decl "+db_dir+" "+cur_dir+"/inhe.cpp 37 5", #printf

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 40 7", #CGChild
"def "+db_dir+" "+cur_dir+"/inhe.cpp 40 7", #CGChild
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 40 7", #CGChild
"override "+db_dir+" "+cur_dir+"/inhe.cpp 40 7", #CGChild

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 41 10", #CChild
"def "+db_dir+" "+cur_dir+"/inhe.cpp 41 10", #CChild
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 41 10", #CChild
"override "+db_dir+" "+cur_dir+"/inhe.cpp 41 10", #CChild

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 44 5", #CGChild
"def "+db_dir+" "+cur_dir+"/inhe.cpp 44 5", #CGChild
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 44 5", #CGChild
"override "+db_dir+" "+cur_dir+"/inhe.cpp 44 5", #CGChild

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 45 5", #~CGChild
"def "+db_dir+" "+cur_dir+"/inhe.cpp 45 5", #~CGChild
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 45 5", #~CGChild
"override "+db_dir+" "+cur_dir+"/inhe.cpp 45 5", #~CGChild

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 46 18", #response
"def "+db_dir+" "+cur_dir+"/inhe.cpp 46 18", #response
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 46 18", #response
"override "+db_dir+" "+cur_dir+"/inhe.cpp 46 18", #response

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 49 6", #CGChild
"def "+db_dir+" "+cur_dir+"/inhe.cpp 49 6", #CGChild
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 49 6", #CGChild
"override "+db_dir+" "+cur_dir+"/inhe.cpp 49 6", #CGChild

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 49 15", #response
"def "+db_dir+" "+cur_dir+"/inhe.cpp 49 15", #response
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 49 15", #response
"override "+db_dir+" "+cur_dir+"/inhe.cpp 49 15", #response

#"decl "+db_dir+" "+cur_dir+"/inhe.cpp 50 5", #printf

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 53 7", #COther
"def "+db_dir+" "+cur_dir+"/inhe.cpp 53 7", #COther
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 53 7", #COther
"override "+db_dir+" "+cur_dir+"/inhe.cpp 53 7", #COther

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 54 10", #CParent0
"def "+db_dir+" "+cur_dir+"/inhe.cpp 54 10", #CParent0
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 54 10", #CParent0
"override "+db_dir+" "+cur_dir+"/inhe.cpp 54 10", #CParent0

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 54 27", #CParent1
"def "+db_dir+" "+cur_dir+"/inhe.cpp 54 27", #CParent1
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 54 27", #CParent1
"override "+db_dir+" "+cur_dir+"/inhe.cpp 54 27", #CParent1

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 57 5", #COther
"def "+db_dir+" "+cur_dir+"/inhe.cpp 57 5", #COther
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 57 5", #COther
"override "+db_dir+" "+cur_dir+"/inhe.cpp 57 5", #COther

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 58 5", #~COther
"def "+db_dir+" "+cur_dir+"/inhe.cpp 58 5", #~COther
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 58 5", #~COther
"override "+db_dir+" "+cur_dir+"/inhe.cpp 58 5", #~COther

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 59 18", #response
"def "+db_dir+" "+cur_dir+"/inhe.cpp 59 18", #response
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 59 18", #response
"override "+db_dir+" "+cur_dir+"/inhe.cpp 59 18", #response

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 62 6", #COther
"def "+db_dir+" "+cur_dir+"/inhe.cpp 62 6", #COther
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 62 6", #COther
"override "+db_dir+" "+cur_dir+"/inhe.cpp 62 6", #COther

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 62 14", #response
"def "+db_dir+" "+cur_dir+"/inhe.cpp 62 14", #response
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 62 14", #response
"override "+db_dir+" "+cur_dir+"/inhe.cpp 62 14", #response

#"decl "+db_dir+" "+cur_dir+"/inhe.cpp 63 5", #printf

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 66 13", #test
"def "+db_dir+" "+cur_dir+"/inhe.cpp 66 13", #test
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 66 13", #test
"override "+db_dir+" "+cur_dir+"/inhe.cpp 66 13", #test

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 66 24", #CParent0
"def "+db_dir+" "+cur_dir+"/inhe.cpp 66 24", #CParent0
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 66 24", #CParent0
"override "+db_dir+" "+cur_dir+"/inhe.cpp 66 24", #CParent0

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 66 34", #a
"def "+db_dir+" "+cur_dir+"/inhe.cpp 66 34", #a
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 66 34", #a
"override "+db_dir+" "+cur_dir+"/inhe.cpp 66 34", #a

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 68 5", #a
"def "+db_dir+" "+cur_dir+"/inhe.cpp 68 5", #a
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 68 5", #a
"override "+db_dir+" "+cur_dir+"/inhe.cpp 68 5", #a

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 68 8", #response
"def "+db_dir+" "+cur_dir+"/inhe.cpp 68 8", #response
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 68 8", #response
"override "+db_dir+" "+cur_dir+"/inhe.cpp 68 8", #response

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 71 5", #main
"def "+db_dir+" "+cur_dir+"/inhe.cpp 71 5", #main
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 71 5", #main
"override "+db_dir+" "+cur_dir+"/inhe.cpp 71 5", #main

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 73 5", #CParent0
"def "+db_dir+" "+cur_dir+"/inhe.cpp 73 5", #CParent0
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 73 5", #CParent0
"override "+db_dir+" "+cur_dir+"/inhe.cpp 73 5", #CParent0

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 73 14", #parent
"def "+db_dir+" "+cur_dir+"/inhe.cpp 73 14", #parent
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 73 14", #parent
"override "+db_dir+" "+cur_dir+"/inhe.cpp 73 14", #parent

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 74 5", #CChild
"def "+db_dir+" "+cur_dir+"/inhe.cpp 74 5", #CChild
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 74 5", #CChild
"override "+db_dir+" "+cur_dir+"/inhe.cpp 74 5", #CChild

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 74 12", #child
"def "+db_dir+" "+cur_dir+"/inhe.cpp 74 12", #child
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 74 12", #child
"override "+db_dir+" "+cur_dir+"/inhe.cpp 74 12", #child

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 75 5", #CGChild
"def "+db_dir+" "+cur_dir+"/inhe.cpp 75 5", #CGChild
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 75 5", #CGChild
"override "+db_dir+" "+cur_dir+"/inhe.cpp 75 5", #CGChild

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 75 13", #gchild
"def "+db_dir+" "+cur_dir+"/inhe.cpp 75 13", #gchild
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 75 13", #gchild
"override "+db_dir+" "+cur_dir+"/inhe.cpp 75 13", #gchild

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 76 5", #COther
"def "+db_dir+" "+cur_dir+"/inhe.cpp 76 5", #COther
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 76 5", #COther
"override "+db_dir+" "+cur_dir+"/inhe.cpp 76 5", #COther

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 76 12", #other
"def "+db_dir+" "+cur_dir+"/inhe.cpp 76 12", #other
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 76 12", #other
"override "+db_dir+" "+cur_dir+"/inhe.cpp 76 12", #other

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 77 5", #parent
"def "+db_dir+" "+cur_dir+"/inhe.cpp 77 5", #parent
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 77 5", #parent
"override "+db_dir+" "+cur_dir+"/inhe.cpp 77 5", #parent

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 77 12", #response
"def "+db_dir+" "+cur_dir+"/inhe.cpp 77 12", #response
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 77 12", #response
"override "+db_dir+" "+cur_dir+"/inhe.cpp 77 12", #response

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 78 5", #child
"def "+db_dir+" "+cur_dir+"/inhe.cpp 78 5", #child
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 78 5", #child
"override "+db_dir+" "+cur_dir+"/inhe.cpp 78 5", #child

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 78 11", #response
"def "+db_dir+" "+cur_dir+"/inhe.cpp 78 11", #response
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 78 11", #response
"override "+db_dir+" "+cur_dir+"/inhe.cpp 78 11", #response

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 79 5", #gchild
"def "+db_dir+" "+cur_dir+"/inhe.cpp 79 5", #gchild
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 79 5", #gchild
"override "+db_dir+" "+cur_dir+"/inhe.cpp 79 5", #gchild

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 79 12", #response
"def "+db_dir+" "+cur_dir+"/inhe.cpp 79 12", #response
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 79 12", #response
"override "+db_dir+" "+cur_dir+"/inhe.cpp 79 12", #response

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 80 5", #other
"def "+db_dir+" "+cur_dir+"/inhe.cpp 80 5", #other
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 80 5", #other
"override "+db_dir+" "+cur_dir+"/inhe.cpp 80 5", #other

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 80 11", #response
"def "+db_dir+" "+cur_dir+"/inhe.cpp 80 11", #response
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 80 11", #response
"override "+db_dir+" "+cur_dir+"/inhe.cpp 80 11", #response

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 81 5", #test
"def "+db_dir+" "+cur_dir+"/inhe.cpp 81 5", #test
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 81 5", #test
"override "+db_dir+" "+cur_dir+"/inhe.cpp 81 5", #test

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 81 11", #parent
"def "+db_dir+" "+cur_dir+"/inhe.cpp 81 11", #parent
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 81 11", #parent
"override "+db_dir+" "+cur_dir+"/inhe.cpp 81 11", #parent

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 82 5", #test
"def "+db_dir+" "+cur_dir+"/inhe.cpp 82 5", #test
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 82 5", #test
"override "+db_dir+" "+cur_dir+"/inhe.cpp 82 5", #test

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 82 11", #child
"def "+db_dir+" "+cur_dir+"/inhe.cpp 82 11", #child
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 82 11", #child
"override "+db_dir+" "+cur_dir+"/inhe.cpp 82 11", #child

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 83 5", #test
"def "+db_dir+" "+cur_dir+"/inhe.cpp 83 5", #test
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 83 5", #test
"override "+db_dir+" "+cur_dir+"/inhe.cpp 83 5", #test

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 83 11", #gchild
"def "+db_dir+" "+cur_dir+"/inhe.cpp 83 11", #gchild
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 83 11", #gchild
"override "+db_dir+" "+cur_dir+"/inhe.cpp 83 11", #gchild

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 84 5", #test
"def "+db_dir+" "+cur_dir+"/inhe.cpp 84 5", #test
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 84 5", #test
"override "+db_dir+" "+cur_dir+"/inhe.cpp 84 5", #test

"decl "+db_dir+" "+cur_dir+"/inhe.cpp 84 11", #other
"def "+db_dir+" "+cur_dir+"/inhe.cpp 84 11", #other
"ref "+db_dir+" "+cur_dir+"/inhe.cpp 84 11", #other
"override "+db_dir+" "+cur_dir+"/inhe.cpp 84 11", #other
]

ans_list = [
# inhe.cpp
["CParent0|"+cur_dir+"/inhe.cpp|3|7|class CParent0"],
["CParent0|"+cur_dir+"/inhe.cpp|3|7|class CParent0"],
[
"CParent0|"+cur_dir+r'/inhe.cpp|11|6|void CParent0::response(void) {',
"CParent0|"+cur_dir+r'/inhe.cpp|28|10|: public CParent0',
"CParent0|"+cur_dir+r'/inhe.cpp|54|10|: public CParent0, public CParent1',
"CParent0|"+cur_dir+r'/inhe.cpp|66|24|static void test(class CParent0 *a)',
"CParent0|"+cur_dir+r'/inhe.cpp|73|5|    CParent0 parent;',
],
[""],

["CParent0|"+cur_dir+"/inhe.cpp|6|5|    CParent0(){}"],
["CParent0|"+cur_dir+"/inhe.cpp|6|5|    CParent0(){}"],
[""],
[""],

["~CParent0|"+cur_dir+"/inhe.cpp|7|5|    ~CParent0(){}"],
["~CParent0|"+cur_dir+"/inhe.cpp|7|5|    ~CParent0(){}"],
[""],
[""],

# 8 18
["response|"+cur_dir+"/inhe.cpp|8|18|    virtual void response(void);"],
["response|"+cur_dir+"/inhe.cpp|11|16|void CParent0::response(void) {"],
[
"response|"+cur_dir+"/inhe.cpp|68|8|    a->response();",
"response|"+cur_dir+"/inhe.cpp|77|12|    parent.response();",
],
[
"response|"+cur_dir+"/inhe.cpp|33|18|    virtual void response(void);",
"response|"+cur_dir+"/inhe.cpp|36|14|void CChild::response(void) {",
"response|"+cur_dir+"/inhe.cpp|59|18|    virtual void response(void);",
"response|"+cur_dir+"/inhe.cpp|62|14|void COther::response(void) {",
],

# 11 6
["CParent0|"+cur_dir+"/inhe.cpp|3|7|class CParent0"],
["CParent0|"+cur_dir+"/inhe.cpp|3|7|class CParent0"],
[
"CParent0|"+cur_dir+r'/inhe.cpp|11|6|void CParent0::response(void) {',
"CParent0|"+cur_dir+r'/inhe.cpp|28|10|: public CParent0',
"CParent0|"+cur_dir+r'/inhe.cpp|54|10|: public CParent0, public CParent1',
"CParent0|"+cur_dir+r'/inhe.cpp|66|24|static void test(class CParent0 *a)',
"CParent0|"+cur_dir+r'/inhe.cpp|73|5|    CParent0 parent;',
],
[""],
# 11 16
["response|"+cur_dir+"/inhe.cpp|8|18|    virtual void response(void);"],
["response|"+cur_dir+"/inhe.cpp|11|16|void CParent0::response(void) {"],
[
"response|"+cur_dir+"/inhe.cpp|68|8|    a->response();",
"response|"+cur_dir+"/inhe.cpp|77|12|    parent.response();",
],
[
"response|"+cur_dir+"/inhe.cpp|33|18|    virtual void response(void);",
"response|"+cur_dir+"/inhe.cpp|36|14|void CChild::response(void) {",
"response|"+cur_dir+"/inhe.cpp|59|18|    virtual void response(void);",
"response|"+cur_dir+"/inhe.cpp|62|14|void COther::response(void) {",
],
# 15 7
["CParent1|"+cur_dir+"/inhe.cpp|15|7|class CParent1"],
["CParent1|"+cur_dir+"/inhe.cpp|15|7|class CParent1"],
[
"CParent1|"+cur_dir+r'/inhe.cpp|23|6|void CParent1::response(void) {',
"CParent1|"+cur_dir+r'/inhe.cpp|54|27|: public CParent0, public CParent1',
],
[""],
# 18 5
["CParent1|"+cur_dir+"/inhe.cpp|18|5|    CParent1(){}"],
["CParent1|"+cur_dir+"/inhe.cpp|18|5|    CParent1(){}"],
[""],
[""],
# 19 5
["~CParent1|"+cur_dir+"/inhe.cpp|19|5|    ~CParent1(){}"],
["~CParent1|"+cur_dir+"/inhe.cpp|19|5|    ~CParent1(){}"],
[""],
[""],
# 20 18
["response|"+cur_dir+"/inhe.cpp|20|18|    virtual void response(void);"],
["response|"+cur_dir+"/inhe.cpp|23|16|void CParent1::response(void) {"],
[""],
[
"response|"+cur_dir+"/inhe.cpp|59|18|    virtual void response(void);",
"response|"+cur_dir+"/inhe.cpp|62|14|void COther::response(void) {",
],
# 23 6
["CParent1|"+cur_dir+"/inhe.cpp|15|7|class CParent1"],
["CParent1|"+cur_dir+"/inhe.cpp|15|7|class CParent1"],
[
"CParent1|"+cur_dir+r'/inhe.cpp|23|6|void CParent1::response(void) {',
"CParent1|"+cur_dir+r'/inhe.cpp|54|27|: public CParent0, public CParent1',
],
[""],
# 23 16
["response|"+cur_dir+"/inhe.cpp|20|18|    virtual void response(void);"],
["response|"+cur_dir+"/inhe.cpp|23|16|void CParent1::response(void) {"],
[""],
[
"response|"+cur_dir+"/inhe.cpp|59|18|    virtual void response(void);",
"response|"+cur_dir+"/inhe.cpp|62|14|void COther::response(void) {",
],
# 27 7
["CChild|"+cur_dir+"/inhe.cpp|27|7|class CChild"],
["CChild|"+cur_dir+"/inhe.cpp|27|7|class CChild"],
[
"CChild|"+cur_dir+r'/inhe.cpp|36|6|void CChild::response(void) {',
"CChild|"+cur_dir+r'/inhe.cpp|41|10|: public CChild',
"CChild|"+cur_dir+r'/inhe.cpp|74|5|    CChild child;',
],
[""],
# 28 10
["CParent0|"+cur_dir+"/inhe.cpp|3|7|class CParent0"],
["CParent0|"+cur_dir+"/inhe.cpp|3|7|class CParent0"],
[
"CParent0|"+cur_dir+r'/inhe.cpp|11|6|void CParent0::response(void) {',
"CParent0|"+cur_dir+r'/inhe.cpp|28|10|: public CParent0',
"CParent0|"+cur_dir+r'/inhe.cpp|54|10|: public CParent0, public CParent1',
"CParent0|"+cur_dir+r'/inhe.cpp|66|24|static void test(class CParent0 *a)',
"CParent0|"+cur_dir+r'/inhe.cpp|73|5|    CParent0 parent;',
],
[""],
# 31 5
["CChild|"+cur_dir+"/inhe.cpp|31|5|    CChild(){}"],
["CChild|"+cur_dir+"/inhe.cpp|31|5|    CChild(){}"],
[""],
[""],
# 39 5
["~CChild|"+cur_dir+"/inhe.cpp|32|5|    ~CChild(){}"],
["~CChild|"+cur_dir+"/inhe.cpp|32|5|    ~CChild(){}"],
[""],
[""],
# 33 18
["response|"+cur_dir+"/inhe.cpp|33|18|    virtual void response(void);"],
["response|"+cur_dir+"/inhe.cpp|36|14|void CChild::response(void) {"],
["response|"+cur_dir+"/inhe.cpp|78|11|    child.response();"],
[
"response|"+cur_dir+"/inhe.cpp|46|18|    virtual void response(void);",
"response|"+cur_dir+"/inhe.cpp|49|15|void CGChild::response(void) {",
"response|"+cur_dir+"/inhe.cpp|8|18|    virtual void response(void);",
],
# 36 6
["CChild|"+cur_dir+"/inhe.cpp|27|7|class CChild"],
["CChild|"+cur_dir+"/inhe.cpp|27|7|class CChild"],
[
"CChild|"+cur_dir+r'/inhe.cpp|36|6|void CChild::response(void) {',
"CChild|"+cur_dir+r'/inhe.cpp|41|10|: public CChild',
"CChild|"+cur_dir+r'/inhe.cpp|74|5|    CChild child;',
],
[""],
# 36 14
["response|"+cur_dir+"/inhe.cpp|33|18|    virtual void response(void);"],
["response|"+cur_dir+"/inhe.cpp|36|14|void CChild::response(void) {"],
["response|"+cur_dir+"/inhe.cpp|78|11|    child.response();"],
[
"response|"+cur_dir+"/inhe.cpp|46|18|    virtual void response(void);",
"response|"+cur_dir+"/inhe.cpp|49|15|void CGChild::response(void) {",
"response|"+cur_dir+"/inhe.cpp|8|18|    virtual void response(void);",
],
# 40 7
["CGChild|"+cur_dir+"/inhe.cpp|40|7|class CGChild"],
["CGChild|"+cur_dir+"/inhe.cpp|40|7|class CGChild"],
[
"CGChild|"+cur_dir+r'/inhe.cpp|49|6|void CGChild::response(void) {',
"CGChild|"+cur_dir+r'/inhe.cpp|75|5|    CGChild gchild;',
],
[""],
# 41 10
["CChild|"+cur_dir+"/inhe.cpp|27|7|class CChild"],
["CChild|"+cur_dir+"/inhe.cpp|27|7|class CChild"],
[
"CChild|"+cur_dir+r'/inhe.cpp|36|6|void CChild::response(void) {',
"CChild|"+cur_dir+r'/inhe.cpp|41|10|: public CChild',
"CChild|"+cur_dir+r'/inhe.cpp|74|5|    CChild child;',
],
[""],
# 44 5
["CGChild|"+cur_dir+"/inhe.cpp|44|5|    CGChild(){}"],
["CGChild|"+cur_dir+"/inhe.cpp|44|5|    CGChild(){}"],
[""],
[""],
# 45 5
["~CGChild|"+cur_dir+"/inhe.cpp|45|5|    ~CGChild(){}"],
["~CGChild|"+cur_dir+"/inhe.cpp|45|5|    ~CGChild(){}"],
[""],
[""],
# 46 18
["response|"+cur_dir+"/inhe.cpp|46|18|    virtual void response(void);"],
["response|"+cur_dir+"/inhe.cpp|49|15|void CGChild::response(void) {"],
["response|"+cur_dir+"/inhe.cpp|79|12|    gchild.response();"],
["response|"+cur_dir+"/inhe.cpp|33|18|    virtual void response(void);"],
# 49 6
["CGChild|"+cur_dir+"/inhe.cpp|40|7|class CGChild"],
["CGChild|"+cur_dir+"/inhe.cpp|40|7|class CGChild"],
[
"CGChild|"+cur_dir+r'/inhe.cpp|49|6|void CGChild::response(void) {',
"CGChild|"+cur_dir+r'/inhe.cpp|75|5|    CGChild gchild;',
],
[""],
# 49 15
["response|"+cur_dir+"/inhe.cpp|46|18|    virtual void response(void);"],
["response|"+cur_dir+"/inhe.cpp|49|15|void CGChild::response(void) {"],
["response|"+cur_dir+"/inhe.cpp|79|12|    gchild.response();"],
["response|"+cur_dir+"/inhe.cpp|33|18|    virtual void response(void);"],
# 53 7
["COther|"+cur_dir+"/inhe.cpp|53|7|class COther"],
["COther|"+cur_dir+"/inhe.cpp|53|7|class COther"],
[
"COther|"+cur_dir+r'/inhe.cpp|62|6|void COther::response(void) {',
"COther|"+cur_dir+r'/inhe.cpp|76|5|    COther other;',
],
[""],
# 54 10
["CParent0|"+cur_dir+"/inhe.cpp|3|7|class CParent0"],
["CParent0|"+cur_dir+"/inhe.cpp|3|7|class CParent0"],
[
"CParent0|"+cur_dir+r'/inhe.cpp|11|6|void CParent0::response(void) {',
"CParent0|"+cur_dir+r'/inhe.cpp|28|10|: public CParent0',
"CParent0|"+cur_dir+r'/inhe.cpp|54|10|: public CParent0, public CParent1',
"CParent0|"+cur_dir+r'/inhe.cpp|66|24|static void test(class CParent0 *a)',
"CParent0|"+cur_dir+r'/inhe.cpp|73|5|    CParent0 parent;',
],
[""],
# 54 27
["CParent1|"+cur_dir+"/inhe.cpp|15|7|class CParent1"],
["CParent1|"+cur_dir+"/inhe.cpp|15|7|class CParent1"],
[
"CParent1|"+cur_dir+r'/inhe.cpp|23|6|void CParent1::response(void) {',
"CParent1|"+cur_dir+r'/inhe.cpp|54|27|: public CParent0, public CParent1',
],
[""],
# 57 5
["COther|"+cur_dir+"/inhe.cpp|57|5|    COther(){}"],
["COther|"+cur_dir+"/inhe.cpp|57|5|    COther(){}"],
[""],
[""],
# 58 5
["~COther|"+cur_dir+"/inhe.cpp|58|5|    ~COther(){}"],
["~COther|"+cur_dir+"/inhe.cpp|58|5|    ~COther(){}"],
[""],
[""],
# 59 18
["response|"+cur_dir+"/inhe.cpp|59|18|    virtual void response(void);"],
["response|"+cur_dir+"/inhe.cpp|62|14|void COther::response(void) {"],
["response|"+cur_dir+"/inhe.cpp|80|11|    other.response();"],
[
"response|"+cur_dir+"/inhe.cpp|8|18|    virtual void response(void);",
"response|"+cur_dir+"/inhe.cpp|20|18|    virtual void response(void);",
],
# 62 6
["COther|"+cur_dir+"/inhe.cpp|53|7|class COther"],
["COther|"+cur_dir+"/inhe.cpp|53|7|class COther"],
[
"COther|"+cur_dir+r'/inhe.cpp|62|6|void COther::response(void) {',
"COther|"+cur_dir+r'/inhe.cpp|76|5|    COther other;',
],
[""],
# 62 14
["response|"+cur_dir+"/inhe.cpp|59|18|    virtual void response(void);"],
["response|"+cur_dir+"/inhe.cpp|62|14|void COther::response(void) {"],
["response|"+cur_dir+"/inhe.cpp|80|11|    other.response();"],
[
"response|"+cur_dir+"/inhe.cpp|8|18|    virtual void response(void);",
"response|"+cur_dir+"/inhe.cpp|20|18|    virtual void response(void);",
],
# 66 13
["test|"+cur_dir+"/inhe.cpp|66|13|static void test(class CParent0 *a)"],
["test|"+cur_dir+"/inhe.cpp|66|13|static void test(class CParent0 *a)"],
[
"test|"+cur_dir+"/inhe.cpp|81|5|    test(&parent);",
"test|"+cur_dir+"/inhe.cpp|82|5|    test(&child);",
"test|"+cur_dir+"/inhe.cpp|83|5|    test(&gchild);",
"test|"+cur_dir+"/inhe.cpp|84|5|    test(&other);",
],
[""],
# 66 24
["CParent0|"+cur_dir+"/inhe.cpp|3|7|class CParent0"],
["CParent0|"+cur_dir+"/inhe.cpp|3|7|class CParent0"],
[
"CParent0|"+cur_dir+r'/inhe.cpp|11|6|void CParent0::response(void) {',
"CParent0|"+cur_dir+r'/inhe.cpp|28|10|: public CParent0',
"CParent0|"+cur_dir+r'/inhe.cpp|54|10|: public CParent0, public CParent1',
"CParent0|"+cur_dir+r'/inhe.cpp|66|24|static void test(class CParent0 *a)',
"CParent0|"+cur_dir+r'/inhe.cpp|73|5|    CParent0 parent;',
],
[""],
# 66 34
["a|"+cur_dir+"/inhe.cpp|66|34|static void test(class CParent0 *a)"],
["a|"+cur_dir+"/inhe.cpp|66|34|static void test(class CParent0 *a)"],
["a|"+cur_dir+r'/inhe.cpp|68|5|    a->response();'],
[""],
# 68 5
["a|"+cur_dir+"/inhe.cpp|66|34|static void test(class CParent0 *a)"],
["a|"+cur_dir+"/inhe.cpp|66|34|static void test(class CParent0 *a)"],
["a|"+cur_dir+r'/inhe.cpp|68|5|    a->response();'],
[""],
# 68 8
["response|"+cur_dir+"/inhe.cpp|8|18|    virtual void response(void);"],
["response|"+cur_dir+"/inhe.cpp|11|16|void CParent0::response(void) {"],
[
"response|"+cur_dir+"/inhe.cpp|68|8|    a->response();",
"response|"+cur_dir+"/inhe.cpp|77|12|    parent.response();",
],
[
"response|"+cur_dir+"/inhe.cpp|33|18|    virtual void response(void);",
"response|"+cur_dir+"/inhe.cpp|36|14|void CChild::response(void) {",
"response|"+cur_dir+"/inhe.cpp|59|18|    virtual void response(void);",
"response|"+cur_dir+"/inhe.cpp|62|14|void COther::response(void) {",
],
# 71 5
["main|"+cur_dir+"/inhe.cpp|71|5|int main()"],
["main|"+cur_dir+"/inhe.cpp|71|5|int main()"],
[""],
[""],
# 73 5
["CParent0|"+cur_dir+"/inhe.cpp|3|7|class CParent0"],
["CParent0|"+cur_dir+"/inhe.cpp|3|7|class CParent0"],
[
"CParent0|"+cur_dir+r'/inhe.cpp|11|6|void CParent0::response(void) {',
"CParent0|"+cur_dir+r'/inhe.cpp|28|10|: public CParent0',
"CParent0|"+cur_dir+r'/inhe.cpp|54|10|: public CParent0, public CParent1',
"CParent0|"+cur_dir+r'/inhe.cpp|66|24|static void test(class CParent0 *a)',
"CParent0|"+cur_dir+r'/inhe.cpp|73|5|    CParent0 parent;',
],
[""],
# 73 14
["parent|"+cur_dir+"/inhe.cpp|73|14|    CParent0 parent;"],
["parent|"+cur_dir+"/inhe.cpp|73|14|    CParent0 parent;"],
[
"parent|"+cur_dir+"/inhe.cpp|77|5|    parent.response();",
"parent|"+cur_dir+"/inhe.cpp|81|11|    test(&parent);",
],
[""],
# 74 5
["CChild|"+cur_dir+"/inhe.cpp|27|7|class CChild"],
["CChild|"+cur_dir+"/inhe.cpp|27|7|class CChild"],
[
"CChild|"+cur_dir+r'/inhe.cpp|36|6|void CChild::response(void) {',
"CChild|"+cur_dir+r'/inhe.cpp|41|10|: public CChild',
"CChild|"+cur_dir+r'/inhe.cpp|74|5|    CChild child;',
],
[""],
# 74 12
["child|"+cur_dir+"/inhe.cpp|74|12|    CChild child;"],
["child|"+cur_dir+"/inhe.cpp|74|12|    CChild child;"],
[
"child|"+cur_dir+"/inhe.cpp|78|5|    child.response();",
"child|"+cur_dir+"/inhe.cpp|82|11|    test(&child);",
],
[""],
# 75 5
["CGChild|"+cur_dir+"/inhe.cpp|40|7|class CGChild"],
["CGChild|"+cur_dir+"/inhe.cpp|40|7|class CGChild"],
[
"CGChild|"+cur_dir+r'/inhe.cpp|49|6|void CGChild::response(void) {',
"CGChild|"+cur_dir+r'/inhe.cpp|75|5|    CGChild gchild;',
],
[""],
# 74 12
["gchild|"+cur_dir+"/inhe.cpp|75|13|    CGChild gchild;"],
["gchild|"+cur_dir+"/inhe.cpp|75|13|    CGChild gchild;"],
[
"gchild|"+cur_dir+"/inhe.cpp|79|5|    gchild.response();",
"gchild|"+cur_dir+"/inhe.cpp|83|11|    test(&gchild);",
],
[""],
# 76 5
["COther|"+cur_dir+"/inhe.cpp|53|7|class COther"],
["COther|"+cur_dir+"/inhe.cpp|53|7|class COther"],
[
"COther|"+cur_dir+r'/inhe.cpp|62|6|void COther::response(void) {',
"COther|"+cur_dir+r'/inhe.cpp|76|5|    COther other;',
],
[""],
# 76 12
["other|"+cur_dir+"/inhe.cpp|76|12|    COther other;"],
["other|"+cur_dir+"/inhe.cpp|76|12|    COther other;"],
[
"other|"+cur_dir+"/inhe.cpp|80|5|    other.response();",
"other|"+cur_dir+"/inhe.cpp|84|11|    test(&other);",
],
[""],
# 77 5
["parent|"+cur_dir+"/inhe.cpp|73|14|    CParent0 parent;"],
["parent|"+cur_dir+"/inhe.cpp|73|14|    CParent0 parent;"],
[
"parent|"+cur_dir+"/inhe.cpp|77|5|    parent.response();",
"parent|"+cur_dir+"/inhe.cpp|81|11|    test(&parent);",
],
[""],
# 77 12
["response|"+cur_dir+"/inhe.cpp|8|18|    virtual void response(void);"],
["response|"+cur_dir+"/inhe.cpp|11|16|void CParent0::response(void) {"],
[
"response|"+cur_dir+"/inhe.cpp|68|8|    a->response();",
"response|"+cur_dir+"/inhe.cpp|77|12|    parent.response();",
],
[
"response|"+cur_dir+"/inhe.cpp|33|18|    virtual void response(void);",
"response|"+cur_dir+"/inhe.cpp|36|14|void CChild::response(void) {",
"response|"+cur_dir+"/inhe.cpp|59|18|    virtual void response(void);",
"response|"+cur_dir+"/inhe.cpp|62|14|void COther::response(void) {",
],
# 78 5
["child|"+cur_dir+"/inhe.cpp|74|12|    CChild child;"],
["child|"+cur_dir+"/inhe.cpp|74|12|    CChild child;"],
[
"child|"+cur_dir+"/inhe.cpp|78|5|    child.response();",
"child|"+cur_dir+"/inhe.cpp|82|11|    test(&child);",
],
[""],
# 78 11
["response|"+cur_dir+"/inhe.cpp|33|18|    virtual void response(void);"],
["response|"+cur_dir+"/inhe.cpp|36|14|void CChild::response(void) {"],
["response|"+cur_dir+"/inhe.cpp|78|11|    child.response();"],
[
"response|"+cur_dir+"/inhe.cpp|46|18|    virtual void response(void);",
"response|"+cur_dir+"/inhe.cpp|49|15|void CGChild::response(void) {",
"response|"+cur_dir+"/inhe.cpp|8|18|    virtual void response(void);",
],
# 79 5
["gchild|"+cur_dir+"/inhe.cpp|75|13|    CGChild gchild;"],
["gchild|"+cur_dir+"/inhe.cpp|75|13|    CGChild gchild;"],
[
"gchild|"+cur_dir+"/inhe.cpp|79|5|    gchild.response();",
"gchild|"+cur_dir+"/inhe.cpp|83|11|    test(&gchild);",
],
[""],
# 79 12
["response|"+cur_dir+"/inhe.cpp|46|18|    virtual void response(void);"],
["response|"+cur_dir+"/inhe.cpp|49|15|void CGChild::response(void) {"],
["response|"+cur_dir+"/inhe.cpp|79|12|    gchild.response();"],
["response|"+cur_dir+"/inhe.cpp|33|18|    virtual void response(void);"],
# 80 5
["other|"+cur_dir+"/inhe.cpp|76|12|    COther other;"],
["other|"+cur_dir+"/inhe.cpp|76|12|    COther other;"],
[
"other|"+cur_dir+"/inhe.cpp|80|5|    other.response();",
"other|"+cur_dir+"/inhe.cpp|84|11|    test(&other);",
],
[""],
# 80 11
["response|"+cur_dir+"/inhe.cpp|59|18|    virtual void response(void);"],
["response|"+cur_dir+"/inhe.cpp|62|14|void COther::response(void) {"],
["response|"+cur_dir+"/inhe.cpp|80|11|    other.response();"],
[
"response|"+cur_dir+"/inhe.cpp|8|18|    virtual void response(void);",
"response|"+cur_dir+"/inhe.cpp|20|18|    virtual void response(void);",
],
# 81 5
["test|"+cur_dir+"/inhe.cpp|66|13|static void test(class CParent0 *a)"],
["test|"+cur_dir+"/inhe.cpp|66|13|static void test(class CParent0 *a)"],
[
"test|"+cur_dir+"/inhe.cpp|81|5|    test(&parent);",
"test|"+cur_dir+"/inhe.cpp|82|5|    test(&child);",
"test|"+cur_dir+"/inhe.cpp|83|5|    test(&gchild);",
"test|"+cur_dir+"/inhe.cpp|84|5|    test(&other);",
],
[""],
# 81 11
["parent|"+cur_dir+"/inhe.cpp|73|14|    CParent0 parent;"],
["parent|"+cur_dir+"/inhe.cpp|73|14|    CParent0 parent;"],
[
"parent|"+cur_dir+"/inhe.cpp|77|5|    parent.response();",
"parent|"+cur_dir+"/inhe.cpp|81|11|    test(&parent);",
],
[""],
# 82 5
["test|"+cur_dir+"/inhe.cpp|66|13|static void test(class CParent0 *a)"],
["test|"+cur_dir+"/inhe.cpp|66|13|static void test(class CParent0 *a)"],
[
"test|"+cur_dir+"/inhe.cpp|81|5|    test(&parent);",
"test|"+cur_dir+"/inhe.cpp|82|5|    test(&child);",
"test|"+cur_dir+"/inhe.cpp|83|5|    test(&gchild);",
"test|"+cur_dir+"/inhe.cpp|84|5|    test(&other);",
],
[""],
# 82 11
["child|"+cur_dir+"/inhe.cpp|74|12|    CChild child;"],
["child|"+cur_dir+"/inhe.cpp|74|12|    CChild child;"],
[
"child|"+cur_dir+"/inhe.cpp|78|5|    child.response();",
"child|"+cur_dir+"/inhe.cpp|82|11|    test(&child);",
],
[""],
# 83 5
["test|"+cur_dir+"/inhe.cpp|66|13|static void test(class CParent0 *a)"],
["test|"+cur_dir+"/inhe.cpp|66|13|static void test(class CParent0 *a)"],
[
"test|"+cur_dir+"/inhe.cpp|81|5|    test(&parent);",
"test|"+cur_dir+"/inhe.cpp|82|5|    test(&child);",
"test|"+cur_dir+"/inhe.cpp|83|5|    test(&gchild);",
"test|"+cur_dir+"/inhe.cpp|84|5|    test(&other);",
],
[""],
# 83 11
["gchild|"+cur_dir+"/inhe.cpp|75|13|    CGChild gchild;"],
["gchild|"+cur_dir+"/inhe.cpp|75|13|    CGChild gchild;"],
[
"gchild|"+cur_dir+"/inhe.cpp|79|5|    gchild.response();",
"gchild|"+cur_dir+"/inhe.cpp|83|11|    test(&gchild);",
],
[""],
# 84 5
["test|"+cur_dir+"/inhe.cpp|66|13|static void test(class CParent0 *a)"],
["test|"+cur_dir+"/inhe.cpp|66|13|static void test(class CParent0 *a)"],
[
"test|"+cur_dir+"/inhe.cpp|81|5|    test(&parent);",
"test|"+cur_dir+"/inhe.cpp|82|5|    test(&child);",
"test|"+cur_dir+"/inhe.cpp|83|5|    test(&gchild);",
"test|"+cur_dir+"/inhe.cpp|84|5|    test(&other);",
],
[""],
# 84 11
["other|"+cur_dir+"/inhe.cpp|76|12|    COther other;"],
["other|"+cur_dir+"/inhe.cpp|76|12|    COther other;"],
[
"other|"+cur_dir+"/inhe.cpp|80|5|    other.response();",
"other|"+cur_dir+"/inhe.cpp|84|11|    test(&other);",
],
[""],
]

err = 0
i = 0
for q in q_list:
    err += common.test_one(q, ans_list[i])
    i+=1
if err == 0:
    print "OK"
else:
    print "ERR: %d"%(err)

exit(err)
