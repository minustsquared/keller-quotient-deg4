#!/usr/bin/env python3
"""Certify [C(u,v):C(G1,G2)] = 3 for the quotient map of the known
counterexample: P=(1+u)^3, Q=(1+u)(4+3u), R=1+12u+9u^2+(6+3u)v, S=3,
T=2-3u-v; G=(T(uR+vS), T^2(vP+u^2Q)).
Method: lex Groebner basis of <G1-s, G2-t> over the exact function field
Q(s,t), variables u>v. The basis is triangular: a univariate eliminant in v
whose degree equals the number of generic-fiber points counted with
multiplicity, plus a back-substitution expressing u rationally in v,s,t
(so the fiber cardinality equals the eliminant degree, and the field
extension degree equals it as well). Exact arithmetic, no floating point."""
from sympy import symbols, expand, groebner, QQ, Poly, degree, factor_list
u, v, s, t = symbols('u v s t')
P = (1+u)**3; Q = (1+u)*(4+3*u); R = 1+12*u+9*u**2+(6+3*u)*v; S = 3; T = 2-3*u-v
G1 = expand(T*(u*R+v*S)); G2 = expand(T**2*(v*P+u**2*Q))
print("G1 =", G1); print("G2 =", G2)
dom = QQ.frac_field(s, t)
gb = groebner([G1 - s, G2 - t], u, v, order='lex', domain=dom)
exprs = list(gb.exprs)
print(f"\nlex Groebner basis (u > v) over Q(s,t): {len(exprs)} elements")
uni = [g for g in exprs if u not in g.free_symbols]
assert len(uni) == 1, "expected exactly one univariate eliminant in v"
elim = Poly(uni[0], v)
print("eliminant degree in v:", elim.degree())
lin = [g for g in exprs if u in g.free_symbols]
dl = max(Poly(g, u).degree() for g in lin)
print("max degree in u of remaining basis elements:", dl)
assert dl == 1, "u is not rational in (v,s,t); degree count would need care"
from sympy import together, fraction, gcd, diff, simplify
num = fraction(together(elim.as_expr()))[0]  # clear Q(s,t) denominators
pn = Poly(num, v)
g = gcd(pn, pn.diff(v))
print("gcd(eliminant, d/dv eliminant) degree:", Poly(g, v).degree() if g.free_symbols & {v} else 0,
      "(0 => squarefree => 3 distinct generic-fiber points)")
mu = elim.degree()
print(f"\nRESULT: mu(G) = [C(u,v):C(G1,G2)] = {mu}")
assert mu == 3
print("matches the cubic fiber description; check PASSED")
