# Paper plan: close the gap list, then draft the paper skeleton

Work in this repository (github.com/Sakeeb91/attractor-atlas, live viewer
sakeeb91.github.io/attractor-atlas). Read README.md and STORY.md first. Conventions: one logical
change = one atomic commit, pushed; verify every render by viewing the PNG; claims must be
measured or carefully hedged.

Environment notes (fresh instances): pip install numpy>=2.3 scipy matplotlib dysts numba.
Installing dysts may downgrade numpy below 2.2, which breaks matplotlib black-background 3D
scatter (renders come out pure black) - reinstall numpy>=2.3 afterwards. numpy histogram calls
must use explicit bin edges (already done in atlas/fingerprint.py). Use np.ptp(arr), not arr.ptp().

## Context: the publication decision (already made)

The project holds three certified, named strange attractors and a quality-diversity search engine:
- Aurelia (C3): (a,b,c)=(1.4,0.5,1.9), spectrum (+0.2327,~0,-1.5119), D_KY 2.155, one saddle-focus
  (0,0,1.523), novelty 0.185 vs dysts (nearest Aizawa).
- Naiad (C2): (1.2,0.68,3.7,1.7,1.2,2.0,2.1), lambda1 +0.296, D_KY 2.110, saddle-focus (0,0,1.651),
  novelty 0.34 (nearest SprottJerk). Off-axis equilibria algebraically impossible.
- Cassiopea (C4): (2.0,0.85,1.8,0.9,1.28,1.8,2.8), lambda1 +0.525, D_KY 2.218, saddle-focus
  (0,0,1.611) + C4 quadruple of distant saddles at radius 3, novelty 0.224 (nearest NoseHoover).
- Engine (atlas/): MAP-Elites over Cn-equivariant flows n=2..5 (complex form
  dw/dt=[a(z-b)+i*omega]w + g*conj(w)^(n-1); dz/dt=mu+nu*z-z^3-lam*|w|^2), batched RK4 evaluator,
  D2-histogram+PCA fingerprints (atlas/fingerprint.py), novelty = min distance to the 135-system
  dysts catalog (results/catalog_fingerprints.json) + archive. First run: 4,608 candidates/127 s,
  62 elites (results/atlas/archive.json).

