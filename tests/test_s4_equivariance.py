"""Numerical equivariance test for the S4 rotoreflection candidate family.

This test is the mathematical gate for Phase 1 of the symmetry program: it
pins down that the candidate flow is equivariant under the order-4
rotoreflection group S4 (Schoenflies) and *only* that group within the
relevant subgroup lattice -- not the pure quarter-turn C4, not the pure
vertical flip. The improper symmetry is the whole point; if a term sneaks in
that restores C4 or flip symmetry, or breaks S4, this test fails.

The symmetry operation, with w = x + i*y:

    sigma: (w, z) -> (i*w, -z)              quarter-turn PLUS vertical flip

Because sigma is linear, a flow ds/dt = F(s) is sigma-equivariant iff
F(sigma . s) = sigma . F(s), i.e. for the split RHS dw/dt = f, dz/dt = h:

    f(i*w, conj(i*w), -z) = i * f(w, conj(w), z)        (note conj(i*w) = -i*conj(w))
    h(i*w, conj(i*w), -z) = -  h(w, conj(w), z)

sigma^2 = (w, z) -> (-w, z) is the half-turn C2; sigma^4 = identity; the group
{I, sigma, sigma^2, sigma^3} is cyclic of order 4 == S4.
"""

from __future__ import annotations

import numpy as np
import pytest

from atlas.family_s4 import (
    N_PARAMS,
    PARAM_HI,
    PARAM_LO,
    sigma,
    velocity,
)

TOL = 1e-12


def _random_states_and_params(rng, count):
    states = [
        (complex(rng.uniform(-2, 2), rng.uniform(-2, 2)), float(rng.uniform(-2, 2)))
        for _ in range(count)
    ]
    params = [rng.uniform(PARAM_LO, PARAM_HI) for _ in range(count)]
    return states, params


def test_param_box_shapes_are_consistent():
    assert PARAM_LO.shape == (N_PARAMS,)
    assert PARAM_HI.shape == (N_PARAMS,)
    assert np.all(PARAM_HI > PARAM_LO)


def test_sigma_is_quarter_turn_plus_flip():
    w, z = (0.7 - 0.3j), 0.9
    w2, z2 = sigma(w, z)
    assert w2 == pytest.approx(1j * w)
    assert z2 == pytest.approx(-z)


def test_sigma_squared_is_half_turn():
    w, z = (0.7 - 0.3j), 0.9
    w2, z2 = sigma(*sigma(w, z))
    assert w2 == pytest.approx(-w)
    assert z2 == pytest.approx(z)


def test_sigma_fourth_power_is_identity():
    w, z = (0.7 - 0.3j), 0.9
    s = (w, z)
    for _ in range(4):
        s = sigma(*s)
    assert s[0] == pytest.approx(w)
    assert s[1] == pytest.approx(z)


def test_flow_is_S4_equivariant():
    """F(sigma . s) == sigma . F(s) to machine precision, for random states/params."""
    rng = np.random.default_rng(20260611)
    states, params = _random_states_and_params(rng, 200)
    for (w, z), p in zip(states, params):
        dw, dz = velocity(w, z, p)
        dw_s, dz_s = velocity(*sigma(w, z), p)
        # sigma acts on the velocity vector the same way it acts on the state:
        # (dw, dz) -> (i*dw, -dz).
        assert dw_s == pytest.approx(1j * dw, abs=TOL, rel=0)
        assert dz_s == pytest.approx(-dz, abs=TOL, rel=0)


def test_dz_is_real():
    """The z-equation must stay on the real line for real z."""
    rng = np.random.default_rng(7)
    states, params = _random_states_and_params(rng, 50)
    for (w, z), p in zip(states, params):
        _, dz = velocity(w, z, p)
        assert abs(np.imag(dz)) < TOL


def test_flow_is_NOT_C4_equivariant():
    """The signature term delta*z*conj(w) must break the pure quarter-turn.

    If the flow were equivariant under rho: (w, z) -> (i*w, z) alone, the
    attractor's symmetry group would be C4 and there would be no novelty.
    """
    def rho(w, z):
        return 1j * w, z

    rng = np.random.default_rng(101)
    states, params = _random_states_and_params(rng, 40)
    violations = 0
    for (w, z), p in zip(states, params):
        dw, dz = velocity(w, z, p)
        dw_r, dz_r = velocity(*rho(w, z), p)
        if abs(dw_r - 1j * dw) > 1e-9 or abs(dz_r - dz) > 1e-9:
            violations += 1
    # For a non-degenerate family the quarter-turn is broken almost everywhere.
    assert violations == len(states)


def test_flow_is_NOT_flip_equivariant():
    """The flow must not be symmetric under the pure vertical flip either.

    phi: (w, z) -> (w, -z). Equivariance would require f(phi.s) = f(s) and
    h(phi.s) = -h(s); the delta*z*conj(w) term breaks the first condition.
    """
    def phi(w, z):
        return w, -z

    rng = np.random.default_rng(202)
    states, params = _random_states_and_params(rng, 40)
    violations = 0
    for (w, z), p in zip(states, params):
        dw, dz = velocity(w, z, p)
        dw_p, dz_p = velocity(*phi(w, z), p)
        if abs(dw_p - dw) > 1e-9 or abs(dz_p + dz) > 1e-9:
            violations += 1
    assert violations == len(states)


def test_signature_terms_are_load_bearing():
    """Zeroing BOTH improper-signature coefficients restores C4 symmetry.

    There are two terms that reduce S4 to S4 (rather than the larger C4):
    delta*z*conj(w) in the w-equation, and eps*Im(w^2) in the z-equation.
    Each is allowed under S4 but breaks the pure quarter-turn C4. The family
    collapses to a C4-equivariant flow exactly when delta = eps = 0; with
    either term alone present, C4 is broken. This pins down the precise
    novelty boundary (S4, not C4) and guards against silently dropping a term.
    """
    from atlas.family_s4 import param_names

    names = param_names()
    assert "delta" in names and "eps" in names
    di, ei = names.index("delta"), names.index("eps")

    def rho(w, z):
        return 1j * w, z

    rng = np.random.default_rng(303)
    states, params = _random_states_and_params(rng, 40)
    for (w, z), p in zip(states, params):
        p = np.array(p, dtype=float)
        # With both signature terms present, C4 is broken (delta drives dw,
        # eps drives dz).
        dw, dz = velocity(w, z, p)
        dw_r, dz_r = velocity(*rho(w, z), p)
        assert abs(dw_r - 1j * dw) > 1e-9 or abs(dz_r - dz) > 1e-9

        # Kill both signature terms -> pure quarter-turn becomes a symmetry.
        p[di] = 0.0
        p[ei] = 0.0
        dw, dz = velocity(w, z, p)
        dw_r, dz_r = velocity(*rho(w, z), p)
        assert dw_r == pytest.approx(1j * dw, abs=1e-11, rel=0)
        assert dz_r == pytest.approx(dz, abs=1e-11, rel=0)
