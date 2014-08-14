#include "DbImplLevelDb.h"
#include <leveldb/db.h>
#include "leveldb/write_batch.h"
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
#include <boost/timer/timer.hpp>

namespace cxxtags {

using namespace std;

typedef map<string, string> SsMap;
typedef pair<string, string> SsPair;
typedef map<string, int> SiMap;
typedef pair<string, int> SiPair;

static leveldb::DB* s_db;
static leveldb::WriteBatch s_wb;
static string s_compileUnit;
static string s_commonDbDir;
static string s_dbDir;
static char gCharBuff0[2048];
static char gCharBuff1[2048];
leveldb::ReadOptions s_defaultRoptions;
leveldb::WriteOptions s_defaultWoptions;
leveldb::Options s_defaultOptions;

const int k_usrDbDirNum = 4; 

static string s_compileUnitId;
static IdTbl *fileIdTbl;
static IdTbl *nameIdTbl;
static IdTbl *usrIdTbl;
static const int k_timerNum = 128;
clock_t s_timeArray[k_timerNum];
boost::timer::cpu_timer* s_timers;

enum {
    TIMER_INS_REF = 64,
    TIMER_INS_DECL,
    TIMER_INS_OVERRIDEN,
    TIMER_USR_DB0,
    TIMER_USR_DB1,
};

int dbWrite(leveldb::DB* db, const string& key, const string& value);
int dbRead(string& value, leveldb::DB* db, const string& key);
int dbClose(leveldb::DB*& db);
int dbTryOpen(leveldb::DB*& db);

int dbTryOpen(leveldb::DB*& db, string dir)
{
    clock_t start = clock();
    leveldb::Status st;
    while(1) {
        st= leveldb::DB::Open(s_defaultOptions, dir, &db);
        if(st.ok()) {
            break;
        }
        clock_t now = clock();
        if((now - start)/(double)CLOCKS_PER_SEC > 10.0) {
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

void DbImplLevelDb::init(const string& out_dir, const string& src_file_name, const string& excludeList, int isPartial, int isSkel, const char* curDir, int argc, const char** argv)
{
    leveldb::DB* dbCommon = NULL;
    s_defaultOptions.create_if_missing = true;

    s_dbDir = out_dir;
    s_compileUnit = src_file_name;
    fileIdTbl = new IdTbl();
    nameIdTbl = new IdTbl();
    usrIdTbl = new IdTbl();

    s_timers = new boost::timer::cpu_timer[k_timerNum];
    for(int i = 0; i < k_timerNum; i++) {
        s_timers[i].stop();
    }

    if(!boost::filesystem::exists(s_dbDir)) {
        if(!boost::filesystem::create_directory(s_dbDir)) {
            printf("ERROR: create directory: %s\n", s_dbDir.c_str());
            return;
        }
    }

    //
    // update file list
    //
    // TODO: add lock
    leveldb::Status status;
    s_commonDbDir = out_dir + "/common";
    if (dbTryOpen(dbCommon, s_commonDbDir) < 0) {
        fprintf(stderr, "Open fail.: %s\n", s_commonDbDir.c_str());
        return;
    }
    assert(dbCommon != NULL);
    string value;
    string keyFile = s_compileUnit;
    int rv = 0;
    // check if already registered
    rv = dbRead(value, dbCommon, "cu2id|" + s_compileUnit);
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
        dbWrite(dbCommon, "cu2id|" + s_compileUnit, s_compileUnitId);
        dbWrite(dbCommon, "id2cu|" + s_compileUnitId, s_compileUnit);
    }
    else if(rv == 0) {
        // alread exists
        s_compileUnitId = value;
    }
    dbClose(dbCommon);

    // open database for this compile unit
    assert(s_compileUnitId != "");
    string db_dir = out_dir + "/" + s_compileUnitId;
    status = leveldb::DB::Open(s_defaultOptions, db_dir.c_str(), &s_db);
    if (!status.ok()) {
        fprintf(stderr, "Open fail: %s\n", status.ToString().c_str());
        return;
    }
}

int dbWrite(leveldb::DB* db, const string& key, const string& value)
{
    leveldb::Status st = db->Put(s_defaultWoptions, key, value);
    // TODO: add error handling
    if (!st.ok()) {
        fprintf(stderr, "Write fail.: %s\n", st.ToString().c_str());
        return -1;
    }
    return 0;
}

int dbRead(string& value, leveldb::DB* db, const string& key)
{
    string result;
    leveldb::Status st = db->Get(s_defaultRoptions, key, &result);
    if(!st.ok()) {
        return -1;
    }
    value = result;
    return 0;
}

static map<string, SsMap > s_usr2fileMap;
SsMap s_usr2refMap;
void DbImplLevelDb::insert_ref_value(const string& usr, const string& filename, const string& name, int line, int col)
{
    s_timers[TIMER_INS_REF].resume();
    
    int fileId = fileIdTbl->GetId(filename);
    int nameId = nameIdTbl->GetId(name);
    int usrId = usrIdTbl->GetId(usr);
    int len = snprintf(gCharBuff0, sizeof(gCharBuff0), "%x|%x|%x|%x", nameId, fileId, line, col);
    SsMap::iterator itr = s_usr2refMap.find(usr);
    if(itr == s_usr2refMap.end()){ 
        s_usr2refMap[usr] = string(gCharBuff0);
    }
    else {
        s_usr2refMap[usr] = itr->second + "," + gCharBuff0;
    }

    if(usr != "") {
        s_usr2fileMap[usr][filename] = "";
    }

    // pos -> usr
    int len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "pos2usr|%x|%x|%x", fileId,  line, col);
    int len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%x", usrId);
    s_wb.Put(gCharBuff0, gCharBuff1);
    s_timers[TIMER_INS_REF].stop();
}

void DbImplLevelDb::insert_decl_value(const string& usr, const string& filename, const string& name, int line, int col, int isDef)
{
    s_timers[TIMER_INS_DECL].resume();
    int len0 = 0;
    int len1 = 0;
    const char* keyPrefix = "usr2decl";
    int fileId = fileIdTbl->GetId(filename);
    int nameId = nameIdTbl->GetId(name);
    int usrId = usrIdTbl->GetId(usr);
    if(isDef) {
        keyPrefix = "usr2def";
        // usrId -> def info
        len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "%s|%s", keyPrefix, usr.c_str()); 
        len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%x|%x|%x|%x",
                nameId, fileId, line, col);
        s_wb.Put(gCharBuff0, gCharBuff1);
        //printf("%s, %s, %s, %x, %x\n", s_compileUnit.c_str(), usr.c_str(), filename.c_str(), line, col);
    }
    else {
        // usrId -> decl info
        len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "%s|%x", keyPrefix, usrId); 
        len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%x|%x|%x|%x",
                nameId, fileId, line, col);
        s_wb.Put(gCharBuff0, gCharBuff1);
    }

    if(usr != "") {
        s_usr2fileMap[usr][filename] = "";
    }

    // pos -> usr
    len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "pos2usr|%x|%x|%x", fileId, line, col); 
    len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%x", usrId);
    s_wb.Put(gCharBuff0, gCharBuff1);
    s_timers[TIMER_INS_DECL].stop();
}

