#!/usr/bin/env python3
"""
Generate the (1,-1,-2)-equivariant Keller systems in degrees <= 4 and <= 5,
run the full degree-4 certification pipeline, and emit:
  - certificates/deg4_main_branches.json   (level-2 certificates, b0 != 0 piece)
  - certificates/deg4_b0_stratum.json      (level-2 certificates, b0  = 0 piece)
  - certificates/environment.json          (software versions, orders, fields)
  - solver_inputs/deg4_decomposition.sing  (level-3 pending: Singular primdec)
  - solver_inputs/deg4_decomposition.m2    (level-3 pending: Macaulay2 decompose)
  - solver_inputs/deg5_system.txt          (open target: 13 unknowns, 17 equations)
  - certificates/transcript.log            (full run transcript)

Evidentiary levels (see note/main.tex, Section 3):
  Level 1 (hand-proved): equivariant ansatz; forced-normalization lemma.
  Level 2 (machine-certified here): det-constancy identities, explicit inverses,
          composition identities, denominator conditions, b0-stratum coverage.
  Level 3 (PENDING): certified exhaustive decomposition of the Keller ideal.
          Nothing in this file discharges Level 3.
"""
import json, sys, time
from pathlib import Path
import sympy
from sympy import (symbols, Matrix, diff, expand, Poly, groebner, QQ, solve,
                   together, fraction, factor_list, cancel, srepr)

ROOT = Path(__file__).resolve().parent.parent
CERT_DIR = ROOT / '03-certificates'
SOLVER_DIR = ROOT / '05-solver-inputs'

x, y, z = symbols('x y z')
p, q, r = symbols('p q r')
LOG = open(CERT_DIR / 'transcript.log', 'w')
def log(msg):
    print(msg, flush=True); LOG.write(msg + '\n'); LOG.flush()

DEDUP_CRITERION = (
    'Dedup criterion (exact, for the audit trail): two solve() branches are '
    'collapsed iff their {unknown: value} maps are identical after sympy\'s '
    'default str() rendering, compared as a sorted tuple of (str(key), str(value)) '
    'pairs. This is SYNTACTIC equality of the already-canonicalized expression, '
    'not a semantic variety-equality check -- no Groebner/ideal-membership test '
    'was run to ask whether two syntactically different maps could parametrize '
    'the same locus. Every duplicate group actually found was exact-string-identical '
    '(same free parameters, same RHS text), consistent with sympy re-deriving one '
    'branch along multiple redundant elimination paths, which is what inspection '
    'of the pre-dedup JSON confirmed. This method could in principle miss a '
    'duplicate pair that is the same locus but written with differently-ordered '
    'or differently-simplified expressions; none of that was tested for.'
)

def dedupe(sols):
    """sympy.solve's case-split re-derives the same branch along multiple
    elimination paths when several vanishing-coefficient equations are
    already implied by earlier ones; collapse those exact duplicates so
    'branches' means distinct solution loci, not re-derivations of one.
    See DEDUP_CRITERION above for exactly what equality test this applies.
    Returns (distinct_solutions, groups) where groups[i] lists the raw
    solve()-branch indices collapsed into distinct_solutions[i], for the
    audit trail."""
    seen, out, groups = {}, [], []
    for raw_i, s in enumerate(sols):
        key = tuple(sorted((str(k), str(v)) for k, v in s.items()))
        if key not in seen:
            seen[key] = len(out)
            out.append(s)
            groups.append([raw_i])
        else:
            groups[seen[key]].append(raw_i)
    return out, groups

def monos(weight, maxdeg):
    out = []
    for i in range(maxdeg + 1):
        for j in range(maxdeg + 1):
            for k in range(maxdeg + 1):
                if 0 < i + j + k <= maxdeg and i - j - 2 * k == weight:
                    out.append(x**i * y**j * z**k)
    return out

def build_system(D):
    m1 = [m for m in monos(-2, D) if m != z]
    m2 = [m for m in monos(-1, D) if m != y]
    m3 = [m for m in monos(1, D) if m != x]
    A = symbols(f'a0:{len(m1)}'); B = symbols(f'b0:{len(m2)}'); C = symbols(f'c0:{len(m3)}')
    F1 = z + sum(ai * mi for ai, mi in zip(A, m1))
    F2 = y + sum(bi * mi for bi, mi in zip(B, m2))
    F3 = x + sum(ci * mi for ci, mi in zip(C, m3))
    unknowns = list(A) + list(B) + list(C)
    J = Matrix([[diff(F, v) for v in (x, y, z)] for F in (F1, F2, F3)])
    det = expand(J.det())
    eqs = [c for m, c in Poly(det, x, y, z).terms() if m != (0, 0, 0)]
    return (F1, F2, F3), unknowns, det, eqs, (m1, m2, m3)

