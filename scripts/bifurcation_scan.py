"""Route to chaos: largest Lyapunov exponent across the rotation rate c.

Sweeps c with a and b held at their canonical values and plots the
largest Lyapunov exponent together with the orbit's z-extent. Windows
with LLE ~ 0 are periodic (limit cycles); LLE > 0 is chaos. The plot is
saved to gallery/bifurcation.png and the sweep data to
results/bifurcation_c.csv.
"""

from __future__ import annotations

import pathlib
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from aurelia.dynamics import A, B, rk4_step, velocity

ROOT = pathlib.Path(__file__).resolve().parents[1]


def largest_lyapunov(c, n=40_000, dt=0.01, transient=12_000):
    s = np.array([0.3, 0.2, 0.1])
    for _ in range(transient):
        s = rk4_step(s, dt, A, B, c)
        if not np.all(np.isfinite(s)) or np.max(np.abs(s)) > 1e3:
            return np.nan, np.nan
    d0 = 1e-8
    shadow = s + np.array([d0, 0.0, 0.0])
    log_sum = 0.0
    z_lo, z_hi = s[2], s[2]
    for _ in range(n):
        s = rk4_step(s, dt, A, B, c)
        shadow = rk4_step(shadow, dt, A, B, c)
        if not np.all(np.isfinite(s)) or np.max(np.abs(s)) > 1e3:
            return np.nan, np.nan
        d = np.linalg.norm(shadow - s) or 1e-16
        log_sum += np.log(d / d0)
        shadow = s + (shadow - s) * (d0 / d)
        z_lo, z_hi = min(z_lo, s[2]), max(z_hi, s[2])
    return log_sum / (n * dt), z_hi - z_lo


def main():
    cs = np.linspace(1.2, 2.6, 281)
    lles, spans = [], []
    for c in cs:
        lle, span = largest_lyapunov(c)
        lles.append(lle)
        spans.append(span)
        print(f"c={c:.3f}  LLE={lle:7.4f}  z-span={span:5.2f}")

    lles = np.array(lles)
    out_csv = ROOT / "results" / "bifurcation_c.csv"
    out_csv.parent.mkdir(exist_ok=True)
    np.savetxt(
        out_csv,
        np.column_stack([cs, lles, spans]),
        delimiter=",",
        header="c,largest_lyapunov_exponent,z_span",
        comments="",
    )

    fig, ax = plt.subplots(figsize=(12, 5), facecolor="#0d0b1a")
    ax.set_facecolor("#0d0b1a")
    ax.axhline(0, color="#5a5480", lw=0.8)
    ax.fill_between(cs, lles, 0, where=lles > 0, color="#f4a261", alpha=0.45, label="chaos")
    ax.plot(cs, lles, color="#ffd97d", lw=1.4)
    ax.axvline(1.9, color="#e0719b", lw=1.0, ls="--", label="canonical c = 1.9")
    ax.set_xlabel("c (rotation rate)", color="#e8e4f0")
    ax.set_ylabel("largest Lyapunov exponent", color="#e8e4f0")
    ax.tick_params(colors="#b8b2cc")
    for spine in ax.spines.values():
        spine.set_color("#5a5480")
    ax.legend(facecolor="#1b1535", labelcolor="#e8e4f0", edgecolor="#5a5480")
    ax.set_title("Aurelia system: route to chaos along c (a=1.4, b=0.5)", color="#e8e4f0")
    fig.tight_layout()
    out_png = ROOT / "gallery" / "bifurcation.png"
    out_png.parent.mkdir(exist_ok=True)
    fig.savefig(out_png, dpi=170, facecolor="#0d0b1a")
    print(f"\nwrote {out_csv}\nwrote {out_png}")


if __name__ == "__main__":
    main()
