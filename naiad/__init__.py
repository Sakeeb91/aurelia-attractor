"""The Naiad attractor: the two-fold (C2) sibling of Aurelia."""

from .dynamics import (
    A, B, G, LAM, MU, NU, W_ROT, DEFAULT_STATE,
    divergence, jacobian, rk4_step, trajectory, velocity,
)

__all__ = [
    "A", "B", "W_ROT", "G", "MU", "NU", "LAM", "DEFAULT_STATE",
    "divergence", "jacobian", "rk4_step", "trajectory", "velocity",
]
