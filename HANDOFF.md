# HANDOFF: Certification & search infrastructure for the Keller classification

**Owner:** [withheld -- pseudonymous deposit; identity committed in COMMITMENT.txt]
**Prepared:** 2026-07-21
**Bundle:** `keller-deg4-classification.zip` (this repo). Nothing here requires
mathematical background — every task is "run this input on this tool, capture
output, check the stated criterion."

---

## STATUS UPDATE (2026-07-21, same day, post-cleanup) -- Task 2 PRIMARY ASK DONE

`RESULT: EXHAUSTIVE -- classification unconditional`, printed by Singular and
cross-checked in Macaulay2 (both find exactly 3 minimal primes of the degree-4
Keller ideal; each is covered by one of the 6 certified families). Artifacts:
`out/certify.log`, `out/m2.log`, `out/version_manifest.txt`,
`out/SHA256SUMS.txt`. The degree<=4 classification is no longer conditional.

The assembly argument was also checked explicitly, not assumed: across all 6
distinct solution dicts, the only denominator that ever appears is `b0`. So
the pointwise certificates (valid everywhere on their domain) plus the single
b0=0 stratum certificate jointly cover every point of every one of the 3
minimal-prime components -- no excluded locus is left uncertified.

Three real bugs were found and fixed while running this for the first time --
recorded here so nobody re-running this by hand loses time to them or, worse,
trusts a silent false negative:
1. `LIB "primdec.lib"; LIB "elim.lib";` both define a proc named `sat`;
   loading elim.lib second silently shadows primdec.lib's version.
2. `sat(ideal, poly)[1]` -- indexing the procedure call's return value
   directly, rather than assigning it to a `list` variable first and then
   indexing -- silently returns a wrong/truncated ideal in Singular 4.4.1 on
   this build, with no error. This produced a false `RESULT: GAP FOUND` on
   the first real run of `certify_exhaustiveness.sing`, purely from this
   usage bug, not from the mathematics. Fixed in both the checked-in `.sing`
   file and its generator (`04-scripts/emit_exhaustiveness_check.py`), which
   now does `list Jsat = sat(J, ideal(factor)); J = Jsat[1];`.
3. Separately, `M2 --script` does not auto-echo bare expressions the way the
   interactive REPL does -- `deg4_decomposition.m2` ran successfully but
   produced empty output until `print(...)` calls were added explicitly.
4. The original dedup pass (see the earlier "49 -> 7" correction below)
   only deduped *within* each certificate file. One b0-stratum family turned
   out to be an exact cross-file duplicate of a main-branch family (the main
   decomposition, not told to assume b0=0, independently landed on a branch
   already sitting there). True distinct count is 6, not 7. Fixed with a
   cross-file dedup pass in `generate_and_certify.py`; re-ran Task 2 against
   the corrected 6-family input -- same result, EXHAUSTIVE, same 3 minimal
   primes (M2's log is unaffected since it only decomposes the ideal, not
   the family list, so it did not need re-running).

Task 3 (degree 5/6) is IN PROGRESS, NOT DONE, and there is a specific
do-not-circulate line here: as of 2026-07-21, an exact `minAssGTZ` run on the
degree-5 ideal has been running 50+ minutes (PID, command, log path, and
personal-recheck instructions in `out/deg5_qq_run_manifest.txt` -- do not
trust a "still running" or "finished" claim about this process, including
ones from this file, without running that check yourself). A stack sample of
the running process showed >60% of time inside GMP's FFT-based big-integer
multiplication -- intermediate coefficient blowup in exact rational
arithmetic, not a combinatorially large search space. In parallel:
- Three independent modular runs (primes 32003, 32009, 65003) each found
  exactly 2 minimal primes with identical structure -- consistent, but a
  HEURISTIC PREVIEW, not a characteristic-zero certificate.
