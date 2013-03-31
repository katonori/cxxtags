/* c-index-test.c */

#include "clang-c/Index.h"
#include "clang-c/CXCompilationDatabase.h"
#include "llvm/Config/config.h"
#include <ctype.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
#include "db.h"

#ifdef CLANG_HAVE_LIBXML
#include <libxml/parser.h>
#include <libxml/relaxng.h>
#include <libxml/xmlerror.h>
#endif

static const char* GetCursorSource(CXCursor Cursor);

/******************************************************************************/
/* Utility functions.                                                         */
/******************************************************************************/

#ifdef _MSC_VER
char *basename(const char* path)
{
    char* base1 = (char*)strrchr(path, '/');
    char* base2 = (char*)strrchr(path, '\\');
    if (base1 && base2)
        return((base1 > base2) ? base1 + 1 : base2 + 1);
    else if (base1)
        return(base1 + 1);
    else if (base2)
        return(base2 + 1);

    return((char*)path);
}
char *dirname(char* path)
{
    char* base1 = (char*)strrchr(path, '/');
    char* base2 = (char*)strrchr(path, '\\');
    if (base1 && base2)
        if (base1 > base2)
          *base1 = 0;
        else
          *base2 = 0;
    else if (base1)
        *base1 = 0;
    else if (base2)
        *base2 = 0;

    return path;
}
#else
extern char *basename(const char *);
extern char *dirname(char *);
#endif

/** \brief Return the default parsing options. */
static unsigned getDefaultParsingOptions() {
  unsigned options = CXTranslationUnit_DetailedPreprocessingRecord;

  if (getenv("CINDEXTEST_EDITING"))
    options |= clang_defaultEditingTranslationUnitOptions();
  if (getenv("CINDEXTEST_COMPLETION_CACHING"))
    options |= CXTranslationUnit_CacheCompletionResults;
  if (getenv("CINDEXTEST_COMPLETION_NO_CACHING"))
    options &= ~CXTranslationUnit_CacheCompletionResults;
  if (getenv("CINDEXTEST_SKIP_FUNCTION_BODIES"))
    options |= CXTranslationUnit_SkipFunctionBodies;
  if (getenv("CINDEXTEST_COMPLETION_BRIEF_COMMENTS"))
    options |= CXTranslationUnit_IncludeBriefCommentsInCodeCompletion;
  
  return options;
}

static int checkForErrors(CXTranslationUnit TU);

static void PrintExtent(FILE *out, unsigned begin_line, unsigned begin_column,
                        unsigned end_line, unsigned end_column) {
  fprintf(out, "[%d:%d - %d:%d]", begin_line, begin_column,
          end_line, end_column);
}

void free_remapped_files(struct CXUnsavedFile *unsaved_files,
                         int num_unsaved_files) {
  int i;
  for (i = 0; i != num_unsaved_files; ++i) {
    free((char *)unsaved_files[i].Filename);
    free((char *)unsaved_files[i].Contents);
  }
  free(unsaved_files);
}

