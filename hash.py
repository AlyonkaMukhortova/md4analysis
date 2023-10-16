def adding_bits(message):
    message = str(message) + '1'
    lmes = len(message)
    mod = lmes % 512
    if 448 < mod:
        mod = abs(512 - mod) + 448
    else:
        mod = abs(448 - mod)
    message = message.ljust(lmes + mod, "0")
    return(message)


def adding_f(message):
    l = bin(len(message))[2:]
    message = adding_bits(message)
    if len(l) > 64:
        l = l[:64]
    else:
        l = l.rjust(64, "0")
    message = message + l
    #print(len(message), message)
    return message


#doing blocks for hashing
def bitting(message):
    if isinstance(message, int):
        b = bin(message)[2:]

    else:
        b = bin(int.from_bytes(message.encode(), 'big'))[2:]
 
    #print(b)
    l = bin(len(b))[2:]
    message = adding_bits(b)
    if len(l) > 64:
        l = l[:64]
    else:
        l = l.rjust(64, "0")
    message = message + l
    #print(len(message), message)
    return message

"""
A = "00000001001000110100010101100111"
B = "10001001101010111100110111101111"
C = "11111110110111001011101010011000"
D = "01110110010101000011001000010000"
"""
A = bin(0x67452301)[2:]
B = bin(0xEFCDAB89)[2:]
C = bin(0x98BADCFE)[2:]
D = bin(0x10325476)[2:]

def no(X):
    no = X ^ 0b11111111111111111111111111111111
    return no


def F(X, Y, Z):
    r1 = int(X, 2) & int(Y, 2)
    r2 = no(int(X, 2)) & int(Z, 2)
    res = r1 | r2
    return res

def G(X, Y, Z):
    r1 = int(X, 2) & int(Y, 2)
    r2 = int(X, 2) & int(Z, 2)
    r3 = int(Z, 2) & int(Y, 2)
    res = r1 | r2 | r3
    return res


def H(X, Y, Z):
    res = int(X, 2) ^ int(Y, 2) ^ int(Z, 2)
    return res


def init_m(str):
    m = []
    for i in range(0, 16):
        m.append(str[i * 32: (i + 1) * 32])
    return m


def set_md4(func, a, b, c, d, x, k, s, p):
    a = ((int(a, 2) + func(b, c, d) + int(x[k], 2) + p)) % (2 ** 32) #[2: ]
    a = bin(a)[2:]
    a = a.rjust(32, '0')
    a = a[-32:]
    a = a[s:] + a[:s]
    
    return a, b, c, d


def set_md4_rev(func, a, b, c, d, x, k, s, p):
    a = a[-s:] + a[:-s]
    a1 = a
    a = ((int(a, 2) - func(b, c, d) - int(x[k], 2) - p)) % (2 ** 32)
    while(a < 0):
        a1 += '1' + a1
        a = ((int(a1, 2) - func(b, c, d) - int(x[k], 2) - p)) % (2 ** 32)

    a = bin(a)[2:]
    a = a.rjust(32, '0')
    a = a[-32:]
    return a, b, c, d


def reverse_steps (hash, X, n):
    hash = bin(hash)[2:]
    hash = hash.rjust(128, "0")
    a = hash[:32]
    b = hash[32:64]
    c = hash[64:96]
    d = hash[96:]
    b, c, d, a = set_md4_rev(H, b, c, d, a, X, 15, 15, n)
    c, d, a, b = set_md4_rev(H, c, d, a, b, X, 7, 11, n)
    d, a, b, c = set_md4_rev(H, d, a, b, c, X, 11, 9, n)
    a, b, c, d = set_md4_rev(H, a, b, c, d, X, 3, 3, n)
    b, c, d, a = set_md4_rev(H, b, c, d, a, X, 13, 15, n)
    c, d, a, b = set_md4_rev(H, c, d, a, b, X, 5, 11, n)
    d, a, b, c = set_md4_rev(H, d, a, b, c, X, 9, 9, n)
    a, b, c, d = set_md4_rev(H, a, b, c, d, X, 1, 3, n)
    b, c, d, a = set_md4_rev(H, b, c, d, a, X, 14, 15, n)
    c, d, a, b = set_md4_rev(H, c, d, a, b, X, 6, 11, n)
    d, a, b, c = set_md4_rev(H, d, a, b, c, X, 10, 9, n)
    a, b, c, d = set_md4_rev(H, a, b, c, d, X, 2, 3, n)
    b, c, d, a = set_md4_rev(H, b, c, d, a, X, 12, 15, n)
    c, d, a, b = set_md4_rev(H, c, d, a, b, X, 4, 11, n)
    d, a, b, c = set_md4_rev(H, d, a, b, c, X, 8, 9, n)

    return a, b, c, d


