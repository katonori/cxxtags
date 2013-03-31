#!/usr/bin/python
""" Usage: call with <filename> <typename>
"""

import sys
import os
import re
import sqlite3
import clang.cindex

in_file_abs = ""
db = None

exception_list = [
"/usr/include/",
]

decl_node_type_list = [
"CLASS_DECL",
"NAMESPACE",
"STRUCT_DECL",
"CLASS_TEMPLATE",
"UNION_DECL",
"VAR_DECL",
"PARM_DECL",
"FIELD_DECL",
"FUNCTION_DECL",
"CXX_METHOD",
"CONSTRUCTOR",
"DESTRUCTOR",
"TYPEDEF_DECL",
"MACRO_DEFINITION",
"ENUM_CONSTANT_DECL",
]

ref_node_type_list = [
"DECL_REF_EXPR",
"MEMBER_REF_EXPR",
"TYPE_REF",
"VARIABLE_REF",
"MEMBER_REF",
"TEMPLATE_REF",
"MACRO_INSTANTIATION",
"NAMESPACE_REF",
]


def q_insert_decl(usr, name, file_name, line, col, kind, val, is_def):
    q = "insert into decl values(\"%s\", \"%s\", \"%s\", %d, %d, \"%s\", %d, %d);" % (usr, name, file_name, line, col, kind, val, is_def)
    db.execute(q)

def q_insert_ref(usr, name, file_name, line, col, kind, ref_file_name, ref_line, ref_col):
    #print "[REF]%s, %s, %s, %d, %d, %s, %s, %s, %d, %d" % (usr, name, file_name, line, col, kind, ref_file_name, ref_line, ref_col)
    q = "insert into ref values(\"%s\",\"%s\", \"%s\", %d, %d, \"%s\", \"%s\", %d, %d);" % (usr, name, file_name, line, col, kind, ref_file_name, ref_line, ref_col)
    db.execute(q)

# generate uniq USR
def get_db_usr(usr, file_name):
    # do nothing
    return usr
    #print "orig: %s, %s" % (usr, file_name)
    #m_file = re.search(r'^/', file_name)
    m = re.search(r"^c:([^@]+)", usr)
    if m:
        m_path = re.search(r"^/", m.group(1))
        if not m_path: # main source file
            usr = re.sub(r"^c:[^@]+", "c:%s" % (in_file_abs), usr)
    return usr

def is_in_exception_list(file_name):
    global exception_list
    for str in exception_list:
        if re.search(str, file_name):
            return 1
    return 0

def visit_node(node):
    global ref_node_type_list
    global decl_node_type_list
    nkn = node.kind.name
    usr = node.get_usr()
    file_name = node.location.file
    if file_name == None:
        file_name = ""
    else:
        file_name = str(file_name)
    if file_name != "" and re.search("^/", file_name) == None:
        file_name = os.path.abspath(file_name) # get absolute path
    if is_in_exception_list(file_name) == 0:
        name = node.displayname
        #name = node.spelling
        #name = clang.cindex.conf.lib.clang_getCursorSpelling(node)
        if nkn in decl_node_type_list:
            # get name from displayname
            name = re.sub(r"\(.*\)", "", name)
            usr = get_db_usr(usr, file_name)
            val = 0
            if nkn == "ENUM_CONSTANT_DECL":
                val = node.enum_value
            # register to db
            q_insert_decl(usr, name, file_name, node.location.line, node.location.column, nkn, val, node.is_definition())
        elif nkn in ref_node_type_list:
            usr = get_db_usr(usr, file_name)
            if name != "":
                # discard "class "
                m = re.match("^class ", name)
                if m:
                    cm = re.search("([^:\s]+)$", name)
                    if cm:
                        name = cm.group(1)

                ref_cur = clang.cindex.conf.lib.clang_getCursorReferenced(node)
                if not ref_cur or ref_cur == clang.cindex.conf.lib.clang_getNullCursor():
                    ref_usr = ""
                    ref_file_name = ""
                    ref_line = -1
                    ref_col = -1
                else:
                    ref_file_name = str(ref_cur.location.file)
                    if ref_file_name == None:
                        ref_file_name = ""
                    if ref_file_name != "" and re.search("^/", ref_file_name) == None:
                        ref_file_name = os.path.abspath(ref_file_name) # get absolute path
                    ref_usr = get_db_usr(ref_cur.get_usr(), ref_file_name)
                    ref_line = ref_cur.location.line
                    ref_col = ref_cur.location.column
                # register to db
                q_insert_ref(ref_usr, name, file_name, node.location.line, node.location.column, nkn, ref_file_name, ref_line, ref_col)

    for c in node.get_children():
        visit_node(c)

###################### main ###################### 
src_name = sys.argv[1]
if not os.path.exists(src_name):
    print "ERROR: file not found: %s\n"%(src_name)
    exit(1)
db_file_name = "%s.db" % (src_name)
if os.path.exists(db_file_name):
    os.remove(db_file_name)
db = sqlite3.connect(db_file_name)
#db.isolation_level = None

db.execute(
        u"""
        create table db_info(
            version integer
            );
        """
)
db.execute(
        u"""
        create table ref(
            usr text,
            name text,
            file_name text,
            line integer,
            col integer,
            kind text,
            ref_file_name text,
            ref_line integer,
            ref_col integer
            );
        """
     )
db.execute(
        u"""
        create table decl(
            usr text,
            name text,
            file_name text,
            line integer,
            col integer,
            kind text,
            val integer,
            is_def integer);
        """
     )
db.execute("insert into db_info values(%d);" % (2))

index = clang.cindex.Index.create()
in_file_abs = os.path.abspath(src_name)
#print "compile args: ", sys.argv[2:len(sys.argv)]
tu = index.parse(src_name, sys.argv[2:len(sys.argv)], None, 1)
#print 'generating tags:', tu.spelling
visit_node(tu.cursor)
db.commit()
db.close()
