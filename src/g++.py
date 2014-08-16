#!/usr/bin/env python

import os, sys
import getopt
import datetime

CXXTAGS = "cxxtags"
#CXXTAGS_OPT = "-E -p"
CXXTAGS_OPT = ""

db_dst = ""
if "CXXTAGS_DB_DST" in os.environ:
    db_dst = os.environ["CXXTAGS_DB_DST"]
else:
    print "ERROR: set tag database directory CXXTAGS_DB_DST to generate tag database"
    sys.exit(1)

compiler = "g++"
if "CXXTAGS_CXX" in os.environ:
    compiler = os.environ["CXXTAGS_CXX"]
exclude = ""
if "CXXTAGS_EXCLUDE" in os.environ:
    exclude = os.environ["CXXTAGS_EXCLUDE"]
if exclude != "":
    exclude = "-e " + exclude

# get output filename
output = None
i = 0
argv_orig = sys.argv[1:]
argv = sys.argv[1:]
"""
while 1:
    if i >= len(argv):
        break
    arg = argv[i]
    if arg == "-o":
        output = argv[i+1] + ".db"
        del argv[i:i+2]
        i += 2
    else:
        i += 1
"""
if not "-MM" in argv:
    args_tmp = [CXXTAGS, CXXTAGS_OPT, exclude, db_dst, " ".join(argv)]
    # run cxxtags
    cmd = " ".join(args_tmp)
    os.system(cmd)

# run compilation
cmd = compiler + " " + " ".join(argv_orig)
exit(os.system(cmd))
