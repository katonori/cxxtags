#include "db.h"
#include <vector>
#include <map>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>

namespace cxxtags {
static const int STEP_MAX_TRY_NUM = 1024;
static void tryStep(sqlite3_stmt *stmt)
{
    for(int i = 0; SQLITE_DONE != sqlite3_step(stmt); i++) {
        if(i > STEP_MAX_TRY_NUM) {
            printf("ERROR: SQLITE3: step\n");
            exit(1);
        }
    }
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

    // instantiate
    mRefMgr = new(DBMgrRef);
    mDeclMgr = new(DBMgrDecl);
    overridenMgr = new(DBMgrOverriden);
    baseClassMgr = new(DBMgrBaseClass);

    // prepare queries
    mRefMgr->InitDb(mDb);
    mDeclMgr->InitDb(mDb);
    overridenMgr->InitDb(mDb);
    baseClassMgr->InitDb(mDb);
}

void IndexDb::insert_ref_value(int usrId, int nameId, int fileId, int line, int col, int kind, int refFileId, int refLine, int refCol)
{
    mRefMgr->InsertValue(usrId, nameId, fileId, line, col, kind, refFileId, refLine, refCol);
    return ;
}

void IndexDb::insert_decl_value(int usrId, int nameId, int fileId, int line, int col, int entityKind, int val, int isVirtual, int isDef, int typeUsrId, int typeKind, int isPointer)
{
    mDeclMgr->InsertValue(usrId, nameId, fileId, line, col, entityKind, val, isVirtual, isDef, typeUsrId, typeKind, isPointer);
}

void IndexDb::insert_overriden_value(int usrId, int nameId, int fileId, int line, int col, int entityKind, int usrIdOverrider, int isDef)
{
    overridenMgr->InsertValue(usrId, nameId, fileId, line, col, entityKind, usrIdOverrider, isDef);
    return ;
}

void IndexDb::insert_base_class_value(int classUsrId, int baseClassUsrId, int line, int col, int accessibility)
{
    baseClassMgr->InsertValue(classUsrId, baseClassUsrId, line, col, accessibility);
    return ;
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

    mRefMgr->FinDb(mDb);
    mDeclMgr->FinDb(mDb);
    overridenMgr->FinDb(mDb);
    baseClassMgr->FinDb(mDb);
    delete mRefMgr;
    delete mDeclMgr;
    delete overridenMgr;
    delete baseClassMgr;

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

// DBMgrBase
void IndexDb::DBMgrBase::InitDb(sqlite3* db)
{
    const char* err = NULL;
    if(SQLITE_OK != sqlite3_prepare_v2(db, mQueryInsertTmpl, -1, &mSqlStmt, &err)) {
        fprintf(stderr, "ERROR: initDb(): prepare: %s\n", sqlite3_errmsg(db));
        exit(1);
    }
}

void IndexDb::DBMgrBase::FinDb(sqlite3* db)
{
    sqlite3_finalize(mSqlStmt);
}

// DBMgrRef
void IndexDb::DBMgrRef::InsertValue(int usrId, int nameId, int fileId, int line, int col, int kind, int refFileId, int refLine, int refCol)
{
    sqlite3_reset(mSqlStmt);
    sqlite3_bind_int(mSqlStmt, 1, usrId);
    sqlite3_bind_int(mSqlStmt, 2, nameId);
    sqlite3_bind_int(mSqlStmt, 3, fileId);
    sqlite3_bind_int(mSqlStmt, 4, line);
    sqlite3_bind_int(mSqlStmt, 5, col);
    sqlite3_bind_int(mSqlStmt, 6, kind);
    sqlite3_bind_int(mSqlStmt, 7, refFileId);
    sqlite3_bind_int(mSqlStmt, 8, refLine);
    sqlite3_bind_int(mSqlStmt, 9, refCol);
    tryStep(mSqlStmt);
}

// DBMgrDecl
void IndexDb::DBMgrDecl::InsertValue(int usrId, int nameId, int fid, int line, int col, int entityKind, int val, int isVirtual, int isDef, int typeUsrId, int typeKind, int isPointer)
{
    sqlite3_reset(mSqlStmt);
    sqlite3_bind_int(mSqlStmt, 1, usrId);
    sqlite3_bind_int(mSqlStmt, 2, nameId);
    sqlite3_bind_int(mSqlStmt, 3, fid);
    sqlite3_bind_int(mSqlStmt, 4, line);
    sqlite3_bind_int(mSqlStmt, 5, col);
    sqlite3_bind_int(mSqlStmt, 6, entityKind);
    sqlite3_bind_int(mSqlStmt, 7, val);
    sqlite3_bind_int(mSqlStmt, 8, isVirtual);
    sqlite3_bind_int(mSqlStmt, 9, isDef);
    sqlite3_bind_int(mSqlStmt, 10, typeUsrId);
    sqlite3_bind_int(mSqlStmt, 11, typeKind);
    sqlite3_bind_int(mSqlStmt, 12, isPointer);
    sqlite3_bind_int(mSqlStmt, 13, 0); // accessibility
    tryStep(mSqlStmt);
}

// DBMgrOverriden
void IndexDb::DBMgrOverriden::InsertValue(int usrId, int nameId, int fid, int line, int col, int entityKind, int overriderUsrId, int isDef)
{
    sqlite3_reset(mSqlStmt);
    sqlite3_bind_int(mSqlStmt, 1, usrId);
    sqlite3_bind_int(mSqlStmt, 2, nameId);
    sqlite3_bind_int(mSqlStmt, 3, fid);
    sqlite3_bind_int(mSqlStmt, 4, line);
    sqlite3_bind_int(mSqlStmt, 5, col);
    sqlite3_bind_int(mSqlStmt, 6, entityKind);
    sqlite3_bind_int(mSqlStmt, 7, overriderUsrId);
    sqlite3_bind_int(mSqlStmt, 8, isDef);
    tryStep(mSqlStmt);
}

// DBMgrBaseClass
void IndexDb::DBMgrBaseClass::InsertValue(int classUsrId, int baseClassUsrId, int line, int col, int accessibility)
{
    sqlite3_reset(mSqlStmt);
    sqlite3_bind_int(mSqlStmt, 1, classUsrId);
    sqlite3_bind_int(mSqlStmt, 2, baseClassUsrId);
    sqlite3_bind_int(mSqlStmt, 3, line);
    sqlite3_bind_int(mSqlStmt, 4, col);
    sqlite3_bind_int(mSqlStmt, 5, accessibility);
    tryStep(mSqlStmt);
}
};
