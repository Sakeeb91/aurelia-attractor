"""Parameter-space search that discovered the Aurelia attractor.

The general seven-parameter C3-equivariant family is

    x' = alpha*(z - beta)*x - omega*y + gamma*(x^2 - y^2)
    y' = omega*x + alpha*(z - beta)*y - 2*gamma*x*y
    z' = mu + nu*z - z^3 - lam*(x^2 + y^2)

This script Monte-Carlo samples that family, keeps bounded orbits with a
positive largest Lyapunov exponent, and prints the hits. The canonical
Aurelia parameters arose from the strongest hit of this search after
rounding to the three-constant form alpha=mu=nu=a, gamma=beta=b,
omega=lam=c with (a, b, c) = (1.4, 0.5, 1.9).

Usage:  python scripts/search_parameters.py [n_trials]
"""

from __future__ import annotations

import sys

import numpy as np


def make_rhs(p):
    alpha, beta, omega, gamma, mu, nu, lam = p

    def rhs(s):
        x, y, z = s
        return np.array(
            [
                alpha * (z - beta) * x - omega * y + gamma * (x * x - y * y),
                omega * x + alpha * (z - beta) * y - 2 * gamma * x * y,
                mu + nu * z - z**3 - lam * (x * x + y * y),
            ]
        )

    return rhs


def rk4(s, dt, rhs):
    k1 = rhs(s)
    k2 = rhs(s + 0.5 * dt * k1)
    k3 = rhs(s + 0.5 * dt * k2)
    k4 = rhs(s + dt * k3)
    return s + dt / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)


def largest_lyapunov(p, n=25_000, dt=0.01, transient=8_000):
    """Benettin two-orbit estimate; returns (LLE, attractor extent) or (None, None)."""
    rhs = make_rhs(p)
    s = np.array([0.3, 0.2, 0.1])
    for _ in range(transient):
        s = rk4(s, dt, rhs)
        if not np.all(np.isfinite(s)) or np.max(np.abs(s)) > 1e3:
            return None, None
    d0 = 1e-8
    shadow = s + np.array([d0, 0.0, 0.0])
    log_sum = 0.0
    lo, hi = s.copy(), s.copy()
    for _ in range(n):
        s = rk4(s, dt, rhs)
        shadow = rk4(shadow, dt, rhs)
        if not np.all(np.isfinite(s)) or np.max(np.abs(s)) > 1e3:
            return None, None
        d = np.linalg.norm(shadow - s) or 1e-16
        log_sum += np.log(d / d0)
        shadow = s + (shadow - s) * (d0 / d)
        lo = np.minimum(lo, s)
        hi = np.maximum(hi, s)
    return log_sum / (n * dt), hi - lo


def main():
    n_trials = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    rng = np.random.default_rng(7)
    hits = []
    for _ in range(n_trials):
        p = (
            rng.uniform(0.5, 2.5),   # alpha
            rng.uniform(-1.0, 1.5),  # beta
            rng.uniform(1.0, 4.0),   # omega
            rng.uniform(0.3, 2.0),   # gamma
            rng.uniform(-1.0, 2.0),  # mu
            rng.uniform(-1.0, 2.0),  # nu
            rng.uniform(0.5, 3.0),   # lam
        )
        lle, extent = largest_lyapunov(p)
        if lle is not None and lle > 0.08 and np.max(extent) > 1.0 and np.min(extent) > 0.3:
            hits.append((lle, p))
            print(f"LLE={lle:6.3f}  p={tuple(round(v, 3) for v in p)}")

    hits.sort(key=lambda h: -h[0])
    print(f"\n{len(hits)} chaotic hits out of {n_trials} trials. Strongest:")
    for lle, p in hits[:5]:
        print(f"  LLE={lle:.3f}  p={tuple(round(v, 3) for v in p)}")


if __name__ == "__main__":
    main()
