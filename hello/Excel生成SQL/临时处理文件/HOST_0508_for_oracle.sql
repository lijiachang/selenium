set define off
-- DELETE FROM ua_plugin_info WHERE scriptName = 'procnumber.py' and SCRIPTPATH ='host/linux/proc';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/linux/proc','procnumber.py','同名进程数','host/linux/proc/procnumber.py','linux','root','python','1525760212348','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/linux/proc/procnumber.py';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/linux/proc/procnumber.py','procName','进程关键字','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'procutil.py' and SCRIPTPATH ='host/linux/proc';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/linux/proc','procutil.py','进程资源占用','host/linux/proc/procutil.py','linux','root','python','1525760212358','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/linux/proc/procutil.py';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/linux/proc/procutil.py','procName','进程关键字','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'procstatisc.py' and SCRIPTPATH ='host/linux/proc';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/linux/proc','procstatisc.py','进程数监控','host/linux/proc/procstatisc.py','linux','root','python','1525760212368','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'logatti.py' and SCRIPTPATH ='host/linux/log';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/linux/log','logatti.py','日志文件信息','host/linux/log/logatti.py','linux','root','python','1525760212378','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/linux/log/logatti.py';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/linux/log/logatti.py','logFilePath','日志路径及含文件名','varchar(200)','',1,0,'','1','1','支持通配符和正则表达式，保持监控最新的文件'); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'logkeyword.py' and SCRIPTPATH ='host/linux/log';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/linux/log','logkeyword.py','日志匹配关键字个数','host/linux/log/logkeyword.py','linux','root','python','1525760212388','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/linux/log/logkeyword.py';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/linux/log/logkeyword.py','logFilePath','日志路径及含文件名','varchar(200)','',1,0,'','1','1','支持通配符和正则表达式，保持监控最新的文件'); 

-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/linux/log/logkeyword.py';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/linux/log/logkeyword.py','logKeyWords','关键字','varchar(200)','',1,0,'','2','2','支持空格、正则表达式和与或非，比如fatal&&ORA-*&&(\d{14})'); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'esbnumber.py' and SCRIPTPATH ='host/linux/tcpport';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/linux/tcpport','esbnumber.py','ESTABLISHED连接数','host/linux/tcpport/esbnumber.py','linux','root','python','1525760212414','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/linux/tcpport/esbnumber.py';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/linux/tcpport/esbnumber.py','dip','目标地址','varchar(50)','',0,0,'','1','1',''); 

