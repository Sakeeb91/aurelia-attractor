# The Aurelia Attractor

*A novel strange attractor with the silhouette of a moon jellyfish — discovered, certified, and named June 10, 2026.*

**[Explore it live in your browser](https://sakeeb91.github.io/aurelia-attractor/)**: a WebGL viewer with 400,000 orbit points, 3,000 particles riding the flow in real time, orbit controls, and live parameter sliders.

**[Read the story](STORY.md)**: a long-form narrative of the discovery, from the failed first family through the 600-universe search to the certification of chaos.

![The Aurelia attractor](gallery/aurelia_hero.png)

## The system

The Aurelia attractor lives in a three-dimensional autonomous flow with two quadratic
nonlinearities in the plane and a cubic one on the axis:

```
dx/dt = a(z − b)x − cy + b(x² − y²)
dy/dt = cx + a(z − b)y − 2bxy
dz/dt = a(1 + z) − z³ − c(x² + y²)
```

with the canonical parameters

```
a = 1.4,   b = 0.5,   c = 1.9
```

and any generic initial condition near the origin, e.g. `(0.3, 0.2, 0.1)`.

Writing the planar coordinates as a single complex number **w = x + iy**, the system
collapses to two elegant equations:

```
dw/dt = [a(z − b) + ic] w + b w̄²
dz/dt = a(1 + z) − z³ − c|w|²
```

The conjugate-squared term `w̄²` is the heart of the design: under a rotation of the
plane by 120°, `w → e^(2πi/3) w` maps solutions to solutions, so the flow is
**equivariant under the cyclic group C₃**. The strange attractor inherits this
three-fold symmetry — visible as the triskelion in the crown view below. The `z`
equation couples back through the radius `|w|²` alone, preserving the symmetry while
pumping trajectories vertically.

## Why "Aurelia"

*Aurelia aurita* is the moon jellyfish. Seen from the side, the attractor is a
translucent bell with veils trailing beneath it and a luminous column rising through
its center — the unstable axis along which trajectories are reinjected. From the
Latin *aureus*, "golden": orbits spend their slow hours in the gilded crown at the
top of the bell before being flung back into the dark. The name was unclaimed in the
dynamical-systems literature at the time of discovery.

## Gallery

| The crown (top view) | The bell (side view) |
|---|---|
| ![Crown view](gallery/aurelia_crown.png) | ![Bell view](gallery/aurelia_bell.png) |

![Contact sheet](gallery/aurelia_sheet.png)

One full orbit of the camera (`python scripts/render_animation.py`):

![Rotating view](gallery/aurelia_rotation.gif)

## Certification of chaos

All numbers below are reproducible with `python scripts/verify_chaos.py`
(recorded in [`results/verification.json`](results/verification.json)).

| Property | Value |
|---|---|
| Lyapunov spectrum (Benettin/QR, 600k steps) | **λ₁ = +0.2327**, λ₂ = +0.0013 ≈ 0, λ₃ = −1.5119 |
| Kaplan–Yorke dimension | **D_KY ≈ 2.155** (fractal) |
| λ₁ across 5 random initial conditions | 0.195 … 0.252 (always positive) |
| Equilibria | exactly one: saddle-focus at (0, 0, 1.5229) |
| Eigenvalues at the equilibrium | 1.432 ± 1.9i (unstable spiral), −5.558 (strong contraction) |
| Boundedness | confirmed over 4,000,000 RK4 steps |
| Time-averaged divergence | −1.290 (dissipative: volumes contract onto the attractor) |
| Attractor extent | x ∈ [−1.40, 1.60], y ∈ [−1.67, 1.27], z ∈ [−0.98, 1.50] |

The signature `(+, 0, −)` spectrum with a fractal dimension strictly between 2 and 3
certifies a **strange attractor**, not a limit cycle or a transient.

### One equilibrium to rule them all

The flow has a *single* fixed point — a saddle-focus on the symmetry axis with
Shilnikov-type geometry. Trajectories spiral outward around the axis (eigenvalues
1.432 ± 1.9i), spill over the rim of the bell, fall along the outer veils, and are
recaptured by the strongly contracting direction (−5.558) at the base of the central
column. Stretch, fold, repeat — forever, never twice the same way.

### Route to chaos and limit cycles

Sweeping the rotation rate `c` with `a, b` fixed
(`python scripts/bifurcation_scan.py`) shows the chaotic sea and its periodic
windows: where the largest Lyapunov exponent falls to ≈ 0, the attractor collapses
to a stable limit cycle; where it is positive, chaos reigns. The canonical
`c = 1.9` sits inside a robust chaotic band.

![Bifurcation scan](gallery/bifurcation.png)

## Novelty

Searched June 10, 2026, before publication:

* **The functional form** — a 3-D autonomous flow built from the C₃-equivariant
  complex coupling `w̄²` (i.e. the pair `x² − y²`, `−2xy`) joined to cubic `z`
  dynamics through `|w|²` — does not appear in the known attractor catalogues
  (Lorenz, Rössler, Thomas, Aizawa/Langford, Halvorsen, Dadras, Chen, Sprott A–S,
  Rabinovich–Fabrikant, multi-scroll/multi-wing families) or in web/literature
  searches for the equation terms.
* **Closest relatives, and how this differs:** Field & Golubitsky's celebrated
  *symmetric chaos icons* use equivariant polynomial couplings of the same spirit —
  but they are 2-D discrete **maps**, not continuous 3-D flows. The Aizawa/Langford
  attractor is a 3-D flow with rotational coupling — but it is SO(2)-symmetric
  (continuous rotation), has no equivariant `w̄²` term, and has a qualitatively
  different two-equilibrium structure. The Aurelia system occupies the unexplored
  intersection: *continuous flow* × *discrete C₃ equivariance* × *single
  saddle-focus*.
* **The name** "Aurelia attractor" had no prior usage.
* **Measured novelty.** Beyond the literature search, novelty is now a number:
  reducing attractors to shape fingerprints (D2 distance histograms + PCA shape
  ratios, see `atlas/fingerprint.py`) and comparing against all 135 known
  chaotic systems in the [dysts](https://github.com/williamgilpin/dysts)
  catalog, Aurelia's nearest known neighbor is the Aizawa attractor at
  distance 0.185. The catalog's own median nearest-neighbor spacing is 0.115;
  83% of known systems sit closer to something known than Aurelia does. By
  this metric, Aurelia is more isolated in shape space than five-sixths of
  the established bestiary, and its nearest relative is exactly the system
  the qualitative analysis predicted.

## Discovery method

The attractor was found by Monte-Carlo search over a seven-parameter
C₃-equivariant family (`python scripts/search_parameters.py`), filtering for
bounded orbits with a strongly positive largest Lyapunov exponent, then judged by
eye for beauty. The winning region of parameter space collapsed — remarkably — to
just **three distinct constants** (a, b, c) = (1.4, 0.5, 1.9) with the largest
Lyapunov exponent essentially unchanged.

## The atlas engine: searching for the next Aurelia

`atlas/` is a quality-diversity search engine that hunts for *new* chaotic
attractors in the C&#8345;-equivariant generalization of Aurelia's design
(rotation orders n = 2 to 5, so two-, four-, and five-fold flowers are in
reach). Instead of optimizing a single score, it runs MAP-Elites: descriptor
space (rotation order × Lyapunov exponent × vertical aspect) is tiled into
cells, and each cell keeps the candidate most *novel* relative to a reference
set of known attractors.

Novelty is a measured number, not a literature claim: every candidate's orbit
is reduced to a shape fingerprint (D2 pairwise-distance histogram + PCA shape
ratios + fill factor), and its novelty is the minimum fingerprint distance to
the [dysts](https://github.com/williamgilpin/dysts) catalog of known chaotic
systems plus everything already discovered in the archive.

```bash
pip install dysts                                # reference catalog (one-time)
python scripts/build_catalog_fingerprints.py     # fingerprint known systems (one-time)
python scripts/run_atlas.py 12 96                # search: 12 generations, batches of 96
python scripts/render_atlas_montage.py           # render the most novel elites
```

The batched evaluator integrates an entire population simultaneously with
vectorized complex RK4 and reproduces Aurelia's Lyapunov exponent as a
sanity check. The archive persists across runs (`results/atlas/archive.json`),
so the search compounds.

## Naiad: the first attractor the atlas found

The first thing the search turned up worth keeping is **Naiad**, the two-fold
(C₂) sibling of Aurelia, named for the water nymph of fountains and springs.
Where Aurelia rotates three-fold, Naiad uses rotation order n = 2, so the
conjugate term is simply `conj(w)`: an anisotropic stretch that makes the
flow symmetric under a half-turn `(x, y) → (−x, −y)`. The attractor is a
flaring **fountain**: a wide turbulent bowl, a bright jet up the central
axis, a narrow stem at the base. Seen from above it is a lens, not a disk,
because two-fold symmetry stretches it along one direction.

![The Naiad attractor](gallery/naiad_hero.png)

| The lens (top) | The jet (side) |
|---|---|
| ![Naiad lens](gallery/naiad_lens.png) | ![Naiad jet](gallery/naiad_jet.png) |

```
dx/dt = (a(z − b) + g)x − w·y
dy/dt = w·x + (a(z − b) − g)y          a=1.2, b=0.68, w=3.7, g=1.7,
dz/dt = mu + nu·z − z³ − lam(x² + y²)   mu=1.2, nu=2.0, lam=2.1
```

Certified the same way as Aurelia (`python scripts/verify_naiad.py`,
recorded in [`results/naiad_verification.json`](results/naiad_verification.json)):

| Property | Value |
|---|---|
| Lyapunov spectrum | **λ₁ = +0.296**, λ₂ = +0.001 ≈ 0, λ₃ = −2.696 |
| Kaplan–Yorke dimension | **D_KY ≈ 2.110** |
| λ₁ across 5 random initial conditions | 0.284 … 0.341 (always positive) |
| Equilibria | exactly one: saddle-focus at (0, 0, 1.651) |
| Eigenvalues at the equilibrium | 1.166 ± 3.286i (unstable spiral), −6.18 |
| Time-averaged divergence | −2.386 (dissipative) |
| Novelty vs the dysts catalog | nearest known system **SprottJerk at distance 0.34** |

That novelty distance of 0.34 makes Naiad *more* isolated in shape space than
Aurelia (0.185), against a catalog whose median nearest-neighbor spacing is
0.115. Like Aurelia, it is organized by a single Shilnikov-type saddle-focus,
here with a faster spiral.

## Cassiopea: the four-fold member

**Cassiopea** completes a three-member family (C₂ Naiad, C₃ Aurelia, C₄
Cassiopea), named for *Cassiopea*, the upside-down jellyfish whose bell
carries a four-leaf-clover marking: a real animal with genuine four-fold
symmetry. The equivariant term is `conj(w)³`, the unique cubic surviving a
quarter-turn `w → iw`. Seen from above the attractor is a **four-armed
pinwheel star** with a white spiral core; from the side, a layered bell
with twin curtains.

![The Cassiopea attractor](gallery/cassiopea_hero.png)

| The star (top) | The bell (side) |
|---|---|
| ![Cassiopea star](gallery/cassiopea_star.png) | ![Cassiopea bell](gallery/cassiopea_bell.png) |

```
dx/dt = a(z − b)x − w·y + g(x³ − 3xy²)
dy/dt = w·x + a(z − b)y + g(y³ − 3x²y)     a=2.0, b=0.85, w=1.8, g=0.9,
dz/dt = mu + nu·z − z³ − lam(x² + y²)       mu=1.28, nu=1.8, lam=2.8
```

Certified via `python scripts/verify_cassiopea.py`
([`results/cassiopea_verification.json`](results/cassiopea_verification.json)):

| Property | Value |
|---|---|
| Lyapunov spectrum | **λ₁ = +0.525**, λ₂ ≈ 0, λ₃ = −2.412 |
| Kaplan–Yorke dimension | **D_KY ≈ 2.218** |
| λ₁ across 5 random initial conditions | 0.490 … 0.555 (always positive) |
| Equilibria | a central saddle-focus at (0, 0, 1.611) plus a C₄ quadruple of distant saddles |
| Eigenvalues at the saddle-focus | 1.522 ± 1.8i (unstable spiral), −5.984 |
| Time-averaged divergence | −1.868 (dissipative) |
| Novelty vs the dysts catalog | nearest known system NoseHoover at distance 0.224 |

Cassiopea carries the **strongest chaos and deepest fractal structure of the
family** (Aurelia λ₁ = 0.233, Naiad 0.296, Cassiopea 0.525), and it is the
first member with off-axis equilibria: four distant saddles at radius 3,
arranged in a square far below the attractor, with the familiar single
saddle-focus engine on the axis.

## Reproduce everything

```bash
pip install -r requirements.txt

python scripts/verify_chaos.py        # certify Aurelia, write results/verification.json
python scripts/render_gallery.py      # render the Aurelia gallery
python scripts/bifurcation_scan.py    # sweep c, plot the route to chaos
python scripts/search_parameters.py   # re-run the original discovery search
python scripts/verify_naiad.py        # certify Naiad, write results/naiad_verification.json
python scripts/render_naiad.py        # render the Naiad gallery
python scripts/verify_cassiopea.py    # certify Cassiopea
python scripts/render_cassiopea.py    # render the Cassiopea gallery
```

Or use it as a library:

```python
from aurelia import trajectory

pts = trajectory(n_steps=1_000_000)   # (N, 3) points on the attractor
```

## License

MIT — see [LICENSE](LICENSE).
