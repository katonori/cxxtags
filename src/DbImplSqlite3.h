#ifndef _DB_H_
#define _DB_H_
#include <string>
#include <map>
#include <stdint.h>
#include <sstream>
#include <sqlite3.h>
#include "IIndexDb.h"

namespace cxxtags {
class DbImplSqlite3 : public IIndexDb {
public:
    DbImplSqlite3() :
        mDb(NULL)
    {}
    virtual void init(std::string db_file_name, std::string src_file_name, std::string excludeList, int isPartial, int isSkel, const char* curDir, int argc, const char** argv);
    virtual void fin(const std::map<std::string, int >& fileMap, const std::map<std::string, int >& usrMap, const std::map<std::string, int >& nameMap);
    virtual void insert_ref_value(int usrId, int nameId, int fileId, int line, int col, int kind, int refFid, int refLine, int refCol);
    virtual void insert_decl_value(int usrId, int nameId, int fileId, int line, int col, int entityKind, int val, int isVirtual, int isDef, int typeUsrId, int typeKind, int isPointer);
    virtual void insert_overriden_value(int usrId, int nameId, int fileId, int line, int col, int entityKind, int overriderUsrId, int isDef);
    virtual void insert_base_class_value(int classUsrId, int baseClassUsrId, int line, int col, int accessibility);
private:
    void addIdList(const std::map<std::string, int >& inMap, std::string tableName);
    void prepareStatement(const char* queryInsertTmpl, sqlite3_stmt **sqlStmt);
    void tryStep(sqlite3_stmt *stmt);
    void finDb(sqlite3_stmt *sqlStmt);
private:
    static const int STEP_MAX_TRY_NUM = 1024;
    static const int DB_VER = 7;
    enum {
        CONTAINED_PART_FULL = 0,
        CONTAINED_PART_PARTIAL = 1,
    };
    sqlite3* mDb;
    sqlite3_stmt* mSqlStmtDecl;
    sqlite3_stmt* mSqlStmtRef;
    sqlite3_stmt* mSqlStmtOverriden;
    sqlite3_stmt* mSqlStmtBaseClass;
};
};

#endif //#ifndef _DB_H_
