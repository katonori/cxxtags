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

    enum {
        TIMER_INS_REF = 64,
        TIMER_INS_REF_1,
        TIMER_INS_REF_2,
        TIMER_INS_DECL,
        TIMER_INS_OVERRIDEN,
        TIMER_USR_DB0,
        TIMER_USR_DB1,
        TIMER_USR_DB2,
        TIMER_USR_DB3,
        TIMER_DB_CACHE,
        TIMER_DB_WRITE,
    };

private:
    int addFilesToFileList(leveldb::DB* db);
    int dbTryOpen(leveldb::DB*& db, std::string dir);
    inline int dbWrite(leveldb::DB* db, const std::string& key, const std::string& value);
    inline int dbRead(std::string& value, leveldb::DB* db, const std::string& key);
    inline int dbFlush(leveldb::DB* db, leveldb::WriteBatch* wb);
    inline int dbClose(leveldb::DB*& db);
    void deleteOldEntries(leveldb::DB* db, const std::string& dbId);
    int writeUsrDb(const SiMap& usrMap, std::map<std::string, SiMap> usrFidMap, leveldb::DB* dbUsrDb, leveldb::WriteBatch& wb_usrdb, const std::string& dbName);

    static inline void timerStart(int idx)
    {
#ifdef TIMER
        m_timers[idx].start();
#endif
    }

    static inline void timerResume(int idx)
    {
#ifdef TIMER
        m_timers[idx].resume();
#endif
    }

    static inline void timerStop(int idx)
    {
#ifdef TIMER
        m_timers[idx].stop();
#endif
    }

    bool        m_isRebuild;
    std::string m_cuDbId;

    std::string m_compileUnit;
    std::string m_commonDbDir;
    std::string m_dbDir;
    char m_CharBuff0[8192];
    char m_CharBuff1[8192];
    leveldb::ReadOptions m_defaultRoptions;
    leveldb::WriteOptions m_defaultWoptions;
    leveldb::Options m_defaultOptions;

    const int k_usrDbDirNum = 1;

    std::string m_compileUnitId;
    FcMap m_fileContextMap;
    SiMap m_refUsrMap;
    SiMap m_defUsrMap;
    const int k_timerNum = 128;
#ifdef TIMER
    boost::timer::cpu_timer* m_timers;
#endif
    SsMap m_finishedFiles;
    std::map<std::string, SiMap > m_usr2fileMap;
    std::string m_buildOpt;
    int m_usrCount = 0;
};


};

#endif //#ifndef _DB_H_
