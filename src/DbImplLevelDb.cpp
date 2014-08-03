#include "DbImplLevelDb.h"
#include <leveldb/c.h>
#include <vector>
#include <map>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>

namespace cxxtags {

static leveldb_t* s_db;
static leveldb_t* s_dbFileList;
static char *s_dbErr = NULL;
static leveldb_writebatch_t* s_wb;
static std::string s_compileUnit;
static char gCharBuff0[2048];
static char gCharBuff1[2048];

void DbImplLevelDb::init(std::string out_dir, std::string src_file_name, std::string excludeList, int isPartial, int isSkel, const char* curDir, int argc, const char** argv)
{
    s_compileUnit = src_file_name;

    leveldb_options_t* options = leveldb_options_create();
    leveldb_options_set_create_if_missing(options, 1);
    s_db = leveldb_open(options, out_dir.c_str(), &s_dbErr);
    if (s_dbErr != NULL) {
        fprintf(stderr, "Open fail.\n");
        return;
    }
    s_wb = leveldb_writebatch_create();
    if(s_wb == NULL) {
        fprintf(stderr, "ERROR: Write Batch fail.\n");
        return;
    }
    std::string fileListDbDir = out_dir + "/file_list";
    s_dbFileList = leveldb_open(options, fileListDbDir.c_str(), &s_dbErr);
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

    //
    // update file list
    //
    // TODO: add lock
    // write
    leveldb_writeoptions_t* woptions = leveldb_writeoptions_create();
    leveldb_put(s_dbFileList, woptions, s_compileUnit.c_str(), s_compileUnit.size(), s_compileUnit.c_str(), s_compileUnit.size(), &s_dbErr);
    if (s_dbErr != NULL) {
        fprintf(stderr, "Write fail.\n");
        return;
    }

    leveldb_free(s_dbErr); s_dbErr = NULL;
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
void DbImplLevelDb::insert_ref_value(std::string usr, std::string filename, std::string name, int line, int col, int kind, int refFileId, int refLine, int refCol)
{
    leveldb_free(s_dbErr);
    s_dbErr = NULL;

    // ref usrId -> decl info
    int len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "usr2ref|%s|%s|%d", usr.c_str(), s_compileUnit.c_str(), s_refCount.GetCount(usr)); 
    int len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%s|%s|%d|%d|%d|%d|%d|%d",
            name.c_str(), filename.c_str(), line, col, kind, refFileId, refLine, refCol);
    leveldb_writebatch_put(s_wb, gCharBuff0, len0, gCharBuff1, len1);

    // pos -> usr
    len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "pos2usr|%s|%d|%d", filename.c_str(),  line, col);
    len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%s", usr.c_str());
    leveldb_writebatch_put(s_wb, gCharBuff0, len0, gCharBuff1, len1);
}

void DbImplLevelDb::insert_decl_value(std::string usr, std::string filename, std::string name, int line, int col, int entityKind, int val, int isVirtual, int isDef, int typeUsrId, int typeKind, int isPointer)
{
    // usrId -> decl info
    int len0 = snprintf(gCharBuff0, sizeof(gCharBuff0), "usr2decl|%s", usr.c_str()); 
    int len1 = snprintf(gCharBuff1, sizeof(gCharBuff1), "%s|%s|%d|%d|%d|%d|%d|%d|%d|%d|%d",
            name.c_str(), filename.c_str(), line, col, entityKind, val, isVirtual, isDef, typeUsrId, typeKind, isPointer);
    leveldb_writebatch_put(s_wb, gCharBuff0, len0, gCharBuff1, len1);

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
        leveldb_put(s_dbFileList, woptions, itr->first.c_str(), itr->first.size(), s_compileUnit.c_str(), s_compileUnit.size(), &s_dbErr);
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
    //addIdList(fileMap, "id2file");
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
    leveldb_close(s_dbFileList);
    if (s_dbErr != NULL) {
        fprintf(stderr, "Close fail.\n");
    }

    leveldb_free(s_dbErr);
    s_dbErr = NULL;
}

};
