#ifndef _DB_H_
#define _DB_H_
#include <string>
#include <map>
#include <stdint.h>
#include <sstream>
#include <sqlite3.h>
#include "IIndexDb.h"

namespace cxxtags {
class DbImplLevelDb : public IIndexDb {
public:
#if 0
    DbImplLevelDb() :
        mDb(NULL)
    {}
#endif
    virtual void init(std::string out_dir, std::string src_file_name, std::string excludeList, int isPartial, int isSkel, const char* curDir, int argc, const char** argv);
    virtual void fin(const std::map<std::string, int >& fileMap, const std::map<std::string, int >& usrMap, const std::map<std::string, int >& nameMap);
    virtual void insert_ref_value(std::string usr, std::string filename, std::string name, int line, int col, int kind, int refFid, int refLine, int refCol);
    virtual void insert_decl_value(std::string usr, std::string filename, std::string name, int line, int col, int entityKind, int val, int isVirtual, int isDef, int typeUsrId, int typeKind, int isPointer);
    virtual void insert_overriden_value(int usrId, int nameId, int fileId, int line, int col, int entityKind, int overriderUsrId, int isDef);
    virtual void insert_base_class_value(int classUsrId, int baseClassUsrId, int line, int col, int accessibility);
    void addIdList(const std::map<std::string, int >& inMap, std::string tableName);
private:
private:
};
};

#endif //#ifndef _DB_H_