int parse_remapped_files(int argc, const char **argv, int start_arg,
                         struct CXUnsavedFile **unsaved_files,
                         int *num_unsaved_files) {
  int i;
  int arg;
  int prefix_len = strlen("-remap-file=");
  *unsaved_files = 0;
  *num_unsaved_files = 0;

  /* Count the number of remapped files. */
  for (arg = start_arg; arg < argc; ++arg) {
    if (strncmp(argv[arg], "-remap-file=", prefix_len))
      break;

    ++*num_unsaved_files;
  }

  if (*num_unsaved_files == 0)
    return 0;

  *unsaved_files
    = (struct CXUnsavedFile *)malloc(sizeof(struct CXUnsavedFile) *
                                     *num_unsaved_files);
  for (arg = start_arg, i = 0; i != *num_unsaved_files; ++i, ++arg) {
    struct CXUnsavedFile *unsaved = *unsaved_files + i;
    const char *arg_string = argv[arg] + prefix_len;
    int filename_len;
    char *filename;
    char *contents;
    FILE *to_file;
    const char *semi = strchr(arg_string, ';');
    if (!semi) {
      fprintf(stderr,
              "error: -remap-file=from;to argument is missing semicolon\n");
      free_remapped_files(*unsaved_files, i);
      *unsaved_files = 0;
      *num_unsaved_files = 0;
      return -1;
    }

    /* Open the file that we're remapping to. */
    to_file = fopen(semi + 1, "rb");
    if (!to_file) {
      fprintf(stderr, "error: cannot open file %s that we are remapping to\n",
              semi + 1);
      free_remapped_files(*unsaved_files, i);
      *unsaved_files = 0;
      *num_unsaved_files = 0;
      return -1;
    }

    /* Determine the length of the file we're remapping to. */
    fseek(to_file, 0, SEEK_END);
    unsaved->Length = ftell(to_file);
    fseek(to_file, 0, SEEK_SET);

    /* Read the contents of the file we're remapping to. */
    contents = (char *)malloc(unsaved->Length + 1);
    if (fread(contents, 1, unsaved->Length, to_file) != unsaved->Length) {
      fprintf(stderr, "error: unexpected %s reading 'to' file %s\n",
              (feof(to_file) ? "EOF" : "error"), semi + 1);
      fclose(to_file);
      free_remapped_files(*unsaved_files, i);
      free(contents);
      *unsaved_files = 0;
      *num_unsaved_files = 0;
      return -1;
    }
    contents[unsaved->Length] = 0;
    unsaved->Contents = contents;

    /* Close the file. */
    fclose(to_file);

    /* Copy the file name that we're remapping from. */
    filename_len = semi - arg_string;
    filename = (char *)malloc(filename_len + 1);
    memcpy(filename, arg_string, filename_len);
    filename[filename_len] = 0;
    unsaved->Filename = filename;
  }

  return 0;
}

/******************************************************************************/
/* Pretty-printing.                                                           */
/******************************************************************************/

static const char *FileCheckPrefix = "CHECK";

int want_display_name = 0;

typedef struct {
  const char *CommentSchemaFile;
#ifdef CLANG_HAVE_LIBXML
  xmlRelaxNGParserCtxtPtr RNGParser;
  xmlRelaxNGPtr Schema;
#endif
} CommentXMLValidationData;

// use same cursor kind names as cindex.py for test cases.
static const char* getCursorString(enum CXCursorKind ck)
{
    switch(ck) {
        case CXCursor_ClassDecl: return "CLASS_DECL";
        case CXCursor_Namespace: return "NAMESPACE";
        case CXCursor_StructDecl: return "STRUCT_DECL";
        case CXCursor_ClassTemplate: return "CLASS_TEMPLATE";
        case CXCursor_UnionDecl: return "UNION_DECL";
        case CXCursor_VarDecl: return "VAR_DECL";
        case CXCursor_ParmDecl: return "PARM_DECL";
        case CXCursor_FieldDecl: return "FIELD_DECL";
        case CXCursor_FunctionDecl: return "FUNCTION_DECL";
        case CXCursor_CXXMethod: return "CXX_METHOD";
        case CXCursor_Constructor: return "CONSTRUCTOR";
        case CXCursor_Destructor: return "DESTRUCTOR";
        case CXCursor_TypedefDecl: return "TYPEDEF_DECL";
        case CXCursor_MacroDefinition: return "MACRO_DEFINITION";
        case CXCursor_EnumConstantDecl: return "ENUM_CONSTANT_DECL";
        case CXCursor_DeclRefExpr: return "DECL_REF_EXPR";
        case CXCursor_MemberRefExpr: return "MEMBER_REF_EXPR";
        case CXCursor_TypeRef: return "TYPE_REF";
        case CXCursor_MemberRef: return "MEMBER_REF";
        case CXCursor_TemplateRef: return "TEMPLATE_REF";
        case CXCursor_MacroInstantiation: return "MACRO_INSTANTIATION";
        case CXCursor_NamespaceRef: return "NAMESPACE_REF";
        default:
        return "NONE";
    }
}

