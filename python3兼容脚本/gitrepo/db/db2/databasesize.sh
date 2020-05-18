#!/bin/bash

database=$1
a=`db2 connect to $database;db2 "CALL GET_DBSIZE_INFO(?, ?, ?, -1)"`
result=`echo "$a"|grep "Parameter Value"|awk -F"Parameter Value : " 'NR==2{print $2}'`

echo '""||""||PM-DB2-databasesize||'$result
#数据库大小，单位bytes   18.06.20