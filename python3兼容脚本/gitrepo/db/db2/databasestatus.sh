#!/bin/bash
if [ $# != 1 ];then
echo "Usage:$0 ServerName"
exit 1;
fi

database=$1
a=`db2 connect to $database;db2 "select DB_STATUS from sysibmadm.SNAPDB";`

if [[ $a =~ "SQL1001N" ]]||[[ $a =~ "SQL1013N" ]]
then
  echo '""||""||APM-DB2-01-01||1'
  exit
fi

DB2ServerOK=`echo "$a"|awk 'NR==11{print}'|sed s/[[:space:]]//g`

if [ $DB2ServerOK == 'ACTIVE' ];then
echo '""||""||APM-DB2-01-01||0'
else
echo '""||""||APM-DB2-01-01||4'
fi
#li revise,2018.0716
#0正常，1服务名错误，4此服务名未启动（非Active）