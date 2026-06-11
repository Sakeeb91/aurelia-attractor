"""Run the quality-diversity search for novel chaotic attractors.

The loop, per generation and rotation order n:
  1. propose a batch: mutations of randomly chosen elites + fresh random draws
  2. evaluate the batch (bounded? chaotic? -> orbit sample)
  3. fingerprint survivors and score novelty against the dysts catalog
     plus the current archive
  4. offer each survivor to the MAP-Elites archive

Outputs:
  results/atlas/archive.json   the full elite map
  gallery/atlas_montage.png    the most novel elites, rendered

Usage:  python scripts/run_atlas.py [generations] [batch]
"""

from __future__ import annotations

import json
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from atlas.family import evaluate_batch, mutate_params, sample_params
from atlas.fingerprint import fingerprint, novelty
from atlas.map_elites import Archive

ROOT = pathlib.Path(__file__).resolve().parents[1]
ARCHIVE_PATH = ROOT / "results" / "atlas" / "archive.json"
ORDERS = (2, 3, 4, 5)


def load_catalog():
    path = ROOT / "results" / "catalog_fingerprints.json"
    cat = json.loads(path.read_text())
    return [np.array(v["fingerprint"]) for v in cat.values()]


def vertical_aspect(points):
    pts = points[np.all(np.isfinite(points), axis=1)]
    span = pts.max(axis=0) - pts.min(axis=0)
    xy = max(span[0], span[1])
    return span[2] / xy if xy > 1e-9 else np.nan


def main():
    generations = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    batch = int(sys.argv[2]) if len(sys.argv) > 2 else 96
    rng = np.random.default_rng(11)

    catalog = load_catalog()
    print(f"reference catalog: {len(catalog)} known systems")

    archive = Archive.load(ARCHIVE_PATH) if ARCHIVE_PATH.exists() else Archive()
    if archive.cells:
        print(f"resuming archive with {len(archive.cells)} elites")

    t0 = time.time()
    n_eval = 0
    for gen in range(generations):
        for n in ORDERS:
            # propose
            params = sample_params(batch, rng)
            elites_n = [e for e in archive.elites() if e["n"] == n]
            n_mut = min(len(elites_n) * 4, int(batch * 0.7))
            for i in range(n_mut):
                parent = np.array(elites_n[rng.integers(len(elites_n))]["params"])
                params[i] = mutate_params(parent, rng)

            # evaluate
            res = evaluate_batch(params, n=n, seed=int(rng.integers(1 << 30)))
            n_eval += batch

            # fingerprint + archive
            added = 0
            for i in range(batch):
                if not res["alive"][i] or not np.isfinite(res["lle"][i]):
                    continue
                if res["lle"][i] < 0.05:
                    continue
                fp = fingerprint(res["points"][i], rng=rng)
                if fp is None:
                    continue
                score = novelty(fp, catalog + archive.fingerprints)
                asp = vertical_aspect(res["points"][i])
                if archive.consider(n, params[i], res["lle"][i], asp, fp, score):
                    added += 1
            rate = n_eval / (time.time() - t0)
            print(f"gen {gen:02d} n={n}: +{added:3d} elites "
                  f"(archive {len(archive.cells):3d}, {rate:.0f} evals/s overall)")

        ARCHIVE_PATH.parent.mkdir(parents=True, exist_ok=True)
        archive.save(ARCHIVE_PATH)

    top = archive.elites()[:8]
    print(f"\n{n_eval} candidates evaluated in {time.time()-t0:.0f}s; "
          f"archive holds {len(archive.cells)} elites across n={sorted({e['n'] for e in archive.elites()})}")
    print("\nmost novel elites:")
    for e in top:
        print(f"  n={e['n']}  novelty={e['novelty']:.3f}  lle={e['lle']:.3f}  "
              f"params={e['params']}")


if __name__ == "__main__":
    main()
