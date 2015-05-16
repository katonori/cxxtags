#include <map>
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <time.h>
#include <unistd.h>

#include <boost/algorithm/string.hpp>

#include <leveldb/db.h>
#include <leveldb/write_batch.h>
#include <leveldb/cache.h>
#include <leveldb/filter_policy.h>

#include "IndexDbLevelDb.h"
#include "config.h"

namespace cxxtags {

using namespace std;

int IndexDbLevelDb::dbTryOpen(leveldb::DB*& db, string dir)
{
    time_t start;
    time(&start);
    leveldb::Status st;
    time_t now;
    while(1) {
        timerStart(TIMER_USR_DB3);
        st= leveldb::DB::Open(m_defaultOptions, dir, &db);
        timerStop(TIMER_USR_DB3);
        if(st.ok() || !st.IsIOError()) {
            break;
        }
        time(&now);
        if(now - start > 30) {
            // timeout
            break;
        }
        //printf("WAITING: %f ms\n", (now - start)*1000.0f/CLOCKS_PER_SEC);
        usleep(1000);
    }
    if (!st.ok()) {
        fprintf(stderr, "Open fail.: wait time %ld sec: %s\n", now - start, st.ToString().c_str());
        return -1;
    }
    return 0;
}

static int makeDirectory(const char* name)
{
    // make database directory
    struct stat statBuf;
    if(stat(name, &statBuf) == 0) {
        if((statBuf.st_mode & S_IFDIR) == 0) {
            fprintf(stderr, "ERROR: Could not make directory \"%s\". The file \"%s\" exists.\n", name, name);
            return -1;
        }
        else {
            // Use the directory already exists.
        }
    }
    else {
        // does not exists
        mkdir(name, 0775);
    }
    return 0;
}

int IndexDbLevelDb::initialize(const string& out_dir, const string& src_file_name, const string& excludeList, bool isRebuild, const char* curDir, int argc, const char** argv)
{
    leveldb::DB* dbCommon = NULL;
    m_defaultOptions.create_if_missing = true;
    //m_defaultOptions.compression = leveldb::kNoCompression;
    m_defaultOptions.compression = leveldb::kSnappyCompression;
    m_defaultOptions.block_cache = leveldb::NewLRUCache(128 * 1024 * 1024); 
    m_defaultOptions.filter_policy = leveldb::NewBloomFilterPolicy(10);

    // build options
    snprintf(m_CharBuff0, sizeof(m_CharBuff0), "%d", isRebuild);
    m_buildOpt = string(curDir) + "|" + excludeList + "|" + m_CharBuff0 + "|";
    for(int i = 0; i < argc; i++) {
        m_buildOpt += " " + string(argv[i]);
    }

    m_dbDir = out_dir;
    m_compileUnit = src_file_name;

#ifdef TIMER
    m_timers = new boost::timer::cpu_timer[k_timerNum];
    for(int i = 0; i < k_timerNum; i++) {
        m_timers[i].stop();
    }
#endif

    if(makeDirectory(m_dbDir.c_str())) {
        return -1; 
    }

    //
    // update file list
    //
    leveldb::Status status;
    m_commonDbDir = out_dir + "/common";
    if (dbTryOpen(dbCommon, m_commonDbDir) < 0) {
        fprintf(stderr, "Open fail.: %s\n", m_commonDbDir.c_str());
        return -1;
    }
    assert(dbCommon != NULL);
    string value;
    string keyFile = m_compileUnit;
    int rv = 0;
    // check if already registered
    rv = dbRead(value, dbCommon, TABLE_NAME_CU_NAME_TO_ID "|" + m_compileUnit);
    if(rv < 0) {
        // not found
        // add file
        string keyFileCount = "compile_unit_count";
        rv = dbRead(value, dbCommon, keyFileCount);
        if(rv < 0) {
            // key not found 
            dbWrite(dbCommon, keyFileCount, "1");
            m_compileUnitId = "0";
        }
        else if(rv == 0) {
            char buf[1024];
            m_compileUnitId = value;
            char* errp = NULL;
            int id = strtol(m_compileUnitId.c_str(), &errp, 16);
            assert(*errp == '\0');
            snprintf(buf, sizeof(buf), "%x", id+1);
            dbWrite(dbCommon, keyFileCount, buf);
        }
        else {
            printf("ERROR: db info\n");
        }
        dbWrite(dbCommon, TABLE_NAME_CU_NAME_TO_ID "|" + m_compileUnit, m_compileUnitId);
    }
    else if(rv == 0) {
        // alread exists
        m_compileUnitId = value;
    }
    dbClose(dbCommon);

    // open database for this compile unit
    assert(!m_compileUnitId.empty());

    // list of files already processed
    if(!isRebuild) {
        leveldb::WriteBatch wb_common;
        leveldb::DB* db_common;
        int rv = dbTryOpen(db_common, m_commonDbDir);
        if(rv < 0) {
            printf("ERROR: common db open: %s\n", m_commonDbDir.c_str());
            return -1;
        }
        leveldb::Iterator* it = db_common->NewIterator(leveldb::ReadOptions());
        for (it->SeekToFirst(); it->Valid(); it->Next()) {
            //cout << it->key().ToString() << ": "  << it->value().ToString() << endl;
            const string& key = it->key().ToString();
            if(key.find(TABLE_NAME_FILE_LIST "|") == 0) {
                m_finishedFiles[key.substr(2)] = it->value().ToString();
                //cout << key.substr(2) << endl;
            }
        }
        dbClose(db_common);
    }
    else {
        m_isRebuild = true;
    }
    return 0;
}

int IndexDbLevelDb::dbWrite(leveldb::DB* db, const string& key, const string& value)
{
    leveldb::Status st = db->Put(m_defaultWoptions, key, value);
    // TODO: add error handling
    if (!st.ok()) {
        fprintf(stderr, "Write fail.: %s\n", st.ToString().c_str());
        assert(0);
        //return -1;
    }
    return 0;
}

int IndexDbLevelDb::dbRead(string& value, leveldb::DB* db, const string& key)
{
    string result;
    leveldb::Status st = db->Get(m_defaultRoptions, key, &result);
    if(!st.ok()) {
        return -1;
    }
    value = result;
    return 0;
}

#if (USE_BASE64 != 0)
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

static inline char* encodePos(char *buff, const Position& pos)
{
    char* p = buff;
    strncpy(p, TABLE_NAME_POSITION_TO_LOCAL_USR_ID, 1);
    p++;
    *p++ = '|';
    p = encodeVal(p, pos.line);
    *p++ = '|';
    p = encodeVal(p, pos.column);
    *p++ = '\0';
    return p;
}

static inline char* encodeRef(char *buff, unsigned int nameId, unsigned int line, unsigned col)
{
    char* p = (char*)buff;
    p = encodeVal(p, nameId);
    *p++ = '|';
    p = encodeVal(p, line);
    *p++ = '|';
    p = encodeVal(p, col);
    *p++ = '\0';
    return p;
}

static inline char* encodeDecl(char *buff, unsigned int nameId, unsigned int line, unsigned col)
{
    return encodeRef(buff, nameId, line, col);
}
#endif

static inline void setKeyValuePos2Usr(char* buffKey, char* buffVal, int buffLen, const Position& pos, std::map<Token, int> tokenList)
{
#if (USE_BASE64 != 0)
    encodePos(buffKey, pos);
    {
        char* p = (char*)buffVal;
        for(const auto& itr : tokenList) {
            p = encodeVal(p, itr.first.usrId);
            *p++ = ',';
        }
        if(p != buffKey) {
            --p; // remvoe the last ','
        }
        *p = '\0';
    }
#else
    snprintf(buffKey, buffLen, TABLE_NAME_POSITION_TO_LOCAL_USR_ID "|%x|%x", line, col);
    snprintf(buffVal, buffLen, "%x", usrId);
#endif
}

static inline void setKeyValueUsr2Decl(char* buffKey, char* buffVal, int buffLen, unsigned int nameId, unsigned int line, unsigned int col, unsigned int usrId)
{
#if (USE_BASE64 != 0)
    {
        char* p = (char*)buffKey;
        strncpy(p, TABLE_NAME_LOCAL_USR_ID_TO_DECL "|", 2);
        p+=2;
        p = encodeVal(p, usrId);
        *p++ = '\0';
    }
    encodeDecl(buffVal, nameId, line, col);
#else
    snprintf(buffKey, buffLen, TABLE_NAME_LOCAL_USR_ID_TO_DECL "|%x", usrId); 
    snprintf(buffVal, buffLen, "%x|%x|%x", nameId, line, col);
#endif
}

static inline void setKeyValueUsr2Def(char* buffKey, char* buffVal, int buffLen, unsigned int nameId, unsigned int line, unsigned int col, int usrId)
{
#if (USE_BASE64 != 0)
    char* p = (char*)buffKey;
    strncpy(p, TABLE_NAME_LOCAL_USR_ID_TO_DEF "|", 2);
    p+=2;
    p = encodeVal(p, usrId);
    *p++ = '\0';
    encodeDecl(buffVal, nameId, line, col);
#else
    // usrId -> def info
    snprintf(buffKey, buffLen, TABLE_NAME_LOCAL_USR_ID_TO_DEF "|%x", usrId); 
    snprintf(buffVal, buffLen, "%x|%x|%x", nameId, line, col);
#endif
}

static inline void encItemInfo(char* buff, int buffLen, unsigned int nameId, unsigned int line, unsigned int col)
{
#if (USE_BASE64 != 0)
    encodeRef(buff, nameId, line, col);
#else
    snprintf(buff, buffLen, "%x|%x|%x", nameId, line, col);
#endif
}

int IndexDbLevelDb::insert_ref_value(const string& usr, const string& filename, const string& name, int line, int col)
{
    FileContext& fctx = m_fileContextMap[filename];

    //printf("REF: %s, %s, %s, %d, %d\n", usr.c_str(), filename.c_str(), name.c_str(), line, col);

    if(m_finishedFiles.find(filename) != m_finishedFiles.end()) {
        // already done
        return 0;
    }
    timerResume(TIMER_INS_REF);

#ifdef TIMER
    m_timers[TIMER_INS_REF_1].resume();
#endif
    int nameId = fctx.m_nameIdTbl.GetId(name);
    int usrId = fctx.m_usrIdTbl.GetId(usr);
    encItemInfo(m_CharBuff0, sizeof(m_CharBuff0), nameId, line, col);
    {
        IsMap& mapRef = fctx.m_usrId2refMap;
        auto itr = mapRef.find(usrId);
        if(itr == mapRef.end()){ 
            mapRef[usrId] = string(m_CharBuff0);
        }
        else {
            itr->second.append(string(",") + m_CharBuff0);
        }
    }

    if(!usr.empty()) {
        m_usr2referenceFileMap[usr].push_back(filename);
    }
#ifdef TIMER
    m_timers[TIMER_INS_REF_1].stop();
#endif

    // pos -> usr
    timerResume(TIMER_INS_REF_2);
    fctx.m_positition2usrList[Position(line, col)][Token(name, usrId)] = 1;
    timerStop(TIMER_INS_REF_2);
    timerStop(TIMER_INS_REF);
    return 0;
}

int IndexDbLevelDb::insert_decl_value(const string& usr, const string& filename, const string& name, int line, int col, int isDef)
{
    FileContext& fctx = m_fileContextMap[filename];

    //printf("DECL: %s, %s, %d, %d, %d\n", usr.c_str(), filename.c_str(), line, col, isDef);
    if(m_finishedFiles.find(filename) != m_finishedFiles.end()) {
        // already done
        return 0;
    }
    timerResume(TIMER_INS_DECL);
    int nameId = fctx.m_nameIdTbl.GetId(name);
    int usrId = fctx.m_usrIdTbl.GetId(usr);
    if(isDef) {
        // usrId -> def info
        setKeyValueUsr2Def(m_CharBuff0, m_CharBuff1, sizeof(m_CharBuff0), nameId, line, col, usrId);
        fctx.m_declList.push_back(SsPair(m_CharBuff0, m_CharBuff1));
        if(!usr.empty()) {
            m_usr2defineFileMap[usr].push_back(filename);
        }
    }
    else {
        // usrId -> decl info
        setKeyValueUsr2Decl(m_CharBuff0, m_CharBuff1, sizeof(m_CharBuff0), nameId, line, col, usrId);
        fctx.m_declList.push_back(SsPair(m_CharBuff0, m_CharBuff1));
    }

    // pos -> usr
    fctx.m_positition2usrList[Position(line, col)][Token(name, usrId)] = 1;
    timerStop(TIMER_INS_DECL);
    return 0;
}

int IndexDbLevelDb::insert_overriden_value(const string& usr, const string& name, const string& filename, int line, int col, const string& usrOverrider, int isDef)
{
    timerResume(TIMER_INS_OVERRIDEN);
    //printf("overriden: %s, %s, %s, line=%d, col=%d\n", usr.c_str(), filename.c_str(), name.c_str(), line, col);
    FileContext& fctx = m_fileContextMap[filename];

    int nameId = fctx.m_nameIdTbl.GetId(name);
    int usrId = fctx.m_usrIdTbl.GetId(usr);
    int usrIdOverrider = fctx.m_usrIdTbl.GetId(usrOverrider);
    // usrId -> decl info
    encItemInfo(m_CharBuff1, sizeof(m_CharBuff1), nameId, line, col);
    if(!fctx.m_usrId2overrideeMap[usrId].empty()) {
        fctx.m_usrId2overrideeMap[usrId].append(string(",") + string(m_CharBuff1));
    }
    else {
        fctx.m_usrId2overrideeMap[usrId] = string(m_CharBuff1);
    }

    fctx.m_usrId2overriderMap[usrIdOverrider][usrId] = 0;

    if(!usr.empty()) {
        m_usr2overriderFileMap[usr].push_back(filename);
    }
    // pos -> usr
    fctx.m_positition2usrList[Position(line, col)][Token(name, usrIdOverrider)] = 1;

    timerStop(TIMER_INS_OVERRIDEN);
    return 0;
}

int IndexDbLevelDb::insert_base_class_value(const string& classUsr, const string& baseClassUsr, int line, int col, int accessibility)
{
    return 0;
}

int IndexDbLevelDb::addIdList(leveldb::WriteBatch* db, const SiMap& inMap, const string& tableName)
{
    string prefix = tableName + "|";
    // lookup map
    for(const auto& itr : inMap) {
#if (USE_BASE64 != 0)
        char* p = m_CharBuff0;
        strncpy(p, prefix.c_str(), prefix.size());
        p += prefix.size();
        p = encodeVal(p, itr.second);
        *p++ = '\0';
#else
        snprintf(m_CharBuff0, sizeof(m_CharBuff0), "%s|%x", tableName.c_str(), itr.second);
#endif
        snprintf(m_CharBuff1, sizeof(m_CharBuff1), "%s", itr.first.c_str());
        db->Put(m_CharBuff0, m_CharBuff1);
    }
    return 0;
}

int IndexDbLevelDb::addFilesToFileList(leveldb::DB* db)
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
    for(const auto& itr : m_fileContextMap) {
        string fn = itr.first;
        string key = TABLE_NAME_FILE_LIST "|" + fn;
        int rv = dbRead(valStr, db, key);
        string fid;
        if(rv < 0) {
            snprintf(buf, sizeof(buf), "%x", id);
            fid = string(buf);
            dbWrite(db, key, m_compileUnitId + "," + fid);
            id++;
        }
        else {
            // get fid
            size_t pos = valStr.find(",");
            assert(pos != string::npos);
            fid = valStr.substr(pos+1, valStr.size()-1);
        }
        m_fileContextMap[fn].m_dbId = fid;

        if(fn == m_compileUnit) {
            m_cuDbId = fid;
        }
    }
    snprintf(buf, sizeof(buf), "%x", id);
    dbWrite(db, keyFileCount, buf);
    return 0;
}

