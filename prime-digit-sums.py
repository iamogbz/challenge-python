import math
import time

primes = []
nav_map = {} # connect graph for groups of five
soln_cache = [] # solution cache
limit = 10**9 + 7 # as per requirements

def primesieve(n):
    primes = []
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
    
    return True # vacuous truth

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
def count(t, n=0):
    if t < 0: raise ValueError("negative length not allowed")
    elif t < 5: return [0,9,90,303,280][t]
    else:
        i = t-n
        st = len(soln_cache) - 1
        if i > st:
            for i0 in range(st,i):
                c_map = {}
                for k,v in soln_cache[-1].items():
                    if k not in nav_map: continue
                    for ns in nav_map[k]:
                        if ns not in c_map: c_map[ns] = 0
                        c_map[ns] += v
                        c_map[ns] %= limit
                soln_cache.append(c_map)
        
    return sum(soln_cache[i].values()) % limit

## main solution
s_t = time.time()
q = int(input().strip())
# q = 2 * 10**4

# get prime factors
st = time.time()
primes = primesieve(45)
et = time.time()
print("sieving:", round(et-st, 3), primes)

# num special 5 digit numbers
st = time.time()
t, sps = specials()
et = time.time()
print("specials:", round(et-st, 3), len(sps))

# initialise solution cache
soln_cache.append({})
for s in sps:
    soln_cache[0][str(s)] = 1

for i in range(q):
    n = int(input().strip())
    # n = 4 * 10**5
    st = time.time()
    c = count(n, t)
    et = time.time()
    print("counting:", round(et-st, 3), c)

e_t = time.time()
print("time:", round(e_t-s_t, 3))
