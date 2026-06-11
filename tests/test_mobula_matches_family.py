"""The mobula package must reproduce the equivariance-verified S4 family flow.

tests/test_s4_equivariance.py proves that atlas.family_s4.velocity is S4-
equivariant. The mobula package re-expresses that same flow in real (x, y, z)
coordinates with the canonical parameters baked in. If the two agree at random
states, the real-coordinate specimen inherits the proven equivariance; if my
hand-derivation of conj(w)^3, delta*z*conj(w), or Im(w^2) is wrong, this fails.
"""

from __future__ import annotations

import numpy as np
import pytest

from atlas.family_s4 import velocity as fam_velocity
from mobula.dynamics import (
    ALPHA, BETA, DELTA, EPS, GAMMA, LAM, NU, OMEGA, divergence, jacobian, velocity,
)

# family_s4 parameter order: (alpha, beta, omega, gamma, delta, nu, lam, eps)
CANON = np.array([ALPHA, BETA, OMEGA, GAMMA, DELTA, NU, LAM, EPS])


def test_real_form_matches_complex_family():
    rng = np.random.default_rng(2026)
    for _ in range(300):
        x, y, z = rng.uniform(-2, 2, 3)
        dw, dz = fam_velocity(complex(x, y), float(z), CANON)
        vx, vy, vz = velocity(np.array([x, y, z]))
        assert vx == pytest.approx(dw.real, abs=1e-12, rel=0)
        assert vy == pytest.approx(dw.imag, abs=1e-12, rel=0)
        assert vz == pytest.approx(float(np.real(dz)), abs=1e-12, rel=0)


def test_jacobian_matches_finite_difference():
    rng = np.random.default_rng(11)
    h = 1e-6
    for _ in range(40):
        s = rng.uniform(-1.5, 1.5, 3)
        J = jacobian(s)
        for k in range(3):
            ds = np.zeros(3); ds[k] = h
            fd = (velocity(s + ds) - velocity(s - ds)) / (2 * h)
            assert np.allclose(J[:, k], fd, atol=1e-5)


def test_divergence_matches_jacobian_trace():
    rng = np.random.default_rng(3)
    for _ in range(40):
        s = rng.uniform(-2, 2, 3)
        assert divergence(s) == pytest.approx(np.trace(jacobian(s)), abs=1e-10)
