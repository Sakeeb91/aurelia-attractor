"""Equilibrium points of the Aurelia system and their linear stability.

Because the flow is C3-equivariant, off-axis equilibria occur in triples
related by 120-degree rotation about the z-axis. On the axis (x = y = 0)
the planar equations vanish identically and equilibria are the real
roots of the cubic a*(1 + z) - z^3 = 0.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import fsolve

from .dynamics import A, B, C, jacobian, velocity


def find_equilibria(a=A, b=B, c=C, n_seeds=400, seed=0, tol=1e-10):
    """Locate all equilibria by multi-start root finding, deduplicated."""
    rng = np.random.default_rng(seed)
    found = []

    # On-axis equilibria: real roots of a*(1+z) - z^3 = 0.
    for z in np.roots([-1.0, 0.0, a, a]):
        if abs(z.imag) < 1e-12:
            found.append(np.array([0.0, 0.0, z.real]))

    # Off-axis equilibria via random multi-start.
    seeds = rng.uniform(-2.5, 2.5, size=(n_seeds, 3))
    for s0 in seeds:
        sol, info, ier, _ = fsolve(
            lambda s: velocity(s, a, b, c), s0, full_output=True, xtol=1e-13
        )
        if ier != 1 or np.linalg.norm(velocity(sol, a, b, c)) > tol:
            continue
        if all(np.linalg.norm(sol - f) > 1e-6 for f in found):
            found.append(sol)

    found.sort(key=lambda s: (round(s[2], 8), round(np.hypot(s[0], s[1]), 8), np.arctan2(s[1], s[0])))
    return found


def classify(eq, a=A, b=B, c=C):
    """Eigenvalues of the Jacobian at an equilibrium and a stability label."""
    eigs = np.linalg.eigvals(jacobian(eq, a, b, c))
    re = np.real(eigs)
    has_complex = np.any(np.abs(np.imag(eigs)) > 1e-9)
    if np.all(re < 0):
        label = "stable focus" if has_complex else "stable node"
    elif np.all(re > 0):
        label = "unstable focus" if has_complex else "unstable node"
    else:
        label = "saddle-focus" if has_complex else "saddle"
    return eigs, label
