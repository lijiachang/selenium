set define off
-- DELETE FROM ua_plugin_info WHERE scriptName = 'databasestatus.sh' and SCRIPTPATH ='db/db2';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResDB2Instance','db/db2','databasestatus.sh','数据库状态','db/db2/databasestatus.sh','linux','root','shell','1528781699871','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'db/db2/databasestatus.sh';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('db/db2/databasestatus.sh','instance','数据库名称','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'appls_cur_cons.sh' and SCRIPTPATH ='db/db2';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResDB2Instance','db/db2','appls_cur_cons.sh','注册的代理程序数','db/db2/appls_cur_cons.sh','linux','root','shell','1528781699885','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'db/db2/appls_cur_cons.sh';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('db/db2/appls_cur_cons.sh','instance','数据库名称','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'appls_in_cons.sh' and SCRIPTPATH ='db/db2';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResDB2Instance','db/db2','appls_in_cons.sh','当前执行的应用程序数','db/db2/appls_in_cons.sh','linux','root','shell','1528781699897','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'db/db2/appls_in_cons.sh';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('db/db2/appls_in_cons.sh','instance','数据库名称','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'locks_waitings.sh' and SCRIPTPATH ='db/db2';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResDB2Instance','db/db2','locks_waitings.sh','等待锁定的当前代理程序数','db/db2/locks_waitings.sh','linux','root','shell','1528781699906','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'db/db2/locks_waitings.sh';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('db/db2/locks_waitings.sh','instance','数据库名称','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'agentreg.sh' and SCRIPTPATH ='db/db2';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResDB2Instance','db/db2','agentreg.sh','连接到数据库的会话数量','db/db2/agentreg.sh','linux','root','shell','1528781699912','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'db/db2/agentreg.sh';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('db/db2/agentreg.sh','instance','数据库名称','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'localconnections.sh' and SCRIPTPATH ='db/db2';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResDB2Instance','db/db2','localconnections.sh','本地连接数','db/db2/localconnections.sh','linux','root','shell','1528781699920','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'db/db2/localconnections.sh';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('db/db2/localconnections.sh','instance','数据库名称','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'local_cons_in_exec.sh' and SCRIPTPATH ='db/db2';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResDB2Instance','db/db2','local_cons_in_exec.sh','在数据库管理器中执行的本地连接数','db/db2/local_cons_in_exec.sh','linux','root','shell','1528781699933','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'db/db2/local_cons_in_exec.sh';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('db/db2/local_cons_in_exec.sh','instance','数据库名称','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'remotconnections.sh' and SCRIPTPATH ='db/db2';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResDB2Instance','db/db2','remotconnections.sh','与数据库管理器的远程连接','db/db2/remotconnections.sh','linux','root','shell','1528781699942','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'db/db2/remotconnections.sh';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('db/db2/remotconnections.sh','instance','数据库名称','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'rem_cons_in_exec.sh' and SCRIPTPATH ='db/db2';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResDB2Instance','db/db2','rem_cons_in_exec.sh','在数据库管理器中执行的远程连接数','db/db2/rem_cons_in_exec.sh','linux','root','shell','1528781699955','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'db/db2/rem_cons_in_exec.sh';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('db/db2/rem_cons_in_exec.sh','instance','数据库名称','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'deadlocks.sh' and SCRIPTPATH ='db/db2';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResDB2Instance','db/db2','deadlocks.sh','发生的死锁总数','db/db2/deadlocks.sh','linux','root','shell','1528781699963','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'db/db2/deadlocks.sh';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('db/db2/deadlocks.sh','instance','数据库名称','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'lock_escals.sh' and SCRIPTPATH ='db/db2';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResDB2Instance','db/db2','lock_escals.sh','锁定已从若干行锁定升级至表锁定的次数','db/db2/lock_escals.sh','linux','root','shell','1528781699971','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'db/db2/lock_escals.sh';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('db/db2/lock_escals.sh','instance','数据库名称','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'lock_waits.sh' and SCRIPTPATH ='db/db2';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResDB2Instance','db/db2','lock_waits.sh','当前挂起的锁定数目','db/db2/lock_waits.sh','linux','root','shell','1528781699980','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'db/db2/lock_waits.sh';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('db/db2/lock_waits.sh','instance','数据库名称','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'bpindexhitratio.sh' and SCRIPTPATH ='db/db2';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResDB2Instance','db/db2','bpindexhitratio.sh','索引读命中率','db/db2/bpindexhitratio.sh','linux','root','shell','1528781699988','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'db/db2/bpindexhitratio.sh';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('db/db2/bpindexhitratio.sh','instance','数据库名称','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'bpdatahitratio.sh' and SCRIPTPATH ='db/db2';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResDB2Instance','db/db2','bpdatahitratio.sh','数据命中率','db/db2/bpdatahitratio.sh','linux','root','shell','1528781699999','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'db/db2/bpdatahitratio.sh';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('db/db2/bpdatahitratio.sh','instance','数据库名称','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'pkg_cache_lookups.sh' and SCRIPTPATH ='db/db2';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResDB2Instance','db/db2','pkg_cache_lookups.sh','程序包高速缓存命中数','db/db2/pkg_cache_lookups.sh','linux','root','shell','1528781700009','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'db/db2/pkg_cache_lookups.sh';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('db/db2/pkg_cache_lookups.sh','instance','数据库名称','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'pkg_cache_num_overflows.sh' and SCRIPTPATH ='db/db2';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResDB2Instance','db/db2','pkg_cache_num_overflows.sh','程序包高速缓存溢出数量','db/db2/pkg_cache_num_overflows.sh','linux','root','shell','1528781700018','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'db/db2/pkg_cache_num_overflows.sh';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('db/db2/pkg_cache_num_overflows.sh','instance','数据库名称','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'cat_cache_lookups.sh' and SCRIPTPATH ='db/db2';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResDB2Instance','db/db2','cat_cache_lookups.sh','目录高速缓存命中数','db/db2/cat_cache_lookups.sh','linux','root','shell','1528781700028','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'db/db2/cat_cache_lookups.sh';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('db/db2/cat_cache_lookups.sh','instance','数据库名称','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'cat_cache_overflows.sh' and SCRIPTPATH ='db/db2';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResDB2Instance','db/db2','cat_cache_overflows.sh','目录高速缓存溢出数量','db/db2/cat_cache_overflows.sh','linux','root','shell','1528781700037','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'db/db2/cat_cache_overflows.sh';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('db/db2/cat_cache_overflows.sh','instance','数据库名称','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'totallogavil.sh' and SCRIPTPATH ='db/db2';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResDB2Instance','db/db2','totallogavil.sh','可用的总日志空间','db/db2/totallogavil.sh','linux','root','shell','1528781700044','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'db/db2/totallogavil.sh';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('db/db2/totallogavil.sh','instance','数据库名称','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'pcttotallogspused.sh' and SCRIPTPATH ='db/db2';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResDB2Instance','db/db2','pcttotallogspused.sh','总日志空间使用率','db/db2/pcttotallogspused.sh','linux','root','shell','1528781700050','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'db/db2/pcttotallogspused.sh';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('db/db2/pcttotallogspused.sh','instance','数据库名称','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'tbsize.sh' and SCRIPTPATH ='db/db2';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResDB2Instance','db/db2','tbsize.sh','空闲页数和表空间使用率','db/db2/tbsize.sh','linux','root','shell','1528781700057','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'db/db2/tbsize.sh';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('db/db2/tbsize.sh','instance','数据库名称','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'catcachepcent.sh' and SCRIPTPATH ='db/db2';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResDB2Instance','db/db2','catcachepcent.sh','目录高速缓存命中数','db/db2/catcachepcent.sh','linux','root','shell','1528781700064','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'db/db2/catcachepcent.sh';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('db/db2/catcachepcent.sh','instance','数据库名称','varchar(50)','',1,0,'','1','1',''); 

-- DELETE FROM ua_plugin_info WHERE scriptName = 'pkgcacheover.sh' and SCRIPTPATH ='db/db2';
INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES ('ResDB2Instance','db/db2','pkgcacheover.sh','程序包高速缓存溢出数量','db/db2/pkgcacheover.sh','linux','root','shell','1528781700071','0','1');
-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = 'db/db2/pkgcacheover.sh';
INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE, PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, VIEWSEQUENCE, NOTE) VALUES ('db/db2/pkgcacheover.sh','instance','数据库名称','varchar(50)','',1,0,'','1','1',''); 

commit;