#ifndef _DB_H_
#include <string>
#include <stdint.h>
#include <sstream>

namespace db {
static const int DB_VER = 5;
static const int INSERT_LIST_MAX = 1023;

void init(std::string db_file_name, std::string src_file_name);
void fin(void);

void insert_ref_value(const char* usr, const char* name, const char* file_name, int32_t line, int32_t col, const char* kind, const char* ref_file_name, int ref_line, int ref_col);
void insert_decl_value(const char* usr, const char* name, const char* file_name, int32_t line, int32_t col, const char* entity_kind, int val, int is_virtual, int is_def);
void insert_overriden_value(const char* usr, const char* name, const char* file_name, int32_t line, int32_t col, const char* entity_kind, const char* usr_overrider, int is_def);

struct arg_t {
    arg_t()
        : bank_no(0)
    {}
    int bank_no;
};

class CDBMgrBase {
public:
    CDBMgrBase(const char* name)
        : mBankNo(0), mTblName(name), count(0)
    {}
    arg_t mArg;
    pthread_t mTid;
    int mBankNo;
    const char *mTblName;
    int count;
    std::ostringstream mOs[2];
    inline void switchBank()
    {
        mBankNo = mBankNo ? 0 : 1;
    }

    void insertValueCore(void* arg);
    void flush();
};

class CDBMgrRef
    : public CDBMgrBase {
public:
    CDBMgrRef()
        : CDBMgrBase("ref")
    {}
    void insertValue(const char* usr, const char* name, const char* file_name, int32_t line, int32_t col, const char* kind, const char* ref_file_name, int ref_line, int ref_col);
};

class CDBMgrDecl
    : public CDBMgrBase {
public:
    CDBMgrDecl()
        : CDBMgrBase("decl")
    {}
    void insertValue(const char* usr, const char* name, const char* file_name, int32_t line, int32_t col, const char* entity_kind, int val, int is_virtual, int is_def);
};

class CDBMgrOverriden
    : public CDBMgrBase {
public:
    CDBMgrOverriden()
        : CDBMgrBase("overriden")
    {}
    void insertValue(const char* usr, const char* name, const char* file_name, int32_t line, int32_t col, const char* entity_kind, const char* usr_overrider, int is_def);
};

};

#endif //#ifndef _DB_H_
