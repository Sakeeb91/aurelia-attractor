"""The icosahedral (I) rotation-equivariant search family, evaluated in batches.

The third and richest polyhedral member (order 60, == A5, the rotation group of
the icosahedron/dodecahedron). Like T and O it acts **irreducibly** on R^3, so
the only I-commuting linear map is rho*I -- no saddle-focus engine.

The icosahedral group has no invariant of degree < 6 beyond r^2 (this is the
classical fact behind C60/fullerene and quasicrystal symmetry). We build the
60 rotation matrices as the closure of a vertex 5-fold and the body-diagonal
3-fold, then construct the lowest icosahedral invariant numerically and
robustly as

    I6(X) = sum_{g in I} ( (g . v) . X )^6        (v a fixed generic unit vector)

which is automatically I-invariant (the sum runs over the whole group). Its
gradient

    grad(I6)(X) = sum_{g in I} 6 ((g . v) . X)^5 (g . v)                [degree 5]

is the degree-5 I-equivariant used in the dissipative ansatz (4 dials), with a
fixed scale so grad(I6) is O(1) on the unit sphere:

    dX/dt = (rho - d*r^2) X  +  a * grad(I6)(X)  +  b * ( X x grad(I6)(X) )

grad(I6) is I-equivariant (gradient of an invariant) and X x grad(I6) is too
(cross of equivariants, I < SO(3)); checked numerically in
tests/test_i_equivariance.py. The a-term reduces SO(3) to I (it is anisotropic);
the b cross term is even under inversion, breaking I_h down to the proper group I
(the attractor is chiral).

Same IRREDUCIBILITY OBSTRUCTION as T and O (atlas/family_t.py): despite the much
higher-degree (degree-5/6) nonlinearity, an exhaustive dt-robust search finds no
strange attractor; bounded orbits relax to equilibria or limit cycles. Retained
for the chaos-vs-symmetry law (Phase 3) as the |G|=60 polyhedral point. The
coarse-dt batch estimate fabricates chaos around stable equilibria; re-certify
at finer dt before trusting any hit.
"""

from __future__ import annotations

import numpy as np

# Parameter order: (rho, d, a, b)
_PARAM_NAMES = ("rho", "d", "a", "b")
PARAM_LO = np.array([1.0, 0.10, -5.0, -8.0])
PARAM_HI = np.array([12.0, 2.00, 5.0, 8.0])
N_PARAMS = 4

ESCAPE = 50.0
_PHI = (1.0 + np.sqrt(5.0)) / 2.0


def _rot(axis, ang):
    a = np.array(axis, float)
    a /= np.linalg.norm(a)
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * (K @ K)


def _build_group():
    """The 60 rotation matrices of the icosahedral group I (closure of gens)."""
    g5 = _rot((0.0, 1.0, _PHI), 2 * np.pi / 5)          # 5-fold about a vertex axis
    g3 = np.array([[0.0, 1, 0], [0, 0, 1], [1, 0, 0]])  # 3-fold = cyclic permutation
    elems = [np.eye(3)]

    def known(M):
        return any(np.allclose(M, E, atol=1e-9) for E in elems)

    changed = True
    while changed and len(elems) < 200:
        changed = False
        for A in list(elems):
            for g in (g5, g3):
                M = A @ g
                if not known(M):
                    elems.append(M)
                    changed = True
    return np.array(elems)


GROUP = _build_group()                       # (60, 3, 3)
assert GROUP.shape[0] == 60, f"icosahedral group built with {GROUP.shape[0]} != 60 elements"

# Fixed generic unit vector and its full orbit; the degree-6 invariant's "directions".
_V = np.array([0.31, 0.52, 0.79])
_V /= np.linalg.norm(_V)
_GV = GROUP @ _V                             # (60, 3)

# Scale so that |grad(I6)| ~ 1 on the unit sphere (keeps the search box comparable
# to the T/O families). Computed deterministically from random unit directions.
def _grad_raw(X):
    proj = X @ _GV.T              # (B, 60)
    return (proj ** 5) @ _GV * 6.0
