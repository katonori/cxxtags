#include "db.h"
#include <sqlite3.h>
#include <vector>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

//#define USE_PTHRED

namespace db {
static sqlite3 *db;
static std::vector<std::string > insert_list_overriden;

static clock_t time_sum0 = 0;
static clock_t time_sum1 = 0;

#ifdef USE_PTHRED
static pthread_mutex_t mutex;
#endif

void CDBMgrBase::flush()
{
    if(count) {
        arg_t arg;
        arg.bank_no = mBankNo;
        insertValueCore(&arg);
        count = 0;
    }
#ifdef USE_PTHRED
    if(mTid) {
        pthread_join(mTid, NULL);
    }
#endif
}

void CDBMgrBase::insertValueCore(void* arg)
{
    int bank_no = ((arg_t*)arg)->bank_no;
    char *err=NULL;
#ifdef USE_PTHRED
    pthread_mutex_lock(&mutex);
#endif 
    sqlite3_exec(db, mOs[bank_no].str().c_str(), NULL, NULL, &err);
#ifdef USE_PTHRED
    pthread_mutex_unlock(&mutex);
#endif
    if(err != SQLITE_OK) {
        printf("ERROR: SQLITE3: %s\n", sqlite3_errmsg(db));
    }
    mOs[bank_no].str("");
    mOs[bank_no].clear();
}

static CDBMgrRef refMgr;

static void runner_ref(void *arg)
{
    refMgr.insertValueCore(arg);
#ifdef USE_PTHRED
    pthread_exit(NULL);
#endif
}

void CDBMgrRef::insertValue(const char* usr, const char* name, const char* file_name, int32_t line, int32_t col, const char* kind, const char* ref_file_name, int ref_line, int ref_col)
{
    clock_t before = clock();
    mOs[mBankNo] << "INSERT INTO ref VALUES ('" << usr << "','" << name << "', '" << file_name
        << "', " << line << ", " << col << ", '" << kind << "', '" << ref_file_name
        << "', " << ref_line << ", " << ref_col << ");";
    count++;
    clock_t after = clock();
    time_sum0 += after - before;
    if(count == INSERT_LIST_MAX) {
#ifdef USE_PTHRED
        if(mTid) {
            pthread_join(mTid, NULL);
        }
#endif
        mArg.bank_no = mBankNo;
#ifdef USE_PTHRED
        if(pthread_create(&mTid, 
                NULL,
                (void*(*)(void*))(runner_ref),
                &mArg)) {
            printf("ERROR: pthread_create()\n");
            exit(1);
        }
#else
        runner_ref(&mArg);
#endif
        switchBank();
        count = 0;
    }
}

void insert_ref_value(const char* usr, const char* name, const char* file_name, int32_t line, int32_t col, const char* kind, const char* ref_file_name, int ref_line, int ref_col)
{
    refMgr.insertValue(usr, name, file_name, line, col, kind, ref_file_name, ref_line, ref_col);
    return ;
}

void init(std::string db_file_name, std::string src_file_name)
{
    char *err=NULL;
    if(sqlite3_open(db_file_name.c_str(), &db ) != SQLITE_OK) {
        printf("ERROR: failt to open db");
        exit(1);
    }
    // begin transaction
    sqlite3_exec(db, "BEGIN EXCLUSIVE;", NULL, NULL, NULL);
    // db_info
    sqlite3_exec(db, "CREATE TABLE db_info(db_format INTEGER, src_file_name TEXT);", NULL, NULL, &err);
    // ref
    sqlite3_exec(db, "CREATE TABLE ref(usr TEXT, name TEXT, file_name TEXT, line INTEGER, col INTEGER, kind TEXT, ref_file_name TEXT, ref_line INTEGER, ref_col INTEGER);", NULL, NULL, &err);
    // decl
    sqlite3_exec(db, "CREATE TABLE decl(usr TEXT, name TEXT, file_name TEXT, line INTEGER, col INTEGER, kind TEXT, val INTEGER, is_virtual INTEGER, is_def INTEGER);", NULL, NULL, &err);
    // overriden
    sqlite3_exec(db, "CREATE TABLE overriden(usr TEXT, name TEXT, file_name TEXT, line INTEGER, col INTEGER, kind TEXT, usr_overrider TEXT, is_def INTEGER);", NULL, NULL, &err);

    std::ostringstream os;
    os << "INSERT INTO db_info VALUES(" << DB_VER << ", '" << src_file_name << "');";
    sqlite3_exec(db, os.str().c_str(), NULL, NULL, &err);

#ifdef USE_PTHRED
    pthread_mutex_init(&mutex, NULL);
#endif
}

static CDBMgrDecl declMgr;

void insert_decl_value(const char* usr, const char* name, const char* file_name, int32_t line, int32_t col, const char* entity_kind, int val, int is_virtual, int is_def)
{
    declMgr.insertValue(usr, name, file_name, line, col, entity_kind, val, is_virtual, is_def);
}

static void runner_decl(void *arg)
{
    declMgr.insertValueCore(arg);
#ifdef USE_PTHRED
    pthread_exit(NULL);
#endif
}

void CDBMgrDecl::insertValue(const char* usr, const char* name, const char* file_name, int32_t line, int32_t col, const char* entity_kind, int val, int is_virtual, int is_def)
{
    clock_t before = clock();
    mOs[mBankNo] << "INSERT INTO decl VALUES ('" << usr << "','" << name << "', '" << file_name
        << "', " << line << ", " << col << ", '" << entity_kind << "', " << val << ", "
        << is_virtual << ", " << is_def << ");";
    clock_t after = clock();
    time_sum0 += after - before;
    count++;
    if(count == INSERT_LIST_MAX) {
#ifdef USE_PTHRED
        if(mTid) {
            pthread_join(mTid, NULL);
        }
#endif
        mArg.bank_no = mBankNo;
#ifdef USE_PTHRED
        if(pthread_create(&mTid, 
                NULL,
                (void*(*)(void*))runner_decl,
                &mArg)) {
            printf("ERROR: pthread_create()\n");
            exit(1);
        }
#else
        runner_decl(&mArg);
#endif
        switchBank();
        count = 0;
    }
}

static CDBMgrOverriden overridenMgr;

static void runner_overriden(void *arg)
{
    overridenMgr.insertValueCore(arg);
#ifdef USE_PTHRED
    pthread_exit(NULL);
#endif
}

void insert_overriden_value(const char* usr, const char* name, const char* file_name, int32_t line, int32_t col, const char* entity_kind, const char* usr_overrider, int is_def)
{
    overridenMgr.insertValue(usr, name, file_name, line, col, entity_kind, usr_overrider, is_def);
    return ;
}

void CDBMgrOverriden::insertValue(const char* usr, const char* name, const char* file_name, int32_t line, int32_t col, const char* entity_kind, const char* usr_overrider, int is_def)
{
    clock_t before = clock();
    mOs[mBankNo] << "INSERT INTO overriden VALUES ('" << usr << "','" << name << "', '" << file_name
        << "', " << line << ", " << col << ", '" << entity_kind << "', '" << usr_overrider 
        << "', " << is_def << ");";
    clock_t after = clock();
    time_sum0 += after - before;
    count++;
    if(count == INSERT_LIST_MAX) {
#ifdef USE_PTHRED
        if(mTid) {
            pthread_join(mTid, NULL);
        }
#endif
        mArg.bank_no = mBankNo;
#ifdef USE_PTHRED
        if(pthread_create(&mTid, 
                NULL,
                (void*(*)(void*))(runner_overriden),
                &mArg)) {
            printf("ERROR: pthread_create()\n");
            exit(1);
        }
#else
        runner_overriden(&mArg);
#endif
        switchBank();
        count = 0;
    }
}

void fin(void)
{
    // flush buffers
    refMgr.flush();
    declMgr.flush();
    overridenMgr.flush();

    // create indices
    sqlite3_exec(db, "CREATE INDEX ref_index0 ON ref(file_name, name, line, col);", NULL, NULL, NULL);
    sqlite3_exec(db, "CREATE INDEX ref_index1 ON ref(file_name);", NULL, NULL, NULL);
    sqlite3_exec(db, "CREATE INDEX decl_index0 ON decl(file_name, name, line, col);", NULL, NULL, NULL);
    sqlite3_exec(db, "CREATE INDEX decl_index1 ON decl(file_name)", NULL, NULL, NULL);
    // end transaction
    sqlite3_exec(db, "END TRANSACTION;", NULL, NULL, NULL);
    if(SQLITE_OK != sqlite3_close(db)) {
        fprintf(stderr, "ERROR: db couldn't close\n");
        fprintf(stderr, "%s\n", sqlite3_errmsg(db));
        exit(1);
    }
    printf("TIME0:DB: %lf\n", ((double)time_sum0)/CLOCKS_PER_SEC);
}
};
