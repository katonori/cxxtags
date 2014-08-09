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

namespace cxxtags {

static leveldb::DB* s_db;
static leveldb::WriteBatch s_wb;
static std::string s_compileUnit;
static std::string s_commonDbDir;
static std::string s_dbDir;
static char gCharBuff0[2048];
static char gCharBuff1[2048];
leveldb::ReadOptions s_defaultRoptions;
leveldb::WriteOptions s_defaultWoptions;
leveldb::Options s_defaultOptions;

static std::string s_compileUnitId;

void dbWrite(leveldb::DB* db, std::string key, std::string value);
int dbRead(std::string& value, leveldb::DB* db, std::string key);
int dbClose(leveldb::DB*& db);
int dbTryOpen(leveldb::DB*& db);

int dbTryOpen(leveldb::DB*& db, std::string dir)
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

void DbImplLevelDb::init(std::string out_dir, std::string src_file_name, std::string excludeList, int isPartial, int isSkel, const char* curDir, int argc, const char** argv)
{
    leveldb::DB* dbCommon = NULL;
    clock_t startTime = clock();
    s_defaultOptions.create_if_missing = true;

    s_dbDir = out_dir;
    s_compileUnit = src_file_name;

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
    fflush(stdout);
    assert(dbCommon != NULL);
    std::string value;
    std::string keyFile = s_compileUnit;
    int rv = 0;
    // check if already registered
    rv = dbRead(value, dbCommon, "cu2id|" + s_compileUnit);
    if(rv < 0) {
        // not found
        // add file
        std::string keyFileCount = "file_count";
        rv = dbRead(value, dbCommon, keyFileCount);
        if(rv < 0) {
            // key not found 
            dbWrite(dbCommon, keyFileCount, "1");
            s_compileUnitId = "0";
        }
        else if(rv == 0) {
            char buf[1024];
            s_compileUnitId = value;
            int id = atoi(s_compileUnitId.c_str());
            snprintf(buf, sizeof(buf), "%d", id+1);
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
    std::string db_dir = out_dir + "/" + s_compileUnitId;
    status = leveldb::DB::Open(s_defaultOptions, db_dir.c_str(), &s_db);
    if (!status.ok()) {
        fprintf(stderr, "Open fail: %s\n", status.ToString().c_str());
        return;
    }

    clock_t endTime = clock();
    //printf("time: init: %f sec\n", (endTime-startTime)/(double)CLOCKS_PER_SEC);
}

void dbWrite(leveldb::DB* db, std::string key, std::string value)
{
    leveldb::Status st = db->Put(s_defaultWoptions, key, value);
    // TODO: add error handling
    if (!st.ok()) {
        fprintf(stderr, "Write fail.: %s\n", st.ToString().c_str());
    }
}

int dbRead(std::string& value, leveldb::DB* db, std::string key)
{
    std::string result;
    leveldb::Status st = db->Get(s_defaultRoptions, key, &result);
    if(!st.ok()) {
        return -1;
    }
    value = result;
    return 0;
}

class RefCount
{
public:
    RefCount()
    {
        mMap[""] = 0;
    }
    std::map<std::string, int > mMap;
    int GetCount(std::string str)
    {
        // lookup map
        std::map<std::string, int >::iterator mapItr = mMap.find(str);
        if(mapItr != mMap.end()){ 
            mapItr->second++;
            return mapItr->second;
        }
        mMap[str] = 0;
        return 0;
    }
    const std::map<std::string, int >& GetTbl(void) const
    {
        return mMap;
    }
};

std::map<std::string, std::string> s_refMap;
RefCount s_refCount;
void DbImplLevelDb::insert_ref_value(std::string usr, int usrId, std::string filename, int fileId, int nameId, int line, int col, int kind, int refFileId, int refLine, int refCol)
{
    int len = snprintf(gCharBuff0, sizeof(gCharBuff0), "%d|%d|%d|%d|%d|%d|%d|%d",
            nameId, fileId, line, col, kind, refFileId, refLine, refCol);
    std::map<std::string, std::string>::iterator itr = s_refMap.find(usr);
    if(itr == s_refMap.end()){ 
        s_refMap[usr] = std::string(gCharBuff0);
    }
    else {
        s_refMap[usr] = itr->second + "," + gCharBuff0;
    }

    // pos -> usr
    int len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "pos2usr|%d|%d|%d", fileId,  line, col);
    int len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%d", usrId);
    s_wb.Put(gCharBuff0, gCharBuff1);
}

void DbImplLevelDb::insert_decl_value(std::string usr, int usrId, std::string filename, int fileId, int nameId, int line, int col, int entityKind, int val, int isVirtual, int isDef, int typeUsrId, int typeKind, int isPointer)
{
    int len0 = 0;
    int len1 = 0;
    const char* keyPrefix = "usr2decl";
    if(isDef) {
        keyPrefix = "usr2def";
        // usrId -> def info
        len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "%s|%s|%s", keyPrefix, s_compileUnitId.c_str(), usr.c_str()); 
        len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%d|%d|%d|%d|%d|%d|%d|%d|%d|%d",
                nameId, fileId, line, col, entityKind, val, isVirtual, typeUsrId, typeKind, isPointer);
        s_wb.Put(gCharBuff0, gCharBuff1);
        //printf("%s, %s, %s, %d, %d\n", s_compileUnit.c_str(), usr.c_str(), filename.c_str(), line, col);
    }
    else {
        // usrId -> decl info
        len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "%s|%d", keyPrefix, usrId); 
        len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%d|%d|%d|%d|%d|%d|%d|%d|%d|%d",
                nameId, fileId, line, col, entityKind, val, isVirtual, typeUsrId, typeKind, isPointer);
        s_wb.Put(gCharBuff0, gCharBuff1);
    }

    // pos -> usr
    len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "pos2usr|%d|%d|%d", fileId, line, col); 
    len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%d", usrId);
    s_wb.Put(gCharBuff0, gCharBuff1);
}

