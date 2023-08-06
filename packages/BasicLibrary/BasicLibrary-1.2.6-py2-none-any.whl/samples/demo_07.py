# a=123 输出a=321
# b=012 输出b=21
# c=-123 输出c=-321

class A:
    def __init__(self):
        print('A')

class B(A):
    def __init__(self):
        print('B')
        super().__init__()

class C(A):
    def __init__(self):
        print('C')
        super().__init__()

class D(B,C):
    def __init__(self):
        print('D')
        super().__init__()

D()