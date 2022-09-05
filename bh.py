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


quad_ = lambda n, k: k**2 - n
const_ = lambda n, k: 1
tt_ = lambda n, k: 2**(n-1) if n > 0 else 1

quad = create_sbh_with_boundary(quad_)
const = create_sbh_with_boundary(const_)
tt = create_sbh_with_boundary(tt_) 
mix = create_sbh_with_boundary(lambda n, k: 2 * quad_(n, k) + 10 * const_(n, k) + 0.5 * tt_(n, k)) 

# below are BH, but not symmetric. 
k_only = lambda n, k: k
cubic = lambda n, k: k**3 - 3 * n * k


def bh(f, n):
    return [f(n, k) for k in list(range(-n, n+1, 2))]


def display(f, up_to_n, width=100):
    for n in range(up_to_n):
        print(str(n).zfill(2), end='')
        print(str(bh(f, n)).center(width), end='')
        print(f"sum={sum(bh(f, n))}", end='')
        print()


display(tt, 11, width=60)