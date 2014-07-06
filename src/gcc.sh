#!/bin/sh

if [ "${CXXTAGS_CC}" = "" ]; then
    CXXTAGS_CC=gcc
fi
${CXXTAGS_CC} $*
cxxtags -p `echo $* | perl -pne 's/ -o\s+(\S+)[ ]*/ -o \1.tagdb /g'`
exit 0

