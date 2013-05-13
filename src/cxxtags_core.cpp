#include "clang-c/Index.h"

#include <string>
#include <vector>
#include <map>

#include <stdio.h>
#include <string.h>
#include <assert.h>
#include <time.h>
#include <unistd.h>
#include "db.h"

namespace cxxtagsIndexer {
int gIsPartial = 0;
/******************************************************************************/
/* Utility functions.                                                         */
/******************************************************************************/

/** \brief Return the default parsing options. */
static inline unsigned getDefaultParsingOptions() {
  unsigned options = CXTranslationUnit_DetailedPreprocessingRecord;
  return options;
}

std::vector<std::string > gExcludeList;
std::string gExcludeListStr;
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

    std::string::size_type pos = name.find("class ");
    if(pos == 0) {
        name = name.substr(6, name.size()-6);
    }
    pos = name.rfind(":");
    if(pos != std::string::npos) {
        name = name.substr(pos+1, name.size()-(pos+1));
    }
    return name;
}

// get source file name
static std::string getCursorSourceLocation(unsigned int& line, unsigned int& column, const CXCursor& Cursor) {
  CXSourceLocation Loc = clang_getCursorLocation(Cursor);
  CXString source;
  CXFile file;
  clang_getExpansionLocation(Loc, &file, &line, &column, 0);
  source = clang_getFileName(file);
  CXString filename = clang_getFileName(file);
  if (!clang_getCString(source)) {
    clang_disposeString(source);
    clang_disposeString(filename);
    return std::string("");
  }
  else {
    std::string b = std::string(clang_getCString(filename));
    clang_disposeString(source);
    clang_disposeString(filename);
    return b;
  }
}

typedef struct {
  const char *CommentSchemaFile;
} CommentXMLValidationData;

// tables that keep allocated IDs.
class IdTbl
{
public:
    IdTbl()
    : mCurId(1)
    {
        mMap[""] = 0;
    }
    std::map<std::string, int > mMap;
    int mCurId;
    int GetId(std::string str)
    {
        // lookup map
        std::map<std::string, int >::iterator mapItr = mMap.find(str);
        if(mapItr != mMap.end()){ 
            return mapItr->second;
        }
        mMap[str] = mCurId;
        int rv = mCurId;
        mCurId++;
        return rv;
    }
    const std::map<std::string, int >& GetTbl(void) const
    {
        return mMap;
    }
};
class IdTbl *fileIdTbl;
class IdTbl *usrIdTbl;
class IdTbl *nameIdTbl;

// Table to keep which cursor types are to be tagged.
#define AVAILABLE_TABLE_MAX 1024
static char isCursorTypeAvailableTable[AVAILABLE_TABLE_MAX];
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
#undef AVAILABLE_TABLE_MAX

// get type information
static void getCXTypeInfo(CXCursor& typeCur, int& typeUsrId, int& typeKind, int& isPointer, const CXType& inType)
{
    CXType cxType = clang_getCanonicalType(inType);
    if(cxType.kind == CXType_Pointer) {
        isPointer = 1;
        cxType = clang_getPointeeType(cxType);
    }
    typeKind = cxType.kind;
    typeCur = clang_getTypeDeclaration(cxType);
    CXString cxTypeUSR = clang_getCursorUSR(typeCur);
    typeUsrId = usrIdTbl->GetId(clang_getCString(cxTypeUSR));
    clang_disposeString(cxTypeUSR);
}

static int canSkip(int isDef, const char* cUsr)
{
    if(gIsPartial) {
        if(strncmp(cUsr, "c:macro", 7) == 0) { // macro is declaration but should be processed
            return 0;
        }
        if(isDef == 0) { // is not definition
            return 1;
        }
        if(strncmp(cUsr, "c:@", 3) != 0) { // is not global symbol 
            return 1;
        }
    }
    return 0;
}

