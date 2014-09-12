#include "DbImplLevelDb.h"
#include <leveldb/db.h>
#include <leveldb/write_batch.h>
#include <leveldb/cache.h>
#include <leveldb/filter_policy.h>
#include <vector>
#include <map>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <unistd.h>
#include <boost/filesystem/path.hpp>
#include <boost/filesystem/operations.hpp>
#include <boost/foreach.hpp>
#include <boost/algorithm/string.hpp>

#define TABLE_NAME_POS2USR_ID "A"
#define TABLE_NAME_REF_USR2GLOBAL_FILE_ID "B"
#define TABLE_NAME_ID2NAME "C"
#define TABLE_NAME_USR_ID2DECL "D"
#define TABLE_NAME_USR2DEF "E"
#define TABLE_NAME_ID2USR "F"
#define TABLE_NAME_GLOBAL_FILE_ID2FILE "G"
#define TABLE_NAME_CU_NAME2ID "H"
//#define TABLE_NAME_ID2CU "I"
//#define TABLE_NAME_FID2CUID "J"
#define TABLE_NAME_FILE2LOCAL_ID "K"
#define TABLE_NAME_USR2REF "L"
#define TABLE_NAME_USR2OVERRIDEE "M"
#define TABLE_NAME_USR2OVERRIDER "N"
#define TABLE_NAME_FILE_LIST "O"
#define TABLE_NAME_REF_USR2GLOBAL_FILE_ID2 "P"
#define TABLE_NAME_BUILD_INFO "Q"
#define TABLE_NAME_USR2ID "R"
#define TABLE_NAME_CUFILES "S"
#define TABLE_NAME_DEF_USR2GLOBAL_FILE_ID "T"
#define TABLE_NAME_DEF_USR2GLOBAL_FILE_ID2 "U"

#define USE_BASE64
//#define USE_USR2FILE_TABLE2
#define TIMER
#define DB_NUM 32

#ifdef TIMER
#include <boost/timer/timer.hpp>
#endif

