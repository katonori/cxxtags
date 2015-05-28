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

#define FUNCTION_TABLE_NUM (1024)
static void (*cursorFunctionTable[FUNCTION_TABLE_NUM])(const CXCursor& Cursor);

#ifndef PATH_MAX
#define PATH_MAX (1024*1024)
#endif
static char s_filenameBuff[PATH_MAX];
static std::vector<std::string > gExcludeList;
static std::string gExcludeListStr;
// Table to keep which cursor types are to be tagged.

static inline void check_rv(int a)
{
    assert(a == 0);
}

/** \brief Return the default parsing options. */
static inline unsigned getDefaultParsingOptions()
{
  unsigned options = CXTranslationUnit_DetailedPreprocessingRecord;
  return options;
}

static inline int isInExcludeList(const std::string& fileName)
{
    for(const auto& itr : gExcludeList) {
        if(fileName.find(itr) == 0) {
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

static inline std::string formatName(const std::string& name)
{
    std::string nameWork(name);
    std::string::size_type pos;
    for(unsigned i = 0; i < sizeof(keywordListWithSpace)/sizeof(keywordListWithSpace[0]); ++i) {
        std::string kw = keywordListWithSpace[i];
        pos = nameWork.find(kw);
        if(pos == 0) {
            nameWork = nameWork.substr(kw.size(), nameWork.size()-kw.size());
            break;
        }
    }
    pos = nameWork.rfind(":");
    if(pos != std::string::npos) {
        nameWork = nameWork.substr(pos+1, nameWork.size()-(pos+1));
    }
    return nameWork;
}

// get source file name
static std::string getCursorSourceLocation(unsigned int& line, unsigned int& column, const CXCursor& Cursor)
{
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

static inline int procCommon(unsigned int& line, unsigned int& column, std::string& fileName, std::string& name, const CXCursor& Cursor)
{
    // file_name
    fileName = getCursorSourceLocation(line, column, Cursor);
    // decide if this Cursor info is to be registered to db.
    if(isInExcludeList(fileName)) {
        return 1;
    }
    // name
    name = getName(Cursor);
    if(name == "") {
        return 1;
    }
    name = formatName(name);

    return 0;
}

// process declarations other than function declarations.
static inline void procDecl(const CXCursor& Cursor)
{
    unsigned int line = 0;
    unsigned int column = 0;
    std::string fileName;
    std::string name;
    if(procCommon(line, column, fileName, name, Cursor) != 0) {
        return;
    }

    CXString cxUSR = clang_getCursorUSR(Cursor);
    const char *cUsr = clang_getCString(cxUSR);
    assert(cUsr);

    if(!gIsOmitLocal || !isLocal(cUsr, Cursor)) {
        int isDef = clang_isCursorDefinition(Cursor);
        // insert to database
        check_rv(gDb->insert_decl_value(cUsr, fileName, name, line, column, isDef));
    }
    clang_disposeString(cxUSR);
}

// process declarations
static inline void procFuncDecl(const CXCursor& Cursor)
{
    unsigned int line = 0;
    unsigned int column = 0;
    std::string fileName;
    std::string name;
    if(procCommon(line, column, fileName, name, Cursor) != 0) {
        return;
    }

    CXString cxUSR = clang_getCursorUSR(Cursor);
    const char *cUsr = clang_getCString(cxUSR);
    assert(cUsr);

    int isDef = clang_isCursorDefinition(Cursor);
    // insert to database
    check_rv(gDb->insert_decl_value(cUsr, fileName, name, line, column, isDef));
    clang_disposeString(cxUSR);
}

// process c++ method declarations
static inline void procCXXMethodDecl(const CXCursor& Cursor)
{
    unsigned int line = 0;
    unsigned int column = 0;
    std::string fileName;
    std::string name;
    if(procCommon(line, column, fileName, name, Cursor) != 0) {
        return;
    }

    CXString cxUSR = clang_getCursorUSR(Cursor);
    const char *cUsr = clang_getCString(cxUSR);
    assert(cUsr);

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
    procFuncDecl(Cursor);
    clang_disposeString(cxUSR);
}

// process c++ references.
static inline void procRef(const CXCursor& Cursor)
{
    unsigned int line = 0;
    unsigned int column = 0;
    std::string fileName;
    std::string name;
    if(procCommon(line, column, fileName, name, Cursor) != 0) {
        return;
    }

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

static inline void procIncludsion(const CXCursor& Cursor)
{
    unsigned int line = 0;
    unsigned int column = 0;
    std::string fileName;
    std::string name;
    if(procCommon(line, column, fileName, name, Cursor) != 0) {
        return;
    }
    CXFile File = clang_getIncludedFile(Cursor);
    CXString Included = clang_getFileName(File);
    const char* includedFilename = clang_getCString(Included);
    if(includedFilename != nullptr) {
        check_rv(gDb->insert_inclusion(fileName, includedFilename, line));
    }
    clang_disposeString(Included);

    return ;
}

// process c++ base class informations
#if 0
static inline void procCXXBaseClassInfo(const CXCursor& Cursor, const char* cUsr, std::string name, std::string fileName, int line, int column)
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
#endif

static inline void procCursor(const CXCursor& Cursor)
{
    CXCursorKind kind = Cursor.kind;
    if(!clang_isInvalid(kind) && cursorFunctionTable[kind]) {
        cursorFunctionTable[kind](Cursor);
    }
    return;
}

#ifdef USE_CLANG_INDEX_SOURCE
static void indexDeclaration(CXClientData client_data, const CXIdxDeclInfo* decl)
{
    //printf("USR: %s, %s\n", decl->entityInfo->USR, decl->entityInfo->name);
    procCursor(decl->cursor);
}

static void indexEntityReference(CXClientData client_data, const CXIdxEntityRefInfo* ref)
{
    unsigned int line = 0;
    unsigned int column = 0; 
    clang_indexLoc_getFileLocation(ref->loc,
            NULL,
            NULL,
            &line,
            &column,
            NULL);
    procCursor(ref->cursor);
}
#else

/******************************************************************************/
/* Callbacks.                                                                 */
/******************************************************************************/

static int printDiagnostic(const CXDiagnostic& Diagnostic)
{
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

static int printDiagnosticSet(const CXDiagnosticSet& Set)
{
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

static int printDiagnostics(CXTranslationUnit TU)
{
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
#endif

inline static void setFunctionForCursorKind(int kind, void (*func)(const CXCursor& Cursor))
{
    cursorFunctionTable[kind] = func;
    assert(kind < FUNCTION_TABLE_NUM);
}

static int performIndexing(const char* cur_dir, const char* out_dir, const char* in_file_name, int argc, const char **argv)
{
    int result;

    memset(cursorFunctionTable, 0, sizeof(cursorFunctionTable));

    // Set which cursor types are to be tagged.
    setFunctionForCursorKind(CXCursor_EnumConstantDecl,       procDecl);
    setFunctionForCursorKind(CXCursor_TypedefDecl,            procDecl);
    setFunctionForCursorKind(CXCursor_ClassDecl,              procDecl);
    setFunctionForCursorKind(CXCursor_EnumDecl,               procDecl);
    setFunctionForCursorKind(CXCursor_Namespace,              procDecl);
    setFunctionForCursorKind(CXCursor_NamespaceAlias,         procDecl);
    setFunctionForCursorKind(CXCursor_StructDecl,             procDecl);
    setFunctionForCursorKind(CXCursor_UnionDecl,              procDecl);
    setFunctionForCursorKind(CXCursor_VarDecl,                procDecl);
    setFunctionForCursorKind(CXCursor_ParmDecl,               procDecl);
    setFunctionForCursorKind(CXCursor_FieldDecl,              procDecl);
    setFunctionForCursorKind(CXCursor_MacroDefinition,        procDecl);
    setFunctionForCursorKind(CXCursor_ClassTemplate,          procDecl);
    setFunctionForCursorKind(CXCursor_FunctionTemplate,       procDecl);
    setFunctionForCursorKind(CXCursor_CXXMethod,              procCXXMethodDecl);
    setFunctionForCursorKind(CXCursor_FunctionDecl,           procFuncDecl);
    setFunctionForCursorKind(CXCursor_Constructor,            procFuncDecl);
    setFunctionForCursorKind(CXCursor_Destructor,             procFuncDecl);
    setFunctionForCursorKind(CXCursor_DeclRefExpr,            procRef);
    setFunctionForCursorKind(CXCursor_MemberRefExpr,          procRef);
    setFunctionForCursorKind(CXCursor_TypeRef,                procRef);
    setFunctionForCursorKind(CXCursor_MemberRef,              procRef);
    setFunctionForCursorKind(CXCursor_NamespaceRef,           procRef);
    setFunctionForCursorKind(CXCursor_MacroExpansion,         procRef);
    setFunctionForCursorKind(CXCursor_TemplateTypeParameter,  procRef);
    setFunctionForCursorKind(CXCursor_TemplateRef,            procRef);
    setFunctionForCursorKind(CXCursor_OverloadedDeclRef,      procRef);
    setFunctionForCursorKind(CXCursor_InclusionDirective,     procIncludsion);
    //setFunctionForCursorKind(CXCursor_CXXBaseSpecifier] = 0;

    gDb = new cxxtags::IndexDbLevelDb();
    check_rv(gDb->initialize(out_dir, in_file_name, gExcludeListStr, gIsRebuild, cur_dir, argc, argv));

    CXIndex Idx = clang_createIndex(/* excludeDeclsFromPCH */0,
            /* displayDiagnosics=*/0);
#ifdef USE_CLANG_INDEX_SOURCE
    CXIndexAction action = clang_IndexAction_create(Idx);

    IndexerCallbacks callbacks;
    callbacks.abortQuery = 0;
    callbacks.diagnostic = 0;
    callbacks.enteredMainFile = 0;
    callbacks.ppIncludedFile = 0;
    callbacks.importedASTFile = 0;
    callbacks.startedTranslationUnit = 0;
    callbacks.indexDeclaration = indexDeclaration;
    callbacks.indexEntityReference = indexEntityReference;
      
    int rv = clang_indexSourceFile(
            action,
            NULL,
            &callbacks,
            sizeof(callbacks),
            CXIndexOpt_IndexFunctionLocalSymbols  |
            CXIndexOpt_SuppressWarnings,
            //0,
            in_file_name,
            argv,
            argc,
            NULL,
            0,
            NULL,
            getDefaultParsingOptions()
            );
    if (rv != 0) {
        fprintf(stderr, "Unable to load translation unit!\n");
        result = 1;
        goto FUNC_END;
    }
    else {
        result = 0;
    }
#else
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
#endif

FUNC_END:
    if(Idx) {
        clang_disposeIndex(Idx);
    }
    check_rv(gDb->finalize());
    delete gDb;
    return result;
}

/******************************************************************************/
/* Command line processing.                                                   */
/******************************************************************************/
static void print_usage(void)
{
    fprintf(stderr, "usage: cxxtags_core [-psE] [-e excludeList] cur_dir out_dir in_file -- {<clang_args>}*\n");
}

static void splitString(std::vector<std::string >& out, std::string str)
{
    std::string::size_type pos = 0;
    while((pos = str.find(":")) != std::string::npos) {
        std::string s = str.substr(0, pos);
        out.push_back(s);
        if(pos == str.size()-1) {
            str = "";
            break;
        }
        str = str.substr(pos+1, str.size()-(pos+1));
    }
    if(str != "") {
        out.push_back(str);
    }
}

static int indexSource(int argc, const char **argv)
{
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
            splitString(gExcludeList, gExcludeListStr);
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
