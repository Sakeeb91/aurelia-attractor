# The Jellyfish in the Equations

*How a hunt for beauty in a seven-dimensional parameter space turned up a new strange attractor, organized by a single unstable point, that looks like a moon jellyfish and answers to three numbers.*

![The Aurelia attractor](gallery/aurelia_hero.png)

There is exactly one place in the Aurelia system where nothing happens.

It sits on the vertical axis, at the point (0, 0, 1.523), and if you could balance there, the equations would hold you motionless forever. You cannot balance there. The point repels almost everything that approaches it, flinging nearby trajectories outward in a widening spiral, over the rim of a bell-shaped shell, down along translucent veils, and back up through a narrow central column to spiral out all over again. No trajectory ever repeats. No trajectory ever leaves. The result, traced over millions of orbits, is the luminous object above: a strange attractor that did not exist in the literature before June 10, 2026, and that looks, from the side, remarkably like a moon jellyfish.

This is the story of how it was found, why it has the shape it has, and what it took to certify that the thing in the picture is genuine chaos rather than an elaborate accident.

## An old kind of object

A dynamical system is just a rule for how a point moves: given where you are, the rule tells you where you go next. Weather, planetary orbits, the voltage in a neuron, all can be written this way. For three centuries after Newton, mathematicians expected such rules to produce tame behavior in the long run. Trajectories should settle down: to a standstill, or to a repeating loop called a limit cycle.

In 1963 the meteorologist Edward Lorenz found a third possibility hiding in a toy model of convection. His trajectories settled onto something, but the something was neither a point nor a loop. It was an infinitely layered butterfly-shaped set on which motion remained forever erratic, forever bounded, and exquisitely sensitive: two trajectories starting a hair apart would diverge exponentially until they bore no resemblance to each other. The set attracted everything around it, yet motion on it never repeated. Such objects came to be called strange attractors, and they are the geometric face of chaos.

Since Lorenz, a bestiary has accumulated. Rössler's single spiral fold. Thomas's cyclically symmetric weave. The Aizawa attractor's rotating column. Sprott's alphabetized menagerie of minimal chaotic flows. Each is a specific system of ordinary differential equations, usually three of them, with specific constants, that happens to fold space onto a fractal set. Finding a new one is not hard if you do not care what it looks like. Finding one worth looking at is a different problem.

## Designing with symmetry

The hunt began with an aesthetic constraint, not a mathematical one: the attractor had to be beautiful. That constraint immediately suggested symmetry.

In the early 1990s, the mathematicians Michael Field and Martin Golubitsky showed how to build chaotic maps whose strange attractors carry the symmetries of polygons and wallpaper patterns. Their book *Symmetry in Chaos* is full of images that look like stained-glass icons, and the trick behind them is a single idea called equivariance. A system is equivariant under a symmetry if the symmetry maps solutions to solutions: rotate a trajectory by 120 degrees, and you get another valid trajectory. An attractor of such a system either has that symmetry itself or comes in a symmetric family of copies. Field and Golubitsky's icons, however, are two-dimensional discrete maps: snapshots, not flows. The motion jumps from point to point.

The question that started this project was simple: what happens if you demand the same kind of symmetry from a continuous three-dimensional flow, the kind of system Lorenz wrote down?

The cleanest way to force three-fold rotational symmetry is to work in a complex variable. Write the horizontal coordinates as a single complex number, w = x + iy, so that rotating the plane by 120 degrees means multiplying w by e^(2πi/3). Most polynomial terms break this symmetry. But the conjugate-squared term w̄² respects it perfectly: rotating w by 120 degrees rotates w̄² by exactly the same angle, because the conjugate reverses the rotation and squaring doubles it, and minus two-thirds of a turn is the same as plus one-third. It is the unique quadratic term with this property, a small piece of algebraic luck.

So the candidate family took the form