void DbImplLevelDb::insert_overriden_value(const string& usr, const string& name, const string& filename, int line, int col, const string& usrOverrider, int isDef)
{
    s_timers[TIMER_INS_OVERRIDEN].resume();
    //printf("overriden: %s, %s, %s\n", usr.c_str(), filename.c_str(), name.c_str());
    int len0 = 0;
    int len1 = 0;
    const char* key = "usr2overrirden";
    int fileId = fileIdTbl->GetId(filename);
    int nameId = nameIdTbl->GetId(name);
    int usrId = usrIdTbl->GetId(usr);
    // usrId -> decl info
    len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "%s|%s", key, usr.c_str()); 
    len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%x|%x|%x|%x",
            nameId, fileId, line, col);
    s_wb.Put(gCharBuff0, gCharBuff1);

    if(usr != "") {
        s_usr2fileMap[usr][filename] = "";
    }

    // pos -> usr
    len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "pos2usr|%x|%x|%x", fileId, line, col); 
    len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%x", usrId);
    s_wb.Put(gCharBuff0, gCharBuff1);
    s_timers[TIMER_INS_OVERRIDEN].stop();
}

void DbImplLevelDb::insert_base_class_value(const string& classUsr, const string& baseClassUsr, int line, int col, int accessibility)
{
}

