#!usr/bin/env python
# encoding: utf-8
# @author: cherry
# @file:demo_02.py
# @time:2021/1/15 11:27 上午

# 求1...10所有偶数之和 2，4，6，8，10
# a = range(2,11)
# sum = 0
# for i in a:
#     if i % 2 == 0:
#         sum = sum + i
#     i += 1
# print(sum)


#有一个列表:[80,13,66,202,0,-13] 把列表中的最大数和列表的第一个元素交换位置
# lista = [80,13,66,202,0,-13]
# print(lista[0])
# print(max(lista))

# for i in range(len(lista)):
#     print(lista[i])



# 用冒泡排序法实现对[88,44,34,44,-20,72]进行降序排序
# lista = [88,44,34,44,-20,72]
# # print(range(len(lista))) 0,1,2,3,4
# for j in range(len(lista)-2):
#     for i in range(len(lista)-1):
#         if lista[i] < lista[i+1] :
#             lista[i],lista[i+1] = lista[i+1],lista[i]
# print(lista)


# 用选择排序法实现对[88,44,34,44,-20,72]进行升序排序
lista = [21,88,44,34,44,-20,72]
# print(range(len(lista)))
# 0,1,2,3,4,5
# for j in range(1,len(lista)):
#     for i in range(len(lista)-j):
#         if lista[i] > lista[i+1] :
#             lista[i],lista[i+1] = lista[i+1],lista[i]
# print(lista)
lista.sort()
# lista.reverse()
print(lista)


