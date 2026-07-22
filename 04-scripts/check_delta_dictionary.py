#!/usr/bin/env python3
"""Verify that Speyer's Delta (Secret Blogging Seminar, July 20 post) descends
to the quotient plane as the leading coefficient of the fiber cubic of G:
  (1) c^2*Delta = s^3 - s^2 - 18st + 16t + 27t^2 under s = bc, t = ac^2
  (1b) p = 8 - 9bc + 27ac^2 is itself a plane invariant: p = 8 - 9s + 27t
  (2) the leading coefficient (in the fiber variable) of the degree-3 fiber
      equation of G over Q(s,t) equals 2*(s^3 - s^2 - 18st + 27t^2 + 16t)
Consequence (stated precisely): G's only critical locus is V(T), contracted
to the origin; over {Delta = 0} the fiber count drops by NONPROPERNESS (the
cubic loses its leading term; a root escapes to infinity), not ramification.
Exact arithmetic throughout."""
from sympy import symbols, expand, simplify, groebner, QQ, Poly, fraction, together, factor
x,y,z,u,v,s,t = symbols('x y z u v s t')
a = (1+x*y)**3*z + y**2*(1+x*y)*(4+3*x*y)
b = y + 3*x*(1+x*y)**2*z + 3*x*y**2*(4+3*x*y)
c = 2*x - 3*x**2*y - x**3*z
Delta = 16*a - b**2 - 18*a*b*c + b**3*c + 27*a**2*c**2
S_, T_ = expand(b*c), expand(a*c**2)
assert simplify(expand(c**2*Delta) - expand(S_**3 - S_**2 - 18*S_*T_ + 16*T_ + 27*T_**2)) == 0
print("(1) c^2*Delta descends: c^2*Delta = s^3 - s^2 - 18st + 16t + 27t^2  VERIFIED")
assert simplify((8 - 9*b*c + 27*a*c**2) - (8 - 9*S_ + 27*T_)) == 0
print("(1b) p = 8 - 9s + 27t is a plane invariant  VERIFIED")
P = (1+u)**3; Q = (1+u)*(4+3*u); R = 1+12*u+9*u**2+(6+3*u)*v; Ssym = 3; T = 2-3*u-v
G1 = expand(T*(u*R+v*Ssym)); G2 = expand(T**2*(v*P+u**2*Q))
gb = groebner([G1-s, G2-t], u, v, order='lex', domain=QQ.frac_field(s,t))
elim = [g for g in gb.exprs if u not in g.free_symbols][0]
lead = Poly(fraction(together(elim))[0], v).LC()
assert simplify(lead/(s**3 - s**2 - 18*s*t + 27*t**2 + 16*t)) == 2
print("(2) leading coeff of G's fiber cubic = 2*(s^3 - s^2 - 18st + 27t^2 + 16t) = 2*c^2*Delta  VERIFIED")
print("ALL DELTA-DICTIONARY CHECKS PASSED")
