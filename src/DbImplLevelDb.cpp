#include "DbImplLevelDb.h"
#include <vector>
#include <map>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>

namespace cxxtags {

#if 0
void DbImplLevelDb::tryStep(sqlite3_stmt *stmt)
{
}

void DbImplLevelDb::prepareStatement(const char* queryInsertTmpl, sqlite3_stmt **sqlStmt)
{
}

void DbImplLevelDb::finDb(sqlite3_stmt *sqlStmt)
{
}
#endif

void DbImplLevelDb::init(std::string db_file_name, std::string src_file_name, std::string excludeList, int isPartial, int isSkel, const char* curDir, int argc, const char** argv)
{
}

void DbImplLevelDb::insert_ref_value(int usrId, int nameId, int fileId, int line, int col, int kind, int refFileId, int refLine, int refCol)
{
}

void DbImplLevelDb::insert_decl_value(int usrId, int nameId, int fileId, int line, int col, int entityKind, int val, int isVirtual, int isDef, int typeUsrId, int typeKind, int isPointer)
{
}

void DbImplLevelDb::insert_overriden_value(int usrId, int nameId, int fileId, int line, int col, int entityKind, int usrIdOverrider, int isDef)
{
}

void DbImplLevelDb::insert_base_class_value(int classUsrId, int baseClassUsrId, int line, int col, int accessibility)
{
}

#if 0
void DbImplLevelDb::addIdList(const std::map<std::string, int >& inMap, std::string tableName)
{
}
#endif

void DbImplLevelDb::fin(const std::map<std::string, int >& fileMap, const std::map<std::string, int >& usrMap, const std::map<std::string, int >& nameMap)
{
}

};
