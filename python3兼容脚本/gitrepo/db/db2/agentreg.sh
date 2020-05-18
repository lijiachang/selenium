#!/bin/bash

database=$1
#|awk 'NR==11{print}'
a=`db2 connect to $database;db2 "select NUM_ASSOC_AGENTS from sysibmadm.SNAPDB";`
AgentsRegd=`echo "$a"|awk 'NR==11{print}'|sed s/[[:space:]]//g`
echo '""||""||APM-DB2-04-01||'$AgentsRegd