def certify(Fs, free):
    """Level-2 certificate for one parametrized family.
    Returns dict with status, inverse, checks. 'pointwise' means: explicit
    polynomial inverse valid for EVERY parameter value in the family's stated
    domain (all denominators are nonzero constants). 'generic_with_exceptional'
    means denominators involve the listed parameter factors; validity holds
    wherever they are nonzero."""
    dom = QQ.frac_field(*(list(free) + [p, q, r])) if free else QQ.frac_field(p, q, r)
    G = groebner([Fs[0] - p, Fs[1] - q, Fs[2] - r], x, y, z, order='lex', domain=dom)
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
            elif f.free_symbols & {p, q, r}:
                return {'status': 'fail', 'reason': f'target-variable denominator {f}'}
    status = 'pointwise' if not exc else 'generic_with_exceptional'
    return {'status': status,
            'exceptional_factors': [str(f) for f in sorted(exc, key=str)],
            'inverse': {'x': str(X), 'y': str(Y), 'z': str(Z)},
            'composition_verified': True}

def run_deg4():
    Fs_sym, unknowns, det, eqs, _ = build_system(4)
    log(f'deg<=4 system: {len(unknowns)} unknowns, {len(eqs)} equations')
    log(DEDUP_CRITERION)
    t0 = time.time()
    sols_raw = solve(eqs, unknowns, dict=True)
    sols, groups = dedupe(sols_raw)
    log(f'main decomposition (sympy triangular solve, UNCERTIFIED completeness): '
        f'{len(sols_raw)} solve() branches, {len(sols)} distinct after dedup, '
        f'in {time.time()-t0:.1f}s')
    for gi, raw_indices in enumerate(groups):
        log(f'  distinct family {gi} <- raw solve() branches {raw_indices}')
    out = []
    for si, s in enumerate(sols):
        free = sorted([u for u in unknowns if u not in s], key=str)
        Fs = [expand(F.subs(s)) for F in Fs_sym]
        dbr = expand(det.subs(s))
        det_const = not (dbr.free_symbols & {x, y, z})
        cert = certify(Fs, free)
        cert.update({'branch': si,
                     'solution': {str(k): str(v) for k, v in s.items()},
                     'free_parameters': [str(f) for f in free],
                     'det_constant_identity': bool(det_const),
                     'det_value': str(dbr) if det_const else None})
        out.append(cert)
        log(f"  branch {si:2d}: det={cert['det_value']}, {cert['status']}"
            + (f" exceptional {cert['exceptional_factors']}" if cert.get('exceptional_factors') else ''))
    json.dump(out, open(CERT_DIR / 'deg4_main_branches.json', 'w'), indent=1)

    # b0 = 0 constructible piece, decomposed independently
    b0 = symbols('b0')
    t0 = time.time()
    ssols_raw = solve(eqs + [b0], unknowns, dict=True)
    ssols_pre, sgroups_pre = dedupe(ssols_raw)
    log(f'b0=0 stratum decomposition (UNCERTIFIED completeness): {len(ssols_raw)} solve() '
        f'branches, {len(ssols_pre)} distinct after within-file dedup, in {time.time()-t0:.1f}s')
    for gi, raw_indices in enumerate(sgroups_pre):
        log(f'  distinct b0-stratum family {gi} <- raw solve() branches {raw_indices}')

    # Cross-file dedup: the main decomposition (not told to assume b0=0) can
    # independently land on a branch that already sits at b0=0, duplicating
    # a family this stratum also finds. Checked by exact solution-dict key,
    # same DEDUP_CRITERION as above, but across both files' outputs.
    def sol_key(s):
        return tuple(sorted((str(k), str(v)) for k, v in s.items()))
    main_keys = {sol_key(s) for s in sols}
    ssols = []
    for si, s in enumerate(ssols_pre):
        k = sol_key(s)
        if k in main_keys:
            log(f'  b0-stratum family {si} is IDENTICAL to a main-branch family '
                f'(cross-file duplicate) -- dropped, already certified above.')
        else:
            ssols.append(s)
    sout = []
    for si, s in enumerate(ssols):
        free = sorted([u for u in unknowns if u not in s], key=str)
        Fs = [expand(F.subs(s)) for F in Fs_sym]
        dbr = expand(det.subs(s))
        cert = certify(Fs, free)
        cert.update({'branch': si,
                     'solution': {str(k): str(v) for k, v in s.items()},
                     'free_parameters': [str(f) for f in free],
                     'det_constant_identity': not (dbr.free_symbols & {x, y, z}),
                     'det_value': str(dbr)})
        sout.append(cert)
        log(f"  b0-stratum branch {si:2d}: {cert['status']}")
    json.dump(sout, open(CERT_DIR / 'deg4_b0_stratum.json', 'w'), indent=1)
    return unknowns, eqs, out, sout

