# Also meaning calling functions

# a class is “data with operations attached” 
# a closure is “operations with data attached.”

# A class that creates callable adder instance
class Adder(object):
    def __init__(self, n):
        self.n = n
    def __call__(self, m):
        return self.n+m

add5_i = Adder(5) # ”instance" or "imparetive"

# print(add5_i)
# <__main__.Adder object at 0x7f3b54192e48>
print(add5_i(10))
add5_i.n = 6
print(add5_i(10))
# A closure style
def make_adder(n):
    def adder(m):
        return m+n
    return adder

add5_f = make_adder(5) # functional

# print(add5_f)
# <function make_adder.<locals>.adder at 0x7f3b54193378>

print(add5_f(12)) # Couldn't change the state of instances


# Cautious about lambda like follow
adders = []
for n in range(5):
    adders.append(lambda m: m+n) #n willn't change
print([adder(10) for adder in adders])
n = 20
print([adder(5) for adder in adders])

adders = []
for n in range(5):
    adders.append(lambda m,n=n: m+n) #n willn't change
print([adder(10) for adder in adders])
n = 20
print([adder(5) for adder in adders])

add4 = adders[4]
print(add4(100)) # can override the bind value
print(adders[0](100,24)) 

# setter and getter decorator

class Car(object):
    def __init__(self):
        self._speed = 100
    @property
    def speed(self):
        print("Speed is", self._speed)
        return self._speed
    @speed.setter
    def speed(self, value):
        print("Setting to", value)
        self._speed = value

car = Car()
car.speed = 80 
x = car.speed

class TalkativeInt(int):
    def __lshift__(self, other):
        print("Shift", self, "by", other)
        return int.__lshift__(self, other)

t = TalkativeInt(8)
res = t<<4
print(res)

# static method 
# Keeping this functionality in a class avoids polluting the global namespace
import math
class RightTriangle(object): 
    # "Class used solely as namespace for related functions"
    @staticmethod
    def hypotenuse(a, b):
        return math.sqrt(a**2 + b**2)
    @staticmethod
    def sin(a, b):
        return a / RightTriangle.hypotenuse(a, b)
    @staticmethod
    def cos(a, b):
        return b / RightTriangle.hypotenuse(a, b)

RightTriangle.hypotenuse(3,4)
rt = RightTriangle()
rt.sin(3,4)
rt.cos(3,4)

# other method somelike static
import functools, operator
class Math(object):
    def product(*nums):
        return functools.reduce(operator.mul, nums)
    def power_chain(*nums):
        return functools.reduce(operator.pow, nums)
Math.product(1,4,68,8)
Math.power_chain(1,4,68,8)
# m = Math()
# m.product(1,2,3) # can't do this;unsupported operand type(s) for *

# Generators
def get_primes():
    candidate = 2
    found = []
    while True:
        if all(candidate % prime != 0 for prime in found):
            yield candidate
            found.append(candidate)
        candidate += 1

prime = get_primes()
print(next(prime))
print(next(prime))
print(next(prime))

# use func zip() to show 
for _ ,p in zip(range(10),prime):
    print(p)

# multi-despatch
class Thing: pass
class Rock(Thing): pass
class Scissors(Thing): pass
class Paper(Thing): pass

def beats(x, y):
    if isinstance(x, Rock):
        if isinstance(y, Rock):
            return None # No winner
        elif isinstance(y, Paper):
            return y
        elif isinstance(y, Scissors):
            return x
        else:
            raise TypeError("Unknown second thing")
    elif isinstance(x, Paper):
        if isinstance(y, Rock):
            return x
        elif isinstance(y, Paper):
            return None # No winner
        elif isinstance(y, Scissors):
            return y
        else:
            raise TypeError("Unknown second thing")
    elif isinstance(x, Scissors):
        if isinstance(y, Rock):
            return y
        elif isinstance(y, Paper):
            return x
        elif isinstance(y, Scissors):
            return None # No winner
        else:
            raise TypeError("Unknown second thing")
    else:
        raise TypeError("Unknown first thing")
rock, paper, scissors = Rock(), Paper(), Scissors()
print("winner",beats(rock,paper));
print("winner",beats(scissors,paper));

class DuckRock(Rock):
    def beats(self, other):
        if isinstance(other, Rock):
            return None # No winner
        elif isinstance(other, Paper):
            return other
        elif isinstance(other, Scissors):
            return self
        else:
            raise TypeError("Unknown second thing")
class DuckPaper(Paper):
    def beats(self, other):
        if isinstance(other, Rock):
            return self
        elif isinstance(other, Paper):
            return None # No winner
        elif isinstance(other, Scissors):
            return other
        else:
            raise TypeError("Unknown second thing")
class DuckScissors(Scissors):
    def beats(self, other):
        if isinstance(other, Rock):
            return other
        elif isinstance(other, Paper):
            return self
        elif isinstance(other, Scissors):
            return None # No winner
        else:
            raise TypeError("Unknown second thing")
def beats2(x, y):
    if hasattr(x, 'beats'):
        return x.beats(y)
    else:
        raise TypeError("Unknown first thing")
rock, paper, scissors = DuckRock(), DuckPaper(), DuckScissors()

print("winner",beats2(rock,paper));
print("winner",beats2(scissors,paper));

from multipledispatch import dispatch
@dispatch(Rock, Rock)
def beats3(x, y): return None
@dispatch(Rock, Paper)
def beats3(x, y): return y
@dispatch(Rock, Scissors)
def beats3(x, y): return x
@dispatch(Paper, Rock)
def beats3(x, y): return x
@dispatch(Paper, Paper)
def beats3(x, y): return None
@dispatch(Paper, Scissors)
def beats3(x, y): return x
@dispatch(Scissors, Rock)
def beats3(x, y): return y
@dispatch(Scissors, Paper)
def beats3(x, y): return x
@dispatch(Scissors, Scissors)
def beats3(x, y): return None

@dispatch(object, object)
def beats3(x, y):
    if not isinstance(x, (Rock, Paper, Scissors)):
        raise TypeError("Unknown first thing")
    else:
        raise TypeError("Unknown second thing")

rock, paper, scissors = Rock(), Paper(), Scissors()
print("winner",beats3(rock,paper));
print("winner",beats3(scissors,paper));