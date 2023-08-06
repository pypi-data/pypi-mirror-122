#!usr/bin/env python
# encoding: utf-8
# @author: cherry
# @file:demo_03.py
# @time:2021/1/18 10:37 上午

# 用冒泡排序法实现对[88,44,34,44,-20,72]进行降序排序
lista = [88,44,34,44,-20,72]
# lista.sort()
# lista.reverse()
for i in range(1,len(lista)):
    for j in range(len(lista)-i):
        if lista[j] < lista[j+1] :
            lista[j],lista[j+1] = lista[j+1],lista[j]
print(lista)