# Jacobian counterexample — equivariant classification project
Working folder index. Prepared 2026-07-21. Owner: [withheld -- pseudonymous deposit; see COMMITMENT.txt].

## Status in one line
Degree-4 classification is an unconditional theorem as of 2026-07-21
(exhaustiveness certified in Singular, cross-checked in Macaulay2). Degree-5
has real partial progress -- three exact, individually verified families --
but is not classified: exhaustiveness is unconfirmed and any "2 components"
figure quoted below is a modular preview only, not a characteristic-zero
fact.

## New: D0 program (degree-seven minimality), 2026-07-22
**Working research note:** degree-(≤4) proved; degree-5/6 vanishing
statements pending exact characteristic-zero certification. See
[`D0_PROGRAM.md`](D0_PROGRAM.md) — a conditional research program, not a
theorem, toward showing the announced degree-7 counterexample is minimal
within its equivariance class. Two pillars: (i) T-constant implies
automorphism (a degree-bookkeeping argument, well inside Moh's classical
plane-degree bound, citation being checked), and (ii) T-constant itself
reduces to seven finite radical-membership checks (`deg5_c_radical.sing`,
`deg6_c_radical.sing`), not a full ideal decomposition. Fast modular
previews (char 32003) of the degree-5 half currently show a clean sweep on
all attempted checks; only exact characteristic-zero certificates are
citable evidence, and modular results never move a status label.

## Degree-5/6 status (read before citing anything about degree 5)
An exact Singular `minAssGTZ` run on the degree-5 ideal is in progress (see
`out/deg5_qq_run_manifest.txt` for the run record). In parallel: three
independent modular runs (primes 32003, 32009, 65003) each found exactly 2
minimal primes with matching structure, and
`04-scripts/reconstruct_deg5_candidates.py` reconstructed exact rational
coefficients from them and independently verified 3 families (one splits into
2 branches) directly over ℚ — real, exact results, saved in
`03-certificates/deg5_candidate_branches.json`. `msolve` was tried as a
second engine and found genuinely inapplicable (it solves zero-dimensional
systems; this ideal is positive-dimensional) — a checked dead end, not a gap.
**None of this establishes exhaustiveness for degree 5.** The modular
component count is a heuristic preview, not a characteristic-zero
certificate. Throughout this repository, "partial, unconfirmed" is the
correct description for degree 5-7 claims, not "classified" or "decided."

## Contents
- **D0_PROGRAM.md** — working research note on degree-seven structural
  minimality (2026-07-22). Conditional; see the note's own status labels.
- **HANDOFF.md** — a self-contained task description for reproducing the
  certification pipeline: run `05-solver-inputs/certify_exhaustiveness.sing`
  in Singular, cross-check in Macaulay2, and confirm the printed
  `RESULT: EXHAUSTIVE` or `RESULT: GAP FOUND` line, plus the degree-5/6
  component lists.
- **01-notes/**
  - propositions-package.pdf — 2-page note: normal form, det DG = -T^2 det DF,
    mu(F)=mu(G).
  - main.pdf — longer conditional classification note (degree ≤ 4).
- **03-certificates/** — machine-verified artifacts: 6 distinct family
  certificates (explicit inverses, det identities, both compositions),
  independent verification report (6/6 pass), environment manifest,
  transcript. (Corrected 2026-07-21, twice, from an initial 49 raw branches
  to 6 distinct: within-file duplicate elimination-path branches were merged
  first, then one cross-file duplicate between a b0-stratum family and a
  main-branch family was found and merged. No family or certificate content
  was lost either time; see `04-scripts/generate_and_certify.py`'s dedup
  step.)
- **04-scripts/** — generate_and_certify.py (discovery),
  verify_certificates.py (independent, solving-free verifier), and
  emit_exhaustiveness_check.py (derives the exhaustiveness-certifier Singular
  input from the certified family list). Deliberately separate programs.
- **05-solver-inputs/** — Singular/Macaulay2 decomposition inputs, the
  auto-generated exhaustiveness certifier with all 6 distinct family ideals
  embedded, and the degree-5 (13 unknowns / 17 equations) and degree-6 (17
  unknowns / 25 equations) systems, plus the degree-5/6 radical-membership
  checks used by the D0 program above.

## Known limitations / remaining work
1. Degrees 5-6 exhaustiveness and the D0 program's radical-membership checks
   are in progress, not done: see "Degree-5/6 status" above and
   `D0_PROGRAM.md`. Exact ℚ runs are ongoing; 3 degree-5 families are
   individually verified but exhaustiveness is unconfirmed, and the D0
   program's seven checks have not yet all certified.
2. `main.pdf` is stale relative to `main.tex` (no LaTeX toolchain was
   available to recompile it here); cosmetic, does not affect the certified
   degree-4 result.

## Claim discipline (read before quoting anything externally)
- Proven by hand: ansatz, normal form (Q in ℂ[u], S in ℂ[v]), the determinant
  identity, μ(F) = μ(G) for dominant F.
- Machine-certified: everything in `03-certificates/`, branchwise.
- Machine-certified, 2026-07-21: exhaustiveness of the degree-≤4
  decomposition. The degree-≤4 classification is unconditional.
- Exact but incomplete, 2026-07-21: 3 degree-5 families
  (`03-certificates/deg5_candidate_branches.json`), each individually
  verified over ℚ (det = -1, explicit inverse, composition checked). Not a
  classification — exhaustiveness of these families is not established.
- Heuristic preview only, not a certificate: degree-5 ideal has "2 minimal
  primes" over three tested finite fields. Not a characteristic-zero fact.
- Not yet established: novelty of the identity beyond what is cited in
  `D0_PROGRAM.md`; anything about degree 5-7 minimality beyond the certified
  degree-4 result.