-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/linux/tcpport/esbnumber.py';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/linux/tcpport/esbnumber.py','dport','目标端口','int','',0,0,'','2','2',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'icmpstatus.py' and SCRIPTPATH ='host/linux/tcpport';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/linux/tcpport','icmpstatus.py','指定ICMP连接状态','host/linux/tcpport/icmpstatus.py','linux','root','python','1525760212436','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/linux/tcpport/icmpstatus.py';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/linux/tcpport/icmpstatus.py','ip','ip地址','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/linux/tcpport/icmpstatus.py';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/linux/tcpport/icmpstatus.py','count','ping的次数','int','',1,0,'','2','2',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'lisnumber.py' and SCRIPTPATH ='host/linux/tcpport';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/linux/tcpport','lisnumber.py','LISTEN端口数','host/linux/tcpport/lisnumber.py','linux','root','python','1525760212459','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/linux/tcpport/lisnumber.py';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/linux/tcpport/lisnumber.py','portnum','监控的端口号','int','',1,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'tcpstatus.py' and SCRIPTPATH ='host/linux/tcpport';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/linux/tcpport','tcpstatus.py','指定TCP连接状态','host/linux/tcpport/tcpstatus.py','linux','root','python','1525760212471','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/linux/tcpport/tcpstatus.py';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/linux/tcpport/tcpstatus.py','dip','目标地址','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/linux/tcpport/tcpstatus.py';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/linux/tcpport/tcpstatus.py','dport','目标端口','int','',1,0,'','2','2',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'udpstatus.py' and SCRIPTPATH ='host/linux/tcpport';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/linux/tcpport','udpstatus.py','指定UDP连接状态','host/linux/tcpport/udpstatus.py','linux','root','python','1525760212484','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/linux/tcpport/udpstatus.py';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/linux/tcpport/udpstatus.py','dip','目标地址','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/linux/tcpport/udpstatus.py';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/linux/tcpport/udpstatus.py','dport','目标端口','int','',1,0,'','2','2',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'cpuload.sh' and SCRIPTPATH ='host/linux';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/linux','cpuload.sh','Cpuload负载监控','host/linux/cpuload.sh','linux','root','shell','1525760212496','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'cpu.py' and SCRIPTPATH ='host/linux';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/linux','cpu.py','Cpu资源监控','host/linux/cpu.py','linux','root','python','1525760212503','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'diskiocheck.py' and SCRIPTPATH ='host/linux';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/linux','diskiocheck.py','diskio监控','host/linux/diskiocheck.py','linux','root','python','1525760212512','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'filesysinode.py' and SCRIPTPATH ='host/linux';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/linux','filesysinode.py','文件系统inode监控','host/linux/filesysinode.py','linux','root','python','1525760212519','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'filesystem.py' and SCRIPTPATH ='host/linux';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/linux','filesystem.py','文件系统监控','host/linux/filesystem.py','linux','root','python','1525760212526','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'diskio.sh' and SCRIPTPATH ='host/linux';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/linux','diskio.sh','磁盘使用率','host/linux/diskio.sh','linux','root','shell','1525760212532','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'kernalcheck.py' and SCRIPTPATH ='host/linux';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/linux','kernalcheck.py','linux内核监控','host/linux/kernalcheck.py','linux','root','python','1525760212539','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'mem.py' and SCRIPTPATH ='host/linux';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/linux','mem.py','内存资源监控','host/linux/mem.py','linux','root','python','1525760212545','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'aixcpu.py' and SCRIPTPATH ='host/aix/perf';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/aix/perf','aixcpu.py','Cpu资源监控','host/aix/perf/aixcpu.py','aix','root','python','1525760212550','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'aixmem.py' and SCRIPTPATH ='host/aix/perf';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/aix/perf','aixmem.py','内存资源监控','host/aix/perf/aixmem.py','aix','root','python','1525760212557','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'aixfilesys.py' and SCRIPTPATH ='host/aix/perf';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/aix/perf','aixfilesys.py','文件系统监控','host/aix/perf/aixfilesys.py','aix','root','python','1525760212564','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'logatti.py' and SCRIPTPATH ='host/aix/log';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/aix/log','logatti.py','日志文件信息','host/aix/log/logatti.py','aix','root','python','1525760212570','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/aix/log/logatti.py';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/aix/log/logatti.py','logFilePath','日志路径及含文件名','varchar(200)','',1,0,'','1','1','支持通配符和正则表达式，保持监控最新的文件'); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'logkeyword.py' and SCRIPTPATH ='host/aix/log';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/aix/log','logkeyword.py','日志匹配关键字个数','host/aix/log/logkeyword.py','aix','root','python','1525760212576','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/aix/log/logkeyword.py';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/aix/log/logkeyword.py','logFilePath','日志路径及含文件名','varchar(200)','',1,0,'','1','1','支持通配符和正则表达式，保持监控最新的文件'); 

-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/aix/log/logkeyword.py';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/aix/log/logkeyword.py','logKeyWords','关键字','varchar(200)','',1,0,'','2','2','支持空格、正则表达式和与或非，比如fatal&&ORA-*&&(\d{14})'); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'procnumber.py' and SCRIPTPATH ='host/aix/proc';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/aix/proc','procnumber.py','同名进程数','host/aix/proc/procnumber.py','aix','root','python','1525760212587','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/aix/proc/procnumber.py';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/aix/proc/procnumber.py','procName','进程关键字','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'procestatistic.py' and SCRIPTPATH ='host/aix/proc';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/aix/proc','procestatistic.py','进程数监控','host/aix/proc/procestatistic.py','aix','root','python','1525760212593','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'procutil.py' and SCRIPTPATH ='host/aix/proc';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/aix/proc','procutil.py','进程资源占用','host/aix/proc/procutil.py','aix','root','python','1525760212599','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/aix/proc/procutil.py';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/aix/proc/procutil.py','procName','进程关键字','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'esbnumber.py' and SCRIPTPATH ='host/aix/tcpport';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/aix/tcpport','esbnumber.py','ESTABLISHED连接数','host/aix/tcpport/esbnumber.py','aix','root','python','1525760212605','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/aix/tcpport/esbnumber.py';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/aix/tcpport/esbnumber.py','dip','目标地址','varchar(50)','',0,0,'','1','1',''); 

