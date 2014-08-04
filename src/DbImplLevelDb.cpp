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
static leveldb_t* s_db_common;
static leveldb_t* s_dbFileList;
static char *s_dbErr = NULL;
static leveldb_writebatch_t* s_wb;
static leveldb_writebatch_t* s_wb_common;
static std::string s_compileUnit;
static char gCharBuff0[2048];
static char gCharBuff1[2048];

static std::string s_compileUnitId;

void dbWrite(leveldb_t* db, std::string key, std::string value);
int dbRead(std::string& value, leveldb_t* db, std::string key);
void DbImplLevelDb::init(std::string out_dir, std::string src_file_name, std::string excludeList, int isPartial, int isSkel, const char* curDir, int argc, const char** argv)
{
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
    rv = dbRead(value, s_dbFileList, "db_dir|" + s_compileUnit);
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
        dbWrite(s_dbFileList, "db_dir|" + s_compileUnit, s_compileUnitId);
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

    db_dir = out_dir + "/common";
    s_db_common = leveldb_open(options, db_dir.c_str(), &s_dbErr);
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

    s_wb_common = leveldb_writebatch_create();
    if(s_wb_common == NULL) {
        fprintf(stderr, "ERROR: Write Batch fail.\n");
        return;
    }
    leveldb_writebatch_clear(s_wb_common);
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

RefCount s_refCount;
void DbImplLevelDb::insert_ref_value(std::string usr, std::string filename, int fileId, std::string name, int line, int col, int kind, int refFileId, int refLine, int refCol)
{
    // ref usrId -> decl info
    int len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "usr2ref|%s|%s|%d", usr.c_str(), s_compileUnit.c_str(), s_refCount.GetCount(usr)); 
    int len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%s|%d|%d|%d|%d|%d|%d|%d",
            name.c_str(), fileId, line, col, kind, refFileId, refLine, refCol);
    leveldb_writebatch_put(s_wb_common, gCharBuff0, len0, gCharBuff1, len1);

    // pos -> usr
    len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "pos2usr|%s|%d|%d", filename.c_str(),  line, col);
    len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%s", usr.c_str());
    leveldb_writebatch_put(s_wb, gCharBuff0, len0, gCharBuff1, len1);
}

void DbImplLevelDb::insert_decl_value(std::string usr, std::string filename, int fileId, std::string name, int line, int col, int entityKind, int val, int isVirtual, int isDef, int typeUsrId, int typeKind, int isPointer)
{
    int len0 = 0;
    int len1 = 0;
    const char* keyPrefix = "usr2decl";
    if(isDef) {
        keyPrefix = "usr2def";
        // usrId -> decl info
        len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "%s|%s|%s", keyPrefix, s_compileUnit.c_str(), usr.c_str()); 
        len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%s|%d|%d|%d|%d|%d|%d|%d|%d|%d",
                name.c_str(), fileId, line, col, entityKind, val, isVirtual, typeUsrId, typeKind, isPointer);
        leveldb_writebatch_put(s_wb_common, gCharBuff0, len0, gCharBuff1, len1);
        //printf("%s, %s, %s, %d, %d\n", s_compileUnit.c_str(), usr.c_str(), filename.c_str(), line, col);
    }
    else {
        // usrId -> decl info
        len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "%s|%s", keyPrefix, usr.c_str()); 
        len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%s|%d|%d|%d|%d|%d|%d|%d|%d|%d",
                name.c_str(), fileId, line, col, entityKind, val, isVirtual, typeUsrId, typeKind, isPointer);
        leveldb_writebatch_put(s_wb, gCharBuff0, len0, gCharBuff1, len1);
    }

    // pos -> usr
    len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "pos2usr|%s|%d|%d", filename.c_str(), line, col); 
    len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%s", usr.c_str());
    leveldb_writebatch_put(s_wb, gCharBuff0, len0, gCharBuff1, len1);
}

void DbImplLevelDb::insert_overriden_value(int usrId, int nameId, int fileId, int line, int col, int entityKind, int usrIdOverrider, int isDef)
{
}

void DbImplLevelDb::insert_base_class_value(int classUsrId, int baseClassUsrId, int line, int col, int accessibility)
{
}

void DbImplLevelDb::addIdList(const std::map<std::string, int >& inMap, std::string tableName)
{
    // lookup map
    std::map<std::string, int >::const_iterator end = inMap.end();
    for(std::map<std::string, int >::const_iterator itr = inMap.begin();
            itr != end;
            itr++) {
        int len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "%s|%s|%d", tableName.c_str(), s_compileUnit.c_str(), itr->second); 
        int len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%s", itr->first.c_str());

        leveldb_writebatch_put(s_wb, gCharBuff0, len0, gCharBuff1, len1);
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
        leveldb_put(s_dbFileList, woptions, key.c_str(), key.size(), s_compileUnit.c_str(), s_compileUnit.size(), &s_dbErr);
        if (s_dbErr != NULL) {
            fprintf(stderr, "Write fail.\n");
            return;
        }
        leveldb_free(s_dbErr);
        s_dbErr = NULL;
    }
}

void DbImplLevelDb::fin(const std::map<std::string, int >& fileMap, const std::map<std::string, int >& usrMap, const std::map<std::string, int >& nameMap)
{
    addIdList(fileMap, "id2file");
    addFilesToFileList(fileMap);
    //addIdList(usrMap, "id2usr");
    //addIdList(nameMap, "id2name");

    leveldb_free(s_dbErr);
    s_dbErr = NULL;
    leveldb_writeoptions_t *woptions = leveldb_writeoptions_create();

    leveldb_write(s_db, woptions, s_wb, &s_dbErr);
    if (s_dbErr != NULL) {
        fprintf(stderr, "Write fail.\n");
    }
    leveldb_close(s_db);
    if (s_dbErr != NULL) {
        fprintf(stderr, "Close fail.\n");
    }

    leveldb_write(s_db_common, woptions, s_wb_common, &s_dbErr);
    if (s_dbErr != NULL) {
        fprintf(stderr, "Write fail.\n");
    }
    leveldb_close(s_db_common);
    if (s_dbErr != NULL) {
        fprintf(stderr, "Close fail.\n");
    }

    leveldb_close(s_dbFileList);
    if (s_dbErr != NULL) {
        fprintf(stderr, "Close fail.\n");
    }

    leveldb_free(s_dbErr);
    s_dbErr = NULL;
}

};