static void PrintCursor(CXCursor Cursor,
                        CommentXMLValidationData *ValidationData) {
  if (clang_isInvalid(Cursor.kind)) {
    CXString ks = clang_getCursorKindSpelling(Cursor.kind);
    printf("Invalid Cursor => %s", clang_getCString(ks));
    clang_disposeString(ks);
  }
  else {
    CXCursor Referenced;
    unsigned int line = 0;
    unsigned int column = 0;
    unsigned int ref_line = 0;
    unsigned int ref_column = 0;
    CXSourceLocation Loc = clang_getCursorLocation(Cursor);
    clang_getSpellingLocation(Loc, 0, &line, &column, 0);
    //CXString name = clang_getCursorDisplayName(Cursor);
    CXString name = clang_getCursorSpelling(Cursor);
    const char* c_name = clang_getCString(name);
    if(strncmp(c_name, "", 1) == 0) {
        return;
    }
    CXString USR = clang_getCursorUSR(Cursor);
    const char *c_usr = clang_getCString(USR);
    const char *c_ref_file_name = "";
    if (!c_usr) {
        c_usr = "";
    }
    const char *c_file_name = GetCursorSource(Cursor);
    const char *c_ks = getCursorString(Cursor.kind);

    int is_def = clang_isCursorDefinition(Cursor);

    switch(Cursor.kind) {
        case CXCursor_TypedefDecl:
        case CXCursor_ClassDecl:
        case CXCursor_Namespace:
        case CXCursor_StructDecl:
        case CXCursor_UnionDecl:
        case CXCursor_VarDecl:
        case CXCursor_ParmDecl:
        case CXCursor_FieldDecl:
        case CXCursor_FunctionDecl:
        case CXCursor_CXXMethod:
        case CXCursor_Constructor:
        case CXCursor_Destructor:
        case CXCursor_MacroDefinition:
            db_regist_decl_value(c_usr, c_name, c_file_name, line, column, c_ks, 0, is_def);
            break;
        case CXCursor_EnumConstantDecl: {
            int val = clang_getEnumConstantDeclValue(Cursor);
            db_regist_decl_value(c_usr, c_name, c_file_name, line, column, c_ks, val, is_def);
            break;
        }
        case CXCursor_DeclRefExpr:
        case CXCursor_MemberRefExpr:
        case CXCursor_TypeRef:
        //case CXCursor_CXXBaseSpecifier:
        case CXCursor_MemberRef:
        case CXCursor_NamespaceRef:
        case CXCursor_MacroExpansion:
            c_usr = "";
            Referenced = clang_getCursorReferenced(Cursor);
            if (!clang_equalCursors(Referenced, clang_getNullCursor())) {
                CXString ref_usr = clang_getCursorUSR(Referenced);
                c_usr = clang_getCString(ref_usr);
                CXFile ref_file;

                CXSourceLocation ref_loc = clang_getCursorLocation(Referenced);
                clang_getSpellingLocation(ref_loc, &ref_file, &ref_line, &ref_column, 0);
                if(ref_file) {
                    c_ref_file_name = clang_getCString(clang_getFileName(ref_file));
                }
            }
            db_regist_ref_value(c_usr, c_name, c_file_name, line, column, c_ks, c_ref_file_name, ref_line, ref_column);
            break;
        // TODO:
        case CXCursor_InclusionDirective:
        case CXCursor_CStyleCastExpr:
        case CXCursor_CharacterLiteral:
        case CXCursor_BinaryOperator:
        case CXCursor_IfStmt:
        case CXCursor_ParenExpr:
        case CXCursor_AsmLabelAttr:
        case CXCursor_CXXThisExpr:
        case CXCursor_UnexposedAttr:
        case CXCursor_UnexposedDecl:
        case CXCursor_UnaryOperator:
        case CXCursor_CXXAccessSpecifier:
        case CXCursor_CallExpr:
        case CXCursor_UnexposedExpr:
        case CXCursor_DeclStmt:
        case CXCursor_CompoundStmt:
        case CXCursor_ReturnStmt:
        case CXCursor_StringLiteral:
        case CXCursor_IntegerLiteral:
            break;
        default:
            //printf("*** VARDECL ***: ");
            break;
    }
  }
  return;
}

static const char* GetCursorSource(CXCursor Cursor) {
  CXSourceLocation Loc = clang_getCursorLocation(Cursor);
  CXString source;
  CXFile file;
  clang_getExpansionLocation(Loc, &file, 0, 0, 0);
  source = clang_getFileName(file);
  CXString filename = clang_getFileName(file);
  if (!clang_getCString(source)) {
    clang_disposeString(source);
    return "<invalid loc>";
  }
  else {
    //const char *b = basename(clang_getCString(source));
    const char *b = clang_getCString(filename);
    clang_disposeString(source);
    return b;
  }
}

/******************************************************************************/
/* Callbacks.                                                                 */
/******************************************************************************/

typedef void (*PostVisitTU)(CXTranslationUnit);

