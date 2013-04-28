#include "db.h"
#include <vector>
#include <map>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>

namespace db {
static sqlite3 *db;
static CDBMgrDecl* declMgr;
static CDBMgrOverriden* overridenMgr;
static CDBMgrRef* refMgr;

void init(std::string db_file_name, std::string src_file_name)
{
    char *err=NULL;
    if(sqlite3_open(db_file_name.c_str(), &db ) != SQLITE_OK) {
        printf("ERROR: failt to open db");
        exit(1);
    }
    // begin transaction
    sqlite3_exec(db, "BEGIN EXCLUSIVE;", NULL, NULL, NULL);
    // db_info
    sqlite3_exec(db, "CREATE TABLE db_info(db_format INTEGER, src_file_name TEXT);", NULL, NULL, &err);
    // file_list
    sqlite3_exec(db, "CREATE TABLE file_list(id INTEGER, name TEXT);", NULL, NULL, &err);
    // ref
    sqlite3_exec(db, "CREATE TABLE ref(usr TEXT, name TEXT, file_id INTEGER, line INTEGER, col INTEGER, kind INTEGER, ref_file_id INTEGER, ref_line INTEGER, ref_col INTEGER);", NULL, NULL, &err);
    // decl
    sqlite3_exec(db, "CREATE TABLE decl(usr TEXT, name TEXT, file_id INTEGER, line INTEGER, col INTEGER, kind INTEGER, val INTEGER, is_virtual INTEGER, is_def INTEGER);", NULL, NULL, &err);
    // overriden
    sqlite3_exec(db, "CREATE TABLE overriden(usr TEXT, name TEXT, file_id INTEGER, line INTEGER, col INTEGER, kind INTEGER, usr_overrider TEXT, is_def INTEGER);", NULL, NULL, &err);

    std::ostringstream os;
    os << "INSERT INTO db_info VALUES(" << DB_VER << ", '" << src_file_name << "');";
    sqlite3_exec(db, os.str().c_str(), NULL, NULL, &err);

    // instantiate
    refMgr = new(CDBMgrRef);
    declMgr = new(CDBMgrDecl);
    overridenMgr = new(CDBMgrOverriden);

    // prepare queries
    refMgr->initDb(db);
    declMgr->initDb(db);
    overridenMgr->initDb(db);
}

static void try_step(sqlite3_stmt *stmt)
{
    for(int i = 0; SQLITE_DONE != sqlite3_step(stmt); i++) {
        if(i > STEP_MAX_TRY_NUM) {
            printf("ERROR: SQLITE3: step\n");
            exit(1);
        }
    }
}

void insert_ref_value(const char* usr, const char* name, int fid, int32_t line, int32_t col, int kind, int refFid, int ref_line, int ref_col)
{
    refMgr->insertValue(usr, name, fid, line, col, kind, refFid, ref_line, ref_col);
    return ;
}

void insert_decl_value(const char* usr, const char* name, int fid, int32_t line, int32_t col, int entity_kind, int val, int is_virtual, int is_def)
{
    declMgr->insertValue(usr, name, fid, line, col, entity_kind, val, is_virtual, is_def);
}

void insert_overriden_value(const char* usr, const char* name, int fid, int32_t line, int32_t col, int entity_kind, const char* usr_overrider, int is_def)
{
    overridenMgr->insertValue(usr, name, fid, line, col, entity_kind, usr_overrider, is_def);
    return ;
}

static void addFileList(const std::map<std::string, int >& fileMap)
{
    const char *err=NULL;
    sqlite3_stmt* stmt;
    std::ostringstream os;
    if(SQLITE_OK != sqlite3_prepare_v2(db, "INSERT INTO file_list VALUES(?, ?);", -1, &stmt, &err)) {
        fprintf(stderr, "ERROR: prepare: %s\n", sqlite3_errmsg(db));
        exit(1);
    }

    // lookup map
    std::map<std::string, int >::const_iterator end = fileMap.end();
    for(std::map<std::string, int >::const_iterator itr = fileMap.begin();
            itr != end;
            itr++) {
        sqlite3_reset(stmt);
        sqlite3_bind_int(stmt, 1, itr->second);
        sqlite3_bind_text(stmt, 2, itr->first.c_str(), -1, SQLITE_STATIC);
        try_step(stmt);
    }
    sqlite3_finalize(stmt);
    return ;
}

void fin(const std::map<std::string, int >& fileMap)
{
    addFileList(fileMap);

    refMgr->finDb(db);
    declMgr->finDb(db);
    overridenMgr->finDb(db);
    delete refMgr;
    delete declMgr;
    delete overridenMgr;

    // create indices
    sqlite3_exec(db, "CREATE INDEX file_list_index0 ON file_list(id);", NULL, NULL, NULL);
    sqlite3_exec(db, "CREATE INDEX file_list_index1 ON file_list(name);", NULL, NULL, NULL);
    sqlite3_exec(db, "CREATE INDEX ref_index0 ON ref(file_id, name, line, col);", NULL, NULL, NULL);
    sqlite3_exec(db, "CREATE INDEX ref_index1 ON ref(file_id);", NULL, NULL, NULL);
    sqlite3_exec(db, "CREATE INDEX ref_index2 ON ref(usr);", NULL, NULL, NULL);
    sqlite3_exec(db, "CREATE INDEX decl_index0 ON decl(file_id, name, line, col);", NULL, NULL, NULL);
    sqlite3_exec(db, "CREATE INDEX decl_index1 ON decl(file_id)", NULL, NULL, NULL);
    sqlite3_exec(db, "CREATE INDEX decl_index2 ON decl(usr)", NULL, NULL, NULL);
    // end transaction
    sqlite3_exec(db, "END TRANSACTION;", NULL, NULL, NULL);
    if(SQLITE_OK != sqlite3_close(db)) {
        fprintf(stderr, "ERROR: %s\n", sqlite3_errmsg(db));
        exit(1);
    }
}

// CDBMgrBase
void CDBMgrBase::initDb(sqlite3* db)
{
    const char* err = NULL;
    if(SQLITE_OK != sqlite3_prepare_v2(db, mQueryInsertTmpl, -1, &mSqlStmt, &err)) {
        fprintf(stderr, "ERROR: initDb(): prepare: %s\n", sqlite3_errmsg(db));
        exit(1);
    }
}

void CDBMgrBase::finDb(sqlite3* db)
{
    sqlite3_finalize(mSqlStmt);
}

// CDBMgrRef
void CDBMgrRef::insertValue(const char* usr, const char* name, int fid, int32_t line, int32_t col, int kind, int refFid, int ref_line, int ref_col)
{
    sqlite3_reset(mSqlStmt);
    sqlite3_bind_text(mSqlStmt, 1, usr, -1, SQLITE_STATIC);
    sqlite3_bind_text(mSqlStmt, 2, name, -1, SQLITE_STATIC);
    sqlite3_bind_int(mSqlStmt, 3, fid);
    sqlite3_bind_int(mSqlStmt, 4, line);
    sqlite3_bind_int(mSqlStmt, 5, col);
    sqlite3_bind_int(mSqlStmt, 6, kind);
    sqlite3_bind_int(mSqlStmt, 7, refFid);
    sqlite3_bind_int(mSqlStmt, 8, ref_line);
    sqlite3_bind_int(mSqlStmt, 9, ref_col);
    try_step(mSqlStmt);
}

// CDBMgrDecl
void CDBMgrDecl::insertValue(const char* usr, const char* name, int fid, int32_t line, int32_t col, int entity_kind, int val, int is_virtual, int is_def)
{
    sqlite3_reset(mSqlStmt);
    sqlite3_bind_text(mSqlStmt, 1, usr, -1, SQLITE_STATIC);
    sqlite3_bind_text(mSqlStmt, 2, name, -1, SQLITE_STATIC);
    sqlite3_bind_int(mSqlStmt, 3, fid);
    sqlite3_bind_int(mSqlStmt, 4, line);
    sqlite3_bind_int(mSqlStmt, 5, col);
    sqlite3_bind_int(mSqlStmt, 6, entity_kind);
    sqlite3_bind_int(mSqlStmt, 7, val);
    sqlite3_bind_int(mSqlStmt, 8, is_virtual);
    sqlite3_bind_int(mSqlStmt, 9, is_def);
    try_step(mSqlStmt);
}

// CDBMgrOverriden
void CDBMgrOverriden::insertValue(const char* usr, const char* name, int fid, int32_t line, int32_t col, int entity_kind, const char* usr_overrider, int is_def)
{
    sqlite3_reset(mSqlStmt);
    sqlite3_bind_text(mSqlStmt, 1, usr, -1, SQLITE_STATIC);
    sqlite3_bind_text(mSqlStmt, 2, name, -1, SQLITE_STATIC);
    sqlite3_bind_int(mSqlStmt, 3, fid);
    sqlite3_bind_int(mSqlStmt, 4, line);
    sqlite3_bind_int(mSqlStmt, 5, col);
    sqlite3_bind_int(mSqlStmt, 6, entity_kind);
    sqlite3_bind_text(mSqlStmt, 7, usr_overrider, -1, SQLITE_STATIC);
    sqlite3_bind_int(mSqlStmt, 8, is_def);
    try_step(mSqlStmt);
}

};
