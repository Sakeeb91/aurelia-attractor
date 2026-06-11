"""A minimal MAP-Elites archive for attractor discovery.

MAP-Elites (Mouret & Clune 2015) replaces "find the best" with "fill a map":
descriptor space is tiled into cells, and each cell keeps the single best
candidate whose behavior lands there. The output is an atlas of diverse
solutions rather than one optimum.

Cells here are (rotation order n, largest Lyapunov exponent, vertical aspect
ratio). Within a cell, candidates compete on novelty: distance to the dysts
catalog of known attractors and to the rest of the archive at insertion time.
"""

from __future__ import annotations

import json

import numpy as np

LLE_EDGES = np.array([0.05, 0.10, 0.15, 0.20, 0.27, 0.35, 0.45, 0.60])
ASPECT_EDGES = np.array([0.2, 0.4, 0.6, 0.85, 1.2, 2.0])


def descriptor_cell(n, lle, aspect):
    """Map behavior to a discrete cell key, or None if outside the map."""
    if not (np.isfinite(lle) and np.isfinite(aspect)):
        return None
    if lle < LLE_EDGES[0] or lle > LLE_EDGES[-1]:
        return None
    i = int(np.searchsorted(LLE_EDGES, lle) - 1)
    j = int(np.clip(np.searchsorted(ASPECT_EDGES, aspect) - 1, 0, len(ASPECT_EDGES) - 2))
    return (int(n), i, j)


class Archive:
    def __init__(self):
        self.cells = {}          # cell key -> elite dict
        self.fingerprints = []   # all elite fingerprints, for novelty pressure

    def consider(self, n, params, lle, aspect, fp, score):
        cell = descriptor_cell(n, lle, aspect)
        if cell is None:
            return False
        cur = self.cells.get(cell)
        if cur is None or score > cur["novelty"]:
            self.cells[cell] = {
                "n": int(n),
                "params": [round(float(v), 6) for v in params],
                "lle": round(float(lle), 5),
                "aspect": round(float(aspect), 4),
                "novelty": round(float(score), 5),
                "fingerprint": [round(float(v), 6) for v in fp],
            }
            self.fingerprints = [np.array(e["fingerprint"]) for e in self.cells.values()]
            return True
        return False

    def elites(self):
        return sorted(self.cells.values(), key=lambda e: -e["novelty"])

    def random_elite(self, rng):
        if not self.cells:
            return None
        return self.cells[list(self.cells.keys())[rng.integers(len(self.cells))]]

    def save(self, path):
        cells = {",".join(map(str, k)): v for k, v in self.cells.items()}
        with open(path, "w") as fh:
            json.dump(cells, fh, indent=1)

    @classmethod
    def load(cls, path):
        a = cls()
        with open(path) as fh:
            cells = json.load(fh)
        for k, v in cells.items():
            a.cells[tuple(int(x) for x in k.split(","))] = v
        a.fingerprints = [np.array(e["fingerprint"]) for e in a.cells.values()]
        return a
