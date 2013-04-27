#ifndef _DB_H_
#include <string>
#include <map>
#include <stdint.h>
#include <sstream>
#include <sqlite3.h>

namespace db {
static const int DB_VER = 5;
static const int STEP_MAX_TRY_NUM = 1024;

void init(std::string db_file_name, std::string src_file_name);
void fin(const std::map<std::string, int >& fileMap);
void insert_ref_value(const char* usr, const char* name, int fid, int32_t line, int32_t col, int kind, int refFid, int ref_line, int ref_col);
void insert_decl_value(const char* usr, const char* name, int fid, int32_t line, int32_t col, int entity_kind, int val, int is_virtual, int is_def);
void insert_overriden_value(const char* usr, const char* name, int fid, int32_t line, int32_t col, int entity_kind, const char* usr_overrider, int is_def);

class CDBMgrBase {
public:
    CDBMgrBase(const char* name, const char* query)
        : mSqlStmt(NULL), mTblName(name), mQueryInsertTmpl(query)
    {}
    void initDb(sqlite3* db);
    void finDb(sqlite3* db);
protected:
    sqlite3_stmt* mSqlStmt;
private:
    const char* mTblName;
    const char* mQueryInsertTmpl;
};

class CDBMgrRef
    : public CDBMgrBase {
public:
    CDBMgrRef()
        : CDBMgrBase("ref", "INSERT INTO ref VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);")
    {}
    void insertValue(const char* usr, const char* name, int fid, int32_t line, int32_t col, int kind, int refFid, int ref_line, int ref_col);
};

class CDBMgrDecl
    : public CDBMgrBase {
public:
    CDBMgrDecl(void)
        : CDBMgrBase("decl", "INSERT INTO decl VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);")
    {}
    void insertValue(const char* usr, const char* name, int fid, int32_t line, int32_t col, int entity_kind, int val, int is_virtual, int is_def);
};

class CDBMgrOverriden
    : public CDBMgrBase {
public:
    CDBMgrOverriden()
        : CDBMgrBase("overriden", "INSERT INTO overriden VALUES (?, ?, ?, ?, ?, ?, ?, ? );")
    {}
    void insertValue(const char* usr, const char* name, int fid, int32_t line, int32_t col, int entity_kind, const char* usr_overrider, int is_def);
};

};

#endif //#ifndef _DB_H_