void PrintDiagnostic(CXDiagnostic Diagnostic) {
  FILE *out = stderr;
  CXFile file;
  CXString Msg;
  unsigned display_opts = CXDiagnostic_DisplaySourceLocation
    | CXDiagnostic_DisplayColumn | CXDiagnostic_DisplaySourceRanges
    | CXDiagnostic_DisplayOption;
  unsigned i, num_fixits;

  if (clang_getDiagnosticSeverity(Diagnostic) == CXDiagnostic_Ignored)
    return;

  Msg = clang_formatDiagnostic(Diagnostic, display_opts);
  fprintf(stderr, "%s\n", clang_getCString(Msg));
  clang_disposeString(Msg);

  clang_getSpellingLocation(clang_getDiagnosticLocation(Diagnostic),
                            &file, 0, 0, 0);
  if (!file)
    return;

  num_fixits = clang_getDiagnosticNumFixIts(Diagnostic);
  fprintf(stderr, "Number FIX-ITs = %d\n", num_fixits);
  for (i = 0; i != num_fixits; ++i) {
    CXSourceRange range;
    CXString insertion_text = clang_getDiagnosticFixIt(Diagnostic, i, &range);
    CXSourceLocation start = clang_getRangeStart(range);
    CXSourceLocation end = clang_getRangeEnd(range);
    unsigned start_line, start_column, end_line, end_column;
    CXFile start_file, end_file;
    clang_getSpellingLocation(start, &start_file, &start_line,
                              &start_column, 0);
    clang_getSpellingLocation(end, &end_file, &end_line, &end_column, 0);
    if (clang_equalLocations(start, end)) {
      /* Insertion. */
      if (start_file == file)
        fprintf(out, "FIX-IT: Insert \"%s\" at %d:%d\n",
                clang_getCString(insertion_text), start_line, start_column);
    } else if (strcmp(clang_getCString(insertion_text), "") == 0) {
      /* Removal. */
      if (start_file == file && end_file == file) {
        fprintf(out, "FIX-IT: Remove ");
        PrintExtent(out, start_line, start_column, end_line, end_column);
        fprintf(out, "\n");
      }
    } else {
      /* Replacement. */
      if (start_file == end_file) {
        fprintf(out, "FIX-IT: Replace ");
        PrintExtent(out, start_line, start_column, end_line, end_column);
        fprintf(out, " with \"%s\"\n", clang_getCString(insertion_text));
      }
      break;
    }
    clang_disposeString(insertion_text);
  }
}

void PrintDiagnosticSet(CXDiagnosticSet Set) {
  int i = 0, n = clang_getNumDiagnosticsInSet(Set);
  for ( ; i != n ; ++i) {
    CXDiagnostic Diag = clang_getDiagnosticInSet(Set, i);
    CXDiagnosticSet ChildDiags = clang_getChildDiagnostics(Diag);
    PrintDiagnostic(Diag);
    if (ChildDiags)
      PrintDiagnosticSet(ChildDiags);
  }  
}

void PrintDiagnostics(CXTranslationUnit TU) {
  CXDiagnosticSet TUSet = clang_getDiagnosticSetFromTU(TU);
  PrintDiagnosticSet(TUSet);
  clang_disposeDiagnosticSet(TUSet);
}