// process declarations other than function declarations.
static inline void procDecl(const CXCursor& Cursor, const char* cUsr, std::string name, std::string fileName, int line, int column, int kind, int val)
{
    int isDef = clang_isCursorDefinition(Cursor);
    if(canSkip(isDef, cUsr)) {
        return ;
    }
    int nameId = nameIdTbl->GetId(name);
    int fileId = fileIdTbl->GetId(fileName);
    int usrId = usrIdTbl->GetId(cUsr);
    // get type information
    CXCursor typeCur;
    int typeUsrId = 0;
    int isPointer = 0;
    int typeKind = 0;
    getCXTypeInfo(typeCur, typeUsrId, typeKind, isPointer, clang_getCursorType(Cursor));
    // insert to database
    db::insert_decl_value(usrId, nameId, fileId, line, column, kind, val, 0, isDef, typeUsrId, typeKind, isPointer);
}

// process declarations
static inline void procFuncDecl(const CXCursor& Cursor, const char* cUsr, std::string name, std::string fileName, int line, int column, int kind, int isVirt)
{
    int isDef = clang_isCursorDefinition(Cursor);
    if(canSkip(isDef, cUsr)) {
        return ;
    }
    int nameId = nameIdTbl->GetId(name);
    int fileId = fileIdTbl->GetId(fileName);
    int usrId = usrIdTbl->GetId(cUsr);
    // get result type information
    CXCursor typeCur;
    int typeUsrId = 0;
    int isPointer = 0;
    int typeKind = 0;
    getCXTypeInfo(typeCur, typeUsrId, typeKind, isPointer, clang_getCursorResultType(Cursor));
    // insert to database
    db::insert_decl_value(usrId, nameId, fileId, line, column, kind, 0, isVirt, isDef, typeUsrId, typeKind, isPointer);
}

// process c++ method declarations
static inline void procCXXMethodDecl(const CXCursor& Cursor, const char* cUsr, std::string name, std::string fileName, int line, int column, int kind)
{
    int isDef = clang_isCursorDefinition(Cursor);
    if(canSkip(isDef, cUsr)) {
        return ;
    }
    int fileId = fileIdTbl->GetId(fileName);
    int usrId = usrIdTbl->GetId(cUsr);
    int isVirt = clang_CXXMethod_isVirtual(Cursor);
    unsigned int numOverridden = 0;
    CXCursor *cursorOverridden;
    clang_getOverriddenCursors(Cursor, 
            &cursorOverridden,
            &numOverridden);
    int nameId = nameIdTbl->GetId(name);
    for(unsigned int i = 0; i < numOverridden; i++) {
        CXString cxRefUSR = clang_getCursorUSR(cursorOverridden[i]);
        const char *cRefUsr = clang_getCString(cxRefUSR);
        assert(cRefUsr);
        int refUsrId = usrIdTbl->GetId(cRefUsr);
        // insert information about overrides to database
        db::insert_overriden_value(refUsrId, nameId, fileId, line, column, kind, usrId, isDef);
    }
    // process as a function declaration is also done. 
    procFuncDecl(Cursor, cUsr, name, fileName, line, column, kind, isVirt);
}

