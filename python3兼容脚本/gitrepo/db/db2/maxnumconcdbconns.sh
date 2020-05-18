#!/bin/bash

database=$1
a=`db2 get snapshot for database on $database|grep "High water mark for connections"`
if [ "$a" = "" ]
then
  result="0"
else
  result=`echo "$a"|awk -F"= " '{print $2}'`
fi
echo '""||""||PM-DB2-maxnumconcdbconns||'$result
#数据库最大并发连接数   18.06.20