void DbImplLevelDb::addIdList(leveldb::WriteBatch* db, const SiMap& inMap, const string& tableName)
{
    // lookup map
    BOOST_FOREACH(const SiPair& itr, inMap) {
        int len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "%s|%x", tableName.c_str(), itr.second); 
        int len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%s", itr.first.c_str());
        db->Put(gCharBuff0, gCharBuff1);
    }
    return ;
}

static SsMap s_file2fidMap;
void addFilesToFileList(leveldb::DB* db, leveldb::WriteBatch* wb, const SiMap& inMap)
{
    char buf[1024];
    int startId = 0;
    string valStr;
    string keyFileCount = "file_count";
    string keyFid2Cuid = "fid2cuid";
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
    BOOST_FOREACH(const SiPair& itr, inMap) {
        string fn = itr.first;
        string key = "file_list|" + fn;
        int rv = dbRead(valStr, db, key);
        if(rv < 0) {
            snprintf(buf, sizeof(buf), "%x", id);
            dbWrite(db, key, s_compileUnitId + "," + string(buf));
            s_file2fidMap[fn] = buf;
            dbWrite(db, keyFid2Cuid + "|" + string(buf), s_compileUnitId);
            id++;
        }
        else {
            // get fid
            size_t pos = valStr.find(",");
            assert(pos != string::npos);
            string fid = valStr.substr(pos+1, valStr.size()-1);
            // set fid to map
            s_file2fidMap[fn] = fid;
            dbWrite(db, keyFid2Cuid + "|" + fid, s_compileUnitId);
        }
    }
    snprintf(buf, sizeof(buf), "%x", id);
    dbWrite(db, keyFileCount, buf);
}

int dbFlush(leveldb::DB* db, leveldb::WriteBatch* wb)
{
    leveldb::Status status = db->Write(s_defaultWoptions, wb);
    if (!status.ok()) {
        fprintf(stderr, "Write fail.: %s\n", status.ToString().c_str());
        return 1;
    }
    return 0;
}

int dbClose(leveldb::DB*& db)
{
    delete db;
    db = NULL;
    return 0;
}

