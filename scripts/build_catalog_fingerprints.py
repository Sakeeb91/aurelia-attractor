"""Fingerprint the dysts catalog of known chaotic systems.

Integrates every continuous system in the dysts database (Gilpin 2021,
arXiv:2110.05266), projects to the first three coordinates when the system
is higher-dimensional, fingerprints the resulting point cloud, and caches
everything to results/catalog_fingerprints.json. This is the reference set
against which candidate attractors are scored for novelty.

Run once:  python scripts/build_catalog_fingerprints.py
"""

from __future__ import annotations

import json
import pathlib
import sys
import warnings

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
warnings.filterwarnings("ignore")

from atlas.fingerprint import fingerprint

OUT = pathlib.Path(__file__).resolve().parents[1] / "results" / "catalog_fingerprints.json"
N_POINTS = 1500


def main():
    import dysts.flows as flows
    from dysts.systems import get_attractor_list

    names = get_attractor_list(sys_class="continuous")
    catalog = {}
    failed = []
    for name in names:
        try:
            model = getattr(flows, name)()
            traj = model.make_trajectory(N_POINTS)
            if traj is None or len(traj) < 400:
                raise ValueError("short or empty trajectory")
            fp = fingerprint(np.asarray(traj)[:, :3])
            if fp is None:
                raise ValueError("degenerate cloud")
            meta = {
                "fingerprint": [round(float(v), 6) for v in fp],
                "lyap": getattr(model, "maximum_lyapunov_estimated", None),
                "d_ky": getattr(model, "kaplan_yorke_dimension", None),
            }
            catalog[name] = meta
            print(f"ok    {name}")
        except Exception as e:                                    # noqa: BLE001
            failed.append(name)
            print(f"skip  {name}: {type(e).__name__}: {e}")

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(catalog, indent=1) + "\n")
    print(f"\nfingerprinted {len(catalog)}/{len(names)} systems "
          f"({len(failed)} skipped) -> {OUT}")


if __name__ == "__main__":
    main()
