# !/usr/bin/env python

from decimal import *

def calc_t(a, k1, k3, na1, nb1, nb3, nc2, nc3):
    return na1 - k1/(nb1 + (nb3 - k3/(nc3 + nc2 * a)) * a)

def calc_n1a(a, k1, k2, k3, na1, nb1, nb3, nc2, nc3):
    npart1 = a ** 2 * na1 * nb3 * nc2
    npart2 = (a * k1 * k2 * k3).sqrt()
    denominator = nb1 * nc3 + nb1 * nc2 * a + a ** 2 * nb3 * nc2 + a * k3
    n1a1 = ( npart2 + npart1) / denominator
    n1a2 = (-npart2 + npart1) / denominator
    return [n1a1, n1a2]

def calc_n1b(a, k1, na1, n1a, nb1):
    return (k1 / (na1 - n1a) - nb1) / a

def calc_n2c(a, k3, nb3, n1b, nc3):
    return (k3 / (nb3 - n1b) - nc3) / a

def calc_n2a(a, k2, nc2, n2c, na2):
    return (k2 / (nc2 - n2c) - na2) / a

def calc_r(n1a, n2a, delta):
    return n1a - n2a - delta

def calc_triangle_arbitrage(a, k1, k2, k3, na1, na2, nb1, nb3, nc2, nc3, delta):
    t = calc_t(a, k1, k3, na1, nb1, nb3, nc2, nc3)
    n1as = calc_n1a(a, k1, k2, k3, na1, nb1, nb3, nc2, nc3)
    r1 = 0
    r2 = 0
    if n1as[0] < t:
        n1a = n1as[0]
        print("n1a", n1a)
        n1b = calc_n1b(a, k1, na1, n1a, nb1)
        print("n1b", n1b)
        n2c = calc_n2c(a, k3, nb3, n1b, nc3)
        print("n2c", n2c)
        n2a = calc_n2a(a, k2, nc2, n2c, na2)
        print("n2a", n2a)
        r1 = calc_r(n1a, n2a, delta)
        print("r1", r1)
    print("\n")
    if n1as[1] < t:
        n1a = n1as[1]
        print("n1a", n1a)
        n1b = calc_n1b(a, k1, na1, n1a, nb1)
        print("n1b", n1b)
        n2c = calc_n2c(a, k3, nb3, n1b, nc3)
        print("n2c", n2c)
        n2a = calc_n2a(a, k2, nc2, n2c, na2)
        print("n2a", n2a)
        r2 = calc_r(n1a, n2a, delta)
        print("r2", r2)
    r = 0
    if r1 > 0 and r2 > 0:
        if r1 > r2:
            r = r1
        else:
            r = r2
    else:
        if r1 > 0:
            r = r1
        elif r2 > 0:
            r = r2            
    return r
