# coding=utf-8
from pysnmp.hlapi import *

errorIndication, errorStatus, errorIndex, varBinds = next(
    getCmd(SnmpEngine(),
           CommunityData('public', mpModel=1),
           UdpTransportTarget(('192.168.120.104', 161)),
           ContextData(),
           ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))  # 0是索引
)

if errorIndication:
    print(errorIndication)
elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
else:
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))

a = getCmd(SnmpEngine(),
           CommunityData('public', mpModel=1),
           UdpTransportTarget(('192.168.120.104', 161)),
           ContextData(),
           ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysUpTime', 0)))
for i in a:
    for x in i:
        if x == 0 or x is None:
            continue
        for s in x:
            print "result:",s.prettyPrint()


