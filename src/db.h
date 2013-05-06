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
void fin(const std::map<std::string, int >& fileMap, const std::map<std::string, int >& usrMap, const std::map<std::string, int >& nameMap);
void insert_ref_value(int usrId, int nameId, int fileId, int line, int col, int kind, int refFid, int refLine, int refCol);
void insert_decl_value(int usrId, int nameId, int fileId, int line, int col, int entityKind, int val, int isVirtual, int isDef);
void insert_overriden_value(int usrId, int nameId, int fileId, int line, int col, int entityKind, int overriderUsrId, int isDef);

class DBMgrBase {
public:
    DBMgrBase(const char* query)
        : mSqlStmt(NULL), mQueryInsertTmpl(query)
    {}
    void InitDb(sqlite3* db);
    void FinDb(sqlite3* db);
protected:
    sqlite3_stmt* mSqlStmt;
private:
    const char* mQueryInsertTmpl;
};

class DBMgrRef
    : public DBMgrBase {
public:
    DBMgrRef()
        : DBMgrBase("INSERT INTO ref VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);")
    {}
    void InsertValue(int usrId, int nameId, int fileId, int line, int col, int kind, int refFid, int refLine, int refCol);
};

class DBMgrDecl
    : public DBMgrBase {
public:
    DBMgrDecl(void)
        : DBMgrBase("INSERT INTO decl VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);")
    {}
    void InsertValue(int usrId, int nameId, int fileId, int line, int col, int entityKind, int val, int is_virtual, int isDef);
};

class DBMgrOverriden
    : public DBMgrBase {
public:
    DBMgrOverriden()
        : DBMgrBase("INSERT INTO overriden VALUES (?, ?, ?, ?, ?, ?, ?, ? );")
    {}
    void InsertValue(int usrId, int nameId, int fileId, int line, int col, int entityKind, int overriderUsrId, int isDef);
};

};

#endif //#ifndef _DB_H_
