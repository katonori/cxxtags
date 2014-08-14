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

static string s_compileUnitId;
static IdTbl *fileIdTbl;
static IdTbl *nameIdTbl;
static IdTbl *usrIdTbl;

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
    clock_t startTime = clock();
    s_defaultOptions.create_if_missing = true;

    s_dbDir = out_dir;
    s_compileUnit = src_file_name;
    fileIdTbl = new IdTbl();
    nameIdTbl = new IdTbl();
    usrIdTbl = new IdTbl();

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

    clock_t endTime = clock();
    //printf("time: init: %f sec\n", (endTime-startTime)/(double)CLOCKS_PER_SEC);
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
SsMap s_refMap;
void DbImplLevelDb::insert_ref_value(const string& usr, const string& filename, const string& name, int line, int col)
{
    int fileId = fileIdTbl->GetId(filename);
    int nameId = nameIdTbl->GetId(name);
    int usrId = usrIdTbl->GetId(usr);
    int len = snprintf(gCharBuff0, sizeof(gCharBuff0), "%x|%x|%x|%x",
            nameId, fileId, line, col);
    SsMap::iterator itr = s_refMap.find(usr);
    if(itr == s_refMap.end()){ 
        s_refMap[usr] = string(gCharBuff0);
    }
    else {
        s_refMap[usr] = itr->second + "," + gCharBuff0;
    }

    if(usr != "") {
        s_usr2fileMap[usr][filename] = "";
    }

    // pos -> usr
    int len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "pos2usr|%x|%x|%x", fileId,  line, col);
    int len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%x", usrId);
    s_wb.Put(gCharBuff0, gCharBuff1);
}

void DbImplLevelDb::insert_decl_value(const string& usr, const string& filename, const string& name, int line, int col, int isDef)
{
    int len0 = 0;
    int len1 = 0;
    const char* keyPrefix = "usr2decl";
    int fileId = fileIdTbl->GetId(filename);
    int nameId = nameIdTbl->GetId(name);
    int usrId = usrIdTbl->GetId(usr);
    if(isDef) {
        keyPrefix = "usr2def";
        if(usr == "c:@C@CppCheckExecutor@F@check#I#*1*1C#") {
            printf("MATCHED: %s, %s: %x, %x, %x, %x\n", s_compileUnit.c_str(), usr.c_str(), nameId, fileId, line, col);
        }
        // usrId -> def info
        len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "%s|%s|%s", keyPrefix, s_compileUnitId.c_str(), usr.c_str()); 
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
}

void DbImplLevelDb::insert_overriden_value(const string& usr, const string& name, int line, int col, const string& usrOverrider, int isDef)
{
    //int fileId = fileIdTbl->GetId(fileName);
    //int nameId = nameIdTbl->GetId(name);
}

void DbImplLevelDb::insert_base_class_value(const string& classUsr, const string& baseClassUsr, int line, int col, int accessibility)
{
}

