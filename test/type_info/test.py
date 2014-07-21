#!/usr/bin/python

import sys
import os
import commands

gErr = 0

CXXTAGS_QUERY = "../../bin/cxxtags_query"

cur_dir = os.getcwd()

testList = [
(1,1, cur_dir+"/main.cpp"), #typedef
(1,9, cur_dir+"/main.cpp"), #struct
(2,9, cur_dir+"/main.cpp"), #a
(3,5, cur_dir+"/main.cpp"), #short
(3,11,cur_dir+"/main.cpp"), #b
(4,5, cur_dir+"/main.cpp"), #char
(4,10,cur_dir+"/main.cpp"), #c
(5,3, cur_dir+"/main.cpp"), #DefStruct0
(7,1, cur_dir+"/main.cpp"), #struct
(7,8, cur_dir+"/main.cpp"), #Struct0
(8,5, cur_dir+"/main.cpp"), #unsigned
(8,18, cur_dir+"/main.cpp"), #d
(9,5, cur_dir+"/main.cpp"), #unsigned
(9,14, cur_dir+"/main.cpp"), #short
(9,20, cur_dir+"/main.cpp"), #e
(10,5, cur_dir+"/main.cpp"), #DefStruct0
(10,16, cur_dir+"/main.cpp"), #f
(13,1, cur_dir+"/main.cpp"), #DefStruct0
(13,12, cur_dir+"/main.cpp"), #val0
(14,1, cur_dir+"/main.cpp"), #Struct0
(14,9, cur_dir+"/main.cpp"), #val1
(15,1, cur_dir+"/main.cpp"), #DefStruct0
(15,13, cur_dir+"/main.cpp"), #val2
(16,1, cur_dir+"/main.cpp"), #Struct0
(16,10, cur_dir+"/main.cpp"), #val3
]

resultList = [
[], #typedef
[], #struct
[], #a
[], #short
[], #b
[], #char
[], #c
#DefStruct0
[
['','a', cur_dir+'/main.cpp','2','9','value','    int a;'],
['','b', cur_dir+'/main.cpp','3','11','value','    short b;'],
['','c', cur_dir+'/main.cpp','4','10','value','    char c;'],
],
[], #struct
#Struct0
[
['Struct0','d',cur_dir+'/main.cpp','8','18','value','    unsigned int d;'],
['Struct0','e',cur_dir+'/main.cpp','9','20','value','    unsigned short e;'],
['Struct0','f',cur_dir+'/main.cpp','10','16','value','    DefStruct0 f;'],
],
[], #unsigned
[], #d
[], #unsigned
[], #short
[], #e
#DefStruct0
[
['','a', cur_dir+'/main.cpp','2','9','value','    int a;'],
['','b', cur_dir+'/main.cpp','3','11','value','    short b;'],
['','c', cur_dir+'/main.cpp','4','10','value','    char c;'],
],
#e
[
['','a', cur_dir+'/main.cpp','2','9','value','    int a;'],
['','b', cur_dir+'/main.cpp','3','11','value','    short b;'],
['','c', cur_dir+'/main.cpp','4','10','value','    char c;'],
],
#DefStruct0
[
['','a', cur_dir+'/main.cpp','2','9','value','    int a;'],
['','b', cur_dir+'/main.cpp','3','11','value','    short b;'],
['','c', cur_dir+'/main.cpp','4','10','value','    char c;'],
],
#val0
[
['','a', cur_dir+'/main.cpp','2','9','value','    int a;'],
['','b', cur_dir+'/main.cpp','3','11','value','    short b;'],
['','c', cur_dir+'/main.cpp','4','10','value','    char c;'],
],
#Struct0
[
['Struct0','d',cur_dir+'/main.cpp','8','18','value','    unsigned int d;'],
['Struct0','e',cur_dir+'/main.cpp','9','20','value','    unsigned short e;'],
['Struct0','f',cur_dir+'/main.cpp','10','16','value','    DefStruct0 f;'],
],
#val1
[
['Struct0','d',cur_dir+'/main.cpp','8','18','value','    unsigned int d;'],
['Struct0','e',cur_dir+'/main.cpp','9','20','value','    unsigned short e;'],
['Struct0','f',cur_dir+'/main.cpp','10','16','value','    DefStruct0 f;'],
],
#DefStruct0
[
['','a', cur_dir+'/main.cpp','2','9','value','    int a;'],
['','b', cur_dir+'/main.cpp','3','11','value','    short b;'],
['','c', cur_dir+'/main.cpp','4','10','value','    char c;'],
],
#val2
[
['','a', cur_dir+'/main.cpp','2','9','value','    int a;'],
['','b', cur_dir+'/main.cpp','3','11','value','    short b;'],
['','c', cur_dir+'/main.cpp','4','10','value','    char c;'],
],
#Struct0
[
['Struct0','d',cur_dir+'/main.cpp','8','18','value','    unsigned int d;'],
['Struct0','e',cur_dir+'/main.cpp','9','20','value','    unsigned short e;'],
['Struct0','f',cur_dir+'/main.cpp','10','16','value','    DefStruct0 f;'],
],
#val3
[
['Struct0','d',cur_dir+'/main.cpp','8','18','value','    unsigned int d;'],
['Struct0','e',cur_dir+'/main.cpp','9','20','value','    unsigned short e;'],
['Struct0','f',cur_dir+'/main.cpp','10','16','value','    DefStruct0 f;'],
],
]

def main():
    global gErr
    if len(resultList) != len(testList):
        print "ERROR: test num"
        sys.exit(1)
    i = 0
    while i < len(resultList):
        line, col, fn = testList[i]
        out = commands.getoutput(CXXTAGS_QUERY + ' ' + 'type ./db main.cpp %d %d'%(line, col))
        res = out.split('\n')
        if res[len(res)-1] == "":
            del res[len(res)-1]
        if len(res) != len(resultList[i]):
            print "ERROR: result num: %d, %d"%(len(res), len(resultList[i]))
            gErr += 1
        else:
            r = 0
            while r < len(res):
                outList = res[r].split('|')
                if outList != resultList[i][r]:
                    print "ERROR: ", outList
                    print "     : ", resultList[i][r]
                    gErr += 1
                r += 1
        i += 1
main()
if gErr == 0:
    print "OK"
sys.exit(gErr)
