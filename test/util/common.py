#!/usr/bin/python

import sys
import commands
sys.path.append("../../src/")
import cxxtags_util

gDebug = 0
CXXTAGS_QUERY = "../../bin/cxxtags_query"

def DebugOn():
    global gDebug
    gDebug = 1

def DbgPrint(msg):
    global gDebug
    if gDebug != 0:
        print msg

def QueryTestExecCommand(mode, fileName, line, col):
    cmd = CXXTAGS_QUERY + " %s db %s %d %d"%(mode, fileName, line, col)
    DbgPrint("$ " + cmd)
    cmdResult = []
    result = commands.getoutput(cmd)
    if result == "":
        return []
    result = result.split('\n')
    for i in result:
        sp = i.split('|')
        name, fn, line, col = sp[0:4]
        lineStr = "".join(sp[4:])
        cmdResult.append((name, int(line), int(col), fn, lineStr))
    return cmdResult

def DoDeclTest(test_data_list_decl, test_data_list_ref):
    err = 0
    for test in test_data_list_decl:
        resultList = []
        DbgPrint("decl test")
        #print test
        usr, dummy, fileName, line, col, dummy, dummy, dummy = test[:8]
        # search references
        for i in test_data_list_ref:
            refUsr, refName, refFileName, refLine, refCol, dummy, dummy, dummy = i
            lineStr = cxxtags_util.get_line_from_file(refFileName, refLine)
            if refUsr == usr:
                resultList.append((refName, refLine, refCol, refFileName, lineStr))

        if len(resultList) == 0:
            continue

        # exec command
        cmdResult = QueryTestExecCommand("ref", fileName, line, col)
        DbgPrint(cmdResult)
        DbgPrint(resultList)
        cmdResult = sorted(cmdResult)
        resultList = sorted(resultList)

        # check result
        i  = 0
        for row in cmdResult:
            if row != resultList[i]:
                print("DIFFER: ")
                print(row)
                print(resultList[i])
                err += 1
            i+=1
    return err

def DoRefTest(test_data_list_ref, test_data_list_decl):
    err = 0
    for test in test_data_list_ref:
        resultList = []
        DbgPrint("ref test")
        #print test
        usr, dummy, fileName, line, col, kind, dummy, dummy = test
        # search declarations
        for i in test_data_list_decl:
            declUsr, declName, declFileName, declLine, declCol, dummy, dummy, dummy = i
            lineStr = cxxtags_util.get_line_from_file(declFileName, declLine)
            if declUsr == usr:
                resultList.append((declName, declLine, declCol, declFileName, lineStr))

        if len(resultList) == 0:
            continue

        # exec command
        cmdResult = QueryTestExecCommand("decl", fileName, line, col)
        DbgPrint(cmdResult)
        DbgPrint(resultList)
        cmdResult = sorted(cmdResult)
        resultList = sorted(resultList)

        # check result
        i  = 0
        for row in cmdResult:
            if row != resultList[i]:
                print "DIFFER: " 
                print row
                print resultList[i]
                err += 1
            i+=1
    return err

