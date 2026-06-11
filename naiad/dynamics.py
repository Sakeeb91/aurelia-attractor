"""Core definition of the Naiad attractor.

The Naiad system is the two-fold (C2) sibling of Aurelia: the same
construction with rotation order n = 2. With w = x + i*y, the planar part
is the complex equation

    dw/dt = [a*(z - b) + i*w_rot] w + g * conj(w)

and conj(w)^(2-1) = conj(w) is the unique linear term that survives the
half-turn w -> -w, so the flow is equivariant under (x, y) -> (-x, -y):
rotating a solution by 180 degrees about the z-axis gives another solution.
The attractor inherits this two-fold symmetry, which is why seen from above
it is a lens, not a disk.

In real coordinates the conj(w) term is an anisotropic stretch: it adds g
to the x-rate and subtracts g from the y-rate, so

    dx/dt = (a*(z - b) + g)*x - w_rot*y
    dy/dt = w_rot*x + (a*(z - b) - g)*y
    dz/dt = mu + nu*z - z^3 - lam*(x^2 + y^2)

Seen from the side the attractor flares like a fountain or a chalice: a
wide turbulent bowl at the top, a bright jet up the central axis, a narrow
stem at the base.

Canonical parameters: a = 1.2, b = 0.68, w_rot = 3.7, g = 1.7,
                      mu = 1.2, nu = 2.0, lam = 2.1.
"""

from __future__ import annotations

import numpy as np

# Canonical parameters of the Naiad attractor.
A, B, W_ROT, G, MU, NU, LAM = 1.2, 0.68, 3.7, 1.7, 1.2, 2.0, 2.1

DEFAULT_STATE = (0.3, 0.2, 0.1)


def velocity(state, a=A, b=B, w=W_ROT, g=G, mu=MU, nu=NU, lam=LAM):
    """Right-hand side of the Naiad system at ``state = (x, y, z)``."""
    x, y, z = state
    return np.array(
        [
            (a * (z - b) + g) * x - w * y,
            w * x + (a * (z - b) - g) * y,
            mu + nu * z - z**3 - lam * (x * x + y * y),
        ]
    )


def jacobian(state, a=A, b=B, w=W_ROT, g=G, mu=MU, nu=NU, lam=LAM):
    """Jacobian matrix of the flow at ``state = (x, y, z)``."""
    x, y, z = state
    return np.array(
        [
            [a * (z - b) + g, -w, a * x],
            [w, a * (z - b) - g, a * y],
            [-2 * lam * x, -2 * lam * y, nu - 3 * z * z],
        ]
    )


def divergence(state, a=A, b=B, w=W_ROT, g=G, mu=MU, nu=NU, lam=LAM):
    """Trace of the Jacobian (local volume contraction rate)."""
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
