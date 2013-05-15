#!/usr/bin/python

import os
import sys
import commands

CXXTAGS = "../../bin/cxxtags"
SQLITE3 = "sqlite3"
gErr = 0

def test(cmd, ref):
    global gErr
    os.system(cmd)
    out = commands.getoutput(SQLITE3 + ' inhe.db "SELECT contained_part FROM db_info"')
    if out != str(ref):
        print "ERROR: %s, %s"%(out, ref)
        gErr += 1

def main():
    global gErr
    test(CXXTAGS + " ../inheritance/inhe.cpp -o inhe.db", 0)
    test(CXXTAGS + " -e /usr ../inheritance/inhe.cpp -o inhe.db", 0)
    test(CXXTAGS + " -p ../inheritance/inhe.cpp -o inhe.db", 1)
    test(CXXTAGS + " --partial ../inheritance/inhe.cpp -o inhe.db", 1)
    test(CXXTAGS + " -e /usr -p ../inheritance/inhe.cpp -o inhe.db", 1)
    test(CXXTAGS + " -e /usr --partial ../inheritance/inhe.cpp -o inhe.db", 1)
    test(CXXTAGS + " --exclude /usr:/opt --partial ../inheritance/inhe.cpp -o inhe.db", 1)

    if gErr:
        print "NG"
    else:
        print "OK"
    sys.exit(gErr)

########
main()
