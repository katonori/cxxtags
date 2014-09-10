#ifndef _IINDEX_DB_H_
#define _IINDEX_DB_H_
#include <string>

namespace cxxtags {
class IIndexDb {
public:
    virtual int init(const std::string& db_file_name, const std::string& src_file_name, const std::string& excludeList, int isPartial, int isSkel, bool isRebuild, const char* curDir, int argc, const char** argv) = 0;
    virtual int fin(void) = 0;
    virtual int insert_ref_value(const std::string& usr, const std::string& filename, const std::string& name, int line, int col) = 0;
    virtual int insert_decl_value(const std::string& usr, const std::string& filename, const std::string& name, int line, int col, int isDef) = 0;
    virtual int insert_overriden_value(const std::string& usr, const std::string& name, const std::string& filename, int line, int col, const std::string& overriderUsr, int isDef) = 0;
    virtual int insert_base_class_value(const std::string& classUsr, const std::string& baseClassUsr, int line, int col, int accessibility) = 0;
};
};

#endif // _IINDEX_DB_H_
