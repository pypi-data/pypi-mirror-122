#!usr/bin/env python
# encoding: utf-8
# @author: cherry
# @file:demo_05.py
# @time:2021/2/4 10:04 上午

# 中位数是有序序列最中间的那个数。如果序列的长度是偶数，则没有最中间的数；此时中位数是最中间的两个数的平均数。
#
# 例如：
#
# [2,3,4]，中位数是 3
# [2,3]，中位数是 (2 + 3) / 2 = 2.5
# 给你一个数组 nums，有一个长度为 k 的窗口从最左端滑动到最右端。窗口中有 k 个数，每次窗口向右移动 1 位。你的任务是找出每次窗口移动后得到的新窗口中元素的中位数，并输出由它们组成的数组。
# 示例：
#
# 给出 nums = [1,3,-1,-3,5,3,6,7]，以及 k = 3。
#
# 窗口位置                      中位数
# ---------------               -----
# [1  3  -1] -3  5  3  6  7       1
#  1 [3  -1  -3] 5  3  6  7      -1
#  1  3 [-1  -3  5] 3  6  7      -1
#  1  3  -1 [-3  5  3] 6  7       3
#  1  3  -1  -3 [5  3  6] 7       5
#  1  3  -1  -3  5 [3  6  7]      6
#  因此，返回该滑动窗口的中位数数组 [1,-1,-1,3,5,6]。
#
#  
#
# 提示：
# 你可以假设 k 始终有效，即：k 始终小于输入的非空数组的元素个数。
# 与真实值误差在 10 ^ -5 以内的答案将被视作正确答案。

class Solution(object):
    def medianSlidingWindow(self, nums, k):
        if k % 2 != 0:
            nums_mid = []
            for i in range(len(nums)-k+1):
                numss = []
                numss.extend(nums[i:i+k])
                # print(numss)
                numss.sort()
                nums_mid.append(numss[k/2])
        else:
            nums_mid = []
            for i in range(len(nums) - k + 1):
                numss = []
                numss.extend(nums[i:i + k])
                # print(numss)
                numss.sort()
                # print(numss)
                sum = numss[int(k / 2) - 1] + numss[int(k / 2)]
                nums_mid.append(float(sum) / 2)
        return nums_mid


nums = [7,3,9,9,1,34,5]
k = 6
print(max(nums))
# solution = Solution().medianSlidingWindow(nums,k)
# print(solution)
