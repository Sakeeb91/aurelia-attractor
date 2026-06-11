"""The C_n-equivariant search family, evaluated in batches.

Generalizes the Aurelia construction to any discrete rotation order n >= 2.
With w = x + iy:

    dw/dt = [alpha*(z - beta) + i*omega] w + gamma * conj(w)^(n-1)
    dz/dt = mu + nu*z - z^3 - lam*|w|^2

n = 3 contains Aurelia. n = 2, 4, 5 are sibling families whose attractors,
when they exist, carry two-, four-, and five-fold symmetry.

The evaluator integrates a whole batch of parameter vectors simultaneously
with vectorized complex RK4, estimates the largest Lyapunov exponent by the
two-orbit Benettin method, and returns a decimated sample of each surviving
orbit for fingerprinting.
"""

from __future__ import annotations

import numpy as np

# (alpha, beta, omega, gamma, mu, nu, lam)
PARAM_LO = np.array([0.5, -1.0, 1.0, 0.3, -1.0, -1.0, 0.5])
PARAM_HI = np.array([2.5, 1.5, 4.0, 2.0, 2.0, 2.0, 3.0])
N_PARAMS = 7

ESCAPE = 50.0


def _deriv(W, Z, p, n):
    al, be, om, ga, mu, nu, lam = p.T
    dW = (al * (Z - be) + 1j * om) * W + ga * np.conj(W) ** (n - 1)
    dZ = mu + nu * Z - Z**3 - lam * (W.real**2 + W.imag**2)
    return dW, dZ


def _rk4(W, Z, p, n, dt):
    k1w, k1z = _deriv(W, Z, p, n)
    k2w, k2z = _deriv(W + 0.5 * dt * k1w, Z + 0.5 * dt * k1z, p, n)
    k3w, k3z = _deriv(W + 0.5 * dt * k2w, Z + 0.5 * dt * k2z, p, n)
    k4w, k4z = _deriv(W + dt * k3w, Z + dt * k3z, p, n)
    return (
        W + dt / 6.0 * (k1w + 2 * k2w + 2 * k3w + k4w),
        Z + dt / 6.0 * (k1z + 2 * k2z + 2 * k3z + k4z),
    )


def evaluate_batch(
    params,
    n,
    dt=0.01,
    transient=8_000,
    lyap_steps=25_000,
    sample_steps=12_000,
    sample_every=8,
    seed=0,
):
    """Evaluate a (B, 7) batch of parameter vectors for rotation order n.

    Returns dict with:
      lle     (B,) largest Lyapunov exponent (nan where dead)
      alive   (B,) bool: bounded and finite throughout
      points  (B, sample_steps // sample_every, 3) orbit samples (nan where dead)
    """
    p = np.asarray(params, dtype=float)
    B = p.shape[0]
    rng = np.random.default_rng(seed)

    W = (rng.uniform(-0.4, 0.4, B) + 1j * rng.uniform(-0.4, 0.4, B)) + (0.3 + 0.2j)
    Z = rng.uniform(-0.2, 0.4, B)
    alive = np.ones(B, dtype=bool)

    def cull():
        nonlocal alive
        bad = ~np.isfinite(Z) | (np.abs(Z) > ESCAPE) | ~np.isfinite(W) | (np.abs(W) > ESCAPE)
        alive &= ~bad
        # freeze dead orbits at zero so they stop generating overflow warnings
        W[bad] = 0.0
        Z[bad] = 0.0

    with np.errstate(all="ignore"):
        for i in range(transient):
            W, Z = _rk4(W, Z, p, n, dt)
            if i % 200 == 0:
                cull()
        cull()

        # Benettin two-orbit estimate
        d0 = 1e-8
        Ws, Zs = W + d0, Z.copy()
        log_sum = np.zeros(B)
        for i in range(lyap_steps):
            W, Z = _rk4(W, Z, p, n, dt)
            Ws, Zs = _rk4(Ws, Zs, p, n, dt)
            dW = Ws - W
            dZ = Zs - Z
            d = np.sqrt(dW.real**2 + dW.imag**2 + dZ**2)
            d = np.where(d > 0, d, 1e-16)
            log_sum += np.log(d / d0)
            scale = d0 / d
            Ws = W + dW * scale
            Zs = Z + dZ * scale
            if i % 200 == 0:
                cull()
        cull()
        lle = np.where(alive, log_sum / (lyap_steps * dt), np.nan)

        # orbit sample for fingerprinting
        n_keep = sample_steps // sample_every
        pts = np.full((B, n_keep, 3), np.nan)
        k = 0
        for i in range(sample_steps):
            W, Z = _rk4(W, Z, p, n, dt)
            if i % sample_every == 0:
                pts[:, k, 0] = W.real
                pts[:, k, 1] = W.imag
                pts[:, k, 2] = Z
                k += 1
            if i % 200 == 0:
                cull()
        cull()
        pts[~alive] = np.nan

    return {"lle": lle, "alive": alive, "points": pts}


def sample_params(B, rng):
    """Uniform random parameter vectors inside the search box."""
    return rng.uniform(PARAM_LO, PARAM_HI, size=(B, N_PARAMS))


def mutate_params(parent, rng, sigma=0.08):
    """Gaussian mutation, clipped to the box; sigma is a fraction of each range."""
    span = PARAM_HI - PARAM_LO
    child = parent + rng.normal(0, sigma, size=parent.shape) * span
    return np.clip(child, PARAM_LO, PARAM_HI)
