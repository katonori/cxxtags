#ifndef _DB_H_
#define _DB_H_
#include <string>
#include <map>
#include <stdint.h>
#include <sstream>
#include <leveldb/db.h>
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
    virtual void fin(const std::map<std::string, int >& usrMap, const std::map<std::string, int >& nameMap);
    virtual void insert_ref_value(std::string usr, int usrId, std::string filename, int nameId, int line, int col, int kind, std::string refFilename, int refLine, int refCol);
    virtual void insert_decl_value(std::string usr, int usrId, std::string filename, int nameId, int line, int col, int entityKind, int val, int isVirtual, int isDef, int typeUsrId, int typeKind, int isPointer);
    virtual void insert_overriden_value(int usrId, int nameId, int line, int col, int entityKind, int overriderUsrId, int isDef);
    virtual void insert_base_class_value(int classUsrId, int baseClassUsrId, int line, int col, int accessibility);
    void addIdList(leveldb::WriteBatch* db, const std::map<std::string, int >& inMap, std::string tableName);
private:
};

// tables that keep allocated IDs.
class IdTbl
{
public:
    IdTbl()
    : mCurId(1)
    {
        mMap[""] = 0;
    }
    std::map<std::string, int > mMap;
    int mCurId;
    int GetId(std::string str)
    {
        // lookup map
        std::map<std::string, int >::iterator mapItr = mMap.find(str);
        if(mapItr != mMap.end()){ 
            return mapItr->second;
        }
        mMap[str] = mCurId;
        int rv = mCurId;
        mCurId++;
        return rv;
    }
    const std::map<std::string, int >& GetTbl(void) const
    {
        return mMap;
    }
};
};

#endif //#ifndef _DB_H_
