#!/usr/bin/python

import commands

gDebug = 0
CXXTAGS_QUERY = "../../bin/cxxtags_query"

def debugOn():
    global gDebug
    gDebug = 1

def DbgPrint(msg):
    global gDebug
    if gDebug != 0:
        print msg

def QueryTestExecCommand(mode, name, fileName, line, col):
    cmd = CXXTAGS_QUERY + " %s db %s -f %s -l %d -c %d"%(mode, name, fileName, line, col)
    DbgPrint("$ " + cmd)
    result = commands.getoutput(cmd).split('\n')
    cmdResult = []
    for i in result:
        fn, line, col = i.split('|')
        cmdResult.append((int(line), int(col), fn))
    return cmdResult

def DoDeclTest(test_data_list_decl, test_data_list_ref):
    err = 0
    for test in test_data_list_decl:
        resultList = []
        DbgPrint("decl test")
        #print test
        usr, name, fileName, line, col, dummy, dummy, dummy, dummy = test
        # search references
        for i in test_data_list_ref:
            refUsr, refName, refFileName, refLine, refCol, dummy, dummy, dummy, dummy = i
            if refUsr == usr:
                resultList.append((refLine, refCol, refFileName))

        if len(resultList) == 0:
            continue

        # exec command
        cmdResult = QueryTestExecCommand("ref", name, fileName, line, col)
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
        usr, name, fileName, line, col, kind, dummy, dummy, dummy = test
        # search declarations
        for i in test_data_list_decl:
            declUsr, declName, declFileName, declLine, declCol, dummy, dummy, dummy, dummy = i
            if declUsr == usr:
                resultList.append((declLine, declCol, declFileName ))

        if len(resultList) == 0:
            continue

        # exec command
        cmdResult = QueryTestExecCommand("decl", name, fileName, line, col)
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

