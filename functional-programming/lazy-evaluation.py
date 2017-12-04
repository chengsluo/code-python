# Chinese translation:惰性求值

# idempotent
# iter_seq = iter(sequence)
# iter(iter_seq) == iter_seq

from collections.abc import Iterable
class Fibonacci(Iterable):
    def __init__(self):
        self.a, self.b = 0, 1
        self.total = 0
    def __iter__(self):
        return self
    def __next__(self):
        self.a, self.b = self.b, self.a + self.b
        self.total += self.a
        return self.a
    def running_sum(self):
        return self.total

fib = Fibonacci()
fib.running_sum()
print(True==('__iter__' in dir(fib) and '__next__' in dir(fib)))

for _, i in zip(range(10), fib):
    print(i," ")
fib.running_sum()
print(next(fib))



def fibonacci():
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a+b

from itertools import tee, accumulate
s, t = tee(fibonacci())
pairs = zip(t, accumulate(s))
for _, (fib, total) in zip(range(7), pairs):
    print(fib, total)


# Chaining Iterables

from itertools import chain,count

def from_logs(fnames):
    yield from (open(file) for file in fnames)

lines = chain.from_iterable(from_logs(['huge.log', 'gigantic.log']))

