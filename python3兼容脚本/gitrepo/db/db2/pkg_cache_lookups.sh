#!/bin/bash

database=$1
a=`db2 connect to $database;db2 "select PKG_CACHE_LOOKUPS from sysibmadm.SNAPDB";`
PKG_CACHE_LOOKUPS=`echo "$a"|awk 'NR==11{print}'|sed s/[[:space:]]//g`
echo '""||""||APM-DB2-07-04||'$PKG_CACHE_LOOKUPS
