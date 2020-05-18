#!/bin/bash


a=`db2level|grep Informational;`
result=`echo "$a"|awk -F"\"" '{print $2}'`

echo '""||""||PM-DB2-version||'$result
#版本   18.06.19