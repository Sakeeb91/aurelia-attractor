"""The octahedral (O) rotation-equivariant search family, evaluated in batches.

The second polyhedral member (order 24, == S4 as an abstract group, the rotation
group of the cube/octahedron). Like T it acts **irreducibly** on R^3, so the only
O-commuting linear map is rho*I -- no saddle-focus engine.

Lowest non-trivial invariant beyond r^2 is the quartic J = x^4 + y^4 + z^4
(the cubic xyz is NOT O-invariant -- it is anti-invariant under the 4-fold c4z,
which is exactly what separates O from T). The dissipative ansatz (4 dials),
with r^2 = x^2+y^2+z^2:

    dX/dt = (rho - d*r^2) X  +  a * (1/4)grad(J)(X)  +  b * ( X x (1/4)grad(J)(X) )

with

    (1/4) grad(J)   = (x^3, y^3, z^3)                            [degree 3]
    X x (x^3,..)    = ( yz(z^2-y^2), zx(x^2-z^2), xy(y^2-x^2) )  [degree 4]

so component-wise:

    dx/dt = (rho - d*r^2) x + a*x^3 + b*yz(z^2 - y^2)
    dy/dt = (rho - d*r^2) y + a*y^3 + b*zx(x^2 - z^2)
    dz/dt = (rho - d*r^2) z + a*z^3 + b*xy(y^2 - x^2)

Both nonlinear terms are O-equivariant (gradient of an O-invariant, and cross of
two O-equivariants since O < SO(3)); checked numerically in
tests/test_o_equivariance.py. The a-term (x^3,y^3,z^3) is the O-signature: it
reduces SO(3) to O. The b cross term is even under inversion, so it breaks the
full group O_h down to the proper rotation group O (the attractor is chiral).

The same IRREDUCIBILITY OBSTRUCTION documented in atlas/family_t.py applies: an
exhaustive dt-robust search finds no strange attractor; bounded orbits relax to
equilibria or limit cycles. The family is retained for the chaos-vs-symmetry
law (Phase 3), where O is one of the polyhedral points quantifying the cliff.

Evaluator mirrors atlas/family_t.py. The coarse-dt two-orbit estimate fabricates
chaos around stable equilibria; re-certify at finer dt before trusting any hit.
"""

from __future__ import annotations

import numpy as np

# Parameter order: (rho, d, a, b)
_PARAM_NAMES = ("rho", "d", "a", "b")
PARAM_LO = np.array([1.0, 0.10, -4.0, -8.0])
PARAM_HI = np.array([12.0, 2.00, 4.0, 8.0])
N_PARAMS = 4

ESCAPE = 60.0

# Generators of O (order 24).
C4Z = np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])  # (x,y,z)->(-y,x,z)
SIGMA3 = np.array([[0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 0.0]])  # (x,y,z)->(y,z,x)


def param_names():
    return list(_PARAM_NAMES)


def group_elements():
    """The 24 rotation matrices of the octahedral group O (closure of the gens)."""
    elems = [np.eye(3)]
    gens = [C4Z, SIGMA3]

    def known(M):
        return any(np.allclose(M, E, atol=1e-9) for E in elems)

    changed = True
    while changed:
        changed = False
        for A in list(elems):
            for g in gens:
                M = A @ g
                if not known(M):
                    elems.append(M)
                    changed = True
    return elems


def velocity(state, p):
    """Right-hand side (dx, dy, dz) at a single real state X = (x, y, z)."""
    x, y, z = (float(v) for v in state)
    rho, d, a, b = (float(v) for v in p)
    r2 = x * x + y * y + z * z
    rad = rho - d * r2
    return np.array(
        [
            rad * x + a * x**3 + b * y * z * (z * z - y * y),
            rad * y + a * y**3 + b * z * x * (x * x - z * z),
            rad * z + a * z**3 + b * x * y * (y * y - x * x),
        ]
    )


