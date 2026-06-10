"""Render the Aurelia attractor gallery.

Produces high-resolution renders in gallery/:
  * aurelia_hero.png   - the signature three-quarter view
  * aurelia_crown.png  - top-down view of the C3 triskelion
  * aurelia_bell.png   - side profile (the jellyfish bell)
  * aurelia_sheet.png  - 2x2 contact sheet of additional angles

Points are colored by height with a custom "abyssal gold" palette and
rendered with heavy alpha blending so density reads as luminosity.
"""

from __future__ import annotations

import pathlib
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from aurelia.dynamics import trajectory

GALLERY = pathlib.Path(__file__).resolve().parents[1] / "gallery"

# Abyssal gold: deep-sea indigo -> violet -> rose -> gold -> moonlight.
AURELIA_CMAP = LinearSegmentedColormap.from_list(
    "aurelia",
    ["#1b1040", "#4b2e83", "#a44a9c", "#e0719b", "#f4a261", "#ffd97d", "#fff3d6"],
)


def _frame(ax, pts, pad=0.04):
    """Clamp axis limits to the data so the attractor fills the frame."""
    for axis, col in zip("xyz", pts.T):
        lo, hi = col.min(), col.max()
        margin = pad * (hi - lo)
        getattr(ax, f"set_{axis}lim")(lo - margin, hi + margin)


def render(pts, elev, azim, path, size=12, dpi=220, point_size=0.05, alpha=0.34):
    c = (pts[:, 2] - pts[:, 2].min()) / np.ptp(pts[:, 2])
    fig = plt.figure(figsize=(size, size), facecolor="black")
    ax = fig.add_subplot(111, projection="3d", facecolor="black")
    ax.scatter(
        pts[:, 0], pts[:, 1], pts[:, 2],
        s=point_size, c=c, cmap=AURELIA_CMAP, alpha=alpha, linewidths=0,
    )
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()
    ax.set_box_aspect((1, 1, 0.9), zoom=1.28)
    _frame(ax, pts)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.savefig(path, dpi=dpi, facecolor="black")
    plt.close(fig)
    print(f"wrote {path}")


def main():
    GALLERY.mkdir(exist_ok=True)
    print("integrating 2.5M points on the attractor...")
    pts = trajectory(n_steps=2_500_000, dt=0.004, transient=30_000)

    render(pts, elev=28, azim=-52, path=GALLERY / "aurelia_hero.png")
    render(pts, elev=90, azim=-90, path=GALLERY / "aurelia_crown.png")
    render(pts, elev=4, azim=-25, path=GALLERY / "aurelia_bell.png")

    fig = plt.figure(figsize=(16, 16), facecolor="black")
    c = (pts[:, 2] - pts[:, 2].min()) / np.ptp(pts[:, 2])
    for i, (elev, azim) in enumerate([(55, -30), (20, 40), (35, 140), (-12, -70)]):
        ax = fig.add_subplot(2, 2, i + 1, projection="3d", facecolor="black")
        ax.scatter(
            pts[:, 0], pts[:, 1], pts[:, 2],
            s=0.04, c=c, cmap=AURELIA_CMAP, alpha=0.28, linewidths=0,
        )
        ax.view_init(elev=elev, azim=azim)
        ax.set_axis_off()
        ax.set_box_aspect((1, 1, 0.9), zoom=1.25)
        _frame(ax, pts)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
    fig.savefig(GALLERY / "aurelia_sheet.png", dpi=140, facecolor="black")
    plt.close(fig)
    print(f"wrote {GALLERY / 'aurelia_sheet.png'}")


if __name__ == "__main__":
    main()
