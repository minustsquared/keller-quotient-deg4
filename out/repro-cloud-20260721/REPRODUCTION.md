# Clean-environment reproduction — 2026-07-21

Independent re-run of the Level-2 pipeline (Task 0 of HANDOFF.md) in an
environment disjoint from the one that produced the audited artifacts.

## Environment

| | Original (audited) | This reproduction |
|---|---|---|
| OS | macOS (Homebrew toolchain) | Ubuntu 24.04.4 LTS, x86_64 (isolated cloud container) |
| Python | 3.14 (Homebrew) | 3.11.15 (system) |
| SymPy | 1.14.0 | 1.14.0 |

SymPy 1.14.0 was vendored as a pure-Python package (with mpmath); no other
third-party code was involved. The audited files in `03-certificates/` and
`05-solver-inputs/` were NOT modified; all regeneration happened in a scratch
copy and was compared back against the audited originals.

## What was run

1. `verify_certificates.py` against the **audited, unmodified** certificates:
   `FAILURES: 0   TIMEOUTS: 0` over all 6 distinct families
   (transcript: `repro_verify_audited.log`).
2. `generate_and_certify.py` from scratch (full rediscovery:
   27 solve() branches -> 5 distinct main families + 1 distinct b0-stratum
   family after cross-file dedup; ~19 s wall clock)
   (transcript: `repro_generate_transcript.log`).
3. `emit_exhaustiveness_check.py` from the regenerated certificates.
4. Byte-comparison of every regenerated artifact against the audited one:

| File | Result |
|---|---|
| `03-certificates/deg4_main_branches.json` | IDENTICAL |
| `03-certificates/deg4_b0_stratum.json` | IDENTICAL |
| `05-solver-inputs/deg4_decomposition.sing` | IDENTICAL |
| `05-solver-inputs/deg4_decomposition.m2` | IDENTICAL |
| `05-solver-inputs/certify_exhaustiveness.sing` | IDENTICAL |
| `05-solver-inputs/deg5_system.txt` | IDENTICAL |

5. `verify_certificates.py` against the regenerated certificates:
   `FAILURES: 0   TIMEOUTS: 0` (same result; necessarily so, given
   byte-identity, but run anyway).

## What this does and does not establish

Establishes: the discovery pipeline and the solving-free verifier are fully
reproducible across OS, CPU architecture-independent Python versions, and
machines; the audited certificates are exactly what the published scripts
produce; the verifier passes on the audited artifacts in an environment that
has never touched them before.

Does not establish anything new about Level 3 (exhaustiveness): that
certification ran in Singular 4.4.1p5 and Macaulay2 1.26.06 on the original
machine (`out/certify.log`, `out/m2.log`) — two independent CAS
implementations, per the reviewer requirement. Neither CAS was installable in
this container (network egress restricted), so the Singular/M2 runs were not
re-executed a third time here.
