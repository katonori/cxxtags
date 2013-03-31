#ifndef _DB_H_
#include <string>

namespace db {
static const int DB_VER = 4;
static const int INSERT_LIST_MAX = 255;

void init(std::string file_name);
void fin(void);

void insert_ref_value(std::string usr, std::string name, std::string file_name, int32_t line, int32_t col, std::string kind, std::string ref_file_name, int ref_line, int ref_col);
void insert_decl_value(std::string usr, std::string name, std::string file_name, int32_t line, int32_t col, std::string entity_kind, int val, int is_virtual, int is_def);
void insert_overriden_value(std::string usr, std::string name, std::string file_name, int32_t line, int32_t col, std::string entity_kind, std::string usr_overrider, int is_def);
};

#endif //#ifndef _DB_H_
