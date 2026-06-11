"""Render the Mobula attractor gallery.

A new palette for the family's first improper-symmetry member: violet-rose
("devil ray" twilight) -- distinct from Aurelia gold, Naiad cyan, Cassiopea
emerald. Color is biased upward so the dark underside of the ray stays visible
against black.

Outputs in gallery/:
  mobula_hero.png    three-quarter view (broad-winged ray with layered veils)
  mobula_pinwheel.png  top-down view of the four-armed S4 pinwheel
  mobula_wing.png    side profile (the devil-ray silhouette)
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

from mobula.dynamics import trajectory

GALLERY = pathlib.Path(__file__).resolve().parents[1] / "gallery"

# Devil-ray twilight: deep indigo-night -> violet -> magenta -> rose -> blush.
MOBULA_CMAP = LinearSegmentedColormap.from_list(
    "mobula",
    ["#160a2b", "#3a1466", "#6b1f9e", "#a833b0", "#e0559b", "#ff96c2", "#ffe3f0"],
)


def _frame(ax, pts, pad=0.04):
    for axis, col in zip("xyz", pts.T):
        lo, hi = col.min(), col.max()
        m = pad * (hi - lo)
        getattr(ax, f"set_{axis}lim")(lo - m, hi + m)


def render(pts, elev, azim, path, size=12, dpi=200, ps=0.06, alpha=0.42):
    t = (pts[:, 2] - pts[:, 2].min()) / (np.ptp(pts[:, 2]) or 1)
    c = 0.32 + 0.68 * t
    fig = plt.figure(figsize=(size, size), facecolor="black")
    ax = fig.add_subplot(111, projection="3d", facecolor="black")
    ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2], s=ps, c=c, cmap=MOBULA_CMAP,
               alpha=alpha, linewidths=0)
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()
    ax.set_box_aspect((1, 1, 1.1), zoom=1.25)
    _frame(ax, pts)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.savefig(path, dpi=dpi, facecolor="black")
    plt.close(fig)
    print(f"wrote {path}")


def main():
    GALLERY.mkdir(exist_ok=True)
    print("integrating 2.5M points...")
    pts = trajectory(n_steps=2_500_000, dt=0.004, transient=40_000)
    render(pts, elev=22, azim=-52, path=GALLERY / "mobula_hero.png")
    render(pts, elev=87, azim=-90, path=GALLERY / "mobula_pinwheel.png")
    render(pts, elev=2, azim=-90, path=GALLERY / "mobula_wing.png")


if __name__ == "__main__":
    main()