namespace cxxtags {

using namespace std;

static string s_compileUnit;
static string s_commonDbDir;
static string s_dbDir;
static char gCharBuff0[2048];
static char gCharBuff1[2048];
leveldb::ReadOptions s_defaultRoptions;
leveldb::WriteOptions s_defaultWoptions;
leveldb::Options s_defaultOptions;
string s_curDbDir;

const int k_usrDbDirNum = 4;

static string s_compileUnitId;
static map<string, FileContext> s_fileContextMap;
static SiMap s_refUsrMap;
static SiMap s_defUsrMap;
static const int k_timerNum = 128;
#ifdef TIMER
boost::timer::cpu_timer* s_timers;
#endif
static SsMap s_finishedFiles;
static map<string, SiMap > s_usr2fileMap;
static string s_buildOpt;

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

static inline void timerStart(int idx)
{
#ifdef TIMER
    s_timers[idx].start();
#endif
}

static inline void timerResume(int idx)
{
#ifdef TIMER
    s_timers[idx].resume();
#endif
}

static inline void timerStop(int idx)
{
#ifdef TIMER
    s_timers[idx].stop();
#endif
}

static inline int dbWrite(leveldb::DB* db, const string& key, const string& value);
static inline int dbRead(string& value, leveldb::DB* db, const string& key);
static inline int dbClose(leveldb::DB*& db);
static inline int dbTryOpen(leveldb::DB*& db, string dir);

static int dbTryOpen(leveldb::DB*& db, string dir)
{
    time_t start;
    time(&start);
    leveldb::Status st;
    while(1) {
        timerStart(TIMER_USR_DB3);
        st= leveldb::DB::Open(s_defaultOptions, dir, &db);
        timerStop(TIMER_USR_DB3);
        if(st.ok() || !st.IsIOError()) {
            break;
        }
        time_t now;
        time(&now);
        if(now - start > 10) {
            // timeout
            break;
        }
        //printf("WAITING: %f ms\n", (now - start)*1000.0f/CLOCKS_PER_SEC);
        usleep(1000);
    }
    if (!st.ok()) {
        fprintf(stderr, "Open fail.: %s: %s\n", s_commonDbDir.c_str(), st.ToString().c_str());
        return -1;
    }
    return 0;
}

int DbImplLevelDb::init(const string& out_dir, const string& src_file_name, const string& excludeList, int isPartial, int isSkel, bool isRebuild, const char* curDir, int argc, const char** argv)
{
    leveldb::DB* dbCommon = NULL;
    s_defaultOptions.create_if_missing = true;
    //s_defaultOptions.compression = leveldb::kNoCompression;
    s_defaultOptions.compression = leveldb::kSnappyCompression;
    s_defaultOptions.block_cache = leveldb::NewLRUCache(128 * 1024 * 1024); 
    s_defaultOptions.filter_policy = leveldb::NewBloomFilterPolicy(10);

    // build options
    s_buildOpt = string(curDir) + "|" + excludeList + "|";
    for(int i = 0; i < argc; i++) {
        s_buildOpt += " " + string(argv[i]);
    }

    s_dbDir = out_dir;
    s_compileUnit = src_file_name;

#ifdef TIMER
    s_timers = new boost::timer::cpu_timer[k_timerNum];
    for(int i = 0; i < k_timerNum; i++) {
        s_timers[i].stop();
    }
#endif

    if(!boost::filesystem::exists(s_dbDir)) {
        boost::filesystem::create_directory(s_dbDir);
    }

    //
    // update file list
    //
    // TODO: add lock
    leveldb::Status status;
    s_commonDbDir = out_dir + "/common";
    if (dbTryOpen(dbCommon, s_commonDbDir) < 0) {
        fprintf(stderr, "Open fail.: %s\n", s_commonDbDir.c_str());
        return -1;
    }
    assert(dbCommon != NULL);
    string value;
    string keyFile = s_compileUnit;
    int rv = 0;
    // check if already registered
    rv = dbRead(value, dbCommon, TABLE_NAME_CU_NAME2ID "|" + s_compileUnit);
    if(rv < 0) {
        // not found
        // add file
        string keyFileCount = "compile_unit_count";
        rv = dbRead(value, dbCommon, keyFileCount);
        if(rv < 0) {
            // key not found 
            dbWrite(dbCommon, keyFileCount, "1");
            s_compileUnitId = "0";
        }
        else if(rv == 0) {
            char buf[1024];
            s_compileUnitId = value;
            char* errp = NULL;
            int id = strtol(s_compileUnitId.c_str(), &errp, 16);
            assert(*errp == '\0');
            snprintf(buf, sizeof(buf), "%x", id+1);
            dbWrite(dbCommon, keyFileCount, buf);
        }
        else {
            printf("ERROR: db info\n");
        }
        dbWrite(dbCommon, TABLE_NAME_CU_NAME2ID "|" + s_compileUnit, s_compileUnitId);
    }
    else if(rv == 0) {
        // alread exists
        s_compileUnitId = value;
    }
    dbClose(dbCommon);

    // open database for this compile unit
    assert(!s_compileUnitId.empty());

    // list of files already processed
    if(!isRebuild) {
        leveldb::WriteBatch wb_common;
        leveldb::DB* db_common;
        int rv = dbTryOpen(db_common, s_commonDbDir);
        if(rv < 0) {
            printf("ERROR: fin: common db open: %s\n", s_commonDbDir.c_str());
            return -1;
        }
        leveldb::Iterator* it = db_common->NewIterator(leveldb::ReadOptions());
        for (it->SeekToFirst(); it->Valid(); it->Next()) {
            //cout << it->key().ToString() << ": "  << it->value().ToString() << endl;
            const string& key = it->key().ToString();
            if(key.find(TABLE_NAME_FILE_LIST "|") == 0) {
                s_finishedFiles[key.substr(2)] = it->value().ToString();
                //cout << key.substr(2) << endl;
            }
        }
        dbClose(db_common);
    }
    return 0;
}

static inline int dbWrite(leveldb::DB* db, const string& key, const string& value)
{
    leveldb::Status st = db->Put(s_defaultWoptions, key, value);
    // TODO: add error handling
    if (!st.ok()) {
        fprintf(stderr, "Write fail.: %s\n", st.ToString().c_str());
        assert(0);
        //return -1;
    }
    return 0;
}

static inline int dbRead(string& value, leveldb::DB* db, const string& key)
{
    string result;
    leveldb::Status st = db->Get(s_defaultRoptions, key, &result);
    if(!st.ok()) {
        return -1;
    }
    value = result;
    return 0;
}

#ifdef USE_BASE64
static char encoding_table[] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                                'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                                'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                                'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
                                'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                                'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                                'w', 'x', 'y', 'z', '0', '1', '2', '3',
                                '4', '5', '6', '7', '8', '9', '+', '/'};

