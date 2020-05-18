#!/bin/bash


currenttime=`date +%s`
dir=$1
if [[ "$#" -eq 0 ]];then
  echo "||$0||FM-PLUGIN-EXECUTE-FAILED||Please usage:$0 [dirpath]"
  exit 2
fi

function CountFile
{
  a=`ls -l $1|wc -l`;
  a=`expr $a - 1`
  echo $a
}
function filecount
{
  sum=0
  for i in $(ls $1)
  do
    if [ -f $i ]
    then
      let sum+=1
    else
      ab=$(filecount $1"/"$i)
      sum=`expr $sum + $ab `
    fi
  done
  echo $sum
}
function counts
{
count=0
for file in `ls -l $1|tail -n +2|awk '{print $NF}'`
do
  if [ -d $1"/"$file ];then
    counts=$(filecount $1"/"$file);
    count=`expr $count + $counts`;
  else
    count=`expr $count + 1`
  fi
done
echo $count
}

ccs=0
for file in `ls -l $dir|tail -n +2|awk '{print $NF}'`
do
  if [ -d $dir"/"$file ];then
    subdir=$dir"/"$file
    cc=$(counts $subdir);
    ccs=`expr $cc + $ccs`;
  else
    ccs=`expr $ccs + 1`
  fi
done
#counts=`expr $count - 1`
echo '""||'$dir'||PM-File-Counts||'$ccs
dirsize=`du -s $dir|awk '{print $1}'|sed s/[[:space:]]//g`
echo '""||'$dir'||PM-Dir-Sizes||'$dirsize
function filetime
{
  for file in `ls $1`
  do
    if [ -d $1"/"$file ];then
      DisposeFilePathList $1"/"$file;
    else
      local filename=$file;
      local filepath=$1;
      local fileupdatetime=$(GetFileUpdateTime_AIX "$filepath");
      echo $fileupdatetime
      #timelist="$timelist $fileupdatetime"
      #echo $timelist
      #echo $fileupdatetime $filepath;
    fi
  done
}
function DisposeFilePathList
{
  timelist=""
  for file in `ls $1`
  do
    #if [ -d $1"/"$file ];then
    #  filetime $1"/"$file;
    #else
    #  local filename=$file;
    #  local filepath=$1"/"$file;
    #  local fileupdatetime=$(GetFileUpdateTime_AIX "$filepath");
    local fileupdatetime=$(filetime $1"/"$file)
      timelist="$timelist $fileupdatetime"
      #echo $timelist
      #echo $fileupdatetime $filepath;
    #fi
  done
  echo $timelist
}

function GetFileUpdateTime_AIX
{
  filetimestamp=`stat -c %Y $1`
  echo $filetimestamp
}

function EmptyOrNot
{
  ficount=`ls -l $dir|wc -l`
  if [[ $ficount -eq 1 ]];then
    echo "Dir is empty."
  else
    a=$(DisposeFilePathList $dir)
    echo $a
  fi
}
dirlastmodifiedtime=$(GetFileUpdateTime_AIX $dir)
echo '""||'$dir'||PM-Dir-last-modified-time||'`expr $currenttime - $dirlastmodifiedtime`

Tlist=($(EmptyOrNot))
if [[ ${Tlist[@]} == "Dir is empty." || ${#Tlist[@]} == 0 ]];then
  echo '""||'$dir'||PM-Latest-modified-time||NULL'
  echo '""||'$dir'||PM-Earliest-modified-time||NULL'
else
Max=${Tlist[0]}
Min=${Tlist[0]}
for i in ${Tlist[@]}
do 
  if [[ ${Max} -le $i ]];then
    Max=$i
  fi
done
for i in ${Tlist[@]}
do
  if [[ ${Min} -ge $i ]];then
    Min=$i
  fi
done
echo '""||'$dir'||PM-Latest-modified-time||'`expr $currenttime - $Max`
echo '""||'$dir'||PM-Earliest-modified-time||'`expr $currenttime - $Min`

fi