-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/aix/tcpport/esbnumber.py';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/aix/tcpport/esbnumber.py','dport','目标端口','int','',0,0,'','2','2',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'icmpstatus.py' and SCRIPTPATH ='host/aix/tcpport';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/aix/tcpport','icmpstatus.py','指定ICMP连接状态','host/aix/tcpport/icmpstatus.py','aix','root','python','1525760212620','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/aix/tcpport/icmpstatus.py';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/aix/tcpport/icmpstatus.py','ip','ip地址','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/aix/tcpport/icmpstatus.py';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/aix/tcpport/icmpstatus.py','count','ping的次数','int','',1,0,'','2','2',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'lisnumber.py' and SCRIPTPATH ='host/aix/tcpport';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/aix/tcpport','lisnumber.py','LISTEN端口数','host/aix/tcpport/lisnumber.py','aix','root','python','1525760212632','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/aix/tcpport/lisnumber.py';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/aix/tcpport/lisnumber.py','portnum','监控的端口号','int','',1,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'tcpstatus.py' and SCRIPTPATH ='host/aix/tcpport';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/aix/tcpport','tcpstatus.py','指定TCP连接状态','host/aix/tcpport/tcpstatus.py','aix','root','python','1525760212641','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/aix/tcpport/tcpstatus.py';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/aix/tcpport/tcpstatus.py','dip','目标地址','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/aix/tcpport/tcpstatus.py';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/aix/tcpport/tcpstatus.py','dport','目标端口','int','',1,0,'','2','2',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'cpu.sh' and SCRIPTPATH ='host/hp-ux';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/hp-ux','cpu.sh','Cpu资源监控','host/hp-ux/cpu.sh','hp-ux','root','shell','1525760212652','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'cpuload.sh' and SCRIPTPATH ='host/hp-ux';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/hp-ux','cpuload.sh','Cpuload负载监控','host/hp-ux/cpuload.sh','hp-ux','root','shell','1525760212658','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'diskio.sh' and SCRIPTPATH ='host/hp-ux';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/hp-ux','diskio.sh','diskio监控','host/hp-ux/diskio.sh','hp-ux','root','shell','1525760212663','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'filesys.sh' and SCRIPTPATH ='host/hp-ux';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/hp-ux','filesys.sh','文件系统监控','host/hp-ux/filesys.sh','hp-ux','root','shell','1525760212669','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'kerna.sh' and SCRIPTPATH ='host/hp-ux';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/hp-ux','kerna.sh','主机内核监控-KERNAL','host/hp-ux/kerna.sh','hp-ux','root','shell','1525760212675','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'mem.sh' and SCRIPTPATH ='host/hp-ux';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/hp-ux','mem.sh','内存资源监控','host/hp-ux/mem.sh','hp-ux','root','shell','1525760212680','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'pageio.sh' and SCRIPTPATH ='host/hp-ux';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/hp-ux','pageio.sh','换页率','host/hp-ux/pageio.sh','hp-ux','root','shell','1525760212685','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'fileinode.sh' and SCRIPTPATH ='host/hp-ux';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/hp-ux','fileinode.sh','文件系统inode监控','host/hp-ux/fileinode.sh','hp-ux','root','shell','1525760212690','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'esbnum.sh' and SCRIPTPATH ='host/hp-ux/tcpport';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/hp-ux/tcpport','esbnum.sh','ESTABLISHED连接数','host/hp-ux/tcpport/esbnum.sh','hp-ux','root','shell','1525760212697','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/hp-ux/tcpport/esbnum.sh';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/hp-ux/tcpport/esbnum.sh','ip','目的端ip','varchar(50)','',0,0,'','1','1',''); 

