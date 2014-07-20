#!/usr/bin/env python

import os, sys
import getopt
import datetime

CXXTAGS = "cxxtags"
CXXTAGS_DB_MANAGER = "cxxtags_db_manager"
CXXTAGS_OPT = "-E -p"

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
if output == None:
    #print "could not determine output file: " + " ".join(argv)
    # generate output filename
    dt = str(datetime.datetime.now())
    dt = dt.replace(" ", "_")
    output = dt.replace(":", "_") + "." + str(os.getpid()) + ".db"
    #print "use random name: "  + output
if not "-MM" in argv:
    args_tmp = [CXXTAGS, CXXTAGS_OPT, exclude, " ".join(argv), " -o " + output]
    # run cxxtags
    cmd = " ".join(args_tmp)
    os.system(cmd)
    args_tmp = [CXXTAGS_DB_MANAGER, "add", db_dst, output]
    cmd = " ".join(args_tmp)
    os.system(cmd)

# run compilation
cmd = compiler + " " + " ".join(argv_orig)
exit(os.system(cmd))
