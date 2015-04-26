cxxtags
=======

### CAUTION: This project is under development.

What is this?
------------------------
**cxxtags** is a tool to tag and index C/C++ source files based on clang. The major difference from ctags is
C++ syntax(ex. class, namespace, template, etc.) support and capability of generating cross reference information.

Several IDEs(Visual Studio, Eclipse, Xcode, etc.) already have this tagging(indexing) feature though, those are tightly
built-in and not portable. **cxxtags** aims to be light-weight and portable source code tagging system.

Old **cxxtags** version based on sqlite3 is moved to [https://github.com/katonori/cxxtags\_sqlite3](https://github.com/katonori/cxxtags_sqlite3)

Requirement
------------------------

* clang libs and headers
    * http://llvm.org/
* leveldb library and C/C++ headers.
    * https://code.google.com/p/leveldb/
* py-leveldb
    * Thread-safe Python bindings for LevelDB. 
    * https://code.google.com/p/py-leveldb/

**cxxtags** is developped and tested on Ubuntu 14.04, python-2.7.6 and clang(LLVM)-3.4.
But it is expected to be able to run on other Unix-like systems inluding cygwin.

How to build
------------------------

* Install the dependent libraries
* Check out the repository

        $ git clone https://github.com/katonori/cxxtags.git

* Build the project using cmake
    * Run cmake and run build. Make sure that llvm-config is in your PATH.
    * You need to specify a variable LEVELDB\_HOME when you execute cmake if libleveldb.so is not under
      the default linker search path.

            $ mkdir -p build && cd build
            $ cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=1 ../
            $ make
            $ make install
            # build the tag database
            $ ../../bin/cxxtags_run_proj _db compile_commands.json

* Install
    * Copy the contents of ${CXXTAGS\_REPOSITORY\_ROOT}/bin directory to your installation path

* See [README.cygwin.md](README.cygwin.md "") for more information for cygwin.

How to use
------------------------

### Build the database

**cxxtags** needs compile options such as "-I" "-D" to retrieve correct informations.

If your project uses cmake, You can generate tag database by steps below.

* Run cmake with `-DCMAKE_EXPORT_COMPILE_COMMANDS=1` option and build as usual. This generate a file "compile\_commands.json"
  which contains the list of built files and their build options and working directory.
* Generate the tag database of the project to directory "\_db" by cxxtags\_run\_proj

        $ cxxtags_run_proj _db compile_commands.json

Or you can also use [Bear](https://github.com/rizsotto/Bear.git) to generate the compialtion database.

For more information about the compilation database, see clang site[http://clang.llvm.org/docs/JSONCompilationDatabase.html](http://clang.llvm.org/docs/JSONCompilationDatabase.html).

### Run query to the database

To retrieve information from the database use *cxxtags_query*. 
For example, if you want to know where an item refered at line #30 and column #8 in file a.cpp is declared.
invoke these command

        # buld the database if it's not done yet
        $ cxxtags _db a.cpp
        # do a query
        $ cxxtags_query def _db a.cpp 30 8

If a.cpp is like this

```C
#include <iostream>
namespace NS0 {
    class C0 {
        public:
            void f0() { std::cout << "C0::f0\n"; }
            void f1() { std::cout << "C0::f1\n"; }
    };
    class C1 {
        public:
            void f0() { std::cout << "C1::f0\n"; }
            void f1() { std::cout << "C1::f1\n"; }
    };
};
namespace NS1 {
    class C0 {
        public:
            void f0() { std::cout << "C0::f0\n"; }
            void f1() { std::cout << "C0::f1\n"; }
    };
    class C1 {
        public:
            void f0() { std::cout << "C1::f0\n"; }
            void f1() { std::cout << "C1::f1\n"; }
    };
};

int main()
{
    NS1::C0 c0;
    c0.f1();
    return 0;
}
```

you will get output linke this.

        f1|/home/user0/devel/cxxtags/src/build/a.cpp|18|18|            void f1() { std::cout << "C0::f1\n"; }

For vim users, the wrapper plugin of *cxxtags_query* [cxxtags-vim](https://github.com/katonori/cxxtags-vim) is available.

Commands
------------------------

### cxxtags
Generates a database file.

    usage: cxxtags [-e exclude_list] database_dir input_file [compiler_arguments]

* -e  
  * Specify directories that contains source/header files that you don't want to generate the tags. Directories are separated by ':' like "/usr/include:/usr/local/include".

Compiler arguments are passed to clang. To get precise information you need to pass correct arguments just like you compile the source.

### cxxtags\_query
perform a query to the database.

    usage: cxxtags_query query_type[decl/def/ref/override/overriden] database_dir item_name file_name line_no column_no'
         : cxxtags_query query_type[name]                                 database_dir item_name'

* query\_type: Specify the type of query. Listed below are acceptable.  
    * decl: Run query information about **declared** location of a specified item.
    * def: Run query information about **defined** location of a specified item.  
    * ref: Run query information about **refered** location of a specified item. 
    * override: Run query information about items that a specified item overrides.
    * overriden: Run query information about items that is overriden by a specified item.
    * name: Search information about all items named *item\_name* in database.
* database\_dir: Database directory generated by **cxxtags** command. You can specify multiple database directory
  separated by ',' like "db0,db1,db2".
* item\_name: Specify the name of the item that you want to inspect.  
* line\_no: Specify the line number the item is located in.
* column\_no: Specify the column number the item is located in.

