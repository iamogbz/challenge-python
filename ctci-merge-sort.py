#!/bin/python3

def merge_sort(A, length):
    if length <= 1:
        return 0, A
    middle = int(length/2)
    left_len = middle
    right_len = length - middle
    left_inversions, left = merge_sort(A[:middle], left_len)
    right_inversions, right = merge_sort(A[middle:], right_len)
    merge_inversions, merged = merge(left, right, left_len, right_len)
    inversions = left_inversions + right_inversions + merge_inversions
    return inversions, merged

def merge(a, b, a_len, b_len):
    result = []
    i, j, inversions = 0, 0, 0
    while i < a_len and j < b_len:
        if a[i] <= b[j]:
            inversions += j
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    inversions += j*(a_len-i)
    result += a[i:]
    result += b[j:]
    return inversions, result

import time
    
s_time = time.time()
cases = int(input())
for i in range(cases):
    n = int(input())
    a_time = time.time()
    data =  list(map(int,input().split()))
    b_time = time.time()
    print("filling:", round(b_time - a_time, 3), "secs")
    a_time = time.time()
    inv, sorted = merge_sort(data, n)
    b_time = time.time()
    print("sorting:", round(b_time - a_time, 3), "secs")
    print (inv,"\n")
t_time = time.time()
print("\ntime:", round(t_time - s_time, 3), "secs")