```
dw/dt = [α(z − β) + iω] w + γ w̄²
dz/dt = μ + νz − z³ − λ|w|²
```

Read it as a machine with three interlocking parts. The term iωw spins the horizontal plane like a turntable. The term α(z − β)w makes that spin unstable or stable depending on the altitude z: above the level z = β trajectories spiral outward, below it they are drawn back in. And the vertical equation is a thermostat: the cubic −z³ caps the altitude while the −λ|w|² term pushes z down whenever trajectories wander far from the axis. Energy pumps in along the axis, spills outward, gets reined back. The γw̄² term, the symmetry carrier, warps the circular spiral into a three-lobed one.

Written back in real coordinates, the system is

```
dx/dt = α(z − β)x − ωy + γ(x² − y²)
dy/dt = ωx + α(z − β)y − 2γxy
dz/dt = μ + νz − z³ − λ(x² + y²)
```

Seven constants. Seven dials, any setting of which is a different universe with different long-run behavior. Almost all of those universes are boring.

## Six hundred universes

There was a first attempt, and it failed in an instructive way. Before the equivariant family above, the search began with a different design: a cyclic system blending sine nonlinearities with bilinear cross-terms, a cousin of the Thomas attractor. It produced chaos readily enough, with largest Lyapunov exponents around 0.02 to 0.04, but the attractors were thin, wiry bands, like a few loops of bent wire. Mathematically chaotic; visually dead. The lesson: weak chaos looks weak. An attractor only develops layered, veil-like structure when the stretching is vigorous, and the stretching rate is exactly what the largest Lyapunov exponent measures. Beauty, it turns out, correlates with a number.

So the second campaign made that number the objective. A Monte-Carlo search drew random settings of the seven dials, six hundred of them, and for each one integrated the equations and estimated the largest Lyapunov exponent: take two trajectories separated by one part in a hundred million, watch how fast the gap grows, renormalize before it saturates, average the growth rate. Settings whose trajectories flew off to infinity were discarded. Settings that converged to fixed points or limit cycles, exponent zero or negative, were discarded. The filter demanded a strongly positive exponent and an orbit that actually filled a respectable volume of space.

Out of six hundred random universes, exactly two passed.

The stronger of the two, with an exponent of 0.27, sat at the unlovely coordinates α = 1.444, β = 0.481, ω = 1.955, γ = 0.485, μ = 1.433, ν = 1.413, λ = 1.905. Rendered, it was immediately the keeper: a domed shell of nested veils with a bright column up the middle, and, seen from directly above, a triskelion, three petals chasing each other around the axis, the C₃ symmetry made visible.

| The crown | The bell |
|---|---|
| ![Crown view](gallery/aurelia_crown.png) | ![Bell view](gallery/aurelia_bell.png) |

Then came the small surprise that gave the system its final form. Those seven awkward constants were not seven independent quantities at all. Nudging each toward a rounder value, with the Lyapunov exponent as a guardrail, they collapsed: α, μ, and ν all wanted to be 1.4; γ and β both wanted to be 0.5; ω and λ both wanted to be 1.9. The chaos did not merely survive the rounding, it strengthened slightly: under matched long measurements, the original constants score an exponent of 0.222 and the rounded ones 0.229. The seven-dial machine was secretly a three-dial machine:

```
dx/dt = a(z − b)x − cy + b(x² − y²)
dy/dt = cx + a(z − b)y − 2bxy        with  a = 1.4,  b = 0.5,  c = 1.9
dz/dt = a(1 + z) − z³ − c(x² + y²)
```

Whether this collapse points at something structural or is a happy coincidence of this corner of parameter space is one of the open questions at the end of this story.

## The anatomy of the jellyfish

Why this shape? The answer lives at that single motionless point.

