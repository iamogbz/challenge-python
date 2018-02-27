import math
import time
import numpy as np
from numpy import linalg as LA

primes = []
nav_map = {} # adjancency matrix for groups of five
limit = 10**9 + 7 # as per requirements

def primesieve(n):
    global primes
    limit = int(n**0.5+1)
    sieve = [True]*limit
    for i in range(2,limit):
        if not sieve[i]: continue
        for j in range(i*i,limit,i):
            sieve[j] = False
        
        primes.append(i)
    
    return primes

def is_prime(n):
    for p in primes:
        if p >= n: break
        elif n % p == 0: return False
    return n > 1

# sum digits of string
def sum_digits(s):
    return sum(map(int, s))
    
def is_special(n):
    l = int(math.log10(n)+1) # number of digits
    d = str(n)
    for i in range(l-2):
        if not is_prime(sum_digits(d[i:i+5])): return False
        if not is_prime(sum_digits(d[i:i+4])): return False
        if not is_prime(sum_digits(d[i:i+3])): return False
    
    return l > 2 # specialness starts from 3

# build map and function cache    
def build_map(k, v):
    if len(k) != 5: return
    if k not in nav_map: 
        nav_map[k] = set()
    
    nav_map[k].add(k[-4:]+str(v))

# build list of numbers satisifying prime requirement
# possible optimisation only track last and first 5 digits
def specials(s=3, t=6):
    l = list(filter(is_special, range(10**(s-1),10**s)))
    for i in range(s, t):
        ns = []
        for n in l:
            d = str(n)
            if is_prime(sum_digits(d[-2:]+'0')):
                ns.append(n*10)
                build_map(d, 0)
            if is_prime(sum_digits('0'+d[:2])):
                build_map('0'+d[:-1], d[-1])
                if is_prime(sum_digits('00'+d[:1])):
                    build_map('00'+d[:-1], d[-1])
            
            for j in range(1,10):
                before = str(j) + d
                
                first3 = sum_digits(before[:3])
                first4 = 2 if i < 3 else first3 + int(before[3])
                first5 = 2 if i < 4 else first4 + int(before[4])
                if is_prime(first3) and is_prime(first4) and is_prime(first5):
                    ns.append(int(before))
                    build_map(before[:i],before[-1])
                
                after = d + str(j)
                last3 = sum_digits(after[-3:])
                last4 = 2 if i < 3 else last3 + int(after[-4])
                last5 = 2 if i < 4 else last4 + int(after[-5])
                if is_prime(last3) and is_prime(last4) and is_prime(last5):
                    ns.append(int(after))
                    build_map(d,j)
        
        if i == t-1: break
        else: l = set(ns)
    return t-1, l

# count number of paths of given length
def count(A, ns, l, t, n=0):
    i = t-n
    if i == 0: return len(sps)
    
    b = LA.matrix_power(A, i-1) # use .dot and cache results
    a = np.dot(A, b)
    leftout = [sum([1 for n in nav_map[ns[i]] if n not in nav_map]) for i in range(l)]
    c = 0
    for i in range(l):
        if not ns[i].startswith('0'):
            c += sum(a[i])
            # number of times visited in i-1 length
            for j in range(l):
                # add terminal values
                c += b[i][j] * leftout[j]
        
    return c

# main solution
s_t = time.time()
q = int(input().strip())
# q = 2 * 10**4

st = time.time()
primes = primesieve(45)
et = time.time()
print("sieving:", round(et-st, 3), primes)

st = time.time()
t, sps = specials()
et = time.time()
print("specials:", round(et-st, 3), len(sps)) # num special 5 digit numbers

# construct adjacency matrix
st = time.time()
ns = list(nav_map.keys())
l = len(ns)
A = np.zeros((l,l),dtype='int64')
for i in range(l):
    for j in range(l):
        if ns[j] in nav_map[ns[i]]: 
            A[i][j] = 1
et = time.time()
print("adj matx:", round(et-st, 3), np.sum(A))

for i in range(q):
    n = int(input().strip())
    # n = 4 * 10**5
    st = time.time()
    c = count(A, ns, l, n, t)
    et = time.time()
    print("counting:", round(et-st, 3), c)

e_t = time.time()
print("time:", round(e_t-s_t, 3))