void PrintMemoryUsage(CXTranslationUnit TU) {
  unsigned long total = 0;
  unsigned i = 0;
  CXTUResourceUsage usage = clang_getCXTUResourceUsage(TU);
  fprintf(stderr, "Memory usage:\n");
  for (i = 0 ; i != usage.numEntries; ++i) {
    const char *name = clang_getTUResourceUsageName(usage.entries[i].kind);
    unsigned long amount = usage.entries[i].amount;
    total += amount;
    fprintf(stderr, "  %s : %ld bytes (%f MBytes)\n", name, amount,
            ((double) amount)/(1024*1024));
  }
  fprintf(stderr, "  TOTAL = %ld bytes (%f MBytes)\n", total,
          ((double) total)/(1024*1024));
  clang_disposeCXTUResourceUsage(usage);  
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

enum CXChildVisitResult FilteredPrintingVisitor(CXCursor Cursor,
                                                CXCursor Parent,
                                                CXClientData ClientData) {
  VisitorData *Data = (VisitorData *)ClientData;
  if (!Data->Filter || (Cursor.kind == *(enum CXCursorKind *)Data->Filter)) {
#if 0
    CXSourceLocation Loc = clang_getCursorLocation(Cursor);
    unsigned line, column;
    clang_getSpellingLocation(Loc, 0, &line, &column, 0);
    printf("// %s: %s:%d:%d: ", FileCheckPrefix,
           GetCursorSource(Cursor), line, column);
#endif
    PrintCursor(Cursor, &Data->ValidationData);
    return CXChildVisit_Recurse;
  }

  return CXChildVisit_Continue;
}

static enum CXChildVisitResult FunctionScanVisitor(CXCursor Cursor,
                                                   CXCursor Parent,
                                                   CXClientData ClientData) {
  const char *startBuf, *endBuf;
  unsigned startLine, startColumn, endLine, endColumn, curLine, curColumn;
  CXCursor Ref;
  VisitorData *Data = (VisitorData *)ClientData;

  if (Cursor.kind != CXCursor_FunctionDecl ||
      !clang_isCursorDefinition(Cursor))
    return CXChildVisit_Continue;

  clang_getDefinitionSpellingAndExtent(Cursor, &startBuf, &endBuf,
                                       &startLine, &startColumn,
                                       &endLine, &endColumn);
  /* Probe the entire body, looking for both decls and refs. */
  curLine = startLine;
  curColumn = startColumn;

  while (startBuf < endBuf) {
    CXSourceLocation Loc;
    CXFile file;
    CXString source;

    if (*startBuf == '\n') {
      startBuf++;
      curLine++;
      curColumn = 1;
    } else if (*startBuf != '\t')
      curColumn++;

    Loc = clang_getCursorLocation(Cursor);
    clang_getSpellingLocation(Loc, &file, 0, 0, 0);

    source = clang_getFileName(file);
    if (clang_getCString(source)) {
      CXSourceLocation RefLoc
        = clang_getLocation(Data->TU, file, curLine, curColumn);
      Ref = clang_getCursor(Data->TU, RefLoc);
      if (Ref.kind == CXCursor_NoDeclFound) {
        /* Nothing found here; that's fine. */
      } else if (Ref.kind != CXCursor_FunctionDecl) {
        printf("// %s: %s:%d:%d: ", FileCheckPrefix, GetCursorSource(Ref),
               curLine, curColumn);
        PrintCursor(Ref, &Data->ValidationData);
        printf("\n");
      }
    }
    clang_disposeString(source);
    startBuf++;
  }

  return CXChildVisit_Continue;
}

/******************************************************************************/
/* Inclusion stack testing.                                                   */
/******************************************************************************/

void InclusionVisitor(CXFile includedFile, CXSourceLocation *includeStack,
                      unsigned includeStackLen, CXClientData data) {

  unsigned i;
  CXString fname;

  fname = clang_getFileName(includedFile);
  printf("file: %s\nincluded by:\n", clang_getCString(fname));
  clang_disposeString(fname);

  for (i = 0; i < includeStackLen; ++i) {
    CXFile includingFile;
    unsigned line, column;
    clang_getSpellingLocation(includeStack[i], &includingFile, &line,
                              &column, 0);
    fname = clang_getFileName(includingFile);
    printf("  %s:%d:%d\n", clang_getCString(fname), line, column);
    clang_disposeString(fname);
  }
  printf("\n");
}

void PrintInclusionStack(CXTranslationUnit TU) {
  clang_getInclusions(TU, InclusionVisitor, NULL);
}

/******************************************************************************/
/* Loading ASTs/source.                                                       */
/******************************************************************************/

static int perform_test_load(CXIndex Idx, CXTranslationUnit TU,
                             const char *filter, const char *prefix,
                             CXCursorVisitor Visitor,
                             PostVisitTU PV,
                             const char *CommentSchemaFile) {

  if (prefix)
    FileCheckPrefix = prefix;

  if (Visitor) {
    enum CXCursorKind K = CXCursor_NotImplemented;
    enum CXCursorKind *ck = &K;
    VisitorData Data;

    /* Perform some simple filtering. */
    if (!strcmp(filter, "all") || !strcmp(filter, "local")) ck = NULL;
    else if (!strcmp(filter, "all-display") || 
             !strcmp(filter, "local-display")) {
      ck = NULL;
      want_display_name = 1;
    }
    else if (!strcmp(filter, "none")) K = (enum CXCursorKind) ~0;
    else if (!strcmp(filter, "category")) K = CXCursor_ObjCCategoryDecl;
    else if (!strcmp(filter, "interface")) K = CXCursor_ObjCInterfaceDecl;
    else if (!strcmp(filter, "protocol")) K = CXCursor_ObjCProtocolDecl;
    else if (!strcmp(filter, "function")) K = CXCursor_FunctionDecl;
    else if (!strcmp(filter, "typedef")) K = CXCursor_TypedefDecl;
    else if (!strcmp(filter, "scan-function")) Visitor = FunctionScanVisitor;
    else {
      fprintf(stderr, "Unknown filter for -test-load-tu: %s\n", filter);
      return 1;
    }

    Data.TU = TU;
    Data.Filter = ck;
    Data.ValidationData.CommentSchemaFile = CommentSchemaFile;
#ifdef CLANG_HAVE_LIBXML
    Data.ValidationData.RNGParser = NULL;
    Data.ValidationData.Schema = NULL;
#endif
    clang_visitChildren(clang_getTranslationUnitCursor(TU), Visitor, &Data);
  }

  if (PV)
    PV(TU);

  PrintDiagnostics(TU);
  if (checkForErrors(TU) != 0) {
    clang_disposeTranslationUnit(TU);
    return -1;
  }

  clang_disposeTranslationUnit(TU);
  return 0;
}

int perform_test_load_source(int argc, const char **argv,
                             const char *filter, CXCursorVisitor Visitor,
                             PostVisitTU PV) {
  CXIndex Idx;
  CXTranslationUnit TU;
  const char *CommentSchemaFile = NULL;
  struct CXUnsavedFile *unsaved_files = 0;
  int num_unsaved_files = 0;
  int result;
  const char *out_file_name = argv[0];
  //const char *in_file_name = argv[1];
  argv++;
  argc--;

  CXString clang_ver = clang_getClangVersion();
  db_init(out_file_name, clang_getCString(clang_ver));
  
  Idx = clang_createIndex(/* excludeDeclsFromPCH */
                          (!strcmp(filter, "local") || 
                           !strcmp(filter, "local-display"))? 1 : 0,
                          /* displayDiagnosics=*/0);

  if (parse_remapped_files(argc, argv, 0, &unsaved_files, &num_unsaved_files)) {
      result = -1;
      goto FUNC_END;
  }

  TU = clang_parseTranslationUnit(Idx, 0,
                                  argv + num_unsaved_files,
                                  argc - num_unsaved_files,
                                  unsaved_files, num_unsaved_files, 
                                  getDefaultParsingOptions());
  if (!TU) {
    fprintf(stderr, "Unable to load translation unit!\n");
    free_remapped_files(unsaved_files, num_unsaved_files);
    result = 1;
    goto FUNC_END;
  }

  result = perform_test_load(Idx, TU, filter, NULL, Visitor, PV,
                             CommentSchemaFile);
  free_remapped_files(unsaved_files, num_unsaved_files);
FUNC_END:
  clang_disposeIndex(Idx);
  db_fin();
  return result;
}

int perform_test_reparse_source(int argc, const char **argv, int trials,
                                const char *filter, CXCursorVisitor Visitor,
                                PostVisitTU PV) {
  CXIndex Idx;
  CXTranslationUnit TU;
  struct CXUnsavedFile *unsaved_files = 0;
  int num_unsaved_files = 0;
  int result;
  int trial;
  int remap_after_trial = 0;
  char *endptr = 0;
  
  Idx = clang_createIndex(/* excludeDeclsFromPCH */
                          !strcmp(filter, "local") ? 1 : 0,
                          /* displayDiagnosics=*/0);
  
  if (parse_remapped_files(argc, argv, 0, &unsaved_files, &num_unsaved_files)) {
    clang_disposeIndex(Idx);
    return -1;
  }
  
  /* Load the initial translation unit -- we do this without honoring remapped
   * files, so that we have a way to test results after changing the source. */
  TU = clang_parseTranslationUnit(Idx, 0,
                                  argv + num_unsaved_files,
                                  argc - num_unsaved_files,
                                  0, 0, getDefaultParsingOptions());
  if (!TU) {
    fprintf(stderr, "Unable to load translation unit!\n");
    free_remapped_files(unsaved_files, num_unsaved_files);
    clang_disposeIndex(Idx);
    return 1;
  }
  
  if (checkForErrors(TU) != 0)
    return -1;

  if (getenv("CINDEXTEST_REMAP_AFTER_TRIAL")) {
    remap_after_trial =
        strtol(getenv("CINDEXTEST_REMAP_AFTER_TRIAL"), &endptr, 10);
  }

  for (trial = 0; trial < trials; ++trial) {
    if (clang_reparseTranslationUnit(TU,
                             trial >= remap_after_trial ? num_unsaved_files : 0,
                             trial >= remap_after_trial ? unsaved_files : 0,
                                     clang_defaultReparseOptions(TU))) {
      fprintf(stderr, "Unable to reparse translation unit!\n");
      clang_disposeTranslationUnit(TU);
      free_remapped_files(unsaved_files, num_unsaved_files);
      clang_disposeIndex(Idx);
      return -1;      
    }

    if (checkForErrors(TU) != 0)
      return -1;
  }
  
  result = perform_test_load(Idx, TU, filter, NULL, Visitor, PV, NULL);

  free_remapped_files(unsaved_files, num_unsaved_files);
  clang_disposeIndex(Idx);
  return result;
}

static int checkForErrors(CXTranslationUnit TU) {
  unsigned Num, i;
  CXDiagnostic Diag;
  CXString DiagStr;

  if (!getenv("CINDEXTEST_FAILONERROR"))
    return 0;

  Num = clang_getNumDiagnostics(TU);
  for (i = 0; i != Num; ++i) {
    Diag = clang_getDiagnostic(TU, i);
    if (clang_getDiagnosticSeverity(Diag) >= CXDiagnostic_Error) {
      DiagStr = clang_formatDiagnostic(Diag,
                                       clang_defaultDiagnosticDisplayOptions());
      fprintf(stderr, "%s\n", clang_getCString(DiagStr));
      clang_disposeString(DiagStr);
      clang_disposeDiagnostic(Diag);
      return -1;
    }
    clang_disposeDiagnostic(Diag);
  }

  return 0;
}

/******************************************************************************/
/* Command line processing.                                                   */
/******************************************************************************/

static CXCursorVisitor GetVisitor(const char *s) {
    return FilteredPrintingVisitor;
}

static void print_usage(void) {
  fprintf(stderr,
    "usage: c-index-test -test-load-source <symbol filter> {<args>}*\n");
  fprintf(stderr,
    " <symbol filter> values:\n%s",
    "   all - load all symbols, including those from PCH\n"
    "   local - load all symbols except those in PCH\n"
    "   category - only load ObjC categories (non-PCH)\n"
    "   interface - only load ObjC interfaces (non-PCH)\n"
    "   protocol - only load ObjC protocols (non-PCH)\n"
    "   function - only load functions (non-PCH)\n"
    "   typedef - only load typdefs (non-PCH)\n"
    "   scan-function - scan function bodies (non-PCH)\n\n");
}

/***/

int cindextest_main(int argc, const char **argv) {
  clang_enableStackTraces();
  if (argc >= 4 && strncmp(argv[1], "-test-load-source", 17) == 0) {
    CXCursorVisitor I = GetVisitor(argv[1] + 17);
    
    PostVisitTU postVisit = 0;
    
    if (I)
      return perform_test_load_source(argc - 3, argv + 3, argv[2], I,
                                      postVisit);
  }
  print_usage();
  return 1;
}

/***/

/* We intentionally run in a separate thread to ensure we at least minimal
 * testing of a multithreaded environment (for example, having a reduced stack
 * size). */

typedef struct thread_info {
  int argc;
  const char **argv;
  int result;
} thread_info;
void thread_runner(void *client_data_v) {
  thread_info *client_data = client_data_v;
  client_data->result = cindextest_main(client_data->argc, client_data->argv);
#ifdef __CYGWIN__
  fflush(stdout);  /* stdout is not flushed on Cygwin. */
#endif
}

#if 1
int main(int argc, const char **argv) {
#else
int c_index_test(int argc, const char **argv) {
#endif
  thread_info client_data;

#ifdef CLANG_HAVE_LIBXML
  LIBXML_TEST_VERSION
#endif

  if (getenv("CINDEXTEST_NOTHREADS"))
    return cindextest_main(argc, argv);

  client_data.argc = argc;
  client_data.argv = argv;
  clang_executeOnThread(thread_runner, &client_data, 0);
  return client_data.result;
}
