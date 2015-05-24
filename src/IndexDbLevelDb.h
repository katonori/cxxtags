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
#ifdef TIMER
#include <boost/timer/timer.hpp>
#endif

namespace cxxtags {

typedef std::map<std::string, std::string>      SsMap;
typedef std::pair<std::string, std::string>     SsPair;
typedef std::map<std::string, int>              SiMap;
typedef std::map<int, std::string>              IsMap;
typedef std::map<int, int>                      IiMap;
typedef std::pair<std::string, int>             SiPair;

// tables that keep allocated IDs.
class IdTbl
{
public:
    IdTbl()
    : mCurId(1)
    {
        mMap[""] = 0;
    }
    SiMap mMap;
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
    const SiMap& GetTbl(void) const
    {
        return mMap;
    }
};

struct Position {
    Position()
    {};
    Position(int line, int column)
        : line(line)
        , column(column)
    {};
    bool operator<(const Position& r) const {
        if(line == r.line) {
            return column < r.column;
        }
        return line < r.line;
    }
    int line;
    int column;
};

struct Token {
    Token()
    {};
    Token(std::string name, int usrId)
        : name(name)
        , usrId(usrId)
    {};
    bool operator<(const Token& r) const {
        return usrId < r.usrId;
    }
    std::string name;
    int usrId;
};

struct FileContext
{
    IdTbl                                       m_nameIdTbl;
    IdTbl                                       m_usrIdTbl;
    std::map<Position, std::map<Token, int>>    m_positition2usrList;
    std::list<SsPair>                           m_declList;
    IsMap                                       m_usrId2overrideeMap;
    std::map<int, IiMap>                        m_usrId2overriderMap;
    IsMap                                       m_usrId2refMap;
    std::string                                 m_dbId;
};
typedef std::map<std::string, FileContext>      FcMap;
typedef std::pair<std::string, FileContext>     FcPair;

class IndexDbLevelDb : public IIndexDb {
public:
    IndexDbLevelDb()
        : m_isRebuild(false)
        , m_cuDbId()
    {}
    // IIndexDb
    int initialize(const std::string& out_dir, const std::string& src_file_name, const std::string& excludeList, bool isRebuild, const char* curDir, int argc, const char** argv) override;
    int finalize(void) override;
    int insert_ref_value(const std::string& usr, const std::string& filename, const std::string& name, int line, int col) override;
    int insert_decl_value(const std::string& usr, const std::string& filename, const std::string& name, int line, int col, int isDef) override;
    int insert_overriden_value(const std::string& usr, const std::string& name, const std::string& filename, int line, int col, const std::string& overriderUsr, int isDef) override;
    int insert_base_class_value(const std::string& classUsr, const std::string& baseClassUsr, int line, int col, int accessibility) override;

    int addIdList(leveldb::WriteBatch* db, const SiMap& inMap, const std::string& tableName);

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
        TIMER_DB_SLEEP,
    };

private:
    int addFilesToFileList(leveldb::DB* db);
    int dbTryOpen(leveldb::DB*& db, const std::string& dir);
    inline int dbWrite(leveldb::DB* db, const std::string& key, const std::string& value);
    inline int dbRead(std::string& value, leveldb::DB* db, const std::string& key);
    inline int dbFlush(leveldb::DB* db, leveldb::WriteBatch* wb);
    inline int dbClose(leveldb::DB*& db);
    int writeUsrDb(const std::map<std::string, SiMap>& usrFidMap, leveldb::DB* dbUsrDb, leveldb::WriteBatch& wb_usrdb, const std::string& dbName);

    inline void timerStart(int idx)
    {
#ifdef TIMER
        m_timers[idx].start();
#endif
    }

    inline void timerResume(int idx)
    {
#ifdef TIMER
        m_timers[idx].resume();
#endif
    }

    inline void timerStop(int idx)
    {
#ifdef TIMER
        m_timers[idx].stop();
#endif
    }

    inline void timerShow(const char* str, int idx)
    {
#ifdef TIMER
        std::cout << str << m_timers[idx].format();
#endif
    }

    bool                            m_isRebuild;
    std::string                     m_cuDbId;
    std::string                     m_compileUnit;
    std::string                     m_commonDbDir;
    std::string                     m_dbDir;
    char                            m_CharBuff0[8192];
    char                            m_CharBuff1[8192];
    leveldb::ReadOptions            m_defaultRoptions;
    leveldb::WriteOptions           m_defaultWoptions;
    leveldb::Options                m_defaultOptions;

    std::string                     m_compileUnitId;
    FcMap                           m_fileContextMap;
#ifdef TIMER
    const int                       k_timerNum = 128;
    boost::timer::cpu_timer*        m_timers;
#endif
    SsMap                           m_finishedFiles;
    std::map<std::string, std::vector<std::string>>   m_usr2defineFileMap;
    std::map<std::string, std::vector<std::string>>   m_usr2referenceFileMap;
    std::map<std::string, std::vector<std::string>>   m_usr2overriderFileMap;
    std::string                     m_buildOpt;
};


};

#endif //#ifndef _DB_H_