static inline char* encodeVal(char* buff, unsigned int val)
{
    do {
        *buff = encoding_table[val & 0x3f];
        val >>= 6;
        buff++;
    } while(val);
    return buff;
}

static inline char* encodePos(char *buff, unsigned int fileId, unsigned int line, unsigned col)
{
    char* p = buff;
    strncpy(p, TABLE_NAME_POS2USR_ID, 1);
    p++;
    *p++ = '|';
    p = encodeVal(p, fileId);
    *p++ = '|';
    p = encodeVal(p, line);
    *p++ = '|';
    p = encodeVal(p, col);
    *p++ = '\0';
    return p;
}

static inline char* encodeRef(char *buff, unsigned int nameId, unsigned int fileId, unsigned int line, unsigned col)
{
    char* p = (char*)buff;
    p = encodeVal(p, nameId);
    *p++ = '|';
    p = encodeVal(p, fileId);
    *p++ = '|';
    p = encodeVal(p, line);
    *p++ = '|';
    p = encodeVal(p, col);
    *p++ = '\0';
    return p;
}

static inline char* encodeDecl(char *buff, unsigned int nameId, unsigned int fileId, unsigned int line, unsigned col)
{
    return encodeRef(buff, nameId, fileId, line, col);
}
#endif

static inline void setKeyValuePos2Usr(char* buffKey, char* buffVal, int buffLen, unsigned int fileId, unsigned int line, unsigned int col, unsigned int usrId)
{
#ifdef USE_BASE64
    encodePos(buffKey, fileId, line, col);
    {
        char* p = (char*)buffVal;
        p = encodeVal(p, usrId);
        *p++ = '\0';
    }
#else
    snprintf(buffKey, buffLen, TABLE_NAME_POS2USR_ID "|%x|%x|%x", fileId,  line, col);
    snprintf(buffVal, buffLen, "%x", usrId);
#endif
}

static inline void setKeyValueUsr2Decl(char* buffKey, char* buffVal, int buffLen, unsigned int nameId, unsigned int fileId, unsigned int line, unsigned int col, unsigned int usrId)
{
#ifdef USE_BASE64
    {
        char* p = (char*)buffKey;
        strncpy(p, TABLE_NAME_USR_ID2DECL "|", 2);
        p+=2;
        p = encodeVal(p, usrId);
        *p++ = '\0';
    }
    encodeDecl(buffVal, nameId, fileId, line, col);
#else
    snprintf(buffKey, buffLen, TABLE_NAME_USR_ID2DECL "|%x", usrId); 
    snprintf(buffVal, buffLen, "%x|%x|%x|%x", nameId, fileId, line, col);
#endif
}

static inline void setKeyValueUsr2Def(char* buffKey, char* buffVal, int buffLen, unsigned int nameId, unsigned int fileId, unsigned int line, unsigned int col, const string& usr)
{
    char* p = (char*)buffKey;
    strncpy(p, TABLE_NAME_USR2DEF "|", 2);
    p+=2;
    strncpy(p, usr.c_str(), usr.size()+1);
#ifdef USE_BASE64
    encodeDecl(buffVal, nameId, fileId, line, col);
#else
    // usrId -> def info
    snprintf(buffVal, buffLen, "%x|%x|%x|%x", nameId, fileId, line, col);
#endif
}

