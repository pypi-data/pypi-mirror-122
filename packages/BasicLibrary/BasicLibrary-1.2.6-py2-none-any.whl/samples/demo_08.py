# 输入一个数是否为质数
def is_prime(n):
    if n<=1:
        return False
    for i in range(2,n):
        if n % i == 0:
            return False
    return True

# a = is_prime(5)
# print(a)


