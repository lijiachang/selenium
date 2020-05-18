# coding=utf-8

from urllib import urlopen
import sys

#
try:
    url = sys.argv[1]
except:
    print("||%s||FM-PLUGIN-EXECUTE-FAILED||Please usage:%s URL" % (sys.argv[0], sys.argv[0]))
    sys.exit(0)
try:
    request_code = urlopen(url).getcode()
except IOError as e:
    if "Temporary failure in name resolution" in str(e):
        print("||%s||FM-PLUGIN-EXECUTE-FAILED||Please check your DNS or Network!" % sys.argv[0])
    if "Name or service not known" in str(e):
        print("||||PM-URL-status||1")
    else:
        print("||%s||FM-PLUGIN-EXECUTE-FAILED||%s" % (sys.argv[0], e))
    sys.exit(0)
status = "0" if request_code == 200 else "1"
print("||||PM-URL-status||" + status)