def emit_solver_inputs(unknowns, eqs):
    vars_str = ','.join(str(u) for u in unknowns)
    polys = ',\n  '.join(str(expand(e)) for e in eqs)
    with open(SOLVER_DIR / 'deg4_decomposition.sing', 'w') as f:
        f.write(f'''// Level-3 certification target: exhaustive decomposition of the
// degree<=4 (1,-1,-2)-equivariant Keller ideal over QQ.
// Compare minimal associated primes against the parametrized families in
// certificates/deg4_main_branches.json and deg4_b0_stratum.json:
// the classification theorem becomes unconditional iff every minimal prime's
// variety is covered by those families.
LIB "primdec.lib";
ring R = 0, ({vars_str}), dp;
ideal I =
  {polys};
list L = minAssGTZ(I);
print(size(L));
L;
''')
    with open(SOLVER_DIR / 'deg4_decomposition.m2', 'w') as f:
        # NB: M2's --script mode does not auto-echo bare expressions the way
        # the interactive REPL does; results must be printed explicitly or
        # the run produces silent, empty output.
        f.write(f'''-- Level-3 certification target (Macaulay2 cross-check)
R = QQ[{vars_str}]
I = ideal(
  {polys})
D = decompose I
print("minimal primes: " | toString(#D));
print(D)
''')

def emit_deg5():
    Fs, unknowns, det, eqs, _ = build_system(5)
    with open(SOLVER_DIR / 'deg5_system.txt', 'w') as f:
        f.write('# Open target: degree<=5 (1,-1,-2)-equivariant Keller system\n')
        f.write(f'# unknowns ({len(unknowns)}): {", ".join(str(u) for u in unknowns)}\n')
        f.write(f'# equations ({len(eqs)}), coefficient field QQ\n')
        f.write(f'# F1 = {Fs[0]}\n# F2 = {Fs[1]}\n# F3 = {Fs[2]}\n\n')
        for e in eqs:
            f.write(str(expand(e)) + '\n')
    log(f'deg<=5 system exported: {len(unknowns)} unknowns, {len(eqs)} equations')

if __name__ == '__main__':
    env = {'python': sys.version, 'sympy': sympy.__version__,
           'coefficient_field': 'QQ; function fields QQ(free params, p, q, r) for inverses',
           'groebner_order_inverse_computation': 'lex, x > y > z',
           'decomposition_method': 'sympy.solve triangular decomposition (Groebner-based); '
                                   'completeness NOT independently certified (Level 3 pending)',
           'normalization': 'anchors z, y, x with unit coefficients; forced by Keller condition '
                            'up to equivariant diagonal linear changes of source and target'}
    json.dump(env, open(CERT_DIR / 'environment.json', 'w'), indent=1)
    unknowns, eqs, mout, sout = run_deg4()
    emit_solver_inputs(unknowns, eqs)
    emit_deg5()
    n_pw = sum(1 for c in mout if c['status'] == 'pointwise')
    n_ex = sum(1 for c in mout if c['status'] == 'generic_with_exceptional')
    s_pw = sum(1 for c in sout if c['status'] == 'pointwise')
    log(f'SUMMARY: main families {len(mout)} ({n_pw} pointwise, {n_ex} with exceptional '
        f'factor b0, valid on b0 != 0); b0=0 stratum families {len(sout)} ({s_pw} pointwise).')
    log('CONDITIONAL on Level-3 decomposition certification; see note/main.tex.')
    LOG.close()