Set the right-hand sides to zero and solve. On the axis, where x = y = 0, the planar equations vanish identically and the vertical one becomes a(1 + z) = z³, a cubic with exactly one real root: z = 1.523. Off the axis, a numerical hunt from four hundred random starting points finds nothing. The Aurelia system has precisely one equilibrium, which is unusual; Lorenz has three, Aizawa-type systems typically two. Everything in the picture is organized by this lone point.

Linearize the flow there and the local character emerges. Two eigenvalues form the complex pair 1.432 ± 1.9i: an unstable spiral, unwinding outward at rate 1.432 while rotating at rate 1.9 (the rotation dial c, surfacing again). The third eigenvalue is −5.558: a powerfully attracting direction. The point is a saddle-focus, and the interplay of its outward spiral and inward crush is the engine of the whole attractor. Trajectories drift up the axis into the equilibrium's neighborhood, get caught in the unstable spiral, and are slung outward and over the rim. They fall along the outside of the bell, where the thermostat in the z-equation catches them, and the strongly contracting direction funnels them back to the base of the central column to ride up and be flung again. Stretch, fold, reinject, forever.

This recirculating geometry is the signature of what dynamicists call Shilnikov-type chaos, after the Russian mathematician who proved in 1965 that a saddle-focus whose trajectories nearly reconnect with the equilibrium forces the existence of infinitely many unstable periodic orbits, chaos in its purest combinatorial form. The Aurelia attractor wears that mechanism on its sleeve: the veils are the stretching, the bright column is the reinjection, and the gilded crown at the top, where the colors in the renders run to gold, is the slow neighborhood of the saddle-focus where trajectories linger before their next ejection.

## Certifying the strange

A picture can lie. A trajectory plotted for a finite time can look chaotic while secretly being a long transient on its way to a limit cycle, or a periodic orbit of enormous period. Certification means numbers, and the numbers form a checklist.

**The Lyapunov spectrum.** A three-dimensional flow has three Lyapunov exponents, measuring exponential stretching along three independent directions. The clean way to compute all three is to carry a small orthogonal frame along the trajectory, letting the linearized flow shear it while repeatedly re-orthogonalizing with QR decomposition; the logarithms of the stretching factors accumulate into the exponents. Over 600,000 steps, the Aurelia spectrum converges to

> λ₁ = +0.2327, λ₂ = +0.0013, λ₃ = −1.5119

This is the textbook signature (+, 0, −) of a strange attractor in three dimensions. The positive exponent is sensitivity: nearby trajectories separate by a factor of e every 4.3 time units. The zero exponent (numerically +0.001) is obligatory for any flow, reflecting the trivial freedom of sliding along the trajectory itself. The large negative exponent is the contraction that glues trajectories onto the attractor. And the sum, strongly negative, means volumes shrink: the system is dissipative, averaging a contraction rate of −1.29, so the attractor occupies zero volume. Rerunning the estimate from five random starting points gives exponents from 0.195 to 0.252, always positive; the chaos is not an artifact of one lucky initial condition.

**The fractal dimension.** Kaplan and Yorke conjectured that the exponents encode the attractor's dimension: count how many exponents you can sum before the total goes negative, then interpolate. For Aurelia, D = 2 + (λ₁ + λ₂)/|λ₃| = 2.155. More than a surface, less than a solid: the veils in the renders are not one sheet but infinitely many, packed into thickness zero, a structure the dimension 2.155 quantifies precisely.

**Boundedness.** Four million integration steps, no escape, every coordinate confined to a box roughly three units on a side. Combined with dissipativity, this rules out the embarrassing alternative that the pretty pictures depict a slow explosion.

All of it is reproducible from the repository with one command per claim, and recorded in [`results/verification.json`](results/verification.json).

## The edge of chaos

Chaos is not the system's only mood. Hold a and b fixed and sweep the rotation rate c from 1.2 to 2.6, computing the largest Lyapunov exponent at each of 281 settings, and the attractor's life story unfolds sideways:

![Bifurcation scan](gallery/bifurcation.png)

