# coding: utf-8

"""M个球编号1-M，顺时针围成一个圈，从1号球开始顺时针数，每数到第N个球，将球拿出圈外，求最后剩下的一个球的编号。"""


def get(m, n):
    ball = range(m + 1)[1:]  # 生成一个列表，[1:] 去掉0

    while len(ball) > 1:  # 开始循环拿出球第N个球（删除第N-1索引）
        print ball
        if n <= len(ball):  # 第N个球 是在列表长度内的好处理，直接删掉对应的N-1索引。 然后
            del ball[n - 1]  # 删掉对应的N-1索引
            ball = ball[n - 1:] + ball[:n - 1] # 把N-1索引前的序列放到后面，重新组成一个列表。如果画图可以理解为，下次指针的初始位置变为N
        else:                # 第N个球 是在列表长度以外的情况，其实就是饶了几圈的问题。用%取余数，可以得到需要删除的索引位置
            index = (n % len(ball)) - 1
            # print index
            del ball[index]
            ball = ball[index:] + ball[:index] if index != -1 else ball  # 同上解释，但是这里要注意，如果%整除了，就说明需要删除最后一位索引，索引为-1，也刚好符合，但是不需要重组列表了，

    print ball


get(10, 3)