void DbImplLevelDb::addIdList(leveldb::WriteBatch* db, const SiMap& inMap, const string& tableName)
{
    // lookup map
    BOOST_FOREACH(SiPair itr, inMap) {
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
    BOOST_FOREACH(SiPair itr, inMap) {
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
        clock_t timeStart = clock();
        leveldb::DB* dbUsrDb = NULL;
        leveldb::WriteBatch wb_usrdb;
        string curDir = s_dbDir + "/usr_db";
        if(!boost::filesystem::exists(curDir)) {
            if(!boost::filesystem::create_directory(curDir)) {
                printf("ERROR: create directory: %s\n", curDir.c_str());
                return;
            }
        }
        const int k_usrDbDirNum = 1; 
        char* errp = NULL;
        int cuId = strtol(s_compileUnitId.c_str(), &errp, 16);
        assert(*errp == '\0');
        snprintf(gCharBuff0, sizeof(gCharBuff0), "%x", (cuId % k_usrDbDirNum)); 
        curDir = curDir + "/" + string(gCharBuff0);
        int rv = dbTryOpen(dbUsrDb, curDir);
        if(rv < 0) {
            printf("ERROR: fin: common db open: %s\n", curDir.c_str());
            return ;
        }
        clock_t time0 = clock();
        clock_t timeArray[128];

        // lookup map
        timeArray[100] = 0;
        timeArray[101] = 0;
        timeArray[102] = 0;
        timeArray[103] = 0;
        int count = 0;
        BOOST_FOREACH(SiPair itr, usrMap) {
            const string& usr = itr.first;
            size_t pos_global = usr.find("c:@", 0);
            size_t pos_macro = usr.find("c:macro", 0);
#if 0
            if(usr != "") {
#else
            if(usr != "" && (pos_global == 0 || pos_macro == 0)) {
#endif
                list<string> file_id_list;
                timeArray[8] = clock();
                BOOST_FOREACH(SsPair itr_file_list, s_usr2fileMap[usr]) {
                    file_id_list.push_back(s_file2fidMap[itr_file_list.first].c_str());
                }
                SiMap file_list_map;
                BOOST_FOREACH(string s, file_id_list) {
                    file_list_map[s] = 0;
                }
                timeArray[9] = clock();

                // check if already registered
                timeArray[0] = clock();
                string value;
                int rv = dbRead(value, dbUsrDb, "usr2file|" + usr);
                timeArray[1] = clock();
                string file_list_string = "";
                if(rv == 0) {
                    string delim = ",";
                    list<string> old_list;
                    boost::split(old_list, value, boost::is_any_of(delim));
                    BOOST_FOREACH(string s, old_list) {
                        file_list_map[s] = 0;
                    }
                }
                timeArray[2] = clock();
                BOOST_FOREACH(SiPair itr_str, file_list_map) {
                    if(file_list_string == "") {
                        file_list_string = itr_str.first;
                    }
                    else {
                        file_list_string += ","+itr_str.first;
                    }
                }
                timeArray[3] = clock();
                wb_usrdb.Put("usr2file|" + usr, file_list_string);
                timeArray[4] = clock();
                timeArray[100] += timeArray[9] - timeArray[8];
                timeArray[101] += timeArray[2] - timeArray[0];
                timeArray[102] += timeArray[3] - timeArray[2];
                timeArray[103] += timeArray[1] - timeArray[0];
                count++;
            }
        }
        timeArray[5] = clock();
        dbFlush(dbUsrDb, &wb_usrdb);
        timeArray[6] = clock();
        dbClose(dbUsrDb);
        timeArray[7] = clock();
        clock_t timeEnd = clock();
        printf("time: 0-1: %f ms\n", (timeArray[1]-timeArray[0])*1000.0/CLOCKS_PER_SEC);
        printf("time: 1-2: %f ms\n", (timeArray[2]-timeArray[1])*1000.0/CLOCKS_PER_SEC);
        printf("time: 2-3: %f ms\n", (timeArray[3]-timeArray[2])*1000.0/CLOCKS_PER_SEC);
        printf("time: 3-4: %f ms\n", (timeArray[4]-timeArray[3])*1000.0/CLOCKS_PER_SEC);
        printf("time: 5-6: %f ms\n", (timeArray[6]-timeArray[5])*1000.0/CLOCKS_PER_SEC);
        printf("time: 6-7: %f ms\n", (timeArray[7]-timeArray[6])*1000.0/CLOCKS_PER_SEC);
        printf("time: 8-9: %f ms\n", (timeArray[9]-timeArray[8])*1000.0/CLOCKS_PER_SEC);
        printf("time: usr_wb0: %f ms\n", (time0-timeStart)*1000.0/CLOCKS_PER_SEC);
        printf("time: usr_wb: %f ms\n", (timeEnd-timeStart)*1000.0/CLOCKS_PER_SEC);
        printf("time: 100: %f ms\n", (timeArray[100])*1000.0/CLOCKS_PER_SEC);
        printf("time: 101: %f ms\n", (timeArray[101])*1000.0/CLOCKS_PER_SEC);
        printf("time: 102: %f ms\n", (timeArray[102])*1000.0/CLOCKS_PER_SEC);
        printf("time: 103: %f ms\n", (timeArray[103])*1000.0/CLOCKS_PER_SEC);
        printf("time: %d times\n", count);
    }

    addIdList(&s_wb, fileMap, "id2file");
    {
        // lookup map
        BOOST_FOREACH(SiPair itr, fileMap) {
            int len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "%s|%s", "file2id", itr.first.c_str()); 
            int len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%x", itr.second);
            s_wb.Put(gCharBuff0, gCharBuff1);
        }
    }

    addIdList(&s_wb, nameMap, "id2name");
    // dump map
    BOOST_FOREACH(SsPair itr, s_refMap) {
        if(itr.first != "") {
            int len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "usr2ref|%s|%s", itr.first.c_str(), s_compileUnitId.c_str()); 
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
