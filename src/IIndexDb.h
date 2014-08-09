#ifndef _IINDEX_DB_H_
#define _IINDEX_DB_H_
#include <string>
#include <map>
#include <stdint.h>
#include <sstream>
#include <sqlite3.h>

namespace cxxtags {
class IIndexDb {
public:
    virtual void init(std::string db_file_name, std::string src_file_name, std::string excludeList, int isPartial, int isSkel, const char* curDir, int argc, const char** argv) = 0;
    virtual void fin(const std::map<std::string, int >& fileMap, const std::map<std::string, int >& usrMap, const std::map<std::string, int >& nameMap) = 0;
    virtual void insert_ref_value(std::string usr, int usrId, std::string filename, int fileId, int nameId, int line, int col, int kind, int refFid, int refLine, int refCol) = 0;
    virtual void insert_decl_value(std::string usr, int usrId, std::string filename, int fileId, int nameId, int line, int col, int entityKind, int val, int isVirtual, int isDef, int typeUsrId, int typeKind, int isPointer) = 0;
    virtual void insert_overriden_value(int usrId, int nameId, int fileId, int line, int col, int entityKind, int overriderUsrId, int isDef) = 0;
    virtual void insert_base_class_value(int classUsrId, int baseClassUsrId, int line, int col, int accessibility) = 0;
};
};

#endif // _IINDEX_DB_H_
