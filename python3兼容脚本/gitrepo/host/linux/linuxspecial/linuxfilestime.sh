#!/bin/bash
#
filename=$1
if [[ "$#" -eq 0 ]];then
  echo "Usage:$0 filename"
  exit 2
fi
filelog=$HOME/filelog.txt
if [[ -f $filelog ]];then
  :
else
  touch $filelog
fi
function GetFileUpdateTime_AIX
{
  filetime=`stat -c %Y $filename`
  echo $filename::$filetime'000'>$filelog;
}
function GetFileUpdateTime_AIX1
{
  local oldtime=`cat $filelog|awk -F"::" '{print $2}'`;
  newfiletime=`stat -c %Y $filename`
  echo $filename::$newfiletime'000'>$filelog;
  if [[ $newfiletime'000' -eq $oldtime ]];then
    echo '""||'$filename'||FileUpdateState||0'
  else
    echo '""||'$filename'||FileUpdateState||1'
    #echo '""||'$filename'||File was updated||time='$newfiletime'000'
  fi
}

if [[ -s $filelog ]];then
  GetFileUpdateTime_AIX1;
else
  GetFileUpdateTime_AIX;
fi
