cxxtags
=======

What is this?
------------------------
**cxxtags** is a tool to tag and index C/C++ source files based on clang. The major difference from ctags is
C++ syntax(ex. class, namespace, template, etc.) support and capability of generating cross reference information.

Several IDEs(Visual Studio, Eclipse, Xcode, etc.) already have this tagging(indexing) feature though, those are tightly
built-in and not portable(even though Eclipse(CDT) is a open source project). **cxxtags** aims to be light-weight and
portable source code tagging system.

### Requirement
**cxxtags** is written in C/C++ and python and based on clang indexer and sqlite3. You need stuffs listed
below to build and run this command.

* clang libs and headers(ver >= 3.2)
* sqlite3 library and C/C++ headers.
* python with sqlite3 support(ver >=2.5)

**cxxtags** is developped and tested on Mac OS X 10.8.2, python-2.7.2 and clang(LLVM)-3.2.
But it is expected to be able to run on other Unix-like systems.

### How to build
* check out repository

        $ git clone https://github.com/katonori/cxxtags.git

* use Unix make
    * set LLVM_HOME in _${CXXTAGS_REPOSITORY_ROOT}_/src/Makefile correctly.  
    * build

              $ cd ${CXXTAGS_REPOSITORY_ROOT}/src && make

    * install

        * copy the contents of ${CXXTAGS_REPOSITORY_ROOT}/bin directory to your installation path

* use CMake
    * prepare the build directory

                $ mkdir -p build && cd build

    * run cmake specifying LLVM_HOME and build

                $ cmake -DLLVM_HOME=/pkg/llvm-3.2/ ../
                $ make
                $ make install

    * install
        * copy the contents of ${CXXTAGS_REPOSITORY_ROOT}/bin directory to your installation path

How to use
------------------------
**cxxtags** needs compile options such as "-I" "-D" to get correct information.
This is difficult in some cases. An easy way to recorde such information is to use wrapper scripts of compilers.
g++.py and gcc.py included in this package are wrapper script of **cxxtags** and compilers. This generate tag database
and run compilers. You can use this script like below


                $ env CXXTAGS_DB_DST=`pwd`/db g++.py -O a.cpp
                
or

                $ env CXXTAGS_DB_DST=`pwd`/db CXX=g++.py make

These commands generate database to the directory \`pwd\`/db. But generated database is generated with "-E" option
so you need to rebuild the database.

                $ cxxtags_db_manager rebuild `pwd`/db


To retrieve information from the database use *cxxtags_query*. 
For example, if you want to know where an item refered at line #8 and column #12 in file b.c is declared.
invoke this command

                $ cxxtags_query def db b.c 8 12

If b.c is like this


         int func()
         {
             return 1;
         }

         int main()
         {
             return func() + 1;
         }


you will get output linke this.

                func|/devel/cxxtags/src/b.c|1|5|int func()


Commands
------------------------

### cxxtags
Generates a database file.

    usage: cxxtags [-E, --empty] [-p, --partial] [-e exclude_list] [-o output_file] input_file [compiler_arguments]

* -E, --empty  
  * Only the build options which are needed to rebuild the database file are generated. This is useful to recorde the build options used in a source package.
    Of course you must rebuild the database to generate complete tag information. Use *cxxtags_db_manager* to rebuild the database.
* -p, --partial  
  * Only partial part of database is built. This option helps save disk space. File local information is not generated.
* -e  
  * Specify directories that contains source/header files that you don't want to generate the tags. Directories are separated by ':' like "/usr/include:/usr/local/include".
* -o  
  * Specify output file name. If no output file names are specified, the output file is named with suffix ".db" is used as output file name.

Compiler arguments are passed to clang. To get precise information you need to pass arguments just like you compile the source.

If some input files are or a input file named like "*.o" is passed to **cxxtags**, **cxxtags** pretend to be a linker command, 
outputs an empty file. This behavior is to be compatible with compiler commands such as g++ and clang.

### cxxtags_db_manager
Merges some database files generated by **cxxtags** to a directory. 

    usage: cxxtags_db_manager add     database_dir input_files [...]
         :                    rebuild [-f,--force] [-p,--partial] database_dir [src_file_name]

* command mode
  * add: Add specified database files to a database set.
  * rebuild: Rebuild a scpeifiled database file. All the files in database are rebuilt If no source files are specified.
* options
  * rebuild mode
    * -f, --force  
      * Force to rebuild a database. If this option is not specified, the specified database is not rebuilt if it seems to be already as you wish.
    * -p, --partial  
      * A database is rebuilt to have partial information. File local information will not be contained to the output database file.

This command updates database directory instead of replacing it if you specify database directory that already exists as *output_directory*.

For performance reason, this command delete input files. If you need input files to be remained, back it up by yourself.

### cxxtags_html_dumper

    usage: cxxtags_html_dumper database_directory

Convert tag database to html files just like htags in GNU global. This is sample tool for using tag database.
**cxxtags_html_dumper** takes the only one argument the tag database directory. This directory should be 
generated by **cxxtags_db_manager**.
**cxxtags_html_dumper** extract several information from the database and generate html files. 

### cxxtags_query
Make a query to the database.

    usage: cxxtags_query query_type[decl/def/ref/override/overriden/type] database_dir item_name file_name line_no column_no'
         : cxxtags_query query_type[name]                                 database_dir item_name [-f file_name] [-p, --partial]'

* query_type: Specify the type of query. Listed below are acceptable.  
    * decl: Query information about **declared** location of a specified item.
    * def: Query information about **defined** location of a specified item.  
    * ref: Query information about **refered** location of a specified item. 
    * override: Query information about items that a specified item overrides.
    * overriden: Query information about items that is overriden by a specified item.
    * name: Search information about all items named *item_name* in database.
    * type: Query type information of a specified item.
* database_dir: Database directory generated by **cxxtags_db_manager** command.  
* item_name: Specify the name of the item that you want to inspect.  
* line_no: line number.
* column_no: column number.
* options
    * in *name* mode
        * -f: Specify the file that contains the item.  
        * -p, --partial: Enable partial match.


Example and Other information
------------------------
* You can find some examples at _test_ directory. You can generate tag database and html files by these commands.  

        $ cd ${CXXTAGS_REPOSITORY_ROOT}/test/inheritance/
        $ make html

  then a directory _${CXXTAGS_REPOSITORY_ROOT}/test/ns/html_ is generated. 

* vim front-end for *cxxtags* is available [https://github.com/katonori/cxxtags-vim](https://github.com/katonori/cxxtags-vim).