// process c++ references.
static inline void procRef(const CXCursor& Cursor, std::string name, std::string fileName, int line, int column, int kind)
{
    const char* cUsr = "";
    unsigned int ref_line = 0;
    unsigned int ref_column = 0;
    int fileId = fileIdTbl->GetId(fileName);
    CXCursor refCur = clang_getCursorReferenced(Cursor);
    if (!clang_equalCursors(refCur, clang_getNullCursor())) {
        // ref_usr
        CXString cxRefUSR = clang_getCursorUSR(refCur);
        cUsr = clang_getCString(cxRefUSR);
        assert(cUsr);
        if(gIsPartial) {
            if(strncmp(cUsr, "c:@", 3) != 0) {
                return ;
            }
        }
        // refered location
        CXFile ref_file;
        CXSourceLocation ref_loc = clang_getCursorLocation(refCur);
        clang_getSpellingLocation(ref_loc, &ref_file, &ref_line, &ref_column, 0);
        int refFid = 0;
        if(ref_file) {
            CXString cxRefFileName = clang_getFileName(ref_file);
            std::string cRefFileName = clang_getCString(cxRefFileName);
            clang_disposeString(cxRefFileName);
            if(isInExcludeList(cRefFileName)) {
                return;
            }
            refFid = fileIdTbl->GetId(cRefFileName);
        }
        int refUsrId = usrIdTbl->GetId(cUsr);
        int nameId = nameIdTbl->GetId(name);
        // insert to database.
        db::insert_ref_value(refUsrId, nameId, fileId, line, column, kind, refFid, ref_line, ref_column);
        clang_disposeString(cxRefUSR);
    }
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

    int val = 0;
    switch(kind) {
        case CXCursor_EnumConstantDecl:
            // get enum constant value
            val = clang_getEnumConstantDeclValue(Cursor);
            // fall through
        case CXCursor_TypedefDecl:
        case CXCursor_TemplateTypeParameter:
        case CXCursor_FunctionTemplate:
        case CXCursor_ClassTemplate:
        case CXCursor_ClassDecl:
        case CXCursor_Namespace:
        case CXCursor_StructDecl:
        case CXCursor_UnionDecl:
        case CXCursor_VarDecl:
        case CXCursor_ParmDecl:
        case CXCursor_FieldDecl:
        case CXCursor_MacroDefinition: {
            procDecl(Cursor, cUsr, name, fileName, line, column, kind, val);
            break;
        }
        case CXCursor_CXXMethod: {
            procCXXMethodDecl(Cursor, cUsr, name, fileName, line, column, kind);
            break;
        }
        case CXCursor_FunctionDecl:
        case CXCursor_Constructor:
        case CXCursor_Destructor: {
            procFuncDecl(Cursor, cUsr, name, fileName, line, column, kind, 0);
            break;
        }
        case CXCursor_DeclRefExpr:
        case CXCursor_MemberRefExpr:
        case CXCursor_TypeRef:
        //case CXCursor_CXXBaseSpecifier:
        case CXCursor_MemberRef:
        case CXCursor_NamespaceRef:
        case CXCursor_TemplateRef:
        case CXCursor_OverloadedDeclRef:
        case CXCursor_MacroExpansion: {
            procRef(Cursor, name, fileName, line, column, kind);
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

typedef void (*PostVisitTU)(CXTranslationUnit);

static void PrintDiagnostic(const CXDiagnostic& Diagnostic) {
  CXString Msg;
  unsigned display_opts = CXDiagnostic_DisplaySourceLocation
    | CXDiagnostic_DisplayColumn | CXDiagnostic_DisplaySourceRanges
    | CXDiagnostic_DisplayOption;

  if (clang_getDiagnosticSeverity(Diagnostic) == CXDiagnostic_Ignored)
    return;

  Msg = clang_formatDiagnostic(Diagnostic, display_opts);
  fprintf(stderr, "%s\n", clang_getCString(Msg));
  clang_disposeString(Msg);
}

static void PrintDiagnosticSet(const CXDiagnosticSet& Set) {
  int i = 0, n = clang_getNumDiagnosticsInSet(Set);
  for ( ; i != n ; ++i) {
    CXDiagnostic Diag = clang_getDiagnosticInSet(Set, i);
    CXDiagnosticSet ChildDiags = clang_getChildDiagnostics(Diag);
    PrintDiagnostic(Diag);
    if (ChildDiags)
      PrintDiagnosticSet(ChildDiags);
  }  
}

static void PrintDiagnostics(CXTranslationUnit TU) {
  CXDiagnosticSet TUSet = clang_getDiagnosticSetFromTU(TU);
  PrintDiagnosticSet(TUSet);
  clang_disposeDiagnosticSet(TUSet);
}

/******************************************************************************/
/* Logic for testing traversal.                                               */
/******************************************************************************/

/* Data used by the visitors. */
typedef struct {
  CXTranslationUnit TU;
  enum CXCursorKind *Filter;
  CommentXMLValidationData ValidationData;
} VisitorData;

enum CXChildVisitResult printingVisitor(CXCursor Cursor,
                                                CXCursor Parent,
                                                CXClientData ClientData) {
  procCursor(Cursor);
  return CXChildVisit_Recurse;
}

/******************************************************************************/
/* Loading ASTs/source.                                                       */
/******************************************************************************/

static int perform_test_load(CXIndex Idx, CXTranslationUnit TU,
                             const char *prefix,
                             CXCursorVisitor Visitor,
                             PostVisitTU PV,
                             const char *CommentSchemaFile) {
  if (Visitor) {
    enum CXCursorKind *ck = NULL;
    VisitorData Data;

    Data.TU = TU;
    Data.Filter = ck;
    Data.ValidationData.CommentSchemaFile = CommentSchemaFile;
    clang_visitChildren(clang_getTranslationUnitCursor(TU), Visitor, &Data);
  }

  if (PV)
    PV(TU);

  PrintDiagnostics(TU);
  clang_disposeTranslationUnit(TU);
  return 0;
}

static int perform_test_load_source(int argc, const char **argv,
                             CXCursorVisitor Visitor,
                             PostVisitTU PV) {
  CXIndex Idx;
  CXTranslationUnit TU;
  const char *CommentSchemaFile = NULL;
  int result;
  const char *cur_dir = argv[0];
  const char *out_file_name = argv[1];
  const char *in_file_name = argv[2];
  // argv[3] is "--"
  // reorder args to pass clang
  argv[3] = argv[2];
  argv+=3;
  argc-=3;

  // Set which cursor types are to be tagged.
  setCursorTypeAvailable(CXCursor_EnumConstantDecl);
  setCursorTypeAvailable(CXCursor_TypedefDecl);
  setCursorTypeAvailable(CXCursor_ClassDecl);
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

  fileIdTbl = new IdTbl();
  usrIdTbl = new IdTbl();
  nameIdTbl = new IdTbl();

  db::init(out_file_name, in_file_name, gExcludeListStr, gIsPartial, cur_dir, argc-1, argv+1);
  
  Idx = clang_createIndex(/* excludeDeclsFromPCH */0,
                          /* displayDiagnosics=*/0);

  TU = clang_parseTranslationUnit(Idx, 0,
                                  argv,
                                  argc,
                                  0, 0, 
                                  getDefaultParsingOptions());
  if (!TU) {
    fprintf(stderr, "Unable to load translation unit!\n");
    result = 1;
    goto FUNC_END;
  }

  result = perform_test_load(Idx, TU, NULL, Visitor, PV,
                             CommentSchemaFile);
FUNC_END:
  clang_disposeIndex(Idx);
  db::fin(fileIdTbl->GetTbl(), usrIdTbl->GetTbl(), nameIdTbl->GetTbl());
  delete fileIdTbl;
  delete usrIdTbl;
  delete nameIdTbl;
  return result;
}

/******************************************************************************/
/* Command line processing.                                                   */
/******************************************************************************/
static void print_usage(void) {
  fprintf(stderr, "usage: cxxtags_core [-p] [-e excludeList] cur_dir out_file in_file -- {<clang_args>}*\n");
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
    argc--; // decrement for command name
    if (argc >= 3) {
        int c = 0;
        while((c = getopt(argc, (char*const*)argv, "e:p")) != -1) {
            switch (c) {
                case 'e':
                    gExcludeListStr = optarg;
                    gExcludeList = splitString(gExcludeListStr);
                    argc-=2;
                    break;
                case 'p':
                    gIsPartial = 1;
                    argc--;
                    break;
                case '?':
                    printf("ERROR: unknown option: -%c", optopt);
                    return 1;
                default:
                    assert(0);
            }
        }
        CXCursorVisitor I = printingVisitor;
        PostVisitTU postVisit = 0;
        if (I) {
            return perform_test_load_source(argc, &argv[optind], I,
                    postVisit);
        }
    }
    print_usage();
    return 1;
}

};

int main(int argc, const char **argv) {
  return cxxtagsIndexer::indexSource(argc, argv);
}
