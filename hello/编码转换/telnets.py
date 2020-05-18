import telnetlib
import time
import sys

IP = sys.argv[1]
port = sys.argv[2]

while True:
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    try:
        telnetlib.Telnet(host=IP, port=port, timeout=5)
    except Exception as e:
        print e
    else:
        print "status OK:" + IP + ":" + str(port)
    time.sleep(10)