static inline void encItemInfo(char* buff, int buffLen, unsigned int nameId, unsigned int fileId, unsigned int line, unsigned int col)
{
#ifdef USE_BASE64
    encodeRef(buff, nameId, fileId, line, col);
#else
    snprintf(buff, buffLen, "%x|%x|%x|%x", nameId, fileId, line, col);
#endif
}

int DbImplLevelDb::insert_ref_value(const string& usr, const string& filename, const string& name, int line, int col)
{
    FileContext& fctx = s_fileContextMap[filename];

    if(s_finishedFiles.find(filename) != s_finishedFiles.end()) {
        // already done
        return 0;
    }
    timerResume(TIMER_INS_REF);

    //s_timers[TIMER_INS_REF_1].resume();
    int fileId = fctx.m_fileIdTbl.GetId(filename);
    int nameId = fctx.m_nameIdTbl.GetId(name);
    s_refUsrMap[usr] = 1;
    int usrId = fctx.m_usrIdTbl.GetId(usr);
    encItemInfo(gCharBuff0, sizeof(gCharBuff0), nameId, fileId, line, col);
    {
        SsMap& mapRef = fctx.m_usr2refMap;
        SsMap::iterator itr = mapRef.find(usr);
        if(itr == mapRef.end()){ 
            mapRef[usr] = string(gCharBuff0);
        }
        else {
            itr->second.append(string(",") + gCharBuff0);
        }
    }

    if(!usr.empty()) {
        s_usr2fileMap[usr][filename] = 0;
    }
    //s_timers[TIMER_INS_REF_1].stop();

    // pos -> usr
    timerResume(TIMER_INS_REF_2);
    setKeyValuePos2Usr(gCharBuff0, gCharBuff1, sizeof(gCharBuff0), fileId, line, col, usrId);
    fctx.m_refList.push_back(SsPair(gCharBuff0, gCharBuff1));
    timerStop(TIMER_INS_REF_2);
    timerStop(TIMER_INS_REF);
    return 0;
}

int DbImplLevelDb::insert_decl_value(const string& usr, const string& filename, const string& name, int line, int col, int isDef)
{
    FileContext& fctx = s_fileContextMap[filename];

    //printf("DECL: %s, %s, %d, %d, %d\n", usr.c_str(), filename.c_str(), line, col, isDef);
    if(s_finishedFiles.find(filename) != s_finishedFiles.end()) {
        // already done
        return 0;
    }
    timerResume(TIMER_INS_DECL);
    int fileId = fctx.m_fileIdTbl.GetId(filename);
    int nameId = fctx.m_nameIdTbl.GetId(name);
    int usrId = fctx.m_usrIdTbl.GetId(usr);
    leveldb::WriteBatch& wb = fctx.m_wb;
    if(isDef) {
        s_defUsrMap[usr] = 1;
        // usrId -> def info
        setKeyValueUsr2Def(gCharBuff0, gCharBuff1, sizeof(gCharBuff0), nameId, fileId, line, col, usr);
        fctx.m_declList.push_back(SsPair(gCharBuff0, gCharBuff1));
    }
    else {
        // usrId -> decl info
        setKeyValueUsr2Decl(gCharBuff0, gCharBuff1, sizeof(gCharBuff0), nameId, fileId, line, col, usrId);
        fctx.m_declList.push_back(SsPair(gCharBuff0, gCharBuff1));
    }

    if(!usr.empty()) {
        s_usr2fileMap[usr][filename] = 0;
    }

    // pos -> usr
    setKeyValuePos2Usr(gCharBuff0, gCharBuff1, sizeof(gCharBuff0), fileId, line, col, usrId);
    fctx.m_declList.push_back(SsPair(gCharBuff0, gCharBuff1));
    timerStop(TIMER_INS_DECL);
    return 0;
}

