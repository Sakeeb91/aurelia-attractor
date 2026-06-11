"""Shape fingerprints for attractors, and novelty as distance.

A fingerprint must be cheap, and invariant to the things that don't matter:
translation, overall scale, and rigid rotation of the attractor. Phase 1
uses classical point-cloud descriptors (no neural nets):

  * D2 shape distribution (Osada et al. 2002): the histogram of pairwise
    distances between random surface points, on the cloud normalized to
    zero mean and unit RMS radius. 32 bins on [0, 3].
  * PCA eigenvalue ratios e2/e1 and e3/e1: how planar / how volumetric.
  * Fill ratio: occupied fraction of a 12^3 grid over the cloud's bounding
    box, a proxy for space-filling versus wiry structure.

Novelty of a candidate = minimum distance from its fingerprint to every
fingerprint in the reference set (the dysts catalog of known attractors,
plus everything already in the archive).
"""

from __future__ import annotations

import numpy as np

D2_BINS = 32
D2_RANGE = (0.0, 3.0)
GRID = 12
FP_DIM = D2_BINS + 3


def fingerprint(points, rng=None):
    """Fingerprint a (N, 3) point cloud. Returns (FP_DIM,) or None if degenerate."""
    pts = np.asarray(points, dtype=float)
    pts = pts[np.all(np.isfinite(pts), axis=1)]
    if len(pts) < 200:
        return None
    pts = pts - pts.mean(axis=0)
    rms = np.sqrt((pts**2).sum(axis=1).mean())
    if not np.isfinite(rms) or rms < 1e-9:
        return None
    pts = pts / rms

    rng = rng or np.random.default_rng(0)
    idx = rng.choice(len(pts), size=min(400, len(pts)), replace=False)
    sub = pts[idx]
    d = np.sqrt(((sub[:, None, :] - sub[None, :, :]) ** 2).sum(-1))
    d = d[np.triu_indices(len(sub), k=1)]
    # explicit edges: numpy 2.1.x's fast path (bins=int + range=) miscounts
    # edge-landing float64 values; the explicit-edges path is correct
    d = np.clip(d.astype(np.float64), D2_RANGE[0], D2_RANGE[1])
    hist, _ = np.histogram(d, bins=np.linspace(*D2_RANGE, D2_BINS + 1), density=True)
    hist = np.sqrt(hist / (hist.sum() + 1e-12))          # Hellinger embedding

    cov = np.cov(pts.T)
    ev = np.sort(np.linalg.eigvalsh(cov))[::-1]
    ratios = ev[1:] / (ev[0] + 1e-12)                     # planarity, volumetricity

    lo, hi = pts.min(axis=0), pts.max(axis=0)
    span = np.where(hi - lo > 1e-9, hi - lo, 1.0)
    cells = np.floor((pts - lo) / span * (GRID - 1e-9)).astype(int)
    fill = len({tuple(c) for c in cells}) / GRID**3

    return np.concatenate([hist, ratios, [fill]])


def distance(fp_a, fp_b):
    """Distance between two fingerprints (Hellinger on D2 + shape features)."""
    a, b = np.asarray(fp_a), np.asarray(fp_b)
    d_hist = np.linalg.norm(a[:D2_BINS] - b[:D2_BINS])
    d_feat = np.linalg.norm(a[D2_BINS:] - b[D2_BINS:])
    return d_hist + 0.5 * d_feat


def novelty(fp, reference_fps):
    """Min distance from fp to the reference set. Infinite if the set is empty."""
    if not len(reference_fps):
        return float("inf")
    return min(distance(fp, ref) for ref in reference_fps)
