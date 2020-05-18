#!/bin/bash

ctime=`date +%s000`
v_cpu_idle=`vmstat 1 2|sed -n 4p|awk '{print $15}'`
v_cpu_percent=`echo "scale=0;100-${v_cpu_idle}"|bc`
cpucheckfile=$HOME/cpucheck.txt
if [[ -f $cpucheckfile ]];then
  :
else
  `touch $cpucheckfile`
fi
if [[ -s $cpucheckfile ]];then
  firstline=`sed -n '1p' $cpucheckfile`
  time=`echo $firstline|awk -F":" '{print $1}'`
  value=`echo $firstline|awk -F":" '{print $2}'`
  #search min value
  minvalue=`awk -F":" '/min/{print $2}' $cpucheckfile`
  
  timeinc=`expr $ctime - $time`
  if [[ $timeinc -gt 1800000 ]];then
    if [[ $v_cpu_percent -le $minvalue ]];then
      `sed 's/min//g' $cpucheckfile|awk '{print>"'$cpucheckfile'"}'`
      `echo $ctime:$v_cpu_percent:'min'>>$cpucheckfile`
      `awk  'NR>1{print>"'$cpucheckfile'"}' $cpucheckfile` 
    else
      `echo $ctime:$v_cpu_percent:>>$cpucheckfile`
      `awk  'NR>1{print>"'$cpucheckfile'"}' $cpucheckfile`
    fi
  else
    if [[ $v_cpu_percent -le $minvalue ]];then
      `sed 's/min//g' $cpucheckfile|awk '{print>"'$cpucheckfile'"}'`
      `echo $ctime:$v_cpu_percent:'min'>>$cpucheckfile`
    else
      `echo $ctime:$v_cpu_percent:>>$cpucheckfile`
    fi
  fi
else
  `echo $ctime:$v_cpu_percent:'min'>>$cpucheckfile`
fi
if [[ $v_cpu_percent -gt 50 ]];then
  UP_CPUUtilDelta=`expr $v_cpu_percent - $minvalue`
  if [[ $UP_CPUUtilDelta -gt 20 ]];then
    echo '""||""||UP_CPUUtilStat||1'
    #echo '""||""||CPU usage higher than 50% and increase abnormal||''increase='$inc'&&&usage='$v_cpu_percent
  else
    echo '""||""||UP_CPUUtilStat||0'
  fi
else
  echo '""||""||UP_CPUUtilStat||0'
fi
#sign as min ,then next value compare with min if < instead else sign - ...