def _deriv(X, Y, Z, p):
    rho, d, a, b = p.T
    r2 = X * X + Y * Y + Z * Z
    rad = rho - d * r2
    dX = rad * X + a * X**3 + b * Y * Z * (Z * Z - Y * Y)
    dY = rad * Y + a * Y**3 + b * Z * X * (X * X - Z * Z)
    dZ = rad * Z + a * Z**3 + b * X * Y * (Y * Y - X * X)
    return dX, dY, dZ


def _rk4(X, Y, Z, p, dt):
    k1x, k1y, k1z = _deriv(X, Y, Z, p)
    k2x, k2y, k2z = _deriv(X + 0.5 * dt * k1x, Y + 0.5 * dt * k1y, Z + 0.5 * dt * k1z, p)
    k3x, k3y, k3z = _deriv(X + 0.5 * dt * k2x, Y + 0.5 * dt * k2y, Z + 0.5 * dt * k2z, p)
    k4x, k4y, k4z = _deriv(X + dt * k3x, Y + dt * k3y, Z + dt * k3z, p)
    return (
        X + dt / 6.0 * (k1x + 2 * k2x + 2 * k3x + k4x),
        Y + dt / 6.0 * (k1y + 2 * k2y + 2 * k3y + k4y),
        Z + dt / 6.0 * (k1z + 2 * k2z + 2 * k3z + k4z),
    )


def evaluate_batch(params, dt=0.005, transient=16_000, lyap_steps=50_000,
                   sample_steps=24_000, sample_every=16, seed=0):
    """Evaluate a (B, 4) batch of O parameter vectors (see family_t for fields)."""
    p = np.asarray(params, dtype=float)
    B = p.shape[0]
    rng = np.random.default_rng(seed)
    X = rng.uniform(0.1, 0.6, B)
    Y = rng.uniform(-0.4, 0.4, B)
    Z = rng.uniform(-0.4, 0.4, B)
    alive = np.ones(B, dtype=bool)

    def cull():
        nonlocal alive
        bad = (~np.isfinite(X) | (np.abs(X) > ESCAPE) | ~np.isfinite(Y) | (np.abs(Y) > ESCAPE)
               | ~np.isfinite(Z) | (np.abs(Z) > ESCAPE))
        alive &= ~bad
        X[bad] = 0.0; Y[bad] = 0.0; Z[bad] = 0.0

    with np.errstate(all="ignore"):
        for i in range(transient):
            X, Y, Z = _rk4(X, Y, Z, p, dt)
            if i % 200 == 0:
                cull()
        cull()
        d0 = 1e-8
        Xs, Ys, Zs = X + d0, Y.copy(), Z.copy()
        log_sum = np.zeros(B)
        for i in range(lyap_steps):
            X, Y, Z = _rk4(X, Y, Z, p, dt)
            Xs, Ys, Zs = _rk4(Xs, Ys, Zs, p, dt)
            dX, dY, dZ = Xs - X, Ys - Y, Zs - Z
            dist = np.sqrt(dX * dX + dY * dY + dZ * dZ)
            dist = np.where(dist > 0, dist, 1e-16)
            log_sum += np.log(dist / d0)
            scale = d0 / dist
            Xs = X + dX * scale; Ys = Y + dY * scale; Zs = Z + dZ * scale
            if i % 200 == 0:
                cull()
        cull()
        lle = np.where(alive, log_sum / (lyap_steps * dt), np.nan)
        n_keep = sample_steps // sample_every
        pts = np.full((B, n_keep, 3), np.nan)
        k = 0
        for i in range(sample_steps):
            X, Y, Z = _rk4(X, Y, Z, p, dt)
            if i % sample_every == 0:
                pts[:, k, 0] = X; pts[:, k, 1] = Y; pts[:, k, 2] = Z
                k += 1
            if i % 200 == 0:
                cull()
        cull()
        pts[~alive] = np.nan
    return {"lle": lle, "alive": alive, "points": pts}


def sample_params(B, rng):
    return rng.uniform(PARAM_LO, PARAM_HI, size=(B, N_PARAMS))


def mutate_params(parent, rng, sigma_frac=0.08):
    span = PARAM_HI - PARAM_LO
    child = parent + rng.normal(0, sigma_frac, size=parent.shape) * span
    return np.clip(child, PARAM_LO, PARAM_HI)