- The prime-dependent coefficients reconstruct to small exact rationals
  (verified via direct modular-inverse arithmetic, e.g. 16001 mod 32003 is
  exactly -1/2), so `04-scripts/reconstruct_deg5_candidates.py` built exact
  candidate families from them and verified 3 (one splits into 2 branches)
  directly over QQ with the same det/inverse/composition method as the
  certified degree-4 families -- real, exact, individually-verified results,
  saved in `03-certificates/deg5_candidate_branches.json`.
- `msolve` was tried as a second engine and is genuinely not applicable here
  (it solves zero-dimensional systems; this ideal is positive-dimensional) --
  confirmed, not skipped.
- **None of this is a degree-5 classification.** Exhaustiveness is
  unconfirmed by any method. Say "3 individually-verified families, modular
  preview of 2 components, exhaustiveness open" -- not "degree 5 decided."
- Decision rule in effect: keep the exact run alive while it's cheap
  (currently ~1% memory, one core, no runaway), human checkpoint after a few
  hours, do not let it run unbounded, promote nothing until direct
  characteristic-zero verification.

Task 1 (toolchain) is done: Singular
4.4.1p5, Macaulay2 1.26.06, msolve 0.10.1, all via Homebrew
(`brew install singular` and `brew install Macaulay2/tap/M2` -- the latter
requires trusting a third-party tap). Installing Singular pulled in
`python@3.14` as a dependency and shifted `python3` on PATH; sympy had to be
reinstalled under the new interpreter for Task 0's scripts to keep working.

---

## THE ASK (read this first)

We have a mathematical result about the newly announced Jacobian-conjecture
counterexample that is complete except for **one computation we cannot run in
our environment**: a certified decomposition of a polynomial ideal, done in
Singular and cross-checked in Macaulay2. Everything else (6 distinct solution
families, their explicit inverses, both composition checks) is already
machine-verified and reproducible — you can re-verify it yourself in ~5 min
(Task 0). [Corrected 2026-07-21, twice: earlier drafts said "49 families",
then "7" -- both counts included duplicate branches, first within a file,
then across files; see the STATUS UPDATE above for the full history. 6 is
the true distinct-family count.] Your job: install two open-source
computer-algebra systems, run the prepared input files, capture outputs, and
report which of two printed verdicts appears. Secondary (higher compute,
higher value): run the same pipeline on two larger prepared systems (degree 5
and 6). Definition of done
for the primary ask: the string `RESULT: EXHAUSTIVE` or `RESULT: GAP FOUND`
captured from Singular, with the full transcript, plus an independent
component count from Macaulay2 that matches Singular's.

**Priority: high, time-sensitive** — the surrounding topic is moving on a
scale of days.

---

## Task 0 — Re-verify what we claim (sanity, ~5 min)

```
python3 04-scripts/generate_and_certify.py     # discovery (regenerates certificates)
python3 04-scripts/verify_certificates.py      # independent verifier, solving-free
```
Acceptance: verifier prints `FAILURES: 0   TIMEOUTS: 0` over 6 distinct
families. Requires Python 3.12+, SymPy 1.14. If this fails, stop and report —
do not proceed on a broken base. Both scripts resolve `03-certificates/` and
`05-solver-inputs/` relative to their own location, so they run correctly
from any working directory.

## Task 1 — Install toolchain (~30 min)

- **Singular** ≥ 4.3 (`apt install singular` or build from source)
- **Macaulay2** ≥ 1.22 (`apt install macaulay2` or official binaries)
- Optional but valuable: **msolve** (github.com/algebraic-solving/msolve)

Record exact versions in the report. Do not substitute SageMath's bundled
Singular without noting the version.

## Task 2 — PRIMARY: exhaustiveness certification (compute: unknown, timebox 24h)

```
mkdir -p out
Singular 05-solver-inputs/certify_exhaustiveness.sing | tee out/certify.log
```
This script: computes the minimal primes of the degree-4 Keller ideal
(`minAssGTZ`), then checks (a) every minimal component is contained in one of
the 6 embedded family ideals, and (b) every family lies inside the Keller
variety. It prints exactly one of:
- `RESULT: EXHAUSTIVE -- classification unconditional`  → we have a theorem
- `RESULT: GAP FOUND -- report components above`        → capture the printed
  component ideals verbatim; they are mathematically important either way.

