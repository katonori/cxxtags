#!/usr/bin/python

import sys
import commands
sys.path.append("../../src/")

gDebug = 0
CXXTAGS_QUERY = "../../bin/cxxtags_query"

def DebugOn():
    global gDebug
    gDebug = 1

def DbgPrint(msg):
    global gDebug
    if gDebug != 0:
        print msg

def GetLineFromFile(fn, line_no):
    line_no = int(line_no)
    fi = open(fn, 'r')
    all_lines = fi.readlines()
    str_line = ""
    if len(all_lines) < line_no:
        my_exit(1, "ERROR: GetLineFromFile: %s, %d\n"%(fn, line_no))
    else:
        str_line = all_lines[line_no-1]
    str_line = str_line.rstrip('\r\n')
    fi.close()
    return str_line

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
            lineStr = GetLineFromFile(refFileName, refLine)
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
                print("ref   : " + resultList[i])
                print("result: " + row)
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
            lineStr = GetLineFromFile(declFileName, declLine)
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
                print("ref   : " + resultList[i])
                print("result: " + row)
                err += 1
            i+=1
    return err

def test_one(q, ans):
    result = 0
    (rv, out) = commands.getstatusoutput(CXXTAGS_QUERY + " " + q)
    #print out
    if rv != 0:
        print "ERROR: rv = %d"%(rv)
        print "    q = ", q
        result += 1
    else:
        outList = list(set(out.split("\n")))
        outList.sort()
        ans.sort()
        if len(outList) != len(ans):
            print "ERROR: len out=%d, ref=%d"%(len(outList), len(ans))
            print "ERROR: q: " + q
            result += 1
        i = 0
        while i < len(outList):
            if outList[i] != ans[i]:
                print q
                print "DIFFER:"
                print("ref   : " + ans[i])
                print("result: " + outList[i])
                result += 1
            i += 1
    return result
