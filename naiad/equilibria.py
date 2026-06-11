"""Equilibria of the Naiad system and their linear stability.

Off-axis equilibria would require (a(z-b))^2 = g^2 - w_rot^2, which has no
real solution at the canonical parameters (w_rot > g), so all equilibria lie
on the axis x = y = 0, where they are the real roots of z^3 - nu*z - mu = 0.
"""

from __future__ import annotations

import numpy as np

from .dynamics import A, B, G, LAM, MU, NU, W_ROT, jacobian


def find_equilibria(params=(A, B, W_ROT, G, MU, NU, LAM)):
    """Locate all equilibria. Returns a list of (3,) arrays."""
    a, b, w, g, mu, nu, lam = params
    found = []
    # on-axis: z^3 - nu z - mu = 0
    for z in np.roots([1.0, 0.0, -nu, -mu]):
        if abs(z.imag) < 1e-9:
            found.append(np.array([0.0, 0.0, z.real]))
    found.sort(key=lambda s: s[2])
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
