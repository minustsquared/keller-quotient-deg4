# The D0 program: toward structural minimality of degree seven

**Status:** Research program / conditional theorem — working research note.
The degree-(≤4) result is proved; the degree-5 and degree-6 vanishing claims
below remain pending exact characteristic-zero certification.

*Working document, 2026-07-22. Status labels are load-bearing: **proved**
means certified in characteristic zero with kept transcripts; **pending**
means exactly that. Prompted by a question raised in discussion of this
classification — whether the low-degree computations expose structure that
could avoid ever-larger Gröbner runs. **They appear to: the remaining
computational content of the program below is seven finite vanishing
checks.***

## The observed law

Every certified family of the degree-≤4 Keller locus of the
(1,−1,−2)-equivariant class has **T ≡ 1** — the orbit-multiplier covariant
is constant, so F₃ = x after normalization (**proved**: all six families,
exhaustive decomposition certified in Singular and Macaulay2). The three
candidate degree-5 components have the same property (**modular-supported**;
exact characteristic-zero checks in progress). The announced degree-7
counterexample has T = 2−3u−v, nonconstant — the feature enabling the
contracted-divisor mechanism.

Define **D₀** = the smallest ordinary polynomial degree of a Keller map in
the normalized equivariant class with nonconstant T. Status: D₀ ≥ 5
(**proved**), D₀ ≥ 6 (**pending** exact degree-5 checks), D₀ ≥ 7
(**pending** degree-6 checks), D₀ ≤ 7 (the counterexample).

## Two pillars, both required

**(i) T constant ⇒ automorphism.** If T ≡ τ ∈ ℂ*, a diagonal target change
normalizes τ to 1 (degree- and automorphism-property-preserving; the
quotient identity persists with correspondingly normalized coordinates).
Then det DG ∈ ℂ*, so G is a plane Keller map; a degree count (weighted to
ordinary: 2(i+j) ≤ 2i+3j ≤ M ⇒ i+j ≤ ⌊M/2⌋) gives
deg G ≤ ⌈(deg F + 2)/2⌉ — so degree 6 upstairs is degree ≤ 4 downstairs,
far inside the classical verified plane-degree bound, commonly attributed
to Moh (plane Keller maps of degree ≤ 100 are automorphisms; exact citation
being checked; the current plane-counterexample bound is 108, historical
context only). Hence G is an automorphism, μ(F) = μ(G) = 1, and F — Keller
and birational — is a polynomial automorphism.

**(ii) deg F ≤ 6 ⇒ T constant.** Equivalent, by the Nullstellensatz, to
finitely many radical memberships: each nonconstant T-coefficient c_i lies
in √(I_D), where I_D is the full normalized Keller ideal at degree D. These
quantify over the entire complex locus directly — no component
decomposition, no exhaustiveness certificate in the loop. Seven checks
total: three at degree 5 (`deg5_c_radical.sing`), four at degree 6
(`deg6_c_radical.sing`), each a Rabinowitsch computation
1 ∈ I + ⟨1 − t·c_i⟩ over ℚ.

**If both pillars close: degree seven is minimal within the equivariance
class of the counterexample.** The Gröbner computations are then witnesses
to a finite vanishing statement inside a transparent argument, not the
argument itself.

## Validation discipline

Two levels throughout: fast modular previews (char 32003) for direction —
currently a clean sweep on every check attempted, including all 47
generators of the degree-5 containment certificate and all three degree-5
c-coefficients — and exact characteristic-zero certificates with kept
transcripts as the only citable evidence. Modular results never move a
status label. An independent `minAssGTZ` decomposition runs in parallel as
corroboration.

## Remaining write-up items (tracked, not hidden)

The per-degree normalization lemma (the unit-anchor slice, which is also
what fixes the Keller constant to −1 without an equation); invariance of
T-nonconstancy under the diagonal equivalences; the degree lemma above,
stated and proved; verification of the exact authorship of the Crelle 340
(1983) plane-degree-100 paper before the bibliography is final. A failed
degree-6 check would mean only that the vanishing is unproved — extracting
and verifying an actual nonconstant-T point would be required before any
stronger conclusion.

## Relation to circulating work

Gallagher's [`RESEARCH.md`](https://github.com/algal/jacobianfun/blob/main/RESEARCH.md)
(in [algal/jacobianfun](https://github.com/algal/jacobianfun), July 20) states
the class-wide quotient identity first and constructs families of every
generic fiber degree; the present program is the complementary
polynomial-degree direction. The classification through degree four, with
certificates, is at https://doi.org/10.5281/zenodo.21479448. A completed
theorem and its certificates will appear as a new version on the same
record.
