# Algebraic rational class
# Represent numbers in form (a + b * sqrt(n)) / c

import sys, os, inspect

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, a)

from factors import gcd

class Algebraic_Rational():

    def __init__ (self, a, b, c, n):
        if a != 0 and b != 0:
            gcd = gcd ([a,b,c])
        if a == 0 and b == 0:
            gcd = 1
        if a == 0 and b != 0:
            gcd = gcd ([b,c])
        if a != 0 and b == 0:
            gcd = gcd ([a,c])
        self.a = a / gcd
        self.b = b / gcd
        self.c = c / gcd
        self.n = n
        self.val = (a + b * (n ** 0.5)) / (c+ 0.0)
        self.num = (a, b, c, n)


    def __eq__ (self, other):
        return self.num == other.num

def Alg_Rational_invert (x):

    a,b,c,n = x.a, x.b, x.c, x.n
    c_new = a * a - n * b * b
    if c_new < 0: # multiply everything by -1 as well
        c_new = -1 * c_new
        c = -1 * c
        
    inv_x = Algebraic_Rational(c * a, -1 * c * b, c_new, n)
    
    return inv_x

def Alg_Rational_add (x1, x2):

    a1, b1, c1, n1 = x1.a, x1.b, x1.c, x1.n
    a2, b2, c2, n2 = x2.a, x2.b, x2.c, x2.n

    if n1 != n2 and b1 * b2 != 0:
        print "Cannot add unlike algebraic fractions"
        sys.exit()

    x_sum = Algebraic_Rational (a1 * c2 + a2 * c1, b1 * c2 + b2 * c1, c1 * c2, n1)

    return x_sum
