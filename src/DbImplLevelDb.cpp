#include "DbImplLevelDb.h"
#include <leveldb/c.h>
#include <vector>
#include <map>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

namespace cxxtags {

static leveldb_t* s_db;
static leveldb_t* s_dbFileList;
static char *s_dbErr = NULL;
static leveldb_writebatch_t* s_wb;
static leveldb_writebatch_t* s_wb_fileList;
static std::string s_compileUnit;
static char gCharBuff0[2048];
static char gCharBuff1[2048];

static std::string s_compileUnitId;

void dbWrite(leveldb_t* db, std::string key, std::string value);
void dbWriteBatch(leveldb_writebatch_t* wb, std::string key, std::string value);
int dbRead(std::string& value, leveldb_t* db, std::string key);
void DbImplLevelDb::init(std::string out_dir, std::string src_file_name, std::string excludeList, int isPartial, int isSkel, const char* curDir, int argc, const char** argv)
{
    clock_t startTime = clock();
    leveldb_options_t* options = leveldb_options_create();
    leveldb_options_set_create_if_missing(options, 1);

    s_compileUnit = src_file_name;

    //
    // update file list
    //
    // TODO: add lock
    std::string fileListDbDir = out_dir + "/file_list";
    s_dbFileList = leveldb_open(options, fileListDbDir.c_str(), &s_dbErr);
    if (s_dbErr != NULL) {
        fprintf(stderr, "Open fail.\n");
        return;
    }
    std::string value;
    std::string keyFile = s_compileUnit;
    int rv = 0;
    // check if already registered
    rv = dbRead(value, s_dbFileList, "cu2id|" + s_compileUnit);
    if(rv == 1) {
        // not found
        // add file
        std::string keyFileCount = "file_count";
        rv = dbRead(value, s_dbFileList, keyFileCount);
        if(rv == 1) {
            // key not found 
            dbWrite(s_dbFileList, keyFileCount, "1");
            s_compileUnitId = "0";
        }
        else if(rv == 0) {
            char buf[1024];
            s_compileUnitId = value;
            int id = atoi(s_compileUnitId.c_str());
            snprintf(buf, sizeof(buf), "%d", id+1);
            dbWrite(s_dbFileList, keyFileCount, buf);
            printf("FILECOUNT UPDATEA: %s, %d\n", s_compileUnitId.c_str(), id);
        }
        else {
            printf("ERROR: db info\n");
        }
        dbWrite(s_dbFileList, "cu2id|" + s_compileUnit, s_compileUnitId);
        dbWrite(s_dbFileList, "id2cu|" + s_compileUnitId, s_compileUnit);
    }
    else if(rv == 0) {
        // alread exists
        s_compileUnitId = value;
    }

    // open database for this compile unit
    std::string db_dir = out_dir + "/" + s_compileUnitId;
    s_db = leveldb_open(options, db_dir.c_str(), &s_dbErr);
    if (s_dbErr != NULL) {
        fprintf(stderr, "Open fail.\n");
        return;
    }

    s_wb = leveldb_writebatch_create();
    if(s_wb == NULL) {
        fprintf(stderr, "ERROR: Write Batch fail.\n");
        return;
    }
    leveldb_writebatch_clear(s_wb);

    s_wb_fileList = leveldb_writebatch_create();
    if(s_wb_fileList == NULL) {
        fprintf(stderr, "ERROR: Write Batch fail.\n");
        return;
    }
    leveldb_writebatch_clear(s_wb_fileList);
    clock_t endTime = clock();
    printf("time: init: %f sec\n", (endTime-startTime)/(double)CLOCKS_PER_SEC);
}

void dbWrite(leveldb_t* db, std::string key, std::string value)
{
    s_dbErr = NULL;
    leveldb_writeoptions_t* woptions = leveldb_writeoptions_create();
    leveldb_put(db, woptions, key.c_str(), key.size(), value.c_str(), value.size(), &s_dbErr);
    // TODO: add error handling
    if (s_dbErr != NULL) {
        fprintf(stderr, "Write fail.\n");
    }
    leveldb_free(s_dbErr);
    s_dbErr = NULL;
}

void dbWriteBatch(leveldb_writebatch_t* wb, std::string key, std::string value)
{
    s_dbErr = NULL;
    leveldb_writebatch_put(wb, key.c_str(), key.size(), value.c_str(), value.size());
    // TODO: add error handling
    if (s_dbErr != NULL) {
        fprintf(stderr, "Write fail.\n");
    }
    leveldb_free(s_dbErr);
    s_dbErr = NULL;
}

int dbRead(std::string& value, leveldb_t* db, std::string key)
{
    leveldb_readoptions_t* roptions = leveldb_readoptions_create();
    size_t read_len;
    char* read = leveldb_get(db, roptions, key.c_str(), key.size(), &read_len, &s_dbErr);
    if(read == NULL) {
        return 1;
    }
    if (s_dbErr != NULL) {
        fprintf(stderr, "Read fail.\n");
        return -1;
    }
    value = std::string(read, read_len);
    leveldb_free(s_dbErr);
    s_dbErr = NULL;
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
    leveldb_writebatch_put(s_wb, gCharBuff0, len0, gCharBuff1, len1);
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
        leveldb_writebatch_put(s_wb, gCharBuff0, len0, gCharBuff1, len1);
        //printf("%s, %s, %s, %d, %d\n", s_compileUnit.c_str(), usr.c_str(), filename.c_str(), line, col);
    }
    else {
        // usrId -> decl info
        len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "%s|%d", keyPrefix, usrId); 
        len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%d|%d|%d|%d|%d|%d|%d|%d|%d|%d",
                nameId, fileId, line, col, entityKind, val, isVirtual, typeUsrId, typeKind, isPointer);
        leveldb_writebatch_put(s_wb, gCharBuff0, len0, gCharBuff1, len1);
    }

    // pos -> usr
    len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "pos2usr|%d|%d|%d", fileId, line, col); 
    len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%d", usrId);
    leveldb_writebatch_put(s_wb, gCharBuff0, len0, gCharBuff1, len1);
}

