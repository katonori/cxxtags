#!/usr/bin/python

import os
import commands
import shutil

CXXTAGS = "../../src/cxxtags"
err = 0

def test(cmd, in0, in1):
    os.system(cmd)
    os.system("sqlite3 %s \".dump\" > out0.txt"%(in0))
    os.system("sqlite3 %s \".dump\" > out1.txt"%(in1))
    if os.system("diff -q out0.txt out1.txt"):
        print "ERROR: " + in1 + ": " + cmd
        return 1
    return 0

# make ref
os.system(CXXTAGS + " main.cpp -I./subdir")
res = commands.getoutput("sqlite3 main.cpp.db \"select * from decl\" | wc -l")
wl_orig = int(res)
if wl_orig < 100:
    print "ERROR: reference generation"
    exit(1)
shutil.copy("main.cpp.db", "ref.full.db")

os.system(CXXTAGS + " -e /usr/include main.cpp -I./subdir")
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
err += test(CXXTAGS + " -e /usr/niclude main.cpp -I./subdir", "main.cpp.db", "ref.full.db")
err += test(CXXTAGS + " -e /usr/niclude -I./subdir main.cpp", "main.cpp.db", "ref.full.db")
err += test(CXXTAGS + " -I./subdir main.cpp -e /usr/include", "main.cpp.db", "ref.db")
err += test(CXXTAGS + " -o a.db -I./subdir main.cpp -e /usr/include", "a.db", "ref.db")
err += test(CXXTAGS + " -I./subdir main.cpp -e /usr/include -o a.db", "a.db", "ref.db")
err += test(CXXTAGS + " -I ./subdir main.cpp -e /usr/include -o a.db", "a.db", "ref.db")

if err == 0:
    print "OK"
exit(err)
