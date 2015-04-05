#ifndef _DB_H_
#define _DB_H_
#include <string>
#include <map>
#include <stdint.h>
#include <sstream>
#include <list>
#include <leveldb/db.h>
#include <leveldb/write_batch.h>
#include "IIndexDb.h"

namespace cxxtags {
class DbImplLevelDb : public IIndexDb {
public:
    DbImplLevelDb()
        : m_isRebuild(false)
        , m_cuDbId()
    {}
    // IIndexDb
    int init(const std::string& out_dir, const std::string& src_file_name, const std::string& excludeList, bool isRebuild, const char* curDir, int argc, const char** argv);
    int fin(void);
    int insert_ref_value(const std::string& usr, const std::string& filename, const std::string& name, int line, int col);
    int insert_decl_value(const std::string& usr, const std::string& filename, const std::string& name, int line, int col, int isDef);
    int insert_overriden_value(const std::string& usr, const std::string& name, const std::string& filename, int line, int col, const std::string& overriderUsr, int isDef);
    int insert_base_class_value(const std::string& classUsr, const std::string& baseClassUsr, int line, int col, int accessibility);

    int addIdList(leveldb::WriteBatch* db, const std::map<std::string, int >& inMap, const std::string& tableName);
private:
    int addFilesToFileList(leveldb::DB* db);

    bool        m_isRebuild;
    std::string m_cuDbId;

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
    int GetId(const std::string& str)
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

typedef std::map<std::string, std::string> SsMap;
typedef std::pair<std::string, std::string> SsPair;
typedef std::map<std::string, int> SiMap;
typedef std::pair<std::string, int> SiPair;
struct FileContext
{
    IdTbl m_fileIdTbl;
    IdTbl m_nameIdTbl;
    IdTbl m_usrIdTbl;
    std::list<SsPair> m_refList;
    std::list<SsPair> m_declList;
    SsMap m_overrideeMap;
    std::map<std::string, SiMap> m_overriderMap;
    SsMap m_usr2refMap;
    std::string m_dbId;
    leveldb::WriteBatch m_wb;
    leveldb::DB* m_db;
};
typedef std::map<std::string, FileContext> FcMap;
typedef std::pair<std::string, FileContext> FcPair;

};

#endif //#ifndef _DB_H_