int DbImplLevelDb::insert_overriden_value(const string& usr, const string& name, const string& filename, int line, int col, const string& usrOverrider, int isDef)
{
    timerResume(TIMER_INS_OVERRIDEN);
    //printf("overriden: %s, %s, %s\n", usr.c_str(), filename.c_str(), name.c_str());
    FileContext& fctx = s_fileContextMap[filename];

    int fileId = fctx.m_fileIdTbl.GetId(filename);
    int nameId = fctx.m_nameIdTbl.GetId(name);
    int usrId = fctx.m_usrIdTbl.GetId(usr);
    int usrIdOverrider = fctx.m_usrIdTbl.GetId(usrOverrider);
    // usrId -> decl info
    encItemInfo(gCharBuff1, sizeof(gCharBuff1), nameId, fileId, line, col);
    if(!fctx.m_overrideeMap[usr].empty()) {
        fctx.m_overrideeMap[usr].append(string(",") + string(gCharBuff1));
    }
    else {
        fctx.m_overrideeMap[usr] = string(gCharBuff1);
    }

#ifdef USE_BASE64
    {
        char* p = gCharBuff1;
        p = encodeVal(p, usrId);
        *p = '\0';
    }
#else
    snprintf(gCharBuff1, sizeof(gCharBuff1), "%x", usrId);
#endif
    fctx.m_overriderMap[usrOverrider][gCharBuff1] = 0;

    if(!usr.empty()) {
        s_usr2fileMap[usr][filename] = 0;
    }
    // pos -> usr
    setKeyValuePos2Usr(gCharBuff0, gCharBuff1, sizeof(gCharBuff0), fileId, line, col, usrIdOverrider);
    fctx.m_wb.Put(gCharBuff0, gCharBuff1);

    timerStop(TIMER_INS_OVERRIDEN);
    return 0;
}

int DbImplLevelDb::insert_base_class_value(const string& classUsr, const string& baseClassUsr, int line, int col, int accessibility)
{
    return 0;
}

int DbImplLevelDb::addIdList(leveldb::WriteBatch* db, const SiMap& inMap, const string& tableName)
{
    string prefix = tableName + "|";
    // lookup map
    BOOST_FOREACH(const SiPair& itr, inMap) {
#ifdef USE_BASE64
        char* p = gCharBuff0;
        strncpy(p, prefix.c_str(), prefix.size());
        p += prefix.size();
        p = encodeVal(p, itr.second);
        *p++ = '\0';
#else
        snprintf(gCharBuff0, sizeof(gCharBuff0), "%s|%x", tableName.c_str(), itr.second);
#endif
        snprintf(gCharBuff1, sizeof(gCharBuff1), "%s", itr.first.c_str());
        db->Put(gCharBuff0, gCharBuff1);
    }
    return 0;
}

int addFilesToFileList(leveldb::DB* db, leveldb::WriteBatch* wb)
{
    char buf[1024];
    int startId = 0;
    string valStr;
    string keyFileCount = "file_count";
    int rv = dbRead(valStr, db, keyFileCount);
    if(rv < 0) {
        // key not found 
        dbWrite(db, keyFileCount, "1");
        startId = 0;
    }
    else if(rv == 0) {
        char* errp = NULL;
        startId = strtol(valStr.c_str(), &errp, 16);
        assert(*errp == '\0');
    }
    else {
        printf("ERROR: db info\n");
    }

    int id = startId;
    typedef pair<string, FileContext> FcPair;
    BOOST_FOREACH(const FcPair& itr, s_fileContextMap) {
        string fn = itr.first;
        string key = TABLE_NAME_FILE_LIST "|" + fn;
        int rv = dbRead(valStr, db, key);
        if(rv < 0) {
            snprintf(buf, sizeof(buf), "%x", id);
            dbWrite(db, key, s_compileUnitId + "," + string(buf));
            s_fileContextMap[fn].m_dbId = buf;
            id++;
        }
        else {
            // get fid
            size_t pos = valStr.find(",");
            assert(pos != string::npos);
            string fid = valStr.substr(pos+1, valStr.size()-1);
            // set fid to map
            s_fileContextMap[fn].m_dbId = fid;
        }
    }
    snprintf(buf, sizeof(buf), "%x", id);
    dbWrite(db, keyFileCount, buf);
    return 0;
}

