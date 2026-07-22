#!/usr/bin/env python3
"""
Degree-5 candidate families, found via modular reconstruction + exact
verification -- NOT a classification result. See the STATUS note this
script writes into its own output for exactly what is and is not established.

Method (per the exact/reconstruction-based check requested 2026-07-21, run
alongside -- not instead of -- the exact QQ minAssGTZ that was slow due to
intermediate coefficient blowup, confirmed via `sample` on the running
process):
  1. minAssGTZ(I) was run over three good primes (32003, 32009, 65003).
     Each found exactly 2 minimal primes, same monomial structure in each.
  2. The prime-dependent numeric coefficients were checked against the
     modular inverse of small rationals (e.g. 16001 mod 32003 == -1/2,
     verified directly: inv(2) mod 32003 == 16002, so -inv(2) == 16001).
     Every coefficient that varied by prime reconstructed to a SMALL
     rational (denominators 2 or 4) -- evidence the true answer is clean,
     not evidence it is complete.
  3. The two resulting exact candidate families (one of which splits into
     two branches under sympy.solve) were verified directly and exactly
     over QQ with the SAME det-constancy / explicit-inverse / composition
     methodology as the certified degree-4 families
     (04-scripts/generate_and_certify.py's `certify`).

What this DOES establish (exact, Level 2, no modular arithmetic involved in
the verification step): each family below is a genuine solution of the
degree-5 Keller system, with det Jacobian identically -1, and admits an
explicit polynomial inverse with both compositions verified.

What this does NOT establish: that these are the ONLY minimal primes of the
degree-5 ideal. The "2 minimal primes" count is from modular arithmetic
(ZZ/32003 etc.) and is a heuristic preview, not a characteristic-zero
certificate -- an unlucky prime could in principle merge or split components
relative to the true answer. The exact QQ minAssGTZ run (separate process,
see out/deg5_qq_run_manifest.txt) is the only path to an actual exhaustiveness
certificate for degree 5, exactly as it was for degree 4. DO NOT CIRCULATE
a "degree 5 is classified" claim on the strength of this file alone.
"""
import json
from pathlib import Path
from sympy import (symbols, expand, Matrix, diff, groebner, QQ, solve,
                    together, fraction, factor_list, cancel, Rational)

ROOT = Path(__file__).resolve().parent.parent
CERT_DIR = ROOT / '03-certificates'

x, y, z = symbols('x y z')
p, q, r = symbols('p q r')
a0, a1, a2, a3, a4 = symbols('a0 a1 a2 a3 a4')
b0, b1, b2, b3, b4 = symbols('b0 b1 b2 b3 b4')
c0, c1, c2 = symbols('c0 c1 c2')

F1s = a0*y**2 + a1*x*y*z + a2*x*y**3 + a3*x**2*z**2 + a4*x**2*y**2*z + z
F2s = b0*x*z + b1*x*y**2 + b2*x**2*y*z + b3*x**2*y**3 + b4*x**3*z**2 + y
F3s = c0*x**2*y + c1*x**3*z + c2*x**3*y**2 + x


def certify_deg5(sub, free):
    Fs = [expand(F.subs(sub)) for F in (F1s, F2s, F3s)]
    J = Matrix([[diff(F, v) for v in (x, y, z)] for F in Fs])
    det = expand(J.det())
    if det.free_symbols & {x, y, z}:
        return {'status': 'fail', 'reason': 'det not constant'}
    dom = QQ.frac_field(*(list(free) + [p, q, r])) if free else QQ.frac_field(p, q, r)
    G = groebner([Fs[0]-p, Fs[1]-q, Fs[2]-r], x, y, z, order='lex', domain=dom)
    inv = solve(list(G.exprs), [x, y, z], dict=True)
    if len(inv) != 1:
        return {'status': 'fail', 'reason': f'{len(inv)} inverse branches'}
    X, Y, Z = [together(inv[0][v]) for v in (x, y, z)]
    comp_ok = all(cancel(F.subs({x: X, y: Y, z: Z}, simultaneous=True) - t) == 0
                  for F, t in zip(Fs, (p, q, r)))
    if not comp_ok:
        return {'status': 'fail', 'reason': 'composition identity failed'}
    exc = set()
    for e in (X, Y, Z):
        den = fraction(together(e))[1]
        for f, _ in factor_list(den)[1]:
            if f.free_symbols & set(free):
                exc.add(f)
    status = 'pointwise' if not exc else 'generic_with_exceptional'
    return {'status': status,
            'det_value': str(det),
            'solution': {str(k): str(v) for k, v in sub.items()},
            'free_parameters': [str(f) for f in free],
            'exceptional_factors': [str(f) for f in sorted(exc, key=str)],
            'inverse': {'x': str(X), 'y': str(Y), 'z': str(Z)},
            'composition_verified': True,
            'source': 'reconstructed from minAssGTZ over ZZ/32003, ZZ/32009, '
                       'ZZ/65003, then verified exactly over QQ (this script)'}


CANDIDATES = [
    ({a1: 0, a3: 0, a4: 0, b2: 0, b4: 0, c0: 0, c1: 0, c2: 0,
      b1: a0*b0, b3: a2*b0}, [a0, a2, b0]),
    ({a0: b2**3/(4*b4*(b0*b2-2*b4)), a1: b2**2/(b0*b2-2*b4), a2: 0,
      a3: b2*b4/(b0*b2-2*b4), a4: 0, b1: b2**2/(4*b4), b3: 0,
      c0: 0, c1: 0, c2: 0}, [b0, b2, b4]),
    ({a1: 2*a0*b0, a2: 0, a3: a0*b0**2, a4: 0, b1: 0, b2: 0, b3: 0,
      b4: 0, c0: 0, c1: 0, c2: 0}, [a0, b0]),
]

if __name__ == '__main__':
    out = []
    for i, (sub, free) in enumerate(CANDIDATES):
        cert = certify_deg5(sub, free)
        cert['branch'] = i
        out.append(cert)
        print(f"branch {i}: {cert['status']}, exceptional={cert.get('exceptional_factors')}")
    json.dump(out, open(CERT_DIR / 'deg5_candidate_branches.json', 'w'), indent=1)
    print(f"\nwrote {len(out)} candidate families to "
          f"{CERT_DIR / 'deg5_candidate_branches.json'}")
    print("STATUS: Level 2 (per-family) exact, Level 3 (exhaustiveness) NOT "
          "established for degree 5. Do not circulate as a classification.")
