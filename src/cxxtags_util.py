#!/usr/bin/python
import os
import sqlite3
import traceback

def my_exit(val, msg):
    traceback.print_stack()
    print msg
    sys.exit(val)

def my_db_connect(fn):
    if not os.path.exists(fn):
        my_exit(1, "ERROR: DB connect: "+fn)
    db = sqlite3.connect(fn, isolation_level='EXCLUSIVE')
    return db


