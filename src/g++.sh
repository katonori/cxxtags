#!/bin/sh

if [ "${CXXTAGS_CXX}" = "" ]; then
    CXXTAGS_CXX=g++
fi

if [ "${CXXTAGS_EXCLUDE}" != "" ]; then
    CXXTAGS_EXCLUDE=" -e ${CXXTAGS_EXCLUDE}"
fi

MATCH=`echo $* | grep -- "-MM " | wc -l`
if [ ${MATCH} -eq 0 ]; then
    cxxtags -p ${CXXTAGS_EXCLUDE} `echo $* | perl -pne 's/ -o\s+(\S+)[ ]*/ -o \1.tagdb /g'`
fi
${CXXTAGS_CXX} $*
exit 0
