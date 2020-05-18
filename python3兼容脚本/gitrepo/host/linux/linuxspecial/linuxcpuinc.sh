#!/bin/sh

ctime=`date +%s000`
v_cpu_idle=`vmstat 1 2|sed -n 4p|awk '{print $15}'`
v_cpu_percent=`echo "scale=0;100-${v_cpu_idle}"|bc`
cpuincfile=$HOME/cpuinc.txt
if [[ -f $cpuincfile ]];then
  :
else
  `touch $cpuincfile`
fi
if [[ -s $cpuincfile ]];then
  lastvalue=`cat $cpuincfile|awk -F":" '{print $2}'`
  inc=`expr $v_cpu_percent - $lastvalue`
  echo '""||""||PM-cpu-increment||'$inc
  echo $ctime:$v_cpu_percent>$cpuincfile
else
  echo '""||""||PM-cpu-increment||'$v_cpu_percent
  echo $ctime:$v_cpu_percent>$cpuincfile
fi

