"""Equilibria of the Mobula system and their linear stability.

On the axis x = y = 0 the planar equations vanish and the z-equation reduces to
z*(nu - z^2) = 0, because S4 forbids a constant term in dz/dt. The on-axis
equilibria are therefore the symmetric triple (0,0,0) and (0,0,+-sqrt(nu)); the
two non-zero ones are exchanged by sigma:(w,z)->(i*w,-z). Off-axis equilibria,
if any, are hunted by multi-start root finding and come in sigma^2-related
pairs (the half-turn (x,y,z)->(-x,-y,z)).
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import fsolve

from .dynamics import (
    ALPHA, BETA, DELTA, EPS, GAMMA, LAM, NU, OMEGA, jacobian, velocity,
)

PARAMS = (ALPHA, BETA, OMEGA, GAMMA, DELTA, NU, LAM, EPS)


def find_equilibria(params=PARAMS, n_seeds=600, seed=0, tol=1e-10):
    """Locate all equilibria (on-axis roots + multi-start search off-axis)."""
    nu = params[5]
    found = [np.array([0.0, 0.0, 0.0])]
    if nu > 0:
        found.append(np.array([0.0, 0.0, np.sqrt(nu)]))
        found.append(np.array([0.0, 0.0, -np.sqrt(nu)]))

    rng = np.random.default_rng(seed)
    for s0 in rng.uniform(-3.0, 3.0, size=(n_seeds, 3)):
        sol, _, ier, _ = fsolve(
            lambda s: velocity(s, *params), s0, full_output=True, xtol=1e-13
        )
        if ier != 1 or np.linalg.norm(velocity(sol, *params)) > tol:
            continue
        if all(np.linalg.norm(sol - f) > 1e-6 for f in found):
            found.append(sol)

    found.sort(key=lambda s: (round(s[2], 8), round(np.hypot(s[0], s[1]), 8),
                              np.arctan2(s[1], s[0])))
    return found


def classify(eq, params=PARAMS):
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