-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/hp-ux/tcpport/esbnum.sh';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/hp-ux/tcpport/esbnum.sh','port','目的端端口','int','',0,0,'','2','2',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'lisnum.sh' and SCRIPTPATH ='host/hp-ux/tcpport';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/hp-ux/tcpport','lisnum.sh','LISTEN端口数','host/hp-ux/tcpport/lisnum.sh','hp-ux','root','shell','1525760212711','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/hp-ux/tcpport/lisnum.sh';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/hp-ux/tcpport/lisnum.sh','port','端口号','int','',0,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'procnum.sh' and SCRIPTPATH ='host/hp-ux/proc';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/hp-ux/proc','procnum.sh','同名进程数','host/hp-ux/proc/procnum.sh','hp-ux','root','shell','1525760212718','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/hp-ux/proc/procnum.sh';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/hp-ux/proc/procnum.sh','processname','进程名','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'procstatis.sh' and SCRIPTPATH ='host/hp-ux/proc';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/hp-ux/proc','procstatis.sh','进程数监控','host/hp-ux/proc/procstatis.sh','hp-ux','root','shell','1525760212728','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'logatti.py' and SCRIPTPATH ='host/solaris/log';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/solaris/log','logatti.py','日志文件信息','host/solaris/log/logatti.py','solaris','root','python','1525760212734','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/solaris/log/logatti.py';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/solaris/log/logatti.py','logFilePath','日志路径及含文件名','varchar(200)','',1,0,'','1','1','支持通配符和正则表达式，保持监控最新的文件'); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'logkeyword.py' and SCRIPTPATH ='host/solaris/log';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/solaris/log','logkeyword.py','日志匹配关键字个数','host/solaris/log/logkeyword.py','solaris','root','python','1525760212739','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/solaris/log/logkeyword.py';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/solaris/log/logkeyword.py','logFilePath','日志路径及含文件名','varchar(200)','',1,0,'','1','1','支持通配符和正则表达式，保持监控最新的文件'); 

-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'host/solaris/log/logkeyword.py';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('host/solaris/log/logkeyword.py','logKeyWords','关键字','varchar(200)','',1,0,'','2','2','支持空格、正则表达式和与或非，比如fatal&&ORA-*&&(\d{14})'); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'cpup.py' and SCRIPTPATH ='host/solaris';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/solaris','cpup.py','Cpu资源监控','host/solaris/cpup.py','solaris','root','python','1525760212750','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'diskdev.py' and SCRIPTPATH ='host/solaris';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/solaris','diskdev.py','diskdev监控','host/solaris/diskdev.py','solaris','root','python','1525760212756','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'filesystem.py' and SCRIPTPATH ='host/solaris';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/solaris','filesystem.py','文件系统监控','host/solaris/filesystem.py','solaris','root','python','1525760212762','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'interface.py' and SCRIPTPATH ='host/solaris';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/solaris','interface.py','网卡错包数','host/solaris/interface.py','solaris','root','python','1525760212768','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'load.py' and SCRIPTPATH ='host/solaris';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/solaris','load.py','Cpuload负载监控','host/solaris/load.py','solaris','root','python','1525760212775','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'mem.py' and SCRIPTPATH ='host/solaris';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/solaris','mem.py','内存资源监控','host/solaris/mem.py','solaris','root','python','1525760212782','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'pageio.sh' and SCRIPTPATH ='host/solaris';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/solaris','pageio.sh','换页率','host/solaris/pageio.sh','solaris','root','shell','1525760212794','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'procnum.sh' and SCRIPTPATH ='host/solaris/proc';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/solaris/proc','procnum.sh','同名进程数','host/solaris/proc/procnum.sh','solaris','root','shell','1525760212800','0','1');
-- DELETE FROM ua_plugin_info WHERE scriptName = 'procstatic.sh' and SCRIPTPATH ='host/solaris/proc';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResUnix','host/solaris/proc','procstatic.sh','进程数监控','host/solaris/proc/procstatic.sh','solaris','root','shell','1525760212805','0','1');
commit;