Below c ≈ 1.40, the exponent hugs zero: the system settles into limit cycles, closed loops of perfectly periodic motion, the fate Lorenz's predecessors expected of all differential equations. At c ≈ 1.40 chaos ignites, burning through a band to about 1.62 before collapsing back to periodicity. A second, broader chaotic continent runs from about 1.81 to 2.33, and the canonical c = 1.9 sits comfortably inside it. Within each band, narrow periodic windows slice through, places where the chaos momentarily crystallizes into order before dissolving again, the same alternation famously found in the logistic map. Past 2.33 the system retires into limit cycles for good, save for one last flicker of chaos near c = 2.40.

This interleaving matters for the certification, too: it shows the chaotic parameter set is robust, a band rather than a knife-edge, which is why small perturbations of the sliders in the [live viewer](https://sakeeb91.github.io/aurelia-attractor/) bend the jellyfish without killing it.

## The name

*Aurelia aurita* is the moon jellyfish, the translucent, domed drifter found in every ocean. The resemblance in the side view needs no argument: the bell, the trailing veils, the luminous core like the jelly's central mass. The Latin root *aureus* means golden, which fits the crown where slow trajectories pool. The name was unclaimed; searches of the dynamical-systems literature in June 2026 found no Aurelia attractor, and no published three-dimensional flow combining discrete C₃ equivariance through the w̄² coupling with cubic vertical dynamics. The closest relatives, Field and Golubitsky's symmetric icons (discrete, two-dimensional) and the Aizawa-Langford flow (continuously rotationally symmetric, two equilibria), each lack what the other has. Aurelia lives in the gap between them: a continuous flow, a discrete symmetry, a single organizing saddle-focus.

Honesty requires the caveats. The novelty claim is a search claim: not found, rather than proven absent, in a literature too large for any search to exhaust. And the chaos certification is numerical. The Lyapunov exponents and the dimension are measurements with error bars, not theorems. A rigorous proof of chaos for this system, of the kind Warwick Tucker achieved for the Lorenz attractor in 2002 using computer-assisted interval arithmetic, does not exist and would be a genuine contribution.

## Open questions

The afternoon that produced Aurelia left more questions than it answered.

- **Does the Shilnikov criterion hold?** The saddle-focus eigenvalues satisfy |−5.558| > 1.432, the inequality in Shilnikov's theorem, but the theorem also requires a homoclinic orbit, a trajectory leaving the equilibrium and returning to it exactly. Numerically the reinjection comes close. Whether a true homoclinic connection exists at nearby parameters is open.
- **Why do seven constants collapse to three?** The rounding may be a coincidence of this basin in parameter space, or the three-constant subfamily may be distinguished, perhaps the symmetric system maximizes stretching under some constraint. Nobody knows.
- **Are there symmetry-broken siblings?** C₃-equivariant systems can host attractors that break the symmetry and come in conjugate triples, merging into a single symmetric attractor at a symmetry-restoring crisis. Whether Aurelia's parameter space contains such regimes, three small jellyfish orbiting where one now swims, is unexplored.
- **The other hit.** The Monte-Carlo search produced a second chaotic universe, at λ ≈ 0.19, never examined beyond a thumbnail. It is still there, in the search script's output, waiting.

The equations fit on three lines. The object they contain has infinitely many layers, a fractional dimension, and the silhouette of a creature that has drifted through the oceans for five hundred million years. You can fly around it [in your browser](https://sakeeb91.github.io/aurelia-attractor/), or trace it yourself from twelve lines of Python in this repository. Either way, somewhere in the middle of it, the one motionless point is holding the whole thing together by pushing everything away.

---

*All quantities cited are computed by the scripts in this repository: the Lyapunov spectrum and dimension by `scripts/verify_chaos.py`, the parameter sweep by `scripts/bifurcation_scan.py`, the discovery search by `scripts/search_parameters.py`, and the renders by `scripts/render_gallery.py`.*
