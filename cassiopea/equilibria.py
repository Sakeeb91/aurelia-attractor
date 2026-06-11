"""Equilibria of the Cassiopea system and their linear stability.

On the axis x = y = 0 the planar equations vanish and equilibria are the
real roots of z^3 - nu*z - mu = 0. Off-axis equilibria, if any, come in
quadruples related by 90-degree rotation; they are hunted by multi-start
root finding.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import fsolve

from .dynamics import A, B, G, LAM, MU, NU, W_ROT, jacobian, velocity


def find_equilibria(params=(A, B, W_ROT, G, MU, NU, LAM), n_seeds=400, seed=0, tol=1e-10):
    """Locate all equilibria (on-axis roots + multi-start search off-axis)."""
    a, b, w, g, mu, nu, lam = params
    found = []
    for z in np.roots([1.0, 0.0, -nu, -mu]):
        if abs(z.imag) < 1e-9:
            found.append(np.array([0.0, 0.0, z.real]))

    rng = np.random.default_rng(seed)
    for s0 in rng.uniform(-2.0, 2.0, size=(n_seeds, 3)):
        sol, _, ier, _ = fsolve(
            lambda s: velocity(s, *params), s0, full_output=True, xtol=1e-13
        )
        if ier != 1 or np.linalg.norm(velocity(sol, *params)) > tol:
            continue
        if all(np.linalg.norm(sol - f) > 1e-6 for f in found):
            found.append(sol)

    found.sort(key=lambda s: (round(s[2], 8), round(np.hypot(s[0], s[1]), 8), np.arctan2(s[1], s[0])))
    return found


def classify(eq, params=(A, B, W_ROT, G, MU, NU, LAM)):
    """Eigenvalues at an equilibrium and a stability label."""
    eigs = np.linalg.eigvals(jacobian(eq, *params))
    re = np.real(eigs)
    has_complex = np.any(np.abs(np.imag(eigs)) > 1e-9)
    if np.all(re < 0):
        label = "stable focus" if has_complex else "stable node"
    elif np.all(re > 0):
        label = "unstable focus" if has_complex else "unstable node"
    else:
        label = "saddle-focus" if has_complex else "saddle"
    return eigs, label
