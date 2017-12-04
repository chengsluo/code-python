def running_sum(numbers, start=0):
    if len(numbers) == 0:
        print("finished")
        return
    total = numbers[0]+start
    print(total)
    running_sum(numbers[1:], total)

# running_sum([i for i in range(998)])

# factorial test

def factorialR(N):
    "Rescurtive factorial function"
    assert isinstance(N,int) and N>1
    return 1 if N<1 else N*factorialR(N-1)

def factorialI(N):
    "Iterative factorial function"
    assert isinstance(N,int) and N>1
    product = 1
    while(N>=1):
        product *= N
        N -= 1
    return product

# fastest factorial in python by higher-order function
from functools import reduce
from operator import mul
def factorialHOF(N):
    return reduce(mul,range(1,N+1),1) # recursion without recursion

# print(factorialHOF(100000))

# Quicksort by Python
def quicksort(lst):
    if len(lst) == 0:
        return lst
    pivot = lst[0]
    pivots = [i for i in lst if i == pivot]
    small = quicksort([i for i in lst if i<pivot])
    large = quicksort([i for i in lst if i>pivot])
    return large + pivots + small

print(quicksort([i for i in range(0,100,2)]))