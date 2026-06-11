"""Full chaos verification of the Naiad attractor.

Mirrors scripts/verify_chaos.py (Aurelia): Lyapunov spectrum, Kaplan-Yorke
dimension, robustness across initial conditions, equilibria with eigenvalues,
long-orbit boundedness, and time-averaged divergence. Also records the
fingerprint-distance novelty against the dysts catalog when available.

Writes results/naiad_verification.json.
"""

from __future__ import annotations

import json
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from naiad.dynamics import A, B, G, LAM, MU, NU, W_ROT, divergence, trajectory
from naiad.equilibria import classify, find_equilibria
from naiad.lyapunov import kaplan_yorke_dimension, lyapunov_spectrum

ROOT = pathlib.Path(__file__).resolve().parents[1]


def novelty_vs_catalog(pts):
    try:
        from atlas.fingerprint import distance, fingerprint
    except Exception:
        return None
    cat_path = ROOT / "results" / "catalog_fingerprints.json"
    if not cat_path.exists():
        return None
    cat = json.loads(cat_path.read_text())
    fp = fingerprint(pts[::8])
    if fp is None:
        return None
    dists = sorted((distance(fp, np.array(v["fingerprint"])), k) for k, v in cat.items())
    return {"nearest": dists[0][1], "distance": round(float(dists[0][0]), 4),
            "next": [[k, round(float(d), 4)] for d, k in dists[1:4]]}


def main():
    params = (A, B, W_ROT, G, MU, NU, LAM)
    results = {
        "system": "Naiad attractor",
        "parameters": {"a": A, "b": B, "w_rot": W_ROT, "g": G, "mu": MU, "nu": NU, "lam": LAM},
    }

    print("Lyapunov spectrum (long run)...")
    spec = lyapunov_spectrum(n_steps=600_000, dt=0.005, params=params)
    ky = kaplan_yorke_dimension(spec)
    results["lyapunov_spectrum"] = [round(v, 5) for v in spec]
    results["kaplan_yorke_dimension"] = round(ky, 5)
    print(f"  spectrum = {np.round(spec, 5)}   D_KY = {ky:.4f}")

    print("Initial-condition robustness...")
    rng = np.random.default_rng(11)
    lles = []
    for _ in range(5):
        s0 = rng.uniform(-0.5, 0.5, 3) + [0.0, 0.0, 0.6]
        lles.append(round(float(lyapunov_spectrum(n_steps=150_000, dt=0.005,
                                                   state0=s0, params=params)[0]), 5))
    results["largest_exponent_across_ics"] = lles
    print(f"  LLE across 5 ICs: {lles}")

    print("Equilibria...")
    results["equilibria"] = []
    for e in find_equilibria(params):
        eigs, label = classify(e, params)
        results["equilibria"].append({
            "point": [round(v, 6) for v in e],
            "eigenvalues": [[round(v.real, 5), round(v.imag, 5)] for v in eigs],
            "type": label,
        })
        print(f"  {np.round(e, 4)}  {label}  eigs={np.round(eigs, 4)}")

    print("Long-orbit boundedness (4M steps)...")
    pts = trajectory(n_steps=4_000_000, dt=0.004, transient=30_000)
    bounded = bool(np.all(np.isfinite(pts)) and np.max(np.abs(pts)) < 10.0)
    mean_div = float(np.mean([divergence(p) for p in pts[::100]]))
    results["bounded_4M_steps"] = bounded
    results["extent_min"] = [round(v, 4) for v in pts.min(0)]
    results["extent_max"] = [round(v, 4) for v in pts.max(0)]
    results["mean_divergence"] = round(mean_div, 5)
    print(f"  bounded={bounded}  extent=[{np.round(pts.min(0),3)}, {np.round(pts.max(0),3)}]"
          f"  mean div={mean_div:.4f}")

    nov = novelty_vs_catalog(pts)
    if nov:
        results["novelty_vs_dysts"] = nov
        print(f"  novelty: nearest={nov['nearest']} at distance {nov['distance']}")

    out = ROOT / "results" / "naiad_verification.json"
    out.write_text(json.dumps(results, indent=2) + "\n")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