static inline int dbFlush(leveldb::DB* db, leveldb::WriteBatch* wb)
{
    leveldb::Status status = db->Write(s_defaultWoptions, wb);
    if (!status.ok()) {
        fprintf(stderr, "Write fail.: %s\n", status.ToString().c_str());
        return -1;
    }
    return 0;
}

static inline int dbClose(leveldb::DB*& db)
{
    delete db;
    db = NULL;
    return 0;
}

int DbImplLevelDb::fin(void)
{
    {
        leveldb::WriteBatch wb_common;
        leveldb::DB* db_common;
        int rv = dbTryOpen(db_common, s_commonDbDir);
        if(rv < 0) {
            printf("ERROR: fin: common db open: %s\n", s_commonDbDir.c_str());
            return -1;
        }
        addFilesToFileList(db_common, &wb_common);
        dbFlush(db_common, &wb_common);
        dbClose(db_common);
    }

    // update UsrDb
    {
        leveldb::DB* dbUsrDb = NULL;
        leveldb::WriteBatch wb_usrdb;
        string curDir = s_dbDir + "/usr_db";
        if(!boost::filesystem::exists(curDir)) {
            if(!boost::filesystem::create_directory(curDir)) {
                printf("ERROR: create directory: %s\n", curDir.c_str());
                return -1;
            }
        }

        map<string, SiMap> refUsrFidMap; // store the file IDs a USR found in
        BOOST_FOREACH(const SiPair& itr, s_refUsrMap) {
            const string& usr = itr.first;
            if(!usr.empty()) {
                SiMap& fidMap = refUsrFidMap[usr];
                BOOST_FOREACH(const SiPair& itr_file_list, s_usr2fileMap[usr]) {
                    fidMap[s_fileContextMap[itr_file_list.first].m_dbId] = 0;
                }
            }
        }

        map<string, SiMap> defUsrFidMap;
        BOOST_FOREACH(const SiPair& itr, s_defUsrMap) {
            const string& usr = itr.first;
            if(!usr.empty()) {
                SiMap& fidMap = defUsrFidMap[usr];
                BOOST_FOREACH(const SiPair& itr_file_list, s_usr2fileMap[usr]) {
                    fidMap[s_fileContextMap[itr_file_list.first].m_dbId] = 0;
                }
            }
        }

        char* errp = NULL;
        int cuId = strtol(s_compileUnitId.c_str(), &errp, 16);
        assert(*errp == '\0');
        snprintf(gCharBuff0, sizeof(gCharBuff0), "%x", (cuId % k_usrDbDirNum)); 
        curDir.append(string("/") + string(gCharBuff0));

        timerStart(TIMER_USR_DB0);
        //////
        // open db
        int rv = dbTryOpen(dbUsrDb, curDir);
        if(rv < 0) {
            printf("ERROR: fin: common db open: %s\n", curDir.c_str());
            return -1;
        }

        // lookup map
        int count = 0;
        BOOST_FOREACH(const SiPair& itr, s_refUsrMap) {
            const string& usr = itr.first;
            bool isGlobal = 0 == strncmp(usr.c_str(), "c:@", 3);
            bool isMacro = 0 == strncmp(usr.c_str(), "c:macro", 7);
#if 1
            if(usr != "") {
#else
            if(!usr.empty() && (isGlobal || isMacro)) {
#endif
                SiMap& file_list_map = refUsrFidMap[usr];
#ifdef USE_USR2FILE_TABLE2
                BOOST_FOREACH(const SiPair& itr_str, file_list_map) {
                    wb_usrdb.Put(TABLE_NAME_REF_USR2GLOBAL_FILE_ID2 "|" + usr + "|" + itr_str.first, "1");
                }
#else
                // check if already registered
                string value;
                int rv = dbRead(value, dbUsrDb, TABLE_NAME_REF_USR2GLOBAL_FILE_ID "|" + usr);
                if(rv == 0) {
                    const string delim = ",";
                    list<string> old_list;
                    boost::split(old_list, value, boost::is_any_of(delim));
                    BOOST_FOREACH(const string& s, old_list) {
                        file_list_map[s] = 0;
                    }
                }
                string file_list_string = "";
                BOOST_FOREACH(const SiPair& itr_str, file_list_map) {
                    file_list_string.append(itr_str.first+",");
                }
                file_list_string = file_list_string.substr(0, file_list_string.size()-1);
                wb_usrdb.Put(TABLE_NAME_REF_USR2GLOBAL_FILE_ID "|" + usr, file_list_string);
#endif

                count++;
            }
        }

        BOOST_FOREACH(const SiPair& itr, s_defUsrMap) {
            const string& usr = itr.first;
            bool isGlobal = 0 == strncmp(usr.c_str(), "c:@", 3);
            bool isMacro = 0 == strncmp(usr.c_str(), "c:macro", 7);
#if 1
            if(usr != "") {
#else
            if(!usr.empty() && (isGlobal || isMacro)) {
#endif
                SiMap& file_list_map = defUsrFidMap[usr];
#ifdef USE_USR2FILE_TABLE2
                BOOST_FOREACH(const SiPair& itr_str, file_list_map) {
                    wb_usrdb.Put(TABLE_NAME_DEF_USR2GLOBAL_FILE_ID2 "|" + usr + "|" + itr_str.first, "1");
                }
#else
                // check if already registered
                string value;
                int rv = dbRead(value, dbUsrDb, TABLE_NAME_DEF_USR2GLOBAL_FILE_ID "|" + usr);
                if(rv == 0) {
                    const string delim = ",";
                    list<string> old_list;
                    boost::split(old_list, value, boost::is_any_of(delim));
                    BOOST_FOREACH(const string& s, old_list) {
                        file_list_map[s] = 0;
                    }
                }
                string file_list_string = "";
                BOOST_FOREACH(const SiPair& itr_str, file_list_map) {
                    file_list_string.append(itr_str.first+",");
                }
                file_list_string = file_list_string.substr(0, file_list_string.size()-1);
                wb_usrdb.Put(TABLE_NAME_DEF_USR2GLOBAL_FILE_ID "|" + usr, file_list_string);
#endif

                count++;
            }
        }
        dbFlush(dbUsrDb, &wb_usrdb);
        dbClose(dbUsrDb);
        timerStop(TIMER_USR_DB0);
        // close db
        //////
#ifdef TIMER
        printf("time: TIMER_USR_DB0: %s", s_timers[TIMER_USR_DB0].format().c_str());
        printf("time: TIMER_USR_DB3: %s", s_timers[TIMER_USR_DB3].format().c_str());
        printf("time: TIMER_INS_REF: %s", s_timers[TIMER_INS_REF].format().c_str());
        //printf("time: TIMER_INS_REF_1: %s", s_timers[TIMER_INS_REF_1].format().c_str());
        printf("time: TIMER_INS_REF_2: %s", s_timers[TIMER_INS_REF_2].format().c_str());
        printf("time: TIMER_INS_DECL: %s", s_timers[TIMER_INS_DECL].format().c_str());
        printf("time: usr count: %d\n", count);
#endif
    }

#ifdef TIMER
    timerStart(TIMER_DB_WRITE);
#endif
    {
        string valFiles;
        typedef pair<string, FileContext> FcPair;
        BOOST_FOREACH(const FcPair& itr, s_fileContextMap) {
            const string& filename = itr.first;
            const string& dbId = itr.second.m_dbId;
            valFiles += "," + dbId;
        }
        BOOST_FOREACH(const FcPair& itr, s_fileContextMap) {
            const string& filename = itr.first;
            const string& dbId = itr.second.m_dbId;
            FileContext& fctx = s_fileContextMap[filename];

            leveldb::DB*& db = fctx.m_db;
            leveldb::WriteBatch& wb = fctx.m_wb;

            // decide db directory
            char* errp = NULL;
            int id = strtol(dbId.c_str(), &errp, 16);
            assert(*errp == '\0');
            snprintf(gCharBuff0, sizeof(gCharBuff0), "%x", id%DB_NUM);
            string dbDir = string(gCharBuff0);

            // check if already exists
            //if(boost::filesystem::exists(s_dbDir + "/" + dbDir)) {
            if(s_finishedFiles.find(filename) != s_finishedFiles.end()) {
                continue;
            }
            int rv = dbTryOpen(db, s_dbDir + "/" + dbDir);
            if(rv < 0) {
                printf("ERROR: fin: open: %s\n", s_commonDbDir.c_str());
                return -1;
            }

            // ref
            BOOST_FOREACH(const SsPair& itr, fctx.m_refList) {
                wb.Put(dbId + itr.first, itr.second);
            }
            // decl
            BOOST_FOREACH(const SsPair& itr, fctx.m_declList) {
                wb.Put(dbId + itr.first, itr.second);
            }
            // override
            {
                BOOST_FOREACH(const SsPair& itr, fctx.m_overrideeMap) {
                    wb.Put(dbId + TABLE_NAME_USR2OVERRIDEE "|" + itr.first, itr.second);
                }
                typedef pair<string, SiMap> PairType;
                BOOST_FOREACH(const PairType& itr, fctx.m_overriderMap) {
                    const SiMap& usrMap = itr.second;
                    string val = "";
                    BOOST_FOREACH(const SiPair& itr_usr, usrMap) {
                        if(val.empty()) {
                            val = itr_usr.first;
                        }
                        else {
                            val.append(string(",") + itr_usr.first);
                        }
                    }
                    wb.Put(dbId + TABLE_NAME_USR2OVERRIDER "|" + itr.first, val);
                }
            }

            // usr
            const SiMap& mapRef = fctx.m_usrIdTbl.GetTbl();
            addIdList(&wb, mapRef, dbId + TABLE_NAME_ID2USR);
            {
                BOOST_FOREACH(const SiPair& itr, mapRef) {
                    string key(dbId + TABLE_NAME_USR2ID "|");
                    key.append(itr.first);
#ifdef USE_BASE64
                    {
                        char* p = gCharBuff1;
                        p = encodeVal(p, itr.second);
                        *p = '\0';
                    }
#else
                    snprintf(gCharBuff1, sizeof(gCharBuff1), "%x", itr.second);
#endif
                    wb.Put(key, gCharBuff1);
                }
            }
            BOOST_FOREACH(const SsPair& itr, fctx.m_usr2refMap) {
                const string& usr = itr.first;
                if(!usr.empty()) {
                    string key(dbId + TABLE_NAME_USR2REF "|");
                    //key.append(usr + "|" + s_compileUnitId);
                    key.append(usr);
                    wb.Put(key, itr.second);
                }
            }
            const SiMap& fileMap = fctx.m_fileIdTbl.GetTbl();
            addIdList(&wb, fileMap, dbId + TABLE_NAME_GLOBAL_FILE_ID2FILE);
            // lookup map
            BOOST_FOREACH(const SiPair& itr, fileMap) {
                string key(dbId + TABLE_NAME_FILE2LOCAL_ID "|");
                key.append(itr.first);
#ifdef USE_BASE64
                {
                    char* p = gCharBuff1;
                    p = encodeVal(p, itr.second);
                    *p = '\0';
                }
#else
                snprintf(gCharBuff1, sizeof(gCharBuff1), "%x", itr.second);
#endif
                wb.Put(key, gCharBuff1);
            }
            const SiMap& nameMap = fctx.m_nameIdTbl.GetTbl();
            addIdList(&wb, nameMap, dbId + TABLE_NAME_ID2NAME);

            wb.Put(dbId + TABLE_NAME_CUFILES, valFiles);
            wb.Put(dbId + TABLE_NAME_BUILD_INFO, s_buildOpt);

            dbFlush(db, &wb);
            dbClose(db);
        }
    }
#ifdef TIMER
    timerStop(TIMER_DB_WRITE);
    printf("time: TIMER_DB_WRITE: %s", s_timers[TIMER_DB_WRITE].format().c_str());
#endif

    delete s_defaultOptions.block_cache;
    return 0;
}

};
