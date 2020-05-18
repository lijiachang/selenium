import time


time_now_HM = time.strftime('%H.%M', time.localtime(int(round(time.time() * 1000)) / 1000))
end_time =time_now_HM[:3]

print  end_time
a =23
print type(a)
print 23/60

t = time.time()
haomiao = (int(round(t * 1000)))+5055933

timeStamp = float(haomiao/1000)
timeArray = time.localtime(timeStamp)
otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
print type(otherStyleTime)

c = "20.59"
if not c.endswith("60"):
    print "yes"