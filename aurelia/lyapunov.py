"""Lyapunov spectrum and fractal dimension of the Aurelia attractor.

The full spectrum is computed with the standard Benettin tangent-space
method: an orthonormal frame is advected by the linearized flow and
re-orthonormalized by QR decomposition at every step; the logarithms of
the diagonal of R accumulate into the exponents.
"""

from __future__ import annotations

import numpy as np

from .dynamics import A, B, C, DEFAULT_STATE, jacobian, rk4_step, velocity


def _tangent_rk4(s, Q, dt, a, b, c):
    """RK4 step of the tangent flow dQ/dt = J(s(t)) @ Q alongside the base flow."""
    k1 = velocity(s, a, b, c)
    j1 = jacobian(s, a, b, c) @ Q
    s2 = s + 0.5 * dt * k1
    k2 = velocity(s2, a, b, c)
    j2 = jacobian(s2, a, b, c) @ (Q + 0.5 * dt * j1)
    s3 = s + 0.5 * dt * k2
    k3 = velocity(s3, a, b, c)
    j3 = jacobian(s3, a, b, c) @ (Q + 0.5 * dt * j2)
    s4 = s + dt * k3
    k4 = velocity(s4, a, b, c)
    j4 = jacobian(s4, a, b, c) @ (Q + dt * j3)
    s_next = s + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
    Q_next = Q + (dt / 6.0) * (j1 + 2 * j2 + 2 * j3 + j4)
    return s_next, Q_next


def lyapunov_spectrum(
    n_steps=400_000,
    dt=0.005,
    transient=20_000,
    state0=DEFAULT_STATE,
    a=A,
    b=B,
    c=C,
):
    """Return the three Lyapunov exponents, largest first."""
    s = np.asarray(state0, dtype=float)
    for _ in range(transient):
        s = rk4_step(s, dt, a, b, c)
    Q = np.eye(3)
    sums = np.zeros(3)
    for _ in range(n_steps):
        s, Q = _tangent_rk4(s, Q, dt, a, b, c)
        Q, R = np.linalg.qr(Q)
        diag = np.abs(np.diag(R))
        sums += np.log(diag)
    return sums / (n_steps * dt)


def kaplan_yorke_dimension(spectrum):
    """Kaplan-Yorke (Lyapunov) dimension from a sorted spectrum."""
    exps = np.sort(np.asarray(spectrum))[::-1]
    cum = 0.0
    for j, lam in enumerate(exps):
        if cum + lam < 0.0:
            if j == 0:
                return 0.0
            return j + cum / abs(lam)
        cum += lam
    return float(len(exps))
