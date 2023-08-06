#!usr/bin/env python
# encoding: utf-8
# @author: cherry
# @file:demo_04.py
# @time:2021/1/25 11:38 上午

# a=123 输出a=321
# b=012 输出b=21
# c=-123 输出c=-321
a = '-123'
a1 = str(a)
print(a[0] + a1[4:0:-1])


# d = [1,2,3,3,3,5,6,4,4] 去除重复数字
# d = [1,2,3,3,3,5,6,4,4]
# d1 = []
# for i in range(len(d)):
#     if d[i] not in d1:
#         d1.append(d[i])
# print(d1)