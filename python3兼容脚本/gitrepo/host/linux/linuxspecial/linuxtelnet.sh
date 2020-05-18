#!/bin/bash

####$1--ip,$2--port####
if [[ $# -ne 2 ]];then
  echo "||$0||FM-PLUGIN-EXECUTE-FAILED||Please usage:$0 [ip] [port]"
  exit 2
fi
a=`
telnet $1 $2<<@@@ 2>&1
quit
@@@
`

if [[ $? -eq 0 ]];then
  keyword=$(echo "$a"|grep "Escape character"|wc -l)
  if [[ $keyword -eq 1 ]];then
    echo '""||connect state to ' $1 $2'||PM-telnet-state||0'
  else
    echo '""||connect state to ' $1 $2'||PM-telnet-state||1'
  fi
else
  #values=$(echo "$a"|sed s/[[:space:]]//g)
  values=$(echo "$a"|head -n 1)
  echo "||$0||FM-PLUGIN-EXECUTE-FAILED||$values"
fi
