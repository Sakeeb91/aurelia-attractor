"""The Aurelia attractor: a novel C3-equivariant strange attractor."""

from .dynamics import A, B, C, DEFAULT_STATE, divergence, jacobian, rk4_step, trajectory, velocity

__all__ = [
    "A",
    "B",
    "C",
    "DEFAULT_STATE",
    "divergence",
    "jacobian",
    "rk4_step",
    "trajectory",
    "velocity",
]