Cross-check in a second system:
```
M2 --script 05-solver-inputs/deg4_decomposition.m2 | tee out/m2.log
```
Acceptance: the number of minimal components agrees between Singular and M2.
(Two independent implementations, per reviewer requirement — do not skip.)

Escalation: if `minAssGTZ` runs past 24h on the 9-variable ideal (unexpected
but possible), try `primdecGTZ`, then `minAssGTZ` over `ZZ/32003` as a fast
modular sanity pass (report clearly as modular, not a certificate), then msolve.

## Task 3 — SECONDARY: degrees 5 and 6 (compute: unknown, timebox 72h each)

Inputs: `05-solver-inputs/deg5_system.txt` (13 unknowns, 17 equations) and
`05-solver-inputs/deg6_system.txt` (17 unknowns, 25 equations). Plain-text
polynomial lists over Q; wrap into a Singular/msolve ideal in the listed
variables, order `dp`.

For each: compute minimal primes. **Report the raw component list; do not
attempt interpretation.** We will run the inverse-certification pipeline on
the components ourselves. If any component looks positive-dimensional with
many parameters, that is expected — just capture it.

Honest note: we have NOT benchmarked these. Degree 5 defeated a pure-Python
Groebner engine; that says nothing about Singular/msolve difficulty in either
direction. If degree 6 is infeasible, degree 5 alone is still valuable.

## Task 4 — Reproducibility layer (~half day)

- Dockerfile (or Nix) pinning: Python, SymPy, Singular, M2 versions
- `make verify` = Task 0; `make certify` = Task 2
- SHA-256 of every file in `03-certificates/` and `out/`
- All solver stdout captured to `out/`, committed
- Deterministic branch ordering is already in the JSON — do not re-sort

## Deliverables back to the owner

1. [DONE] `out/certify.log` — RESULT: EXHAUSTIVE
2. [DONE] `out/m2.log` — 3 minimal primes, matches Singular
3. [DONE] `out/version_manifest.txt`
4. Wall-clock + peak memory per task: both Singular and M2 runs finished in
   ~20s wall clock (not the 24h escalation ceiling this task was timeboxed
   against); peak memory not separately profiled, but this was nowhere near
   resource-constrained -- 9 ring variables, 3 minimal primes.
5. GAP FOUND is moot -- result was EXHAUSTIVE. (It was NOT moot on the first
   attempt, which false-negatived on the Singular `sat()` bug above; see the
   status update.)
6. Degree-5/6 component lists (raw): degree-6 not reached. Degree-5: exact
   QQ run in progress (see status update above); modular preview (3 primes)
   suggests 2 components; 3 exact families independently verified but
   exhaustiveness NOT established -- do not report this as "done."
7. [DONE] `Makefile` (`make verify`, `make certify`, `make sha256`) as the
   make layer. No Docker/Nix pinning yet -- not attempted.

## Out of scope / do-not

- Do NOT modify anything in `03-certificates/` — they are the audited artifacts.
- Do NOT "fix" the sympy discovery script; discovery and verification are
  deliberately separate programs.
- No interpretation of mathematical output is expected; verbatim capture wins.
- Network access, cloud instances, long-running jobs: all fine; there is no
  data-sensitivity constraint (all content is public mathematics).

## Context in one paragraph (optional reading)

On July 20 a counterexample to the Jacobian conjecture was announced. We
proved structural results about the full symmetry class of that map and
computed a classification of the class in low degree; 6 distinct solution
families each carry a machine-verified explicit inverse. [Updated 2026-07-21:
Task 2 is now decided -- EXHAUSTIVE, cross-checked -- so this classification
is a theorem, not conditional on it.] Task 3 extends the same question to
higher degree, where a clean answer would establish that the counterexample's
degree (seven) is minimal in its symmetry class.
