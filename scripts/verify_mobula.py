"""Full chaos verification of the Mobula attractor.

Mirrors scripts/verify_cassiopea.py: Lyapunov spectrum, Kaplan-Yorke dimension,
robustness across initial conditions, equilibria with eigenvalues, long-orbit
boundedness, time-averaged divergence, the S4 symmetry residual of the orbit,
and the fingerprint-distance novelty against the dysts catalog.

Writes results/mobula_verification.json.
"""

from __future__ import annotations

import json
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from mobula.dynamics import (
    ALPHA, BETA, DELTA, EPS, GAMMA, LAM, NU, OMEGA, divergence, trajectory,
)
from mobula.equilibria import classify, find_equilibria
from mobula.lyapunov import kaplan_yorke_dimension, lyapunov_spectrum

ROOT = pathlib.Path(__file__).resolve().parents[1]
PARAMS = (ALPHA, BETA, OMEGA, GAMMA, DELTA, NU, LAM, EPS)


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


def symmetry_residuals(pts, n_query=2500, n_base=8000, seed=0):
    """Normalized nearest-neighbour RMS of sigma(cloud) and a flip-control.

    sigma:(x,y,z)->(-y,x,-z) is the S4 generator (w->i*w is (x,y)->(-y,x);
    z->-z). The pure flip (x,y,z)->(x,y,-z) is NOT a symmetry; its larger
    residual is the control that shows sigma is special.
    """
    q = pts[np.all(np.isfinite(pts), axis=1)]
    q = q - q.mean(0)
    extent = float(np.ptp(q, axis=0).max())
    rng = np.random.default_rng(seed)
    base = q[rng.choice(len(q), size=min(n_base, len(q)), replace=False)]
    qi = q[rng.choice(len(q), size=min(n_query, len(q)), replace=False)]

    def nn_rms(transformed):
        d = np.empty(len(transformed))
        for k, t in enumerate(transformed):
            d[k] = np.sqrt(((base - t) ** 2).sum(1)).min()
        return float(np.sqrt((d ** 2).mean()) / extent)

    sig = np.column_stack([-qi[:, 1], qi[:, 0], -qi[:, 2]])
    flip = np.column_stack([qi[:, 0], qi[:, 1], -qi[:, 2]])
    return nn_rms(sig), nn_rms(flip)


def main():
    results = {
        "system": "Mobula attractor",
        "symmetry": "S4 rotoreflection (Schoenflies), generator sigma:(w,z)->(i*w,-z)",
        "parameters": {"alpha": ALPHA, "beta": BETA, "omega": OMEGA, "gamma": GAMMA,
                       "delta": DELTA, "nu": NU, "lam": LAM, "eps": EPS},
    }

    print("Lyapunov spectrum (long run)...")
    spec = lyapunov_spectrum(n_steps=600_000, dt=0.005, params=PARAMS)
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
                                                   state0=s0, params=PARAMS)[0]), 5))
    results["largest_exponent_across_ics"] = lles
    print(f"  LLE across 5 ICs: {lles}")

    print("Equilibria...")
    results["equilibria"] = []
    for e in find_equilibria(PARAMS):
        eigs, label = classify(e, PARAMS)
        results["equilibria"].append({
            "point": [round(v, 6) for v in e],
            "eigenvalues": [[round(v.real, 5), round(v.imag, 5)] for v in eigs],
            "type": label,
        })
        print(f"  {np.round(e, 4)}  {label}  eigs={np.round(eigs, 4)}")

    print("Long-orbit boundedness (4M steps)...")
    pts = trajectory(n_steps=4_000_000, dt=0.004, transient=40_000)
    bounded = bool(np.all(np.isfinite(pts)) and np.max(np.abs(pts)) < 10.0)
    mean_div = float(np.mean([divergence(p) for p in pts[::100]]))
    results["bounded_4M_steps"] = bounded
    results["extent_min"] = [round(v, 4) for v in pts.min(0)]
    results["extent_max"] = [round(v, 4) for v in pts.max(0)]
    results["mean_divergence"] = round(mean_div, 5)
    print(f"  bounded={bounded}  extent=[{np.round(pts.min(0),3)}, {np.round(pts.max(0),3)}]"
          f"  mean div={mean_div:.4f}")

    sig_res, flip_res = symmetry_residuals(pts)
    results["s4_symmetry_residual"] = round(sig_res, 5)
    results["flip_control_residual"] = round(flip_res, 5)
    print(f"  S4 residual={sig_res:.4f}  (pure-flip control={flip_res:.4f}; "
          f"ratio {flip_res/sig_res:.2f}x)")

    nov = novelty_vs_catalog(pts)
    if nov:
        results["novelty_vs_dysts"] = nov
        print(f"  novelty: nearest={nov['nearest']} at distance {nov['distance']}")

    out = ROOT / "results" / "mobula_verification.json"
    out.write_text(json.dumps(results, indent=2) + "\n")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