_rng0 = np.random.default_rng(0)
_u = _rng0.normal(size=(2000, 3))
_u /= np.linalg.norm(_u, axis=1, keepdims=True)
_GRAD_SCALE = 1.0 / float(np.mean(np.linalg.norm(_grad_raw(_u), axis=1)))


def param_names():
    return list(_PARAM_NAMES)


def group_elements():
    return [GROUP[i] for i in range(GROUP.shape[0])]


def invariant_I6(X):
    """The lowest icosahedral invariant (degree 6), evaluated at a single state."""
    return float(np.sum((_GV @ np.asarray(X, float)) ** 6))


def grad_I6(X):
    """Gradient of I6 (degree-5 I-equivariant), single state, scaled to O(1)."""
    x = np.asarray(X, float)
    proj = _GV @ x
    return (6.0 * _GRAD_SCALE) * ((proj ** 5)[:, None] * _GV).sum(0)


def velocity(state, p):
    """Right-hand side (dx, dy, dz) at a single real state X = (x, y, z)."""
    x = np.asarray(state, float)
    rho, d, a, b = (float(v) for v in p)
    r2 = float(x @ x)
    g = grad_I6(x)
    return (rho - d * r2) * x + a * g + b * np.cross(x, g)


def _grad_batch(X):
    # X: (B, 3) -> (B, 3)
    proj = X @ _GV.T                      # (B, 60)
    return (6.0 * _GRAD_SCALE) * ((proj ** 5) @ _GV)


def _deriv(X, p):
    rho = p[:, 0:1]; d = p[:, 1:2]; a = p[:, 2:3]; b = p[:, 3:4]
    r2 = (X * X).sum(1, keepdims=True)
    g = _grad_batch(X)
    cross = np.cross(X, g)
    return (rho - d * r2) * X + a * g + b * cross


def _rk4(X, p, dt):
    k1 = _deriv(X, p)
    k2 = _deriv(X + 0.5 * dt * k1, p)
    k3 = _deriv(X + 0.5 * dt * k2, p)
    k4 = _deriv(X + dt * k3, p)
    return X + dt / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)


def evaluate_batch(params, dt=0.005, transient=16_000, lyap_steps=50_000,
                   sample_steps=24_000, sample_every=16, seed=0):
    """Evaluate a (B, 4) batch of I parameter vectors (see family_t for fields)."""
    p = np.asarray(params, dtype=float)
    B = p.shape[0]
    rng = np.random.default_rng(seed)
    X = np.column_stack([rng.uniform(0.1, 0.6, B), rng.uniform(-0.4, 0.4, B),
                         rng.uniform(-0.4, 0.4, B)])
    alive = np.ones(B, dtype=bool)

    def cull():
        nonlocal alive, X
        bad = ~np.all(np.isfinite(X), axis=1) | (np.abs(X) > ESCAPE).any(axis=1)
        alive &= ~bad
        X[bad] = 0.0

    with np.errstate(all="ignore"):
        for i in range(transient):
            X = _rk4(X, p, dt)
            if i % 200 == 0:
                cull()
        cull()
        Xs = X.copy(); Xs[:, 0] += 1e-8
        d0 = 1e-8
        log_sum = np.zeros(B)
        for i in range(lyap_steps):
            X = _rk4(X, p, dt); Xs = _rk4(Xs, p, dt)
            dv = Xs - X
            dist = np.sqrt((dv * dv).sum(1))
            dist = np.where(dist > 0, dist, 1e-16)
            log_sum += np.log(dist / d0)
            Xs = X + dv * (d0 / dist)[:, None]
            if i % 200 == 0:
                cull()
        cull()
        lle = np.where(alive, log_sum / (lyap_steps * dt), np.nan)
        n_keep = sample_steps // sample_every
        pts = np.full((B, n_keep, 3), np.nan)
        k = 0
        for i in range(sample_steps):
            X = _rk4(X, p, dt)
            if i % sample_every == 0:
                pts[:, k, :] = X
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
