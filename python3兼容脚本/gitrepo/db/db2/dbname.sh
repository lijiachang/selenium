#!/bin/bash

sql=`db2 list db directory|grep "Database name";`
dbnames=`echo "$sql"|awk -F"= " '{print $2}'`

arr=$(echo $dbnames|tr " " "\n")
for x in $arr;do
  echo '""||""||PM-DB2-dbname||'$x
done

#数据库名称   18.06.21