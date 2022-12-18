# implementation of Merkle-Hellman knapsack cipher
# see "Merkle-Hellman knapsack cryptosystem" Wikipedia article

import random
# we're using the default random number generator
# for a cryptographically secure implementation, this would have to be changed

# from code by Dr. Coleman
def gcd(a, b):
    r = a % b
    while(r > 0):
        a, b = b, r
        r = a % b
    return b

# from code by Dr. Coleman
def egcd(a, b):
    s, t = 1, 0 # coefficients to express current a in terms of original a,b
    x, y = 0, 1 # coefficients to express current b in terms of original a,b
    q, r = divmod(a, b)
    while(r > 0):
        a, b = b, r
        old_x, old_y = x, y
        x, y = s - q*x, t - q*y
        s, t = old_x, old_y
        q, r = divmod(a, b)
    return b, x, y

# computes multiplicative inverse of n (mod m)
def mod_inverse(x, n):
    _, x, y = egcd(x, n)
    return x % n

def superincreasing_seq(length):
    # generate a superincreasing sequence of the given length
    w = []
    s = 0 # running sum
    for _ in range(length):
        next_num = random.randint(s+1, 2*(s+1)) # randomly pick the next number
        w += [next_num]
        s += next_num
    return w

def generate_private_key(length=8):
    w = superincreasing_seq(length)
    s = sum(w)
    q = random.randint(s+1, 2*(s+1))
    while True:
        r = random.randint(s//2, q-1)
        if gcd(r, q) == 1:
            break
    return q, w, r

def generate_public_key(q, w, r):
    b = list(map(lambda x: (x*r) % q, w))
    return b

def encrypt(b, msg):
    msg = bin(msg)[2:]
    offset = len(b) - len(msg)
    c = sum(j if i=='1' else 0 for i, j in zip(msg, b[offset:]))
    return c

def greedy_knapsack(w, s):
    a = []
    for i in w[::-1]:
        if i > s:
            a += [0]
        else:
            a += [1]
            s -= i
    return a[::-1]

def decrypt(q, w, r, c):
    x = mod_inverse(r, q)
    msg = greedy_knapsack(w, c*x%q)
    msg = ''.join(str(i) for i in msg)
    return int(msg, 2)


# Sample use

q, w, r = generate_private_key()
b = generate_public_key(q, w, r)
c = [encrypt(b, ord(i)) for i in 'CRYPTOGRAPHY']

msg = ''.join(chr(decrypt(q, w, r, i)) for i in c)
