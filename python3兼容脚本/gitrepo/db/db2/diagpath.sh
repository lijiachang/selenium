#!/bin/bash

a=`db2 get dbm cfg|grep DIAGPATH;`
result=`echo "$a"|awk -F"= " '{print $2}'`

echo '""||""||PM-DB2-diagpath||'$result
#诊断日志路径   18.06.19