int IndexDbLevelDb::dbFlush(leveldb::DB* db, leveldb::WriteBatch* wb)
{
    leveldb::Status status = db->Write(m_defaultWoptions, wb);
    if (!status.ok()) {
        fprintf(stderr, "Write fail.: %s\n", status.ToString().c_str());
        return -1;
    }
    return 0;
}

int IndexDbLevelDb::dbClose(leveldb::DB*& db)
{
    delete db;
    db = NULL;
    return 0;
}

int IndexDbLevelDb::writeUsrDb(const map<string, SiMap> usrFidMap, leveldb::DB* dbUsrDb, leveldb::WriteBatch& wb_usrdb, const string& dbName)
{
    // lookup map
    for(const auto& itr : usrFidMap) {
        const string& usr = itr.first;
        if(usr != "") {
            SiMap file_list_map = itr.second;
#ifdef USE_USR2FILE_TABLE2
            for(const auto& itr_str : file_list_map) {
                wb_usrdb.Put(dbName + "|" + usr + "|" + itr_str.first, "1");
            }
#else
            // check if already registered
            string value;
            int rv = dbRead(value, dbUsrDb, dbName + "|" + usr);
            if(rv == 0) {
                const string delim = ",";
                list<string> old_list;
                boost::split(old_list, value, boost::is_any_of(delim));
                for(const auto& itr_old : old_list) {
                    file_list_map[itr_old] = 0;
                }
            }
            string file_list_string = "";
            for(const auto& itr_str : file_list_map) {
                file_list_string.append(itr_str.first+",");
            }
            file_list_string = file_list_string.substr(0, file_list_string.size()-1);
            wb_usrdb.Put(dbName + "|" + usr, file_list_string);
#endif
        }
    }
    return 0;
}

int IndexDbLevelDb::finalize(void)
{
    {
        leveldb::WriteBatch wb_common;
        leveldb::DB* db_common;
        int rv = dbTryOpen(db_common, m_commonDbDir);
        if(rv < 0) {
            printf("ERROR: finalize: common db open: %s\n", m_commonDbDir.c_str());
            return -1;
        }
        addFilesToFileList(db_common);
        dbFlush(db_common, &wb_common);
        dbClose(db_common);
    }

    // update UsrDb
    {
        leveldb::DB* dbUsrDb = NULL;
        leveldb::WriteBatch wb_usrdb;
        string curDir = m_dbDir + "/usr_db";
        if(makeDirectory(curDir.c_str())) {
            return -1; 
        }

        map<string, SiMap> refUsrFidMap; // store the file IDs a USR found
        for(const auto& itr : m_usr2referenceFileMap) {
            const string& usr = itr.first;
            SiMap& fidMap = refUsrFidMap[usr];
            for(const auto& itr_file_list : itr.second) {
                fidMap[m_fileContextMap[itr_file_list].m_dbId] = 0;
            }
        }

        map<string, SiMap> defUsrFidMap;
        for(const auto& itr : m_usr2defineFileMap) {
            const string& usr = itr.first;
            SiMap& fidMap = defUsrFidMap[usr];
            for(const auto& itr_file_list : itr.second) {
                fidMap[m_fileContextMap[itr_file_list].m_dbId] = 0;
            }
        }

        map<string, SiMap> overriderUsrFidMap;
        for(const auto& itr : m_usr2overriderFileMap) {
            const string& usr = itr.first;
            SiMap& fidMap = overriderUsrFidMap[usr];
            for(const auto& itr_file_list : itr.second) {
                fidMap[m_fileContextMap[itr_file_list].m_dbId] = 0;
            }
        }

        char* errp = NULL;
        int cuId = strtol(m_compileUnitId.c_str(), &errp, 16);
        assert(*errp == '\0');
        snprintf(m_CharBuff0, sizeof(m_CharBuff0), "%x", (cuId % USR_DB_NUM)); 
        curDir.append(string("/") + string(m_CharBuff0));

        timerStart(TIMER_USR_DB0);
        //////
        // open db
        int rv = dbTryOpen(dbUsrDb, curDir);
        if(rv < 0) {
            printf("ERROR: finalize: common db open: %s\n", curDir.c_str());
            return -1;
        }

#ifdef USE_USR2FILE_TABLE2
        writeUsrDb(refUsrFidMap,             dbUsrDb, wb_usrdb, TABLE_NAME_USR_TO_GLOBAL_FILE_ID_REF);
        writeUsrDb(defUsrFidMap,             dbUsrDb, wb_usrdb, TABLE_NAME_USR_TO_GLOBAL_FILE_ID_DEF2);
        writeUsrDb(overriderUsrFidMap,       dbUsrDb, wb_usrdb, TABLE_NAME_USR_TO_GLOBAL_FILE_ID_OVERRIDER);
#else
        writeUsrDb(refUsrFidMap,             dbUsrDb, wb_usrdb, TABLE_NAME_USR_TO_GLOBAL_FILE_ID_REF);
        writeUsrDb(defUsrFidMap,             dbUsrDb, wb_usrdb, TABLE_NAME_USR_TO_GLOBAL_FILE_ID_DEF);
        writeUsrDb(overriderUsrFidMap,       dbUsrDb, wb_usrdb, TABLE_NAME_USR_TO_GLOBAL_FILE_ID_OVERRIDER);
#endif

        dbFlush(dbUsrDb, &wb_usrdb);
        dbClose(dbUsrDb);
        timerStop(TIMER_USR_DB0);
        // close db
        //////
#ifdef TIMER
        printf("---- Statistics ----\n");
        timerShow("time: TIMER_USR_DB0: ", TIMER_USR_DB0);
        timerShow("time: TIMER_USR_DB3: ", TIMER_USR_DB3);
        timerShow("time: TIMER_INS_REF: ", TIMER_INS_REF);
        timerShow("time: TIMER_INS_REF_1: ", TIMER_INS_REF_1);
        timerShow("time: TIMER_INS_REF_2: ", TIMER_INS_REF_2);
        timerShow("time: TIMER_INS_DECL: ", TIMER_INS_DECL);
#endif
    }

#ifdef TIMER
    timerStart(TIMER_DB_WRITE);
#endif
    {
        string valFiles;
        leveldb::WriteBatch wbList[DB_NUM];
        char dbDirtyFlags[DB_NUM] = {0};

        for(const auto &itr : m_fileContextMap) {
            //const string& filename = itr->first;
            const string& dbId = itr.second.m_dbId;
            valFiles += "," + dbId;
        }
        for(const auto &fctxItr : m_fileContextMap) {
            const string& filename = fctxItr.first;
            const FileContext& fctx = fctxItr.second;
            const string& dbId = fctx.m_dbId;

            // decide db directory
            char* errp = NULL;
            int id = strtol(dbId.c_str(), &errp, 16);
            int idRem = id % DB_NUM;

            // check if already exists
            if(m_finishedFiles.find(filename) != m_finishedFiles.end()) {
                continue;
            }

            leveldb::WriteBatch& wb = wbList[idRem];
            dbDirtyFlags[idRem] = 1;

            // position to usr
            for(const auto& itr : fctx.m_positition2usrList) {
                setKeyValuePos2Usr(m_CharBuff0, m_CharBuff1, sizeof(m_CharBuff0), itr.first, itr.second);
                wb.Put(dbId + m_CharBuff0, m_CharBuff1);
            }
            // decl
            for(const auto& itr : fctx.m_declList) {
                wb.Put(dbId + itr.first, itr.second);
            }
            // override
            for(const auto& itr : fctx.m_usrId2overrideeMap) {
#if (USE_BASE64 != 0)
                char* p = m_CharBuff0;
                p = encodeVal(p, itr.first);
                *p = '\0';
#else
                snprintf(m_CharBuff0, sizeof(m_CharBuff0), "%x", itr.first);
#endif
                // overridee -> overrider
                wb.Put(dbId + TABLE_NAME_LOCAL_USR_ID_TO_OVERRIDER "|" + m_CharBuff0, itr.second);
            }
            for(const auto& itr : fctx.m_usrId2overriderMap) {
                const IiMap& usrMap = itr.second;
#if (USE_BASE64 != 0)
                char* p = m_CharBuff0;
                p = encodeVal(p, itr.first);
                *p = '\0';
#else
                snprintf(m_CharBuff0, sizeof(m_CharBuff0), "%x", itr.first);
#endif
                string val = "";
                for(const auto& itr_usr : usrMap) {
#if (USE_BASE64 != 0)
                    char* p = m_CharBuff1;
                    p = encodeVal(p, itr_usr.first);
                    *p = '\0';
#else
                    snprintf(m_CharBuff1, sizeof(m_CharBuff1), "%x", itr_usr.first);
#endif
                    if(val.empty()) {
                        val = m_CharBuff1;
                    }
                    else {
                        val.append(string(",") + m_CharBuff1);
                    }
                }
                // overrider -> overridee
                wb.Put(dbId + TABLE_NAME_LOCAL_USR_ID_TO_OVERRIDEE "|" + m_CharBuff0, val);
            }

            // usr
            const SiMap& mapRef = fctx.m_usrIdTbl.GetTbl();
            addIdList(&wb, mapRef, dbId + TABLE_NAME_LOCAL_USR_ID_TO_USR);
            for(const auto& itr : mapRef) {
                string key(dbId + TABLE_NAME_USR_TO_LOCAL_ID "|");
                key.append(itr.first);
#if (USE_BASE64 != 0)
                char* p = m_CharBuff1;
                p = encodeVal(p, itr.second);
                *p = '\0';
#else
                snprintf(m_CharBuff1, sizeof(m_CharBuff1), "%x", itr.second);
#endif
                wb.Put(key, m_CharBuff1);
            }

            for(auto& itr : fctx.m_usrId2refMap) {
                int usrId = itr.first;
#if (USE_BASE64 != 0)
                string key(dbId + TABLE_NAME_LOCAL_USR_ID_TO_REF "|");
                char* p = m_CharBuff0;
                p = encodeVal(p, usrId);
                *p = '\0';
                key.append(m_CharBuff0);
#else
                snprintf(m_CharBuff0, sizeof(m_CharBuff0), "%x", usrId);
                string key(dbId + TABLE_NAME_LOCAL_USR_ID_TO_REF "|" + m_CharBuff0);
#endif
                wb.Put(key, itr.second);
            }
            const SiMap& nameMap = fctx.m_nameIdTbl.GetTbl();
            addIdList(&wb, nameMap, dbId + TABLE_NAME_TOKEN_ID_TO_NAME);

            wb.Put(dbId + TABLE_NAME_CUFILES, valFiles);
            wb.Put(dbId + TABLE_NAME_BUILD_INFO, m_compileUnit + "|" + filename + "|" + m_buildOpt);
        }

        for(int i = 0; i < DB_NUM; i++) {
            if(dbDirtyFlags[i]) {
                leveldb::DB* db;
                snprintf(m_CharBuff0, sizeof(m_CharBuff0), "%x", i);
                string dbDir = string(m_CharBuff0);
                int rv = dbTryOpen(db, m_dbDir + "/" + dbDir);
                if(rv < 0) {
                    printf("ERROR: finalize: open: %s\n", m_commonDbDir.c_str());
                    return -1;
                }
                dbFlush(db, &wbList[i]);
                dbClose(db);
            }
        }
    }
#ifdef TIMER
    timerStop(TIMER_DB_WRITE);
    timerShow("time: TIMER_DB_WRITE: ", TIMER_DB_WRITE);
#endif

    delete m_defaultOptions.block_cache;
    return 0;
}

};
