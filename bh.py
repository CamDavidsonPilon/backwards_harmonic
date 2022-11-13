from fractions import Fraction
from functools import cache

Fraction.__str__ = lambda self: f"{self.numerator}/{self.denominator}"
Fraction.__repr__ = lambda self: str(self)


def create_sbh_with_boundary(boundary_condition):
    
    @cache
    def f_(n, k):
        if k == -n or k == n:
            return boundary_condition(n, k) # boundary_condition should be symmetric
        if k > 0:
            return f_(n, -k)
        else:
            return 2 * f_(n-1, k-1) - f_(n, k - 2)
    return f_


const = lambda n, k: 1
linear = lambda n, k: k
quad = lambda n, k:    k**2 - 1 * n
cubic = lambda n, k: k * quad(n, k) - 2 * n * linear(n, k)  # k**3 - 3 * n * k ** 1
quartic = lambda n, k: k * cubic(n, k) - 3 * n * quad(n, k) + 2 * n #  k**4 - 6 * n * k ** 2 + 2 * n + 3 * n ** 2



"""
Thinking about functions that define only the boundary...
"""
tt_ = create_sbh_with_boundary(lambda n, k: 2**(n-1) if n > 0 else 1)

"""
vector space => we can add these functions
"""
linear_sum = lambda n, k: 2 * quad(n, k) + 10 * const(n, k) + 0.5 * tt_(n, k)


def emp_verify(f, up_to_n):
    for n in range(up_to_n):
        for k in range(-n, n+1, 2):
            assert f(n + 1, k - 1) + f(n + 1, k + 1) == 2 * f(n, k), f"{f(n + 1, k - 1)=} + {f(n + 1, k + 1)=} != 2 * {f(n, k)=}"



def bh(f, n):
    return [f(n, k) for k in range(-n, n+1, 2)]


def display(f, up_to_n, width=100):
    for n in range(up_to_n):
        print(str(n).zfill(2), end='')
        print(str(bh(f, n)).center(width), end='')
        print(f"sum={sum(bh(f, n))}", end='')
        print()


display(quartic, 9, width=60)
emp_verify(quartic, 200)



"""
          v0
        w1  w1
      x2  x0  x2
    y3  y1  y1  y3
  z4  z2  z0  z2  z4


0 = v0 - w1
0 =     2w1 - x2 - x0
0 =          2x2      - y3 - y1
0 =                x0      - y1
0 =                     2y3     - z2      - z4
0 =                         2y1 - z2 - z0

"""