#include <map>
#include <string>
#include <vector>

#include <assert.h>
#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#include <clang-c/Index.h>

#include "IndexDbLevelDb.h"
#include "IIndexDb.h"

namespace cxxtags {
static bool gIsRebuild = false;
static bool gIsOmitLocal = false;
static std::string gLastClassUsr = "";
cxxtags::IIndexDb* gDb;

const char* keywordListWithSpace[] = {
    "class ",
    "enum ",
    "struct ",
    "union ",
};

#ifndef PATH_MAX
#define PATH_MAX (1024*1024)
#endif
static char s_filenameBuff[PATH_MAX];
static std::vector<std::string > gExcludeList;
static std::string gExcludeListStr;
// Table to keep which cursor types are to be tagged.
#define AVAILABLE_TABLE_MAX 1024
static char isCursorTypeAvailableTable[AVAILABLE_TABLE_MAX];

static inline void check_rv(int a) {
    assert(a == 0);
}

/** \brief Return the default parsing options. */
static inline unsigned getDefaultParsingOptions() {
  unsigned options = CXTranslationUnit_DetailedPreprocessingRecord;
  return options;
}

static inline int isInExcludeList(std::string fileName)
{
    std::vector<std::string >::iterator itrEnd = gExcludeList.end();
    for(std::vector<std::string >::iterator itr = gExcludeList.begin();
        itr != itrEnd;
        itr++) {
        if(fileName.find(*itr) == 0) {
            return 1;
        }
    }
    return 0;
}

static inline std::string getName(const CXCursor& C)
{
    //CXString cxName = clang_getCursorDisplayName(C);
    CXString cxName = clang_getCursorSpelling(C);
    const char* cName = clang_getCString(cxName);
    std::string name = std::string(cName);
    clang_disposeString(cxName);
    return name;
}


static inline std::string formatName(std::string name)
{
    std::string::size_type pos;
    for(unsigned i = 0; i < sizeof(keywordListWithSpace)/sizeof(keywordListWithSpace[0]); ++i) {
        std::string kw = keywordListWithSpace[i];
        pos = name.find(kw);
        if(pos == 0) {
            name = name.substr(kw.size(), name.size()-kw.size());
            break;
        }
    }
    pos = name.rfind(":");
    if(pos != std::string::npos) {
        name = name.substr(pos+1, name.size()-(pos+1));
    }
    return name;
}

// get source file name
static std::string getCursorSourceLocation(unsigned int& line, unsigned int& column, const CXCursor& Cursor) {
    std::string filename = "";
    CXSourceLocation Loc = clang_getCursorLocation(Cursor);
    CXFile file;
    clang_getSpellingLocation(Loc, &file, &line, &column, 0);
    CXString fn = clang_getFileName(file);
    if (!clang_getCString(fn)) {
        clang_disposeString(fn);
    }
    else {
        std::string str = std::string(clang_getCString(fn));
        clang_disposeString(fn);
        filename = str;
    }
    // convert to absolute path
    if(filename != "") {
        char* p = realpath(filename.c_str(), s_filenameBuff);
        if(p != s_filenameBuff) {
            printf("ERROR: realpath: %s, %p\n", filename.c_str(), p);
        }
        filename = std::string(s_filenameBuff);
    }
    return filename;
}

static inline void setCursorTypeAvailable(int val)
{
    assert(val < AVAILABLE_TABLE_MAX); 
    isCursorTypeAvailableTable[val] = 1;
}
static inline char isCursorTypeAvailable(int val)
{
    assert(val < AVAILABLE_TABLE_MAX); 
    return isCursorTypeAvailableTable[val];
}

static bool isLocal(const std::string& usr, const CXCursor& cursor)
{
    if((cursor.kind == CXCursor_VarDecl || cursor.kind == CXCursor_ParmDecl)
            && (usr.find("c:@") != 0 && usr.find("c:macro") != 0)) {
        CXCursor parentCur = clang_getCursorLexicalParent(cursor);
        if(parentCur.kind == CXCursor_FunctionDecl
            || parentCur.kind == CXCursor_CXXMethod
            || parentCur.kind == CXCursor_Constructor
            || parentCur.kind == CXCursor_Destructor) {
            //printf("OMIT: %s\n", usr.c_str());
            return true;
        }
    }
    return false;
}

// process declarations other than function declarations.
static inline void procDecl(const CXCursor& Cursor, const char* cUsr, std::string name, std::string fileName, int line, int column)
{
    if(!gIsOmitLocal || !isLocal(cUsr, Cursor)) {
        int isDef = clang_isCursorDefinition(Cursor);
        // insert to database
        check_rv(gDb->insert_decl_value(cUsr, fileName, name, line, column, isDef));
    }
}

// process declarations
static inline void procFuncDecl(const CXCursor& Cursor, const char* cUsr, std::string name, std::string fileName, int line, int column)
{
    int isDef = clang_isCursorDefinition(Cursor);
    // insert to database
    check_rv(gDb->insert_decl_value(cUsr, fileName, name, line, column, isDef));
}

// process c++ method declarations
static inline void procCXXMethodDecl(const CXCursor& Cursor, const char* cUsr, std::string name, std::string fileName, int line, int column)
{
    unsigned int numOverridden = 0;
    CXCursor *cursorOverridden;
    clang_getOverriddenCursors(Cursor, 
            &cursorOverridden,
            &numOverridden);
    for(unsigned int i = 0; i < numOverridden; i++) {
        CXString cxRefUSR = clang_getCursorUSR(cursorOverridden[i]);
        const char *cRefUsr = clang_getCString(cxRefUSR);
        assert(cRefUsr);
        int isDef = clang_isCursorDefinition(Cursor);
        // insert information about overrides to database
        check_rv(gDb->insert_overriden_value(cRefUsr, name, fileName, line, column, cUsr, isDef));
    }
    //int isVirt = clang_CXXMethod_isVirtual(Cursor);
    clang_disposeOverriddenCursors(cursorOverridden);
    // process as a function declaration is also done. 
    procFuncDecl(Cursor, cUsr, name, fileName, line, column);
}

// process c++ references.
static inline void procRef(const CXCursor& Cursor, std::string name, std::string fileName, int line, int column)
{
    const char* cUsr = nullptr;
    CXCursor refCur = clang_getCursorReferenced(Cursor);
    std::string cRefFileName;
    if (!clang_equalCursors(refCur, clang_getNullCursor())) {
        // ref_usr
        CXString cxRefUSR = clang_getCursorUSR(refCur);
        cUsr = clang_getCString(cxRefUSR);
        std::string usr(cUsr);
        assert(cUsr);
        if(gIsOmitLocal && isLocal(cUsr, refCur)) {
            return ;
        }
        // insert to database.
        check_rv(gDb->insert_ref_value(cUsr, fileName, name, line, column));
        clang_disposeString(cxRefUSR);
    }
    return ;
}

// process c++ base class informations
static inline void procCXXBaseClassInfo(const CXCursor& Cursor, std::string name, std::string fileName, int line, int column)
{
    // USR of class
    CXString cxBaseUsr = clang_getCursorUSR(Cursor);
    const char* cBaseUsr = clang_getCString(cxBaseUsr);
    // USR of base class
    CXCursor refCur = clang_getCursorReferenced(Cursor);
    cxBaseUsr = clang_getCursorUSR(refCur);
    cBaseUsr = clang_getCString(cxBaseUsr);
    int accessibility = clang_getCXXAccessSpecifier(Cursor);
    // insert to database
    check_rv(gDb->insert_base_class_value(gLastClassUsr, cBaseUsr, line, column, accessibility));
    clang_disposeString(cxBaseUsr);
}

static inline void procCursor(const CXCursor& Cursor) {
    CXCursorKind kind = Cursor.kind;
    if (!clang_isInvalid(kind)) {
        if(isCursorTypeAvailable(kind) == 0) {
            return;
        }
        unsigned int line = 0;
        unsigned int column = 0;

        // file_name
        std::string fileName = getCursorSourceLocation(line, column, Cursor);
        // decide if this Cursor info is to be registered to db.
        if(isInExcludeList(fileName)) {
            return;
        }
        // name
        std::string name = getName(Cursor);
        if(name == "") {
            return;
        }
        name = formatName(name);
        // usr
        CXString cxUSR = clang_getCursorUSR(Cursor);
        const char *cUsr = clang_getCString(cxUSR);
        assert(cUsr);

        //int val = 0;
        switch(kind) {
            case CXCursor_EnumConstantDecl:
                // get enum constant value
                //val = clang_getEnumConstantDeclValue(Cursor);
                // fall through
            case CXCursor_TypedefDecl:
            case CXCursor_TemplateTypeParameter:
            case CXCursor_FunctionTemplate:
            case CXCursor_ClassTemplate:
            case CXCursor_Namespace:
            case CXCursor_UnionDecl:
            case CXCursor_FieldDecl:
            case CXCursor_VarDecl:
            case CXCursor_ParmDecl:
            case CXCursor_MacroDefinition: {
                procDecl(Cursor, cUsr, name, fileName, line, column);
                break;
            }
            case CXCursor_StructDecl:
            case CXCursor_ClassDecl:
            case CXCursor_EnumDecl: {
                gLastClassUsr = cUsr;
                procDecl(Cursor, cUsr, name, fileName, line, column);
                break;
            }
            case CXCursor_CXXMethod: {
                procCXXMethodDecl(Cursor, cUsr, name, fileName, line, column);
                break;
            }
            case CXCursor_FunctionDecl:
            case CXCursor_Constructor:
            case CXCursor_Destructor: {
                procFuncDecl(Cursor, cUsr, name, fileName, line, column);
                break;
            }
            case CXCursor_CXXBaseSpecifier: {
                procCXXBaseClassInfo(Cursor, name, fileName, line, column);
                break;
            }
            case CXCursor_DeclRefExpr:
            case CXCursor_MemberRefExpr:
            case CXCursor_TypeRef:
            case CXCursor_MemberRef:
            case CXCursor_NamespaceRef:
            case CXCursor_TemplateRef:
            case CXCursor_OverloadedDeclRef:
            case CXCursor_MacroExpansion: {
                procRef(Cursor, name, fileName, line, column);
                break;
            }
            // TODO:
            case CXCursor_InclusionDirective:
                break;
            default:
                assert(0);
                break;
        }
        clang_disposeString(cxUSR);
    }
    return;
}

/******************************************************************************/
/* Callbacks.                                                                 */
/******************************************************************************/

static int printDiagnostic(const CXDiagnostic& Diagnostic) {
    int rv = 0;
    CXString Msg;
    unsigned display_opts = CXDiagnostic_DisplaySourceLocation
        | CXDiagnostic_DisplayColumn | CXDiagnostic_DisplaySourceRanges
        | CXDiagnostic_DisplayOption;

    int severity = clang_getDiagnosticSeverity(Diagnostic);
    if (severity == CXDiagnostic_Ignored) {
        return 0;
    }
    if (severity == CXDiagnostic_Error || severity == CXDiagnostic_Fatal) {
        rv = 1;
    }

    Msg = clang_formatDiagnostic(Diagnostic, display_opts);
    fprintf(stderr, "%s\n", clang_getCString(Msg));
    clang_disposeString(Msg);

    return rv;
}

static int printDiagnosticSet(const CXDiagnosticSet& Set) {
    int rv = 0;
    int n = clang_getNumDiagnosticsInSet(Set);
    for (int i = 0; i < n ; ++i) {
        CXDiagnostic Diag = clang_getDiagnosticInSet(Set, i);
        CXDiagnosticSet ChildDiags = clang_getChildDiagnostics(Diag);
        if(printDiagnostic(Diag)) {
            rv = 1;
        }
        if (ChildDiags) {
            printDiagnosticSet(ChildDiags);
        }
    }  
    return rv;
}

static int printDiagnostics(CXTranslationUnit TU) {
    CXDiagnosticSet TUSet = clang_getDiagnosticSetFromTU(TU);
    int rv = printDiagnosticSet(TUSet);
    clang_disposeDiagnosticSet(TUSet);
    return rv;
}

/******************************************************************************/
/* Logic for testing traversal.                                               */
/******************************************************************************/

static enum CXChildVisitResult visitorFunc(CXCursor Cursor,
        CXCursor Parent,
        CXClientData ClientData) {
    procCursor(Cursor);
    return CXChildVisit_Recurse;
}

/******************************************************************************/
/* Loading ASTs/source.                                                       */
/******************************************************************************/

static int performIndexing(const char* cur_dir, const char* out_dir, const char* in_file_name, int argc, const char **argv) {
    int result;

    // Set which cursor types are to be tagged.
    setCursorTypeAvailable(CXCursor_EnumConstantDecl);
    setCursorTypeAvailable(CXCursor_TypedefDecl);
    setCursorTypeAvailable(CXCursor_ClassDecl);
    setCursorTypeAvailable(CXCursor_EnumDecl);
    setCursorTypeAvailable(CXCursor_Namespace);
    setCursorTypeAvailable(CXCursor_StructDecl);
    setCursorTypeAvailable(CXCursor_UnionDecl);
    setCursorTypeAvailable(CXCursor_VarDecl);
    setCursorTypeAvailable(CXCursor_ParmDecl);
    setCursorTypeAvailable(CXCursor_FieldDecl);
    setCursorTypeAvailable(CXCursor_MacroDefinition);
    setCursorTypeAvailable(CXCursor_CXXMethod);
    setCursorTypeAvailable(CXCursor_FunctionDecl);
    setCursorTypeAvailable(CXCursor_Constructor);
    setCursorTypeAvailable(CXCursor_Destructor);
    setCursorTypeAvailable(CXCursor_DeclRefExpr);
    setCursorTypeAvailable(CXCursor_MemberRefExpr);
    setCursorTypeAvailable(CXCursor_TypeRef);
    setCursorTypeAvailable(CXCursor_MemberRef);
    setCursorTypeAvailable(CXCursor_NamespaceRef);
    setCursorTypeAvailable(CXCursor_MacroExpansion);
    setCursorTypeAvailable(CXCursor_TemplateTypeParameter);
    setCursorTypeAvailable(CXCursor_FunctionTemplate);
    setCursorTypeAvailable(CXCursor_ClassTemplate);
    setCursorTypeAvailable(CXCursor_TemplateRef);
    setCursorTypeAvailable(CXCursor_OverloadedDeclRef);
    setCursorTypeAvailable(CXCursor_CXXBaseSpecifier);

    gDb = new cxxtags::IndexDbLevelDb();
    check_rv(gDb->init(out_dir, in_file_name, gExcludeListStr, gIsRebuild, cur_dir, argc, argv));

    CXIndex Idx = clang_createIndex(/* excludeDeclsFromPCH */0,
            /* displayDiagnosics=*/0);

    CXTranslationUnit TU = clang_parseTranslationUnit(Idx, in_file_name,
            argv,
            argc,
            0, 0, 
            getDefaultParsingOptions());
    if (!TU) {
        fprintf(stderr, "Unable to load translation unit!\n");
        result = 1;
        goto FUNC_END;
    }

    clang_visitChildren(clang_getTranslationUnitCursor(TU), visitorFunc, NULL);

    result = printDiagnostics(TU);
    clang_disposeTranslationUnit(TU);

FUNC_END:
    if(Idx) {
        clang_disposeIndex(Idx);
    }
    check_rv(gDb->fin());
    return result;
}

/******************************************************************************/
/* Command line processing.                                                   */
/******************************************************************************/
static void print_usage(void) {
    fprintf(stderr, "usage: cxxtags_core [-psE] [-e excludeList] cur_dir out_dir in_file -- {<clang_args>}*\n");
}

static std::vector<std::string > splitString(std::string str)
{
    std::vector<std::string > list;
    std::string::size_type pos = 0;
    while((pos = str.find(":")) != std::string::npos) {
        std::string s = str.substr(0, pos);
        list.push_back(s);
        if(pos == str.size()-1) {
            str = "";
            break;
        }
        str = str.substr(pos+1, str.size()-(pos+1));
    }
    if(str != "") {
        list.push_back(str);
    }
    return list;
}

static int indexSource(int argc, const char **argv) {
    //clang_enableStackTraces();
    argv++; // increment for command name
    argc--; // decrement for command name
    if (argc < 3) {
        print_usage();
        return 1;
    }

    while(argc) {
        if(strncmp(*argv, "-e", 2) == 0) { 
            gExcludeListStr = argv[1];
            gExcludeList = splitString(gExcludeListStr);
            argv+=2;
            argc-=2;
        }
        else if(strncmp(*argv, "-p", 2) == 0) {
            gIsOmitLocal = true;
            argv++;
            argc--;
        }
        else if(strncmp(*argv, "-f", 2) == 0) {
            gIsRebuild = true;
            argv++;
            argc--;
        }
        else {
            break;
        }
    }
    const char *cur_dir = argv[0];
    const char *out_dir = argv[1];
    const char *in_file_name = argv[2];
    // increment argv to pass clang
    argv+=3;
    argc-=3;
    return performIndexing(cur_dir, out_dir, in_file_name, argc, argv);
}

};

int main(int argc, const char **argv) {
    return cxxtags::indexSource(argc, argv);
}
