#!/bin/bash

database=$1
a=`db2 connect to $database;db2 "select TBSP_NAME,TBSP_UTILIZATION_PERCENT,TBSP_FREE_PAGES from sysibmadm.TBSP_UTILIZATION where TBSP_NAME not in ('TEMPSPACE1')";`
a=`echo "$a"|awk '{L[NR]=$0}END{for (i=11;i<=NR-2;i++){print L[i]}}'`
a=($a)
#echo ${#a[@]}
#echo "$a"
len=${#a[*]}
#for((i=0;i<$len;i++))
#do
#  if  (( (i+1)%3==0 )) ;then
#    echo -e ${a[$i]}
#  else
#    echo -e ${a[$i]} "\c"
#  fi
#done

for ((i=0;i<$len;i=i+3))
do
    m=i+1
    n=i+2
    echo '""||'$database'-'${a[$i]}"||APM-DB2-06-06||"${a[$n]}
    echo '""||'$database'-'${a[$i]}"||APM-DB2-06-10||"${a[$m]}
done
