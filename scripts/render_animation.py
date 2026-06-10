"""Render a slowly orbiting camera animation of the Aurelia attractor.

Writes gallery/aurelia_rotation.gif (72 frames, one full orbit).
"""

from __future__ import annotations

import pathlib
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from aurelia.dynamics import trajectory
from scripts.render_gallery import AURELIA_CMAP, _frame

GALLERY = pathlib.Path(__file__).resolve().parents[1] / "gallery"


def main():
    GALLERY.mkdir(exist_ok=True)
    print("integrating 700k points...")
    pts = trajectory(n_steps=700_000, dt=0.004, transient=30_000)
    c = (pts[:, 2] - pts[:, 2].min()) / np.ptp(pts[:, 2])

    fig = plt.figure(figsize=(6, 6), facecolor="black")
    ax = fig.add_subplot(111, projection="3d", facecolor="black")
    ax.scatter(
        pts[:, 0], pts[:, 1], pts[:, 2],
        s=0.05, c=c, cmap=AURELIA_CMAP, alpha=0.3, linewidths=0,
    )
    ax.set_axis_off()
    ax.set_box_aspect((1, 1, 0.9), zoom=1.28)
    _frame(ax, pts)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    n_frames = 72

    def update(i):
        ax.view_init(elev=24, azim=-52 + 360.0 * i / n_frames)
        return ()

    anim = FuncAnimation(fig, update, frames=n_frames)
    out = GALLERY / "aurelia_rotation.gif"
    anim.save(out, writer=PillowWriter(fps=12), dpi=80)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