void DbImplLevelDb::fin(void)
{
    const SiMap& fileMap = fileIdTbl->GetTbl();
    const SiMap& nameMap = nameIdTbl->GetTbl();
    const SiMap& usrMap = usrIdTbl->GetTbl();
    clock_t clockStart = clock();

    // usr
    addIdList(&s_wb, usrMap, "id2usr");

    {
        leveldb::WriteBatch wb_common;
        leveldb::DB* db_common;
        int rv = dbTryOpen(db_common, s_commonDbDir);
        if(rv < 0) {
            printf("ERROR: fin: common db open: %s\n", s_commonDbDir.c_str());
            return ;
        }
        addFilesToFileList(db_common, &wb_common, fileMap);
        dbFlush(db_common, &wb_common);
        dbClose(db_common);
    }

    // update UsrDb
    // TODO: speed up this part
    {
        leveldb::DB* dbUsrDb = NULL;
        leveldb::WriteBatch wb_usrdb;
        string curDir = s_dbDir + "/usr_db";
        if(!boost::filesystem::exists(curDir)) {
            if(!boost::filesystem::create_directory(curDir)) {
                printf("ERROR: create directory: %s\n", curDir.c_str());
                return;
            }
        }
        map<string, SiMap> usrFidMap;
        BOOST_FOREACH(const SiPair& itr, usrMap) {
            const string& usr = itr.first;
            if(usr != "") {
                SiMap& fidMap = usrFidMap[usr];
                BOOST_FOREACH(const SsPair& itr_file_list, s_usr2fileMap[usr]) {
                    fidMap[s_file2fidMap[itr_file_list.first]] = 0;
                }
            }
        }

        char* errp = NULL;
        int cuId = strtol(s_compileUnitId.c_str(), &errp, 16);
        assert(*errp == '\0');
        snprintf(gCharBuff0, sizeof(gCharBuff0), "%x", (cuId % k_usrDbDirNum)); 
        curDir = curDir + "/" + string(gCharBuff0);

        s_timers[TIMER_USR_DB0].start();
        //////
        // open db
        int rv = dbTryOpen(dbUsrDb, curDir);
        if(rv < 0) {
            printf("ERROR: fin: common db open: %s\n", curDir.c_str());
            return ;
        }
        s_timers[TIMER_USR_DB1].start();

        // lookup map
        int count = 0;
        BOOST_FOREACH(const SiPair& itr, usrMap) {
            const string& usr = itr.first;
            size_t pos_global = usr.find("c:@", 0);
            size_t pos_macro = usr.find("c:macro", 0);
#if 0
            if(usr != "") {
#else
            if(usr != "" && (pos_global == 0 || pos_macro == 0)) {
#endif
                SiMap& file_list_map = usrFidMap[usr];
                // check if already registered
                s_timers[2].resume();
                string value;
                int rv = dbRead(value, dbUsrDb, "usr2file|" + usr);
                s_timers[2].stop();
                s_timers[3].resume();
                if(rv == 0) {
                    const string delim = ",";
                    list<string> old_list;
                    boost::split(old_list, value, boost::is_any_of(delim));
                    BOOST_FOREACH(const string& s, old_list) {
                        file_list_map[s] = 0;
                    }
                }
                s_timers[3].stop();
                s_timers[4].resume();
                string file_list_string = "";
                BOOST_FOREACH(const SiPair& itr_str, file_list_map) {
                    file_list_string += itr_str.first+",";
                }
                file_list_string = file_list_string.substr(0, file_list_string.size()-1);
                s_timers[4].stop();
                wb_usrdb.Put("usr2file|" + usr, file_list_string);
                count++;
            }
        }
        s_timers[5].start();
        dbFlush(dbUsrDb, &wb_usrdb);
        s_timers[5].stop();
        s_timers[6].start();
        dbClose(dbUsrDb);
        s_timers[6].stop();
        s_timers[TIMER_USR_DB1].stop();
        s_timers[TIMER_USR_DB0].stop();
        // close db
        //////
        s_timeArray[7] = clock();
        clock_t timeEnd = clock();
        printf("time: TIMER_USR_DB0: %s", s_timers[TIMER_USR_DB0].format().c_str());
        printf("time: TIMER_USR_DB1: %s", s_timers[TIMER_USR_DB1].format().c_str());
        printf("time: 2: %s", s_timers[2].format().c_str());
        printf("time: 3: %s", s_timers[3].format().c_str());
        printf("time: 4: %s", s_timers[4].format().c_str());
        printf("time: 5: %s", s_timers[5].format().c_str());
        printf("time: 6: %s", s_timers[5].format().c_str());
        printf("time: TIMER_INS_REF: %s", s_timers[TIMER_INS_REF].format().c_str());
        printf("time: TIMER_INS_DECL: %s", s_timers[TIMER_INS_DECL].format().c_str());
        printf("time: %d times\n", count);
    }

    addIdList(&s_wb, fileMap, "id2file");
    {
        // lookup map
        BOOST_FOREACH(const SiPair& itr, fileMap) {
            int len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "%s|%s", "file2id", itr.first.c_str()); 
            int len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%x", itr.second);
            s_wb.Put(gCharBuff0, gCharBuff1);
        }
    }

    addIdList(&s_wb, nameMap, "id2name");
    // dump map
    BOOST_FOREACH(const SsPair& itr, s_usr2refMap) {
        const string& usr = itr.first;
        if(usr != "") {
            int len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "usr2ref|%s|%s", usr.c_str(), s_compileUnitId.c_str()); 
            s_wb.Put(gCharBuff0, itr.second);
        }
    }
    dbFlush(s_db, &s_wb);
    dbClose(s_db);

    clock_t clockEnd = clock();
    printf("time: fin: %f sec\n", (clockEnd-clockStart)/(double)CLOCKS_PER_SEC);
    delete fileIdTbl;
    delete nameIdTbl;
    delete usrIdTbl;
}

};