def md4_half_hash(a, b, c, d, X, m, n):
    a, b, c, d = set_md4(F, a, b, c, d, X, 0, 3, 0)
    d, a, b, c = set_md4(F, d, a, b, c, X, 1, 7, 0)
    c, d, a, b = set_md4(F, c, d, a, b, X, 2, 11, 0)
    b, c, d, a = set_md4(F, b, c, d, a, X, 3, 19, 0)
    a, b, c, d = set_md4(F, a, b, c, d, X, 4, 3, 0)
    d, a, b, c = set_md4(F, d, a, b, c, X, 5, 7, 0)
    c, d, a, b = set_md4(F, c, d, a, b, X, 6, 11, 0)
    b, c, d, a = set_md4(F, b, c, d, a, X, 7, 19, 0)
    a, b, c, d = set_md4(F, a, b, c, d, X, 8, 3, 0)
    d, a, b, c = set_md4(F, d, a, b, c, X, 9, 7, 0)
    c, d, a, b = set_md4(F, c, d, a, b, X, 10, 11, 0)
    b, c, d, a = set_md4(F, b, c, d, a, X, 11, 19, 0)
    a, b, c, d = set_md4(F, a, b, c, d, X, 12, 3, 0)
    d, a, b, c = set_md4(F, d, a, b, c, X, 13, 7, 0)
    c, d, a, b = set_md4(F, c, d, a, b, X, 14, 11, 0)
    b, c, d, a = set_md4(F, b, c, d, a, X, 15, 19, 0)

    a, b, c, d = set_md4(G, a, b, c, d, X, 0, 3, m)
    d, a, b, c = set_md4(G, d, a, b, c, X, 4, 5, m)
    c, d, a, b = set_md4(G, c, d, a, b, X, 8, 9, m)
    b, c, d, a = set_md4(G, b, c, d, a, X, 12, 13, m)
    a, b, c, d = set_md4(G, a, b, c, d, X, 1, 3, m)
    d, a, b, c = set_md4(G, d, a, b, c, X, 5, 5, m)
    c, d, a, b = set_md4(G, c, d, a, b, X, 9, 9, m)
    b, c, d, a = set_md4(G, b, c, d, a, X, 13, 13, m)
    a, b, c, d = set_md4(G, a, b, c, d, X, 2, 3, m)
    d, a, b, c = set_md4(G, d, a, b, c, X, 6, 5, m)
    c, d, a, b = set_md4(G, c, d, a, b, X, 10, 9, m)
    b, c, d, a = set_md4(G, b, c, d, a, X, 14, 13, m)
    a, b, c, d = set_md4(G, a, b, c, d, X, 3, 3, m)
    d, a, b, c = set_md4(G, d, a, b, c, X, 7, 5, m)
    c, d, a, b = set_md4(G, c, d, a, b, X, 11, 9, m)
    b, c, d, a = set_md4(G, b, c, d, a, X, 15, 13, m)

    a, b, c, d = set_md4(H, a, b, c, d, X, 0, 3, n)

    return a, b, c, d


