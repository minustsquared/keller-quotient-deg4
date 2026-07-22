#!/usr/bin/env python3
"""Machine verification of the dictionary between the quotient calculus
(propositions note) and the derivation summary published by A. Lou
(aaronlou.com/jacobian_counterexample_derivation.pdf, July 20 2026):
  (a) Lou Lemma 1: det d(c3,c2,c1,c0,rho)/d(x,beta,gamma,delta,eps) = -rho^2
  (b) the explicit map of Lou Thm 3 has det JF = -2 and the claimed
      3-point fiber over (0,2,0)
  (c) DICTIONARY: the weight-1 component satisfies F/x = T(u,v) = 2*gamma
      identically, with u=xy, v=x^2 z  (so V(T) = {gamma=0}, the locus where
      the quadratic factor drops degree; NOT the rho=1-normalized
      common-root locus)
  (d) our quotient identity det DG = -T^2 det DF holds for this map, with
      components taken in weight order (-2,-1,1) (Lou's order (1,-1,-2) is
      an odd permutation, flipping the sign of det DF: -2 -> +2)
Exact arithmetic throughout."""
from sympy import symbols, Matrix, expand, factor, simplify, solve, Rational
x,b,g,d,e,y,z,u,v = symbols('x beta gamma delta epsilon y z u v')
c3,c2,c1,c0 = x*g, x*d+b*g, x*e+b*d, b*e
rho = x**2*e - x*b*d + b**2*g
M = Matrix([[expand(f).diff(w) for w in (x,b,g,d,e)] for f in (c3,c2,c1,c0,rho)])
assert simplify(M.det() + rho**2) == 0
print("(a) det(5x5) = -rho^2: VERIFIED")
F1 = x**3*z - 3*x**2*y + 2*x
F2 = -3*x**3*y**2*z + 9*x**2*y**3 - 6*x**2*y*z + 12*x*y**2 - 3*x*z + y
F3 = -x**3*y**3*z + 3*x**2*y**4 - 3*x**2*y**2*z + 7*x*y**3 - 3*x*y*z + 4*y**2 - z
J = Matrix([[f.diff(w) for w in (x,y,z)] for f in (F1,F2,F3)])
assert expand(J.det()) == -2
for p in [(-1,2,-8),(0,2,16),(1,-1,-5)]:
    assert tuple(f.subs(dict(zip((x,y,z),p))) for f in (F1,F2,F3)) == (0,2,0)
print("(b) det JF = -2 and 3-point fiber over (0,2,0): VERIFIED")
G_ = (2-3*x*y+x**2*z)/2
assert expand(F1/x - 2*G_) == 0
print("(c) T = F1/x = 2*gamma identically: VERIFIED (V(T) = {gamma=0})")
G1 = expand(F2*F1); G2 = expand(F3*F1**2)
G1uv = simplify(G1.subs({y:u/x, z:v/x**2})); G2uv = simplify(G2.subs({y:u/x, z:v/x**2}))
assert G1uv.free_symbols <= {u,v} and G2uv.free_symbols <= {u,v}
Gm = Matrix([[expand(G1uv).diff(w) for w in (u,v)],[expand(G2uv).diff(w) for w in (u,v)]])
T = 2 - 3*u + v
detDF_weight_order = 2   # (-2,-1,1) ordering: odd permutation of Lou's, so -(-2)
assert simplify(expand(Gm.det()) - (-(T**2)*detDF_weight_order)) == 0
print("(d) det DG = -T^2 * det DF (weight order (-2,-1,1)): VERIFIED")
print("ALL DICTIONARY CHECKS PASSED")
