#pragma once
#include <string>

namespace cxxtags {
class IIndexDb {
public:
    virtual int initialize(const std::string& db_file_name, const std::string& src_file_name, const std::string& excludeList, bool isRebuild, const char* curDir, int argc, const char** argv) = 0;
    virtual int finalize(void) = 0;
    virtual int insert_ref_value(const std::string& usr, const std::string& filename, const std::string& name, int line, int col) = 0;
    virtual int insert_decl_value(const std::string& usr, const std::string& filename, const std::string& name, int line, int col, int isDef) = 0;
    virtual int insert_overriden_value(const std::string& usr, const std::string& name, const std::string& filename, int line, int col, const std::string& overriderUsr, int isDef) = 0;
    virtual int insert_base_class_value(const std::string& classUsr, const std::string& baseClassUsr, int line, int col, int accessibility) = 0;
    virtual int insert_inclusion(const std::string& filename, const std::string& includedFilename, int line) = 0;
    virtual ~IIndexDb() {};
};
};
