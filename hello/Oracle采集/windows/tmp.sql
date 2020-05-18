set linesize 32767
set pagesize 9999
set numwidth 40
SELECT   resource_name,
                     current_utilization,
                     max_utilization,
                     LIMIT,
                     ROUND (current_utilization / LIMIT * 100) || '%' rate,
                     ROUND (max_utilization / LIMIT * 100) || '%' maxrate
              FROM   (SELECT   resource_name,
                               current_utilization,
                               max_utilization,
                               TO_NUMBER (initial_allocation) LIMIT
                        FROM   v$resource_limit
                       WHERE   resource_name IN ('sessions')
                               AND max_utilization > 0);
exit