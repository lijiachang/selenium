init = {"A": 10, "B": 7, "C": 5, "D": 4}

for x in xrange(120):
    max_value = max(init.values())
    for i in init:
        init[i] = init[i] + 1 if init[i] != max_value else init[i] - 3

print sorted(init.items(), key=lambda d: d[0])


sum = 0
for i in range(100 + 1):
    sum+=i
print sum


def digui(n):
    if n >0:

        return n + digui(n-1)
    else:
        return 0


print digui(100)

aaa = ["a", "b", "c", "d"]
for x,y in enumerate(aaa):
    print x,y