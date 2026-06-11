"""Render the most novel elites from the atlas archive as a montage.

Usage:  python scripts/render_atlas_montage.py [n_elites]
Writes gallery/atlas_montage.png
"""

from __future__ import annotations

import pathlib
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from atlas.family import evaluate_batch
from atlas.map_elites import Archive
from scripts.render_gallery import AURELIA_CMAP

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main():
    k = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    archive = Archive.load(ROOT / "results" / "atlas" / "archive.json")
    elites = archive.elites()[:k]

    cols = 4
    rows = (len(elites) + cols - 1) // cols
    fig = plt.figure(figsize=(4.2 * cols, 4.2 * rows), facecolor="black")

    for idx, e in enumerate(elites):
        res = evaluate_batch(
            np.array([e["params"]]), n=e["n"],
            lyap_steps=2_000, sample_steps=200_000, sample_every=1,
        )
        pts = res["points"][0]
        pts = pts[np.all(np.isfinite(pts), axis=1)]
        ax = fig.add_subplot(rows, cols, idx + 1, projection="3d", facecolor="black")
        if len(pts):
            c = (pts[:, 2] - pts[:, 2].min()) / (np.ptp(pts[:, 2]) or 1)
            ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2],
                       s=0.05, c=c, cmap=AURELIA_CMAP, alpha=0.35, linewidths=0)
        ax.view_init(elev=32, azim=-50)
        ax.set_axis_off()
        ax.set_title(
            f"n={e['n']}  novelty {e['novelty']:.2f}  lle {e['lle']:.2f}",
            color="#9d97b8", fontsize=9, pad=2,
        )
        print(f"rendered elite {idx+1}/{len(elites)} (n={e['n']})")

    fig.subplots_adjust(left=0, right=1, top=0.96, bottom=0, wspace=0, hspace=0.08)
    out = ROOT / "gallery" / "atlas_montage.png"
    fig.savefig(out, dpi=130, facecolor="black")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
