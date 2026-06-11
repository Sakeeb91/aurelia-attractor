"""Core definition of the Cassiopea attractor.

The Cassiopea system is the four-fold (C4) member of the family that
contains Aurelia (C3) and Naiad (C2). With w = x + i*y the planar part is

    dw/dt = [a*(z - b) + i*w_rot] w + g * conj(w)^3

and conj(w)^3 is the unique cubic term equivariant under the quarter-turn
w -> i*w, so rotating a solution by 90 degrees about the z-axis yields
another solution. The attractor inherits the four-fold symmetry: seen from
above it is a four-armed pinwheel star; from the side, a layered bell with
twin curtains and a bright jet up the axis.

In real coordinates, conj(w)^3 = (x^3 - 3xy^2) - i*(3x^2 y - y^3):

    dx/dt = a(z - b)x - w_rot*y + g(x^3 - 3xy^2)
    dy/dt = w_rot*x + a(z - b)y + g(y^3 - 3x^2 y)
    dz/dt = mu + nu*z - z^3 - lam*(x^2 + y^2)

Canonical parameters: a = 2.0, b = 0.85, w_rot = 1.8, g = 0.9,
                      mu = 1.28, nu = 1.8, lam = 2.8.
"""

from __future__ import annotations

import numpy as np

# Canonical parameters of the Cassiopea attractor.
A, B, W_ROT, G, MU, NU, LAM = 2.0, 0.85, 1.8, 0.9, 1.28, 1.8, 2.8

DEFAULT_STATE = (0.3, 0.2, 0.1)


def velocity(state, a=A, b=B, w=W_ROT, g=G, mu=MU, nu=NU, lam=LAM):
    """Right-hand side of the Cassiopea system at ``state = (x, y, z)``."""
    x, y, z = state
    return np.array(
        [
            a * (z - b) * x - w * y + g * (x**3 - 3 * x * y * y),
            w * x + a * (z - b) * y + g * (y**3 - 3 * x * x * y),
            mu + nu * z - z**3 - lam * (x * x + y * y),
        ]
    )


def jacobian(state, a=A, b=B, w=W_ROT, g=G, mu=MU, nu=NU, lam=LAM):
    """Jacobian matrix of the flow at ``state = (x, y, z)``."""
    x, y, z = state
    return np.array(
        [
            [a * (z - b) + 3 * g * (x * x - y * y), -w - 6 * g * x * y, a * x],
            [w - 6 * g * x * y, a * (z - b) + 3 * g * (y * y - x * x), a * y],
            [-2 * lam * x, -2 * lam * y, nu - 3 * z * z],
        ]
    )


def divergence(state, a=A, b=B, w=W_ROT, g=G, mu=MU, nu=NU, lam=LAM):
    """Trace of the Jacobian. The cubic terms cancel: g(3x^2-3y^2)+g(3y^2-3x^2)=0."""
    _, _, z = state
    return 2 * a * (z - b) + nu - 3 * z * z


def rk4_step(state, dt, a=A, b=B, w=W_ROT, g=G, mu=MU, nu=NU, lam=LAM):
    """One classical fourth-order Runge-Kutta step."""
    k1 = velocity(state, a, b, w, g, mu, nu, lam)
    k2 = velocity(state + 0.5 * dt * k1, a, b, w, g, mu, nu, lam)
    k3 = velocity(state + 0.5 * dt * k2, a, b, w, g, mu, nu, lam)
    k4 = velocity(state + dt * k3, a, b, w, g, mu, nu, lam)
    return state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)


def trajectory(n_steps=500_000, dt=0.004, transient=30_000, state0=DEFAULT_STATE,
               a=A, b=B, w=W_ROT, g=G, mu=MU, nu=NU, lam=LAM):
    """Integrate the flow and return an ``(n_steps, 3)`` array on the attractor."""
    s = np.asarray(state0, dtype=float)
    for _ in range(transient):
        s = rk4_step(s, dt, a, b, w, g, mu, nu, lam)
    pts = np.empty((n_steps, 3))
    for i in range(n_steps):
        s = rk4_step(s, dt, a, b, w, g, mu, nu, lam)
        pts[i] = s
    return pts
