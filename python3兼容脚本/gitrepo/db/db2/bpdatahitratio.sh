#!/bin/bash

database=$1
a=`db2 connect to $database;db2 "select case POOL_DATA_L_READS when  0 then 1 else (POOL_DATA_L_READS * 1.  - POOL_DATA_P_READS * 1.) / POOL_DATA_L_READS end * 100. from sysibmadm.SNAPDB";`
BufferPoolHitRatio=`echo "$a"|awk 'NR==11{print}'|sed s/[[:space:]]//g`
echo '""||""||APM-DB2-07-03||'$BufferPoolHitRatio
