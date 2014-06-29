#include "db.h"
#include <vector>
#include <map>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>

namespace cxxtags {

void IndexDb::tryStep(sqlite3_stmt *stmt)
{
    for(int i = 0; SQLITE_DONE != sqlite3_step(stmt); i++) {
        if(i > STEP_MAX_TRY_NUM) {
            printf("ERROR: SQLITE3: step\n");
            exit(1);
        }
    }
}

void IndexDb::prepareStatement(const char* queryInsertTmpl, sqlite3_stmt **sqlStmt)
{
    const char* err = NULL;
    if(SQLITE_OK != sqlite3_prepare_v2(mDb, queryInsertTmpl, -1, sqlStmt, &err)) {
        fprintf(stderr, "ERROR: initDb(): prepare: %s\n", sqlite3_errmsg(mDb));
        exit(1);
    }
}

void IndexDb::finDb(sqlite3_stmt *sqlStmt)
{
    sqlite3_finalize(sqlStmt);
}

void IndexDb::init(std::string db_file_name, std::string src_file_name, std::string excludeList, int isPartial, const char* curDir, int argc, const char** argv)
{
    char *err=NULL;
    if(sqlite3_open(db_file_name.c_str(), &mDb ) != SQLITE_OK) {
        printf("ERROR: faild to open db: %s", db_file_name.c_str());
        exit(1);
    }

    // format build options
    std::string build_opt = "";
    for(int i = 0; i < argc; i++) {
        build_opt += argv[i];
        build_opt += " ";
    }
    if(!build_opt.empty()) {
        build_opt = build_opt.substr(0, build_opt.length()-1);
    }

    // begin transaction
    sqlite3_exec(mDb, "BEGIN EXCLUSIVE;", NULL, NULL, NULL);
    //
    // db_info
    //
    // contained_part| 0:full, 1:partial
    //
    sqlite3_exec(mDb, "CREATE TABLE db_info(db_format INTEGER, src_file_name TEXT, exclude_list TEXT, contained_part INTEGER, build_dir TEXT, build_options);", NULL, NULL, &err);
    // file_list
    sqlite3_exec(mDb, "CREATE TABLE file_list(id INTEGER, name TEXT);", NULL, NULL, &err);
    // usr_list
    sqlite3_exec(mDb, "CREATE TABLE usr_list(id INTEGER, name TEXT);", NULL, NULL, &err);
    // name_list
    sqlite3_exec(mDb, "CREATE TABLE name_list(id INTEGER, name TEXT);", NULL, NULL, &err);
    // ref
    sqlite3_exec(mDb, "CREATE TABLE ref(usr_id INTEGER, name_id INTEGER, file_id INTEGER, line INTEGER, col INTEGER, kind INTEGER, ref_file_id INTEGER, ref_line INTEGER, ref_col INTEGER);", NULL, NULL, &err);
    // decl
    sqlite3_exec(mDb, "CREATE TABLE decl(usr_id INTEGER, name_id INTEGER, file_id INTEGER, line INTEGER, col INTEGER, kind INTEGER, val INTEGER, is_virtual INTEGER, is_def INTEGER, type_usr_id INTEGER, type_kind INTEGER, is_pointer, accessibility INTEGER);", NULL, NULL, &err);
    // overriden
    sqlite3_exec(mDb, "CREATE TABLE overriden(usr_id INTEGER, name_id INTEGER, file_id INTEGER, line INTEGER, col INTEGER, kind INTEGER, overrider_usr_id INTEGER, is_def INTEGER);", NULL, NULL, &err);
    //
    // base class info
    //
    // accessibility| 0: invalid, 1: public, 2: protected, 3: private
    //
    sqlite3_exec(mDb, "CREATE TABLE base_class(class_usr_id INTEGER, base_class_usr_id INTEGER, line INTEGER, col INTEGER, accessibility INTEGER);", NULL, NULL, &err);
    // include
    sqlite3_exec(mDb, "CREATE TABLE include(file_id INTEGER, included_file_id INTEGER, line INTEGER, col INTEGER);", NULL, NULL, &err);

    // register databasee information
    std::ostringstream os;
    int contained_part = isPartial ? CONTAINED_PART_PARTIAL : CONTAINED_PART_FULL;
    os << "INSERT INTO db_info VALUES(" << DB_VER << ", '" << src_file_name << "','" << excludeList << "'," << contained_part << ", '" << curDir << "','" << build_opt << "');";
    sqlite3_exec(mDb, os.str().c_str(), NULL, NULL, &err);

    // prepare queries
    prepareStatement("INSERT INTO ref VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", &mSqlStmtRef);
    prepareStatement("INSERT INTO decl VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", &mSqlStmtDecl);
    prepareStatement("INSERT INTO overriden VALUES (?, ?, ?, ?, ?, ?, ?, ? );", &mSqlStmtOverriden);
    prepareStatement("INSERT INTO base_class VALUES (?, ?, ?, ?, ?);", &mSqlStmtBaseClass);
}

void IndexDb::insert_ref_value(int usrId, int nameId, int fileId, int line, int col, int kind, int refFileId, int refLine, int refCol)
{
    sqlite3_reset(mSqlStmtRef);
    sqlite3_bind_int(mSqlStmtRef, 1, usrId);
    sqlite3_bind_int(mSqlStmtRef, 2, nameId);
    sqlite3_bind_int(mSqlStmtRef, 3, fileId);
    sqlite3_bind_int(mSqlStmtRef, 4, line);
    sqlite3_bind_int(mSqlStmtRef, 5, col);
    sqlite3_bind_int(mSqlStmtRef, 6, kind);
    sqlite3_bind_int(mSqlStmtRef, 7, refFileId);
    sqlite3_bind_int(mSqlStmtRef, 8, refLine);
    sqlite3_bind_int(mSqlStmtRef, 9, refCol);
    tryStep(mSqlStmtRef);
}

void IndexDb::insert_decl_value(int usrId, int nameId, int fileId, int line, int col, int entityKind, int val, int isVirtual, int isDef, int typeUsrId, int typeKind, int isPointer)
{
    sqlite3_reset(mSqlStmtDecl);
    sqlite3_bind_int(mSqlStmtDecl, 1, usrId);
    sqlite3_bind_int(mSqlStmtDecl, 2, nameId);
    sqlite3_bind_int(mSqlStmtDecl, 3, fileId);
    sqlite3_bind_int(mSqlStmtDecl, 4, line);
    sqlite3_bind_int(mSqlStmtDecl, 5, col);
    sqlite3_bind_int(mSqlStmtDecl, 6, entityKind);
    sqlite3_bind_int(mSqlStmtDecl, 7, val);
    sqlite3_bind_int(mSqlStmtDecl, 8, isVirtual);
    sqlite3_bind_int(mSqlStmtDecl, 9, isDef);
    sqlite3_bind_int(mSqlStmtDecl, 10, typeUsrId);
    sqlite3_bind_int(mSqlStmtDecl, 11, typeKind);
    sqlite3_bind_int(mSqlStmtDecl, 12, isPointer);
    sqlite3_bind_int(mSqlStmtDecl, 13, 0); // accessibility
    tryStep(mSqlStmtDecl);
}

void IndexDb::insert_overriden_value(int usrId, int nameId, int fileId, int line, int col, int entityKind, int usrIdOverrider, int isDef)
{
    sqlite3_reset(mSqlStmtOverriden);
    sqlite3_bind_int(mSqlStmtOverriden, 1, usrId);
    sqlite3_bind_int(mSqlStmtOverriden, 2, nameId);
    sqlite3_bind_int(mSqlStmtOverriden, 3, fileId);
    sqlite3_bind_int(mSqlStmtOverriden, 4, line);
    sqlite3_bind_int(mSqlStmtOverriden, 5, col);
    sqlite3_bind_int(mSqlStmtOverriden, 6, entityKind);
    sqlite3_bind_int(mSqlStmtOverriden, 7, usrIdOverrider);
    sqlite3_bind_int(mSqlStmtOverriden, 8, isDef);
    tryStep(mSqlStmtOverriden);
}

void IndexDb::insert_base_class_value(int classUsrId, int baseClassUsrId, int line, int col, int accessibility)
{
    sqlite3_reset(mSqlStmtBaseClass);
    sqlite3_bind_int(mSqlStmtBaseClass, 1, classUsrId);
    sqlite3_bind_int(mSqlStmtBaseClass, 2, baseClassUsrId);
    sqlite3_bind_int(mSqlStmtBaseClass, 3, line);
    sqlite3_bind_int(mSqlStmtBaseClass, 4, col);
    sqlite3_bind_int(mSqlStmtBaseClass, 5, accessibility);
    tryStep(mSqlStmtBaseClass);
}

void IndexDb::addIdList(const std::map<std::string, int >& inMap, std::string tableName)
{
    const char *err=NULL;
    sqlite3_stmt* stmt;
    std::ostringstream os;
    os << "INSERT INTO " << tableName << " VALUES(?, ?);";
    if(SQLITE_OK != sqlite3_prepare_v2(mDb, os.str().c_str(), -1, &stmt, &err)) {
        fprintf(stderr, "ERROR: prepare: %s\n", sqlite3_errmsg(mDb));
        exit(1);
    }

    // lookup map
    std::map<std::string, int >::const_iterator end = inMap.end();
    for(std::map<std::string, int >::const_iterator itr = inMap.begin();
            itr != end;
            itr++) {
        sqlite3_reset(stmt);
        sqlite3_bind_int(stmt, 1, itr->second);
        sqlite3_bind_text(stmt, 2, itr->first.c_str(), -1, SQLITE_STATIC);
        tryStep(stmt);
    }
    sqlite3_finalize(stmt);
    return ;
}

void IndexDb::fin(const std::map<std::string, int >& fileMap, const std::map<std::string, int >& usrMap, const std::map<std::string, int >& nameMap)
{
    addIdList(fileMap, "file_list");
    addIdList(usrMap, "usr_list");
    addIdList(nameMap, "name_list");

    finDb(mSqlStmtRef);
    finDb(mSqlStmtDecl);
    finDb(mSqlStmtOverriden);
    finDb(mSqlStmtBaseClass);

    // create indices
    sqlite3_exec(mDb, "CREATE INDEX file_list_index0 ON file_list(id);", NULL, NULL, NULL);
    sqlite3_exec(mDb, "CREATE INDEX file_list_index1 ON file_list(name);", NULL, NULL, NULL);
    sqlite3_exec(mDb, "CREATE INDEX usr_list_index0 ON usr_list(id);", NULL, NULL, NULL);
    sqlite3_exec(mDb, "CREATE INDEX usr_list_index1 ON usr_list(name);", NULL, NULL, NULL);
    sqlite3_exec(mDb, "CREATE INDEX name_list_index0 ON name_list(id);", NULL, NULL, NULL);
    sqlite3_exec(mDb, "CREATE INDEX name_list_index1 ON name_list(name);", NULL, NULL, NULL);
    sqlite3_exec(mDb, "CREATE INDEX ref_index0 ON ref(file_id, name_id, line, col);", NULL, NULL, NULL);
    sqlite3_exec(mDb, "CREATE INDEX ref_index1 ON ref(file_id);", NULL, NULL, NULL);
    sqlite3_exec(mDb, "CREATE INDEX ref_index2 ON ref(usr_id);", NULL, NULL, NULL);
    sqlite3_exec(mDb, "CREATE INDEX decl_index0 ON decl(file_id, name_id, line, col);", NULL, NULL, NULL);
    sqlite3_exec(mDb, "CREATE INDEX decl_index1 ON decl(file_id)", NULL, NULL, NULL);
    sqlite3_exec(mDb, "CREATE INDEX decl_index2 ON decl(usr_id)", NULL, NULL, NULL);
    sqlite3_exec(mDb, "CREATE INDEX decl_index3 ON decl(usr_id, is_def)", NULL, NULL, NULL);
    // end transaction
    sqlite3_exec(mDb, "END TRANSACTION;", NULL, NULL, NULL);
    if(SQLITE_OK != sqlite3_close(mDb)) {
        fprintf(stderr, "ERROR: %s\n", sqlite3_errmsg(mDb));
        exit(1);
    }
}

};
