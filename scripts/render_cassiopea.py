"""Render the Cassiopea attractor gallery.

Color is biased upward (emerald "star jelly" palette) so the dark base of
the bell stays visible against black.

Outputs in gallery/:
  cassiopea_hero.png   three-quarter view
  cassiopea_star.png   top-down view of the four-armed pinwheel star
  cassiopea_bell.png   side profile
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

from cassiopea.dynamics import trajectory

GALLERY = pathlib.Path(__file__).resolve().parents[1] / "gallery"

# Fountain spray: deep teal-night -> cyan -> aqua -> pale spray -> moonlight.
CASSIOPEA_CMAP = LinearSegmentedColormap.from_list(
    "cassiopea",
    ["#06231c", "#0d4a36", "#1a7a4f", "#3fbf7f", "#9ff2c4", "#eafff3", "#ffffff"],
)


def _frame(ax, pts, pad=0.04):
    for axis, col in zip("xyz", pts.T):
        lo, hi = col.min(), col.max()
        m = pad * (hi - lo)
        getattr(ax, f"set_{axis}lim")(lo - m, hi + m)


def render(pts, elev, azim, path, size=12, dpi=200, ps=0.06, alpha=0.42):
    # bias color upward so the dark stem stays visible
    t = (pts[:, 2] - pts[:, 2].min()) / (np.ptp(pts[:, 2]) or 1)
    c = 0.35 + 0.65 * t
    fig = plt.figure(figsize=(size, size), facecolor="black")
    ax = fig.add_subplot(111, projection="3d", facecolor="black")
    ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2], s=ps, c=c, cmap=CASSIOPEA_CMAP,
               alpha=alpha, linewidths=0)
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()
    ax.set_box_aspect((1, 1, 1.15), zoom=1.25)
    _frame(ax, pts)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.savefig(path, dpi=dpi, facecolor="black")
    plt.close(fig)
    print(f"wrote {path}")


def main():
    GALLERY.mkdir(exist_ok=True)
    print("integrating 2.5M points...")
    pts = trajectory(n_steps=2_500_000, dt=0.004, transient=30_000)
    render(pts, elev=24, azim=-50, path=GALLERY / "cassiopea_hero.png")
    render(pts, elev=86, azim=-90, path=GALLERY / "cassiopea_star.png")
    render(pts, elev=2, azim=-90, path=GALLERY / "cassiopea_bell.png")


if __name__ == "__main__":
    main()