def func(str, a, b, c, d, hash, passw):
    N = len(str)
    for i in range (0, N // (16 * 32)):
        
        X = init_m(str[i * 512: (i + 1) * 512])
        aa = a
        bb = b
        cc = c
        dd = d
        
        m = 0x5A827999
        n = 0x6ED9EBA1

        aa, bb, cc, dd = md4_half_hash(a, b, c, d, X, m, n)
        a1, b1, c1, d1 = reverse_steps(hash, X, n)

        if aa == a1 and bb == b1 and cc == c1 and dd == d1:
            
            if hex(int(md4_hash(str, a, b, c, d), 2)) == hex(hash):
                
                print('found', passw)
                
                return True
    
    print('False')
    return False


def check(str, a, b, c, d, hash, passw, afc, bfc, cfc, dfc):
    N = len(str)
    h = hex(int(md4_hash(str, a, b, c, d), 2))
    #print(h, hex(hash))
    for i in range (0, N // (16 * 32)):
        X = init_m(str[i * 512: (i + 1) * 512])
        aa = a
        bb = b
        cc = c
        dd = d
        
        m = 0x5A827999
        n = 0x6ED9EBA1

        aa, bb, cc, dd = md4_half_hash(a, b, c, d, X, m, n)
        if aa == afc and bb == bfc and cc == cfc and dd == dfc:
            #print('True')
            if hex(int(md4_hash(str, a, b, c, d), 2)) == hex(hash):
                print('found', passw)
                return True
    print('False')
    return False


def md4_hash(str, a, b, c, d):
    N = len(str)
    for i in range (0, N // (16 * 32)):
        X = init_m(str[i * 512: (i + 1) * 512])
        
        aa = a
        bb = b
        cc = c
        dd = d
        
        m = 0x5A827999
        n = 0x6ED9EBA1

        a, b, c, d = set_md4(F, a, b, c, d, X, 0, 3, 0)
        d, a, b, c = set_md4(F, d, a, b, c, X, 1, 7, 0)
        c, d, a, b = set_md4(F, c, d, a, b, X, 2, 11, 0)
        b, c, d, a = set_md4(F, b, c, d, a, X, 3, 19, 0)
        a, b, c, d = set_md4(F, a, b, c, d, X, 4, 3, 0)
        d, a, b, c = set_md4(F, d, a, b, c, X, 5, 7, 0)
        c, d, a, b = set_md4(F, c, d, a, b, X, 6, 11, 0)
        b, c, d, a = set_md4(F, b, c, d, a, X, 7, 19, 0)
        a, b, c, d = set_md4(F, a, b, c, d, X, 8, 3, 0)
        d, a, b, c = set_md4(F, d, a, b, c, X, 9, 7, 0)
        c, d, a, b = set_md4(F, c, d, a, b, X, 10, 11, 0)
        b, c, d, a = set_md4(F, b, c, d, a, X, 11, 19, 0)
        a, b, c, d = set_md4(F, a, b, c, d, X, 12, 3, 0)
        d, a, b, c = set_md4(F, d, a, b, c, X, 13, 7, 0)
        c, d, a, b = set_md4(F, c, d, a, b, X, 14, 11, 0)
        b, c, d, a = set_md4(F, b, c, d, a, X, 15, 19, 0)

        a, b, c, d = set_md4(G, a, b, c, d, X, 0, 3, m)
        d, a, b, c = set_md4(G, d, a, b, c, X, 4, 5, m)
        c, d, a, b = set_md4(G, c, d, a, b, X, 8, 9, m)
        b, c, d, a = set_md4(G, b, c, d, a, X, 12, 13, m)
        a, b, c, d = set_md4(G, a, b, c, d, X, 1, 3, m)
        d, a, b, c = set_md4(G, d, a, b, c, X, 5, 5, m)
        c, d, a, b = set_md4(G, c, d, a, b, X, 9, 9, m)
        b, c, d, a = set_md4(G, b, c, d, a, X, 13, 13, m)
        a, b, c, d = set_md4(G, a, b, c, d, X, 2, 3, m)
        d, a, b, c = set_md4(G, d, a, b, c, X, 6, 5, m)
        c, d, a, b = set_md4(G, c, d, a, b, X, 10, 9, m)
        b, c, d, a = set_md4(G, b, c, d, a, X, 14, 13, m)
        a, b, c, d = set_md4(G, a, b, c, d, X, 3, 3, m)
        d, a, b, c = set_md4(G, d, a, b, c, X, 7, 5, m)
        c, d, a, b = set_md4(G, c, d, a, b, X, 11, 9, m)
        b, c, d, a = set_md4(G, b, c, d, a, X, 15, 13, m)

        a, b, c, d = set_md4(H, a, b, c, d, X, 0, 3, n)
        #print(a, b, c, d, '1')
        d, a, b, c = set_md4(H, d, a, b, c, X, 8, 9, n)
        c, d, a, b = set_md4(H, c, d, a, b, X, 4, 11, n)
        b, c, d, a = set_md4(H, b, c, d, a, X, 12, 15, n)
        a, b, c, d = set_md4(H, a, b, c, d, X, 2, 3, n)
        d, a, b, c = set_md4(H, d, a, b, c, X, 10, 9, n)
        c, d, a, b = set_md4(H, c, d, a, b, X, 6, 11, n)
        b, c, d, a = set_md4(H, b, c, d, a, X, 14, 15, n)
        a, b, c, d = set_md4(H, a, b, c, d, X, 1, 3, n)
        d, a, b, c = set_md4(H, d, a, b, c, X, 9, 9, n)
        c, d, a, b = set_md4(H, c, d, a, b, X, 5, 11, n)
        b, c, d, a = set_md4(H, b, c, d, a, X, 13, 15, n)
        a, b, c, d = set_md4(H, a, b, c, d, X, 3, 3, n)
        d, a, b, c = set_md4(H, d, a, b, c, X, 11, 9, n)
        c, d, a, b = set_md4(H, c, d, a, b, X, 7, 11, n)
        b, c, d, a = set_md4(H, b, c, d, a, X, 15, 15, n)
        a1, b1, c1, d1 = a, b, c, d
        
        a = bin((int(a, 2) + int(aa, 2)) % 2 ** 32)[2:].rjust(32, "0")
        b = bin((int(b, 2) + int(bb, 2)) % 2 ** 32)[2:].rjust(32, "0")
        c = bin((int(c, 2) + int(cc, 2)) % 2 ** 32)[2:].rjust(32, "0")
        d = bin((int(d, 2) + int(dd, 2)) % 2 ** 32)[2:].rjust(32, "0")

    return(a1 + b1 + c1 + d1)


def ha(passw):
    k = bitting(passw)
    hash = md4_hash(k, A, B, C, D)
    hash = hex(int(hash, 2))
    print(hash)


passw = ''

ha(passw)
k = bitting(passw)

func(k, A, B, C, D, 0x9bdccc5603b83d8e899a18577373b77b, passw)

