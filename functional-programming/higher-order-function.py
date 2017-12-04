# Classic "FP-style"
transformed = map(tranformation, iterator)
# Comprehension
transformed = (transformation(x) for x in iterator)

# Classic "FP-style"
filtered = filter(predicate, iterator)
# Comprehension
filtered = (x for x in iterator if predicate(x))

from functools import reduce

total = reduce(operator.add, it, 0)
# total = sum(it) # equivalent


# reduce(fun,sequece[,initial])
# map() and filter() are also a special cases of reduce()
add5 = lambda x:x+5
print(reduce(lambda l,x:l+[add5(x)],range(10),[]))

# simpler: iters=map(add5,range(10))
# [x for x in iters]
isOdd = lambda x:x%2
print(reduce(lambda l,x:l+[x] if isOdd(x) else l,range(10),[]))

# simpler: iters=filter(isOdd,range[10])
# [x for x in iters]


# sum 1-5
print(reduce(lambda x,l:x+l,range(6)))

# statistic frequency
str ="an apple a banane two orange all fruits a pear"
list = str.split(' ')
def fun(dict,x):
    if x in dict:
        dict[x]=dict[x]+1
    else:
        dict[x]=1
    return dict

result=reduce(fun,list,{})
print(result)


def compose(*funcs):
    """Return a new function s.t.
        compose(f,g,...)(x) == f(g(...(x)))"""
    def inner(data, funcs=funcs):
        result = data
        for f in reversed(funcs):
            result = f(result)
        return result
    return inner

times2 = lambda x: x*2
minus3 = lambda x: x-3
mod6 = lambda x: x%6
f = compose(mod6, times2, minus3)
# check function, return True or False
all(f(i)==((i-3)*2)%6 for i in range(1000000))


all_pred = lambda item, *tests: all(p(item) for p in tests)
any_pred = lambda item, *tests: any(p(item) for p in tests)
from functools import partial
is_lt100 = partial(operator.ge, 100) # less than 100? 
is_gt10 = partial(operator.le, 10) # greater than 10?
# use partial() add args
from nums import is_prime # implemented elsewhere
all_pred(71, is_lt100, is_gt10, is_prime)
predicates = (is_lt100, is_gt10, is_prime)
all_pred(107, *predicates)

# check each func sperately
>>> from toolz.functoolz import juxt
>>> juxt([is_lt100, is_gt10, is_prime])(71)
(True, True, True)
>>> all(juxt([is_lt100, is_gt10, is_prime])(71))
True
>>> juxt([is_lt100, is_gt10, is_prime])(107)
(False, True, True)

# Compare ad hoc lambda with `operator` function
sum1 = reduce(lambda a, b: a+b, iterable, 0)
sum2 = reduce(operator.add, iterable, 0)
sum3 = sum(iterable) # The actual Pythonic way



# define some_func and other_func are equivalent

@enhanced
def some_func(*args):
pass
def other_func(*args):
pass
other_func = enhanced(other_func)

#  More thing
# functools.lru_cache , functools.total_ordering , and functools.wraps


