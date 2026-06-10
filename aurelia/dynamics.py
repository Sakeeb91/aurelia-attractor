"""Core definition of the Aurelia attractor.

The Aurelia system is a three-dimensional autonomous flow:

    dx/dt = a*(z - b)*x - c*y + b*(x^2 - y^2)
    dy/dt = c*x + a*(z - b)*y - 2*b*x*y
    dz/dt = a*(1 + z) - z^3 - c*(x^2 + y^2)

Writing w = x + i*y, the planar part is a single complex equation

    dw/dt = (a*(z - b) + i*c) * w + b * conj(w)^2

so the system is equivariant under the rotation w -> exp(2*pi*i/3) * w:
rotating a solution by 120 degrees about the z-axis yields another
solution. The strange attractor inherits this three-fold (C3) symmetry.

Canonical parameters: a = 1.4, b = 0.5, c = 1.9.
"""

from __future__ import annotations

import numpy as np

# Canonical parameters of the Aurelia attractor.
A, B, C = 1.4, 0.5, 1.9

# A generic initial condition inside the basin of attraction.
DEFAULT_STATE = (0.3, 0.2, 0.1)


def velocity(state, a=A, b=B, c=C):
    """Right-hand side of the Aurelia system at ``state = (x, y, z)``."""
    x, y, z = state
    return np.array(
        [
            a * (z - b) * x - c * y + b * (x * x - y * y),
            c * x + a * (z - b) * y - 2.0 * b * x * y,
            a * (1.0 + z) - z**3 - c * (x * x + y * y),
        ]
    )


def jacobian(state, a=A, b=B, c=C):
    """Jacobian matrix of the flow at ``state = (x, y, z)``."""
    x, y, z = state
    return np.array(
        [
            [a * (z - b) + 2.0 * b * x, -c - 2.0 * b * y, a * x],
            [c - 2.0 * b * y, a * (z - b) - 2.0 * b * x, a * y],
            [-2.0 * c * x, -2.0 * c * y, a - 3.0 * z * z],
        ]
    )


def divergence(state, a=A, b=B, c=C):
    """Trace of the Jacobian (local volume contraction rate)."""
    _, _, z = state
    return 2.0 * a * (z - b) + a - 3.0 * z * z


def rk4_step(state, dt, a=A, b=B, c=C):
    """One classical fourth-order Runge-Kutta step."""
    k1 = velocity(state, a, b, c)
    k2 = velocity(state + 0.5 * dt * k1, a, b, c)
    k3 = velocity(state + 0.5 * dt * k2, a, b, c)
    k4 = velocity(state + dt * k3, a, b, c)
    return state + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def trajectory(
    n_steps=500_000,
    dt=0.004,
    transient=30_000,
    state0=DEFAULT_STATE,
    a=A,
    b=B,
    c=C,
):
    """Integrate the flow and return an ``(n_steps, 3)`` array on the attractor.

    The first ``transient`` steps are discarded so the returned points lie
    on the attractor rather than on the approach to it.
    """
    s = np.asarray(state0, dtype=float)
    for _ in range(transient):
        s = rk4_step(s, dt, a, b, c)
    pts = np.empty((n_steps, 3))
    for i in range(n_steps):
        s = rk4_step(s, dt, a, b, c)
        pts[i] = s
    return pts
