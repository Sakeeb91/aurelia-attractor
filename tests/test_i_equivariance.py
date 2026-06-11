"""Numerical equivariance test for the icosahedral (I) candidate family.

Pins down that the candidate flow is equivariant under the icosahedral rotation
group I (order 60, == A5) and only that group within the relevant lattice: NOT the
full I_h with reflections (the cross term breaks inversion -> the attractor is
chiral), and NOT all of SO(3) (the degree-5 invariant gradient is anisotropic).

The group, its degree-6 invariant, and grad(I6) are constructed in atlas/family_i
(60 matrices from a vertex 5-fold and the body-diagonal 3-fold; I6 = sum over the
group of ((g.v).X)^6). Because the elements are proper rotations, equivariance
means F(g.s) = g.F(s).
"""

from __future__ import annotations

import numpy as np
import pytest

from atlas.family_i import (
    GROUP,
    N_PARAMS,
    PARAM_HI,
    PARAM_LO,
    invariant_I6,
    velocity,
)

TOL = 1e-9
INV = -np.eye(3)


def _rand_rotation(rng):
    A = rng.normal(size=(3, 3))
    Q, R = np.linalg.qr(A)
    Q = Q @ np.diag(np.sign(np.diag(R)))
    if np.linalg.det(Q) < 0:
        Q[:, 0] = -Q[:, 0]
    return Q


def _states_params(rng, count):
    return ([rng.uniform(-1.5, 1.5, 3) for _ in range(count)],
            [rng.uniform(PARAM_LO, PARAM_HI) for _ in range(count)])


def test_param_box_shapes_are_consistent():
    assert PARAM_LO.shape == (N_PARAMS,)
    assert PARAM_HI.shape == (N_PARAMS,)
    assert np.all(PARAM_HI > PARAM_LO)


def test_group_has_order_60_of_proper_rotations():
    assert GROUP.shape == (60, 3, 3)
    for g in GROUP:
        assert np.allclose(g @ g.T, np.eye(3), atol=TOL)
        assert np.linalg.det(g) == pytest.approx(1.0, abs=1e-9)


def test_I6_is_icosahedrally_invariant():
    rng = np.random.default_rng(1)
    for _ in range(20):
        X = rng.uniform(-1.5, 1.5, 3)
        base = invariant_I6(X)
        for g in GROUP:
            assert invariant_I6(g @ X) == pytest.approx(base, rel=1e-9, abs=1e-9)


def test_I6_is_not_isotropic():
    """If I6 were just c*r^6 the family would secretly be SO(3)-symmetric."""
    a = invariant_I6(np.array([1.0, 0.0, 0.0]))
    b = invariant_I6(np.array([1.0, 1.0, 1.0]) / np.sqrt(3))
    assert abs(a - b) > 1e-6


def test_flow_is_I_equivariant_under_full_group():
    rng = np.random.default_rng(20260615)
    states, params = _states_params(rng, 25)
    for X, p in zip(states, params):
        FX = velocity(X, p)
        for g in GROUP:
            assert np.allclose(velocity(g @ X, p), g @ FX, atol=1e-8, rtol=0)


def test_flow_is_NOT_inversion_equivariant():
    """The cross term is even under inversion, so I_h is broken -> proper I (chiral)."""
    rng = np.random.default_rng(11)
    states, params = _states_params(rng, 40)
    violations = sum(
        not np.allclose(velocity(INV @ X, p), INV @ velocity(X, p), atol=1e-8)
        for X, p in zip(states, params)
    )
    assert violations == len(states)


def test_flow_is_NOT_SO3_equivariant():
    rng = np.random.default_rng(22)
    states, params = _states_params(rng, 30)
    violations = 0
    for X, p in zip(states, params):
        g = _rand_rotation(rng)
        if not np.allclose(velocity(g @ X, p), g @ velocity(X, p), atol=1e-7):
            violations += 1
    assert violations == len(states)


def test_nonlinear_terms_are_load_bearing():
    """a = b = 0 -> only the radial scalar term, which is fully SO(3)-equivariant."""
    from atlas.family_i import param_names

    names = param_names()
    ai, bi = names.index("a"), names.index("b")
    rng = np.random.default_rng(33)
    states, params = _states_params(rng, 25)
    for X, p in zip(states, params):
        p = np.array(p, dtype=float)
        g = _rand_rotation(rng)
        assert not np.allclose(velocity(g @ X, p), g @ velocity(X, p), atol=1e-7)
        p[ai] = 0.0
        p[bi] = 0.0
        assert np.allclose(velocity(g @ X, p), g @ velocity(X, p), atol=1e-9)
        assert np.allclose(velocity(INV @ X, p), INV @ velocity(X, p), atol=1e-9)