void DbImplLevelDb::insert_overriden_value(int usrId, int nameId, int fileId, int line, int col, int entityKind, int usrIdOverrider, int isDef)
{
}

void DbImplLevelDb::insert_base_class_value(int classUsrId, int baseClassUsrId, int line, int col, int accessibility)
{
}

void DbImplLevelDb::addIdList(leveldb::WriteBatch* db, const std::map<std::string, int >& inMap, std::string tableName)
{
    // lookup map
    std::map<std::string, int >::const_iterator end = inMap.end();
    for(std::map<std::string, int >::const_iterator itr = inMap.begin();
            itr != end;
            itr++) {
        int len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "%s|%d", tableName.c_str(), itr->second); 
        int len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%s", itr->first.c_str());

        db->Put(gCharBuff0, gCharBuff1);
    }
    return ;
}

void addFilesToFileList(leveldb::WriteBatch* wb, const std::map<std::string, int >& inMap)
{
    std::map<std::string, int >::const_iterator end = inMap.end();
    for(std::map<std::string, int >::const_iterator itr = inMap.begin();
            itr != end;
            itr++) {
        std::string key = "file_list|" + itr->first;
        wb->Put(key, s_compileUnitId);
    }
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

void DbImplLevelDb::fin(const std::map<std::string, int >& fileMap, const std::map<std::string, int >& usrMap, const std::map<std::string, int >& nameMap)
{
    clock_t clockStart = clock();

    // usr
    addIdList(&s_wb, usrMap, "id2usr");
    {
        // lookup map
        std::map<std::string, int >::const_iterator end = usrMap.end();
        for(std::map<std::string, int >::const_iterator itr = usrMap.begin();
                itr != end;
                itr++) {
            int len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "%s|%s", "usr2id", itr->first.c_str()); 
            int len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%d", itr->second);

            s_wb.Put(gCharBuff0, gCharBuff1);
        }
    }

    {
        clock_t timeStart = clock();
        leveldb::DB* dbUsrDb = NULL;
        leveldb::WriteBatch wb_usrdb;
        std::string curDir = s_dbDir + "/usr_db";
        if(!boost::filesystem::exists(curDir)) {
            if(!boost::filesystem::create_directory(curDir)) {
                printf("ERROR: create directory: %s\n", curDir.c_str());
                return;
            }
        }
        const int k_usrDbDirNum = 8; 
        int cuId = atoi(s_compileUnitId.c_str());
        snprintf(gCharBuff0, sizeof(gCharBuff0), "%d", (cuId % k_usrDbDirNum)); 
        curDir = curDir + "/" + std::string(gCharBuff0);
        int rv = dbTryOpen(dbUsrDb, curDir);
        if(rv < 0) {
            printf("ERROR: fin: common db open: %s\n", curDir.c_str());
            return ;
        }
        // lookup map
        std::map<std::string, int >::const_iterator end = usrMap.end();
        for(std::map<std::string, int >::const_iterator itr = usrMap.begin();
                itr != end;
                itr++) {
            if(itr->first != "") {
                std::string value;
                // check if already registered
                int rv = dbRead(value, dbUsrDb, "usr2cuid|" + itr->first);
                if(rv < 0) {
                    wb_usrdb.Put("usr2cuid|" + itr->first, s_compileUnitId);
                }
                else if(rv == 0) {
                    // alread exists
                    wb_usrdb.Put("usr2cuid|" + itr->first, value + "," + s_compileUnitId);
                }
            }
        }
        dbFlush(dbUsrDb, &wb_usrdb);
        dbClose(dbUsrDb);
        clock_t timeEnd = clock();
        printf("time: usr_wb: %f ms\n", (timeEnd-timeStart)*1000.0/CLOCKS_PER_SEC);
    }

    {
        leveldb::WriteBatch wb;
        addFilesToFileList(&wb, fileMap);
        leveldb::DB* db;
        int rv = dbTryOpen(db, s_commonDbDir);
        if(rv < 0) {
            printf("ERROR: fin: common db open: %s\n", s_commonDbDir.c_str());
            return ;
        }
        dbFlush(db, &wb);
        dbClose(db);
    }

    addIdList(&s_wb, fileMap, "id2file");
    {
        // lookup map
        std::map<std::string, int >::const_iterator end = fileMap.end();
        for(std::map<std::string, int >::const_iterator itr = fileMap.begin();
                itr != end;
                itr++) {
            int len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "%s|%s", "file2id", itr->first.c_str()); 
            int len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%d", itr->second);

            s_wb.Put(gCharBuff0, gCharBuff1);
        }
    }

    addIdList(&s_wb, nameMap, "id2name");
    // dump map
    std::map<std::string, std::string>::const_iterator end = s_refMap.end();
    for(std::map<std::string, std::string>::const_iterator itr = s_refMap.begin();
            itr != end;
            itr++) {
        if(itr->first != "") {
            int len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "usr2ref|%s|%s", itr->first.c_str(), s_compileUnitId.c_str()); 
            s_wb.Put(gCharBuff0, itr->second);
        }
    }
    dbFlush(s_db, &s_wb);
    dbClose(s_db);

    clock_t clockEnd = clock();
    printf("time: fin: %f sec\n", (clockEnd-clockStart)/(double)CLOCKS_PER_SEC);
}

};
