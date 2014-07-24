#!/usr/bin/python

import os
import commands
import shutil
import sys
import re

LLVM_HOME =os.environ.get("LLVM_HOME")
CLANG_HOME =os.environ.get("CLANG_HOME")
if LLVM_HOME == None:
    print "ERROR: set LLVM_HOME"
    sys.exit(1)
if CLANG_HOME == None:
    print "ERROR: set CLANG_HOME"
    sys.exit(1)

CXXTAGS = "../../bin/cxxtags"
CXXTAGS_INCLUDES = "-I%s/include"%(CLANG_HOME)
USAGE = "usage: cxxtags [-E, --empty] [-p, --partial] [-e,--exclude exclude_list] [-o out_file] input_file [compiler_arguments]"
DB_INFO_COLS = 7
DB_VER = 7
err = 0

def msgTest(cmd, refMsg, refRv):
    rv = commands.getoutput("(%s > /dev/null 2>&1); echo $?"%(cmd))
    if rv != str(refRv):
        print "ERROR: return value: ",rv
        return 1
    out = commands.getoutput("%s"%(cmd))
    if out != refMsg:
        print "ERROR: message: ",out
        return 1
    return 0

def test(cmd, in0, in1, buildOption0, buildOption1, excludeList0, excludeList1):
    print cmd
    os.system(cmd)
    os.system("sqlite3 %s \".dump\" | grep -v 'INSERT INTO \"db_info\" VALUES' > out0.txt"%(in0))
    info0 = commands.getoutput('sqlite3 '+in0+' "SELECT * FROM db_info;"').split('|')
    os.system("sqlite3 %s \".dump\" | grep -v 'INSERT INTO \"db_info\" VALUES' > out1.txt"%(in1))
    info1 = commands.getoutput('sqlite3 ' + in1 + ' "SELECT * FROM db_info;"').split('|')
    if len(info0) != DB_INFO_COLS or (len(info0) != len(info1)):
        print "ERROR: db_info: ", info0
        print "              : ", info1
        return 1
    if info0[0] != str(DB_VER) or info1[0] != str(DB_VER):
        print "ERROR: db_info: DB_VER: ", info0
        return 1
    if info0[1] != info1[1]:
        print "ERROR: db_info: file name: ", info0
        print "                         : ", info1
        return 1
    if info0[2] != excludeList0 or info1[2] != excludeList1:
        print "ERROR: db_info: excludeList1: ", info0
        print "                            : ", info1
        return 1
    if info0[3] != info1[3]:
        print "ERROR: db_info: contained info: ", info0
        print "                              : ", info1
        return 1
    if info0[4] != info1[4]:
        print "ERROR: db_info: build dir: ", info0
        print "                         : ", info1
        return 1
    if info0[DB_INFO_COLS-1] != buildOption0:
        print "ERROR: db_info: ", info0
        print "     : buildOption:: ", buildOption0
        return 1
    if info1[DB_INFO_COLS-1] != buildOption1:
        print "ERROR: db_info: ", info1
        print "     : buildOption:: ", buildOption1
        return 1
    if os.system("diff -q out0.txt out1.txt"):
        print "ERROR: " + in1 + ": " + cmd
        return 1
    return 0

# make ref
buildOptRef = "-I./subdir " + CXXTAGS_INCLUDES
excludeListRef = "/usr/include"
os.system(CXXTAGS + " main.cpp "+buildOptRef)
res = commands.getoutput("sqlite3 main.cpp.db \"select * from decl\" | wc -l")
wl_orig = int(res)
if wl_orig < 100:
    print "ERROR: reference generation"
    exit(1)
shutil.copy("main.cpp.db", "ref.full.db")

os.system(CXXTAGS + " -e "+excludeListRef+" main.cpp "+buildOptRef)
res = commands.getoutput("sqlite3 main.cpp.db \"select * from decl\" | wc -l")
wl_exclude = int(res)
if wl_exclude < 100:
    print "ERROR: reference generation"
    exit(1)
shutil.copy("main.cpp.db", "ref.db")

if wl_orig <= wl_exclude:
    print "ERROR: exception list: line_num"
    err += 1
res = commands.getoutput("sqlite3 main.cpp.db \"select * from decl\" | grep /usr/include")
if res != "":
    print "ERROR: exception list: grep"
    err += 1

# argument tests
err += msgTest(CXXTAGS, USAGE, 1)
excludeList = "/usr/niclude"
err += test(CXXTAGS + " -e "+excludeList+" main.cpp "+buildOptRef, "main.cpp.db", "ref.full.db", buildOptRef, buildOptRef, excludeList, '')
err += test(CXXTAGS + " -e "+excludeList+" "+buildOptRef+" main.cpp", "main.cpp.db", "ref.full.db", buildOptRef, buildOptRef, excludeList, '')
err += test(CXXTAGS + " "+buildOptRef+" main.cpp -e "+excludeListRef, "main.cpp.db", "ref.db", buildOptRef, buildOptRef, excludeListRef, excludeListRef)
err += test(CXXTAGS + " -o a.db "+buildOptRef+" main.cpp -e "+excludeListRef, "a.db", "ref.db", buildOptRef, buildOptRef, excludeListRef, excludeListRef)
err += test(CXXTAGS + " "+buildOptRef+" main.cpp -e "+excludeListRef+" -o a.db", "a.db", "ref.db", buildOptRef, buildOptRef, excludeListRef, excludeListRef)
buildOpt = "-I ./subdir " + CXXTAGS_INCLUDES
err += test(CXXTAGS + " "+buildOpt+" main.cpp -e "+excludeListRef+" -o a.db", "a.db", "ref.db", buildOpt, buildOptRef, excludeListRef, excludeListRef)

# -g option test
"""
OPT_REF=" -I/usr/lib/llvm-3.5//include/ -I/ -I../../ -D_GNU_SOURCE -DA -DB"
cmd = CXXTAGS + " -v -G test.o | grep 'build option'"
print cmd
res = commands.getoutput(cmd)
m = re.match(r'^build option.+:(.+)$', res)
if m:
    res = m.group(1)
    if res != OPT_REF:
        print "ERROR: opt_ref: " + OPT_REF
        print "ERROR: opt: " + res
        err += 1
else:
    print "ERROR: could not get bild option from elf information"
    err += 1
"""

if err == 0:
    print "OK"
exit(err)
