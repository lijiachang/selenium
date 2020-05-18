#!/bin/bash

database=$1
a=`db2 connect to $database;db2 "select (1-CAT_CACHE_INSERTS/CAT_CACHE_LOOKUPS)*100 from sysibmadm.SNAPDB";`
CtlgCacheHitRatio=`echo "$a"|awk 'NR==11{print}'|sed s/[[:space:]]//g`
echo '""||""||APM-DB2-07-06||'$CtlgCacheHitRatio
