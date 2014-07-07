#!/bin/sh

if [ "${CXXTAGS_CC}" = "" ]; then
    CXXTAGS_CC=gcc
fi

if [ "${CXXTAGS_EXCLUDE}" != "" ]; then
    CXXTAGS_EXCLUDE=" -e ${CXXTAGS_EXCLUDE}"
fi

MATCH=`echo $* | grep -- "-MM " | wc -l`
if [ ${MATCH} -eq 0 ]; then
    cxxtags -p ${CXXTAGS_EXCLUDE} `echo $* | perl -pne 's/ -o\s+(\S+)[ ]*/ -o \1.tagdb /g'`
fi
${CXXTAGS_CC} $*
exit 0

