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
    virtual void init(const std::string& out_dir, const std::string& src_file_name, const std::string& excludeList, int isPartial, int isSkel, const char* curDir, int argc, const char** argv);
    virtual void fin(void);
    virtual void insert_ref_value(const std::string& usr, const std::string& filename, const std::string& name, int line, int col);
    virtual void insert_decl_value(const std::string& usr, const std::string& filename, const std::string& name, int line, int col, int isDef);
    virtual void insert_overriden_value(const std::string& usr, const std::string& name, int line, int col, const std::string& overriderUsr, int isDef);
    virtual void insert_base_class_value(const std::string& classUsr, const std::string& baseClassUsr, int line, int col, int accessibility);
    void addIdList(leveldb::WriteBatch* db, const std::map<std::string, int >& inMap, const std::string& tableName);
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
