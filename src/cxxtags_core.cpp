#include "clang-c/Index.h"

#include <string>
#include <vector>
#include <map>

#include <stdio.h>
#include <string.h>
#include <assert.h>
#include <time.h>
#include <unistd.h>
#include <getopt.h>
#include "db.h"

namespace cxxtagsIndexer {
static int gIsPartial = 0;
static int gIsEmpty = 0;
static std::string gLastClassUsr = "";
cxxtags::IndexDb* gDb;
/******************************************************************************/
/* Utility functions.                                                         */
/******************************************************************************/

/** \brief Return the default parsing options. */
static inline unsigned getDefaultParsingOptions() {
  unsigned options = CXTranslationUnit_DetailedPreprocessingRecord;
  return options;
}

static std::vector<std::string > gExcludeList;
static std::string gExcludeListStr;
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
  CXFile file;
  clang_getExpansionLocation(Loc, &file, &line, &column, 0);
  CXString filename = clang_getFileName(file);
  if (!clang_getCString(filename)) {
    clang_disposeString(filename);
    return std::string("");
  }
  else {
    std::string b = std::string(clang_getCString(filename));
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
static IdTbl *fileIdTbl;
static IdTbl *usrIdTbl;
static IdTbl *nameIdTbl;

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

static bool isBuiltinType(int typeKind)
{
    switch(typeKind) {
        case CXType_Bool: 
        case CXType_Char_U:
        case CXType_UChar:
        case CXType_Char16:
        case CXType_Char32:
        case CXType_UShort:
        case CXType_UInt:
        case CXType_ULong:
        case CXType_ULongLong:
        case CXType_UInt128:
        case CXType_Char_S:
        case CXType_SChar:
        case CXType_WChar:
        case CXType_Short:
        case CXType_Int:
        case CXType_Long:
        case CXType_LongLong:
        case CXType_Int128:
        case CXType_Float:
        case CXType_Double:
        case CXType_LongDouble:
            return true;
        default:
            return false;
    }
    return false;
}

static bool isLocalDecl(CXCursorKind parentKind)
{
    switch(parentKind) {
        case CXCursor_FunctionDecl: 
        case CXCursor_ParmDecl:
            return true;
        default:
            return false;
    }
    return false;
}

// process declarations other than function declarations.
static inline void procDecl(const CXCursor& Cursor, const char* cUsr, std::string name, std::string fileName, int line, int column, int kind, int val)
{
    int isDef = clang_isCursorDefinition(Cursor);
    int nameId = nameIdTbl->GetId(name);
    int fileId = fileIdTbl->GetId(fileName);
    int usrId = usrIdTbl->GetId(cUsr);
    // get type information
    CXCursor typeCur;
    int typeUsrId = 0;
    int isPointer = 0;
    int typeKind = 0;
    CXType curTypeOrig = clang_getCursorType(Cursor);

    getCXTypeInfo(typeCur, typeUsrId, typeKind, isPointer, curTypeOrig);
    //printf("decl: %s: %s, %s, %d, %d, kind=%d, typeKind=%d, typeKind2=%d\n", cUsr, name.c_str(), fileName.c_str(), line, column, kind, curTypeOrig.kind, typeKind);
    //
    // if the option '-p' is specified
    // 
    if(gIsPartial) {
        CXCursor parentCur = clang_getCursorSemanticParent(Cursor);
        if(curTypeOrig.kind == CXType_LValueReference) {
            curTypeOrig = clang_getPointeeType(curTypeOrig);
        }
        while(curTypeOrig.kind == CXType_Pointer) {
            curTypeOrig = clang_getPointeeType(curTypeOrig);
        }
        //printf("%s, %s, %d, %d, parent=%d, type=%d, cursorKind=%d\n", fileName.c_str(), name.c_str(), line, column, parentCur.kind, curTypeOrig.kind, Cursor.kind);
        // type is canonical && scope is function internal then skip
        if(isBuiltinType(curTypeOrig.kind) && isLocalDecl(parentCur.kind)) {
            return;
        }
    }
    // insert to database
    gDb->insert_decl_value(usrId, nameId, fileId, line, column, kind, val, 0, isDef, typeUsrId, typeKind, isPointer);
}

// process declarations
static inline void procFuncDecl(const CXCursor& Cursor, const char* cUsr, std::string name, std::string fileName, int line, int column, int kind, int isVirt)
{
    int isDef = clang_isCursorDefinition(Cursor);
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
    gDb->insert_decl_value(usrId, nameId, fileId, line, column, kind, 0, isVirt, isDef, typeUsrId, typeKind, isPointer);
}

// process c++ method declarations
static inline void procCXXMethodDecl(const CXCursor& Cursor, const char* cUsr, std::string name, std::string fileName, int line, int column, int kind)
{
    int isDef = clang_isCursorDefinition(Cursor);
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
        gDb->insert_overriden_value(refUsrId, nameId, fileId, line, column, kind, usrId, isDef);
    }
    clang_disposeOverriddenCursors(cursorOverridden);
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
        //printf("ref: %s: %d, %d\n", cUsr, line, column);
        //
        // if the option '-p' is specified
        // 
        if(gIsPartial) {
            // skip if the scope is function internal
            CXCursor parentCur = clang_getCursorSemanticParent(refCur);
            if(isLocalDecl(parentCur.kind)) {
                return;
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
        gDb->insert_ref_value(refUsrId, nameId, fileId, line, column, kind, refFid, ref_line, ref_column);
        clang_disposeString(cxRefUSR);
    }
}

// process c++ base class informations
static inline void procCXXBaseClassInfo(const CXCursor& Cursor, std::string name, std::string fileName, int line, int column, int kind)
{
    // USR of class
    CXString cxBaseUsr = clang_getCursorUSR(Cursor);
    const char* cBaseUsr = clang_getCString(cxBaseUsr);
    // USR of base class
    CXCursor refCur = clang_getCursorReferenced(Cursor);
    cxBaseUsr = clang_getCursorUSR(refCur);
    cBaseUsr = clang_getCString(cxBaseUsr);
    int accessibility = clang_getCXXAccessSpecifier(Cursor);
    // convert to ID
    int classUsrId = usrIdTbl->GetId(gLastClassUsr);
    int baseClassUsrId = usrIdTbl->GetId(cBaseUsr);
    // insert to database
    gDb->insert_base_class_value(classUsrId, baseClassUsrId, line, column, accessibility);
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
        case CXCursor_Namespace:
        case CXCursor_UnionDecl:
        case CXCursor_VarDecl:
        case CXCursor_ParmDecl:
        case CXCursor_FieldDecl:
        case CXCursor_MacroDefinition: {
            procDecl(Cursor, cUsr, name, fileName, line, column, kind, val);
            break;
        }
        case CXCursor_StructDecl:
        case CXCursor_ClassDecl:
        case CXCursor_EnumDecl: {
            gLastClassUsr = cUsr;
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
        case CXCursor_CXXBaseSpecifier: {
            procCXXBaseClassInfo(Cursor, name, fileName, line, column, kind);
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

static enum CXChildVisitResult printingVisitor(CXCursor Cursor,
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
  CXIndex Idx = 0;
  CXTranslationUnit TU;
  const char *CommentSchemaFile = NULL;
  int result;
  const char *cur_dir = argv[0];
  const char *out_file_name = argv[1];
  const char *in_file_name = argv[2];
  // increment argv to pass clang
  argv+=2;
  argc-=2;

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

  fileIdTbl = new IdTbl();
  usrIdTbl = new IdTbl();
  nameIdTbl = new IdTbl();

  gDb = new cxxtags::IndexDb();
  gDb->init(out_file_name, in_file_name, gExcludeListStr, gIsPartial, cur_dir, argc-1, argv+1);

  if(gIsEmpty) {
      result = 0;
      // add the source file to the file list
      fileIdTbl->GetId(in_file_name);
      goto FUNC_END;
  }
  
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
  if(Idx) {
    clang_disposeIndex(Idx);
  }
  gDb->fin(fileIdTbl->GetTbl(), usrIdTbl->GetTbl(), nameIdTbl->GetTbl());
  delete fileIdTbl;
  delete usrIdTbl;
  delete nameIdTbl;
  return result;
}

/******************************************************************************/
/* Command line processing.                                                   */
/******************************************************************************/
static void print_usage(void) {
    fprintf(stderr, "usage: cxxtags_core [-pE] [-e excludeList] cur_dir out_file in_file -- {<clang_args>}*\n");
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
    if (argc >= 3) {
        while(argc) {
            if(strncmp(*argv, "-e", 2) == 0) { 
                gExcludeListStr = argv[1];
                gExcludeList = splitString(gExcludeListStr);
                argv+=2;
                argc-=2;
            }
            else if(strncmp(*argv, "-p", 2) == 0) {
                gIsPartial = 1;
                argv++;
                argc--;
            }
            else if(strncmp(*argv, "-E", 2) == 0) {
                gIsEmpty = 1;
                argv++;
                argc--;
            }
            else {
                break;
            }
        }
        CXCursorVisitor I = printingVisitor;
        PostVisitTU postVisit = 0;
        if (I) {
            return perform_test_load_source(argc, argv, I, postVisit);
        }
    }
    print_usage();
    return 1;
}

};

int main(int argc, const char **argv) {
    return cxxtagsIndexer::indexSource(argc, argv);
}