void DbImplLevelDb::insert_overriden_value(int usrId, int nameId, int fileId, int line, int col, int entityKind, int usrIdOverrider, int isDef)
{
}

void DbImplLevelDb::insert_base_class_value(int classUsrId, int baseClassUsrId, int line, int col, int accessibility)
{
}

void DbImplLevelDb::addIdList(leveldb_writebatch_t* db, const std::map<std::string, int >& inMap, std::string tableName)
{
    // lookup map
    std::map<std::string, int >::const_iterator end = inMap.end();
    for(std::map<std::string, int >::const_iterator itr = inMap.begin();
            itr != end;
            itr++) {
        int len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "%s|%d", tableName.c_str(), itr->second); 
        int len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%s", itr->first.c_str());

        leveldb_writebatch_put(db, gCharBuff0, len0, gCharBuff1, len1);
    }
    return ;
}

void addFilesToFileList(const std::map<std::string, int >& inMap)
{
    std::map<std::string, int >::const_iterator end = inMap.end();
    for(std::map<std::string, int >::const_iterator itr = inMap.begin();
            itr != end;
            itr++) {
        leveldb_writeoptions_t* woptions = leveldb_writeoptions_create();
        std::string key = "file_list|" + itr->first;
        leveldb_put(s_dbFileList, woptions, key.c_str(), key.size(), s_compileUnitId.c_str(), s_compileUnitId.size(), &s_dbErr);
        if (s_dbErr != NULL) {
            fprintf(stderr, "Write fail.\n");
            return;
        }
        leveldb_free(s_dbErr);
        s_dbErr = NULL;
    }
}

int dbFlush(leveldb_t* db, leveldb_writebatch_t* wb)
{
    leveldb_writeoptions_t *woptions = leveldb_writeoptions_create();
    leveldb_write(db, woptions, wb, &s_dbErr);
    if (s_dbErr != NULL) {
        fprintf(stderr, "Write fail.\n");
        return 1;
    }
    return 0;
}

int dbClose(leveldb_t* db)
{
    leveldb_close(db);
    if (s_dbErr != NULL) {
        fprintf(stderr, "Close fail.\n");
        return 1;
    }
    return 0;
}

void DbImplLevelDb::fin(const std::map<std::string, int >& fileMap, const std::map<std::string, int >& usrMap, const std::map<std::string, int >& nameMap)
{
    clock_t clockStart = clock();
    // usr
    addIdList(s_wb, usrMap, "id2usr");
    {
        // lookup map
        std::map<std::string, int >::const_iterator end = usrMap.end();
        for(std::map<std::string, int >::const_iterator itr = usrMap.begin();
                itr != end;
                itr++) {
            int len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "%s|%s", "usr2id", itr->first.c_str()); 
            int len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%d", itr->second);

            leveldb_writebatch_put(s_wb, gCharBuff0, len0, gCharBuff1, len1);

            std::string value;
            // check if already registered
            int rv = dbRead(value, s_dbFileList, "usr2cuid|" + itr->first);
            if(rv == 1) {
                dbWriteBatch(s_wb_fileList, "usr2cuid|" + itr->first, s_compileUnitId);
            }
            else if(rv == 0) {
                // alread exists
                dbWriteBatch(s_wb_fileList, "usr2cuid|" + itr->first, value + "," + s_compileUnitId);
            }
        }
    }
    addFilesToFileList(fileMap);
    dbFlush(s_dbFileList, s_wb_fileList);
    dbClose(s_dbFileList);

    addIdList(s_wb, fileMap, "id2file");
    {
        // lookup map
        std::map<std::string, int >::const_iterator end = fileMap.end();
        for(std::map<std::string, int >::const_iterator itr = fileMap.begin();
                itr != end;
                itr++) {
            int len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "%s|%s", "file2id", itr->first.c_str()); 
            int len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%d", itr->second);

            leveldb_writebatch_put(s_wb, gCharBuff0, len0, gCharBuff1, len1);
        }
    }

    addIdList(s_wb, nameMap, "id2name");
    // dump map
    std::map<std::string, std::string>::const_iterator end = s_refMap.end();
    for(std::map<std::string, std::string>::const_iterator itr = s_refMap.begin();
            itr != end;
            itr++) {
        if(itr->first != "") {
            int len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "usr2ref|%s|%s", itr->first.c_str(), s_compileUnitId.c_str()); 
            leveldb_writebatch_put(s_wb, gCharBuff0, len0, itr->second.c_str(), itr->second.size());
        }
    }
    dbFlush(s_db, s_wb);
    dbClose(s_db);

    leveldb_free(s_dbErr);
    s_dbErr = NULL;
    clock_t clockEnd = clock();
    printf("time: fin: %f sec\n", (clockEnd-clockStart)/(double)CLOCKS_PER_SEC);
}

};
