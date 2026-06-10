# The Aurelia Attractor

*A novel strange attractor with the silhouette of a moon jellyfish — discovered, certified, and named June 10, 2026.*

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

## Discovery method

The attractor was found by Monte-Carlo search over a seven-parameter
C₃-equivariant family (`python scripts/search_parameters.py`), filtering for
bounded orbits with a strongly positive largest Lyapunov exponent, then judged by
eye for beauty. The winning region of parameter space collapsed — remarkably — to
just **three distinct constants** (a, b, c) = (1.4, 0.5, 1.9) with the largest
Lyapunov exponent essentially unchanged.

## Reproduce everything

```bash
pip install -r requirements.txt

python scripts/verify_chaos.py        # certify chaos, write results/verification.json
python scripts/render_gallery.py      # render the gallery images
python scripts/bifurcation_scan.py    # sweep c, plot the route to chaos
python scripts/search_parameters.py   # re-run the original discovery search
```

Or use it as a library:

```python
from aurelia import trajectory

pts = trajectory(n_steps=1_000_000)   # (N, 3) points on the attractor
```

## License

MIT — see [LICENSE](LICENSE).