**The paper is a METHODS paper**: "quality-diversity search with catalog-grounded novelty discovers
families of equivariant strange attractors." The three attractors are exhibits, NOT the claim.
Do not frame as "new chaotic systems" (saturated genre; see Sprott, "A proposed standard for the
publication of new chaotic systems", IJBC 2011). Venues: arXiv nlin.CD first, then GECCO QD track
or ALIFE (methods audience) or Chaos/AIP (dysts lineage). Known positioning risk: Letellier &
Gilmore have extensive work on equivariant 3-D flows (*The Symmetry of Chaos*, 2007) and the
multi-scroll literature has Cn-symmetric constructions; current README/STORY novelty framing
(only Field-Golubitsky + Aizawa as relatives) must be strengthened against that.

## The gap list (work in this order, one commit each minimum)

1. **Literature positioning pass** (highest value). Survey and summarize, with full citations:
   Letellier & Gilmore equivariant/cover-image flow work; Cn-symmetric multi-scroll/multi-wing
   attractors (Lu, Chen lineage); Sprott 1994 "Some simple chaotic flows" + Sprott 2011 standard;
   Gilpin dysts (arXiv:2110.05266); Mouret & Clune MAP-Elites (arXiv:1504.04909); Lehman & Stanley
   novelty search; Field & Golubitsky *Symmetry in Chaos*. For each: what they did, how this work
   differs, what claims need rewording. Use WebSearch/alphaxiv-paper-lookup skills. Output:
   docs/RELATED_WORK.md + a follow-up commit softening any README/STORY claim that does not survive
   (especially "no published 3-D flow with discrete Cn equivariance": verify or hedge it).
2. **Lyapunov rigor**. New scripts/convergence_study.py: for each of the three systems compute the
   full spectrum at dt in {0.01, 0.005, 0.0025}, n_steps in {2e5, 4e5, 8e5}, 10 random ICs;
   report mean +/- std for lambda1 and D_KY (segment-based error bars); confirm lambda2 -> 0 as a
   consistency check. Output: results/convergence.json + a small figure (gallery/convergence.png)
   + updated certified numbers in README if they shift (they should not by much).
3. **Fingerprint validation**. New scripts/validate_fingerprint.py: (a) within-dysts sanity: do
   known families cluster (Lorenz-like near Lorenz-like)? nearest-neighbor table for 10 famous
   systems; (b) robustness: fingerprint variance across trajectory seeds/subsamples for one system
   vs between-system distances (signal-to-noise ratio); (c) a 2-D embedding (MDS or PCA of the
   distance matrix) with the three new attractors plotted among the catalog. Output: results +
   gallery/fingerprint_map.png (this is likely a key paper figure).
4. **Shilnikov homoclinic hunt** (strengthens the dynamics story). New scripts/homoclinic_hunt.py:
   for Aurelia, shoot trajectories from the saddle-focus unstable eigenplane (small radius along
   eigenvectors of the Jacobian at (0,0,1.523)), measure closest return to the equilibrium, sweep
   one parameter (c) and bisect on the return-distance minimum. Report whether a near-homoclinic
   parameter exists. Repeat for Naiad/Cassiopea if cheap. Output: results + one figure.
5. **Optional, only if time**: quantify the beauty claim: scatter lambda1 and D_KY of archive
   elites vs a simple visual-richness proxy (fill factor from the fingerprint); one figure, or
   drop aesthetics to a remark in the paper.

## Then: the paper skeleton

Create paper/main.tex (start venue-agnostic: plain article class + natbib; switch to ACM sigconf
for GECCO or AIP template for Chaos at submission). Sections, with content mapping:
1. Introduction: discovery-of-dynamics framing; Sprott 1994 random search as ancestor; what QD adds.
2. Related work: from docs/RELATED_WORK.md (gap task 1).
3. Method: 3.1 the equivariant family (complex form, why conj(w)^(n-1), one paragraph of the
   machine metaphor from STORY.md); 3.2 batched evaluation + gates (atlas/family.py); 3.3 shape
   fingerprints + catalog-grounded novelty (atlas/fingerprint.py, dysts); 3.4 MAP-Elites archive
   (atlas/map_elites.py: cells = symmetry order x lambda1 x aspect).
4. Results: 4.1 the atlas run (4,608 candidates, 62 elites, throughput); 4.2 the three certified
   systems w/ table (params, spectra, D_KY, equilibria, novelty distances + the 83% baseline stat);
   4.3 convergence/error bars (gap 2); 4.4 fingerprint map figure (gap 3); 4.5 bifurcation +
   Shilnikov evidence (existing bifurcation_c.csv + gap 4); 4.6 the non-monotonic chaos-vs-n
   observation (0.296, 0.233, 0.525) as an open question.
5. Limitations: numerical (not rigorous) certification; dysts is 135 systems, not the literature;
   fingerprint crudeness; aesthetics subjectivity.
6. Reproducibility: everything is one script per claim in the public repo + live viewer URL.
Figures already available: gallery/{aurelia,naiad,cassiopea}_*.png, atlas_montage.png,
bifurcation.png; add convergence.png + fingerprint_map.png from the gap work.
Commit the skeleton with placeholder text per section, then fill sections in separate commits.

## Acceptance criteria

Each gap item: script committed, results committed, one-line summary added to README only if it
changes a public claim. Paper skeleton compiles (pdflatex). Everything pushed. Report at the end:
which claims survived the literature pass, the error-barred lambda1 values, the fingerprint
validation verdict, and homoclinic-hunt outcome.
