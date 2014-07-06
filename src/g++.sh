#!/bin/sh

if [ "${CXXTAGS_CXX}" = "" ]; then
    CXXTAGS_CXX=g++
fi
${CXXTAGS_CXX} $*
cxxtags -p `echo $* | perl -pne 's/ -o\s+(\S+)[ ]*/ -o \1.tagdb /g'`
exit 0
