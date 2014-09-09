#!/usr/bin/python
import os
import sys
import sqlite3
import traceback
import re

FILE_INDEX_FILE_NAME = "file_index.db"
SCRIPT_DIR = os.path.dirname(__file__)

def my_exit(val, msg):
    traceback.print_stack()
    print msg
    sys.exit(val)

def get_line_from_file(fn, line_no):
    line_no = int(line_no)
    fi = open(fn, 'r')
    all_lines = fi.readlines()
    str_line = ""
    if len(all_lines) < line_no:
        my_exit(1, "ERROR: get_line_from_file: %s, %d\n"%(fn, line_no))
    else:
        str_line = all_lines[line_no-1]
    str_line = str_line.rstrip('\r\n')
    fi.close()
    return str_line

def get_usr_id(fn, usr):
    db = db_connect(fn)
    cur = db.cursor()
    cur.execute('SELECT usr_list.id FROM usr_list WHERE name=?;', (usr,))
    row = cur.fetchone()
    db.close()
    if row:
        return row[0]
    return -1

def rebuild_and_connect_if_is_skel(db_dir, fn):
    db = db_connect(fn)
    cur = db.cursor()
    cur.execute("SELECT src_file_name, is_skel FROM db_info;")
    #isSkel = is_db_skel(db)
    row = cur.fetchone()
    if row:
        srcFilename, isSkel = row
    else:
        return None
    if isSkel == 1:
        db.close()
        # rebuild database
        cmd = SCRIPT_DIR + "/cxxtags_db_manager rebuild %s %s"%(db_dir, os.path.abspath(srcFilename))
        rv = os.system(cmd)
        if rv == 0:
            db = db_connect(fn)
        else:
            print "ERROR: rebuild of the database file faild: rv=%d: "%(rv) + cmd
    return db

def db_connect(fn):
    if not os.path.exists(fn):
        my_exit(1, "ERROR: DB connect: "+fn)
    db = sqlite3.connect(fn, isolation_level='EXCLUSIVE')
    return db

def is_db_skel(db):
    cur = db.cursor()
    cur.execute("SELECT is_skel FROM db_info;")
    row = cur.fetchone()
    if row:
        return row[0]
    return None

def get_db_file_list(db_dir):
    db = db_connect(db_dir + "/" + FILE_INDEX_FILE_NAME)
    cur = db.cursor()
    cur.execute("SELECT db_file FROM file_index;")
    db_dict = {}
    for i in cur.fetchall():
        fn = db_dir + "/" + i[0]
        if not db_dict.has_key(fn):
            db_dict[fn] = 1
    return db_dict.keys()

def get_src_file_list(db_dir):
    db = db_connect(db_dir + "/" + FILE_INDEX_FILE_NAME)
    cur = db.cursor()
    cur.execute("SELECT * FROM file_index;")
    src_files = []
    for i in cur.fetchall():
        (srcFile, isSrc, dbFile) = i
        if isSrc != 0:
            src_files.append(srcFile)
    return src_files

def get_db_by_file_name(db_dir, file_name):
    file_name = os.path.abspath(file_name)
    db = db_connect(db_dir + "/" + FILE_INDEX_FILE_NAME)
    cur = db.cursor()
    cur.execute("SELECT db_file FROM file_index WHERE file_name=?;", (file_name,))
    row = cur.fetchone()
    if row == None:
        my_exit(1, "database file is not found: " + file_name)
    db_fn = row[0]
    return db_connect(db_dir + "/" + db_fn)

def get_db_files_by_src_file_name(db_dir, file_name):
    db_list = []
    if file_name == "":
        return db_list
    db = db_connect(db_dir + "/" + FILE_INDEX_FILE_NAME)
    cur = db.cursor()
    cur.execute("SELECT file_name, db_file FROM file_index WHERE file_name LIKE ?;", ('%'+file_name,))
    for row in cur.fetchall():
        res_src_file, res_db_file = row
        if pathCmp(res_src_file, file_name):
            db_list.append(db_dir + '/' + res_db_file)
    return db_list

def get_db_by_file_name_match(db_dir, file_name):
    db_list = []
    db = db_connect(db_dir + "/" + FILE_INDEX_FILE_NAME)
    cur = db.cursor()
    cur.execute("SELECT file_name, db_file FROM file_index WHERE file_name LIKE ?;", ('%'+file_name+'%',))
    for row in cur.fetchall():
        res_src_file, res_db_file = row
        if re.search(file_name + '$', res_src_file):
            db_list.append(db_dir + '/' + res_db_file)
    return db_list

# compare path.
def pathCmp(pathFull, pathPart):
    if -1 == pathPart.find('/'): # basename
        # if a basename specified complete match is needed.
        if pathPart == os.path.basename(pathFull):
            return True
    else:
        # If the path includes directory partial match is OK.
        if -1 != pathFull.find(pathPart):
            return True
    return False

QUERY_JOINED_TABLE_FILELIST_REF = 'ref, file_list ON ref.file_id=file_list.id'
QUERY_JOINED_TABLE_REF = '(((ref, file_list ON ref.file_id=file_list.id), file_list AS ref_file_list ON ref.ref_file_id=ref_file_list.id),usr_list ON ref.usr_id=usr_list.id), name_list ON ref.name_id=name_list.id'
QUERY_JOINED_TABLE_FILELIST_DECL = 'decl, file_list ON decl.file_id=file_list.id'
QUERY_JOINED_TABLE_DECL = '(((decl, file_list ON decl.file_id=file_list.id), usr_list ON decl.usr_id=usr_list.id), name_list ON decl.name_id=name_list.id), usr_list AS usr_list_type ON decl.type_usr_id=usr_list_type.id'
QUERY_JOINED_TABLE_FILELIST_OVERRIDEN = 'overriden,file_list ON overriden.file_id=file_list.id'
QUERY_JOINED_TABLE_OVERRIDEN = '(((overriden,file_list ON overriden.file_id=file_list.id), usr_list ON usr_list.id=overriden.usr_id), usr_list AS usr_list_overrider ON usr_list_overrider.id=overriden.overrider_usr_id), name_list ON overriden.name_id=name_list.id'
QUERY_JOINED_TABLE_BASE_CLASS = '(base_class, usr_list ON base_class.class_usr_id=usr_list.id), usr_list AS usr_list_base ON usr_list_base.id=base_class.base_class_usr_id'
