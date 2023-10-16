import os
import hash as hs


num = os.cpu_count()
print(num)


def proc(i, A, B, C, D, hash):
    for j in range(0, 2**32):
        first = bin(j)[2:].rjust(32, "0")
        second = bin(i - 1)[2:].rjust(32, "0")
        str1 = str = first + second
        str = hs.adding_f(str)
        k = hs.func(str, A, B, C, D, hash, str1)
        if k is True:
            return True


def main():
    hash = 0x9bdccc5603b83d8e899a18577373b77b
    num = os.cpu_count()
    t = 0
    A = hs.A
    B = hs.B
    C = hs.C
    D = hs.D
    num = 2
    for i in range(1, num):
            proc(i, A, B, C, D, hash)


main()