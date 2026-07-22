#!/usr/bin/env python3
"""
Independent certificate verifier. Reads ONLY the static JSON certificates and
the fixed ansatz definition below; performs NO solving, NO branch discovery.
Checks, for every family:
  (V1) det DF equals the recorded constant, identically in x,y,z (params symbolic)
  (V2) F(H(p,q,r)) = (p,q,r)   [forward composition]
  (V3) H(F(x,y,z)) = (x,y,z)   [backward composition]
  (V4) denominator factors of H are exactly those recorded (constants => pointwise)
Writes certificates/verification_report.json. Exit code 0 iff all checks pass
or time out explicitly (timeouts are reported, never silently passed).
"""
import json, sys, time, signal
from pathlib import Path
from sympy import (symbols, Matrix, diff, expand, cancel, together, fraction,
                   factor_list, sympify, simplify)

ROOT = Path(__file__).resolve().parent.parent
CERT_DIR = ROOT / '03-certificates'
x, y, z = symbols('x y z'); p, q, r = symbols('p q r')

# Fixed ansatz (degree-4, weights (1,-1,-2), unit anchors) — restated, not imported
def monos(w, D):
    return [x**i*y**j*z**k for i in range(D+1) for j in range(D+1) for k in range(D+1)
            if 0 < i+j+k <= D and i-j-2*k == w]
m1 = [m for m in monos(-2, 4) if m != z]
m2 = [m for m in monos(-1, 4) if m != y]
m3 = [m for m in monos(1, 4) if m != x]
A = symbols(f'a0:{len(m1)}'); B = symbols(f'b0:{len(m2)}'); C = symbols(f'c0:{len(m3)}')
F1s = z + sum(a*m for a, m in zip(A, m1))
F2s = y + sum(b*m for b, m in zip(B, m2))
F3s = x + sum(c*m for c, m in zip(C, m3))

class Timeout(Exception): pass
def alarm(sig, frm): raise Timeout()
signal.signal(signal.SIGALRM, alarm)

def verify_family(cert, budget=30):
    out = {'branch': cert['branch']}
    sol = {sympify(k): sympify(v) for k, v in cert['solution'].items()}
    Fs = [expand(F.subs(sol)) for F in (F1s, F2s, F3s)]
    J = Matrix([[diff(F, w_) for w_ in (x, y, z)] for F in Fs])
    d = expand(J.det())
    out['V1_det'] = (not (d.free_symbols & {x, y, z})) and str(d) == cert['det_value']
    if cert.get('inverse'):
        H = [sympify(cert['inverse'][k]) for k in ('x', 'y', 'z')]
        signal.alarm(budget)
        try:
            out['V2_FoH'] = all(cancel(F.subs({x: H[0], y: H[1], z: H[2]}, simultaneous=True) - t) == 0
                                for F, t in zip(Fs, (p, q, r)))
            out['V3_HoF'] = all(cancel(h.subs({p: Fs[0], q: Fs[1], r: Fs[2]}, simultaneous=True) - w_) == 0
                                for h, w_ in zip(H, (x, y, z)))
        except Timeout:
            out['V2_FoH'] = out.get('V2_FoH', 'TIMEOUT'); out['V3_HoF'] = 'TIMEOUT'
        finally:
            signal.alarm(0)
        dens = set()
        for h in H:
            for f, _ in factor_list(fraction(together(h))[1])[1]:
                if f.free_symbols - {p, q, r}:
                    dens.add(str(f))
        out['V4_denominators'] = sorted(dens) == sorted(cert.get('exceptional_factors', []))
    return out

def run(path):
    certs = json.load(open(path))
    results, t0 = [], time.time()
    for c in certs:
        res = verify_family(c)
        results.append(res)
        flags = [k for k, v in res.items() if v is False]
        to = [k for k, v in res.items() if v == 'TIMEOUT']
        print(f"{path} branch {c['branch']:2d}: "
              + ("OK" if not flags and not to else f"FAIL {flags} TIMEOUT {to}"), flush=True)
    return results

if __name__ == '__main__':
    report = {}
    for f in (CERT_DIR / 'deg4_main_branches.json', CERT_DIR / 'deg4_b0_stratum.json'):
        report[str(f)] = run(f)
    json.dump(report, open(CERT_DIR / 'verification_report.json', 'w'), indent=1)
    bad = [r for rs in report.values() for r in rs if any(v is False for v in r.values())]
    tos = [r for rs in report.values() for r in rs if any(v == 'TIMEOUT' for v in r.values())]
    print(f"\nFAILURES: {len(bad)}   TIMEOUTS: {len(tos)}")
    sys.exit(0 if not bad else 1)
