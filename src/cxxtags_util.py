#!/usr/bin/python
import os
import sys
import sqlite3
import traceback

def my_exit(val, msg):
    traceback.print_stack()
    print msg
    sys.exit(val)

def db_connect(fn):
    if not os.path.exists(fn):
        my_exit(1, "ERROR: DB connect: "+fn)
    db = sqlite3.connect(fn, isolation_level='EXCLUSIVE')
    return db

def get_db_file_list(db_dir):
    db = db_connect(db_dir + "/" + "file_index.db")
    cur = db.cursor()
    cur.execute("SELECT db_file FROM file_index;")
    db_list = []
    for i in cur.fetchall():
        db_list.append(db_dir + "/" + i[0])
    return db_list

def get_db_by_file_name(db_dir, file_name):
    file_name = os.path.abspath(file_name)
    db = db_connect(db_dir + "/" + "file_index.db")
    cur = db.cursor()
    cur.execute("SELECT db_file FROM file_index WHERE file_name='%s';"%(file_name))
    row = cur.fetchone()
    if row == None:
        my_exit(1, "database file is not found: " + file_name)
    db_fn = row[0]
    return db_connect(db_dir + "/" + db_fn)

QUERY_JOINED_TABLE_REF = '(ref,file_list AS ref_file_list ON ref.ref_file_id=ref_file_list.id),file_list ON ref.file_id=file_list.id'
QUERY_JOINED_TABLE_DECL = 'decl,file_list ON decl.file_id=file_list.id'
QUERY_JOINED_TABLE_OVERRIDEN = 'overriden,file_list ON overriden.file_id=file_list.id'
