"""Qualitative-results figure (and real-CT teaser backdrop).

Usage once patches are exported from the pipeline:
    python scripts/qualitative.py cases.npz            -> fig/qualitative.pdf
    python scripts/qualitative.py --placeholder        -> layout placeholder

cases.npz must hold, for N cases (2D axial slices through the reference, in the
shared current-frame grid, 0.7 mm pixels, HU):
    current   (N, H, W)  current-scan slice through the query p
    earlier   (N, H, W)  resampled earlier-scan slice through the reference
    query     (N, 2)     p in pixel (row, col) of `current`
    ref       (N, 2)     earlier reference in pixels of `earlier`
    ours      (N, 2)     Diverse search selection
    spline    (N, 2)     spline mapped point
    sam       (N, 2)     SAM standalone point
    cands     (N, M, 2)  retained centres projected to the slice (NaN-padded)
    title     (N,)       short case label, e.g. "staging, 4 mm nodule"
Slices should be windowed for lung: [-1000, 400] HU.
"""
import sys, os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
sys.path.insert(0, os.path.dirname(__file__))
import style as S

S.apply()
OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
PX_MM = 0.7


def mark(ax, rc, **kw):
    if rc is None or np.any(np.isnan(rc)):
        return
    ax.plot(rc[1], rc[0], ls="none", **kw)


def draw(cases, n_cols=6):
    n = len(cases["current"])
    n_cols = min(n_cols, n)
    fig, axes = plt.subplots(2, n_cols, figsize=(S.PAGE_W, 2.55))
    axes = np.atleast_2d(axes)
    for k in range(n_cols):
        a0, a1 = axes[0, k], axes[1, k]
        for a in (a0, a1):
            a.set_xticks([]); a.set_yticks([]); a.grid(False)
        a0.imshow(np.clip(cases["current"][k], -1000, 400), cmap="gray", vmin=-1000, vmax=400)
        mark(a0, cases["query"][k], marker="+", ms=8, mew=1.3, color="#ffd400")
        a1.imshow(np.clip(cases["earlier"][k], -1000, 400), cmap="gray", vmin=-1000, vmax=400)
        c = cases["cands"][k]
        c = c[~np.isnan(c).any(1)]
        a1.plot(c[:, 1], c[:, 0], "o", ms=1.8, color=S.OURS, alpha=0.6)
        ref = cases["ref"][k]
        a1.add_patch(Circle((ref[1], ref[0]), 3.0 / PX_MM, fill=False, ls=":", lw=0.8,
                            color="white"))
        mark(a1, ref, marker="*", ms=8, color=S.SPLINE, mec="white", mew=0.4)
        mark(a1, cases["ours"][k], marker="o", ms=5, mfc="none", mec=S.OURS, mew=1.3)
        mark(a1, cases["spline"][k], marker="^", ms=5, mfc="none", mec="#ffd400", mew=1.1)
        mark(a1, cases["sam"][k], marker="s", ms=4.5, mfc="none", mec="#e87ba4", mew=1.1)
        a0.set_title(str(cases["title"][k]), fontsize=6, loc="left")
    axes[0, 0].set_ylabel("Current")
    axes[1, 0].set_ylabel("Earlier")
    fig.subplots_adjust(wspace=0.04, hspace=0.06)
    return fig


def placeholder(n_cols=6):
    fig, axes = plt.subplots(2, n_cols, figsize=(S.PAGE_W, 2.4))
    labels = ["success", "success", "success", "spline fails", "large motion", "failure"]
    for k in range(n_cols):
        for r, a in enumerate(axes[:, k]):
            a.set_xticks([]); a.set_yticks([]); a.grid(False)
            a.set_facecolor("#efeeea")
            for s in a.spines.values():
                s.set_visible(True); s.set_color(S.MUTED); s.set_linestyle((0, (2, 2)))
            a.text(0.5, 0.5, ("current CT\n+ query" if r == 0 else
                              "earlier CT\nref / ours /\nspline / SAM"),
                   ha="center", va="center", fontsize=6, color=S.INK2, transform=a.transAxes)
        axes[0, k].set_title(labels[k], fontsize=6, loc="left", color=S.SPLINE)
    fig.suptitle("PLACEHOLDER: export patches and run scripts/qualitative.py cases.npz",
                 fontsize=7, color="#c0392b", y=1.02)
    fig.subplots_adjust(wspace=0.05, hspace=0.06)
    return fig


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != "--placeholder":
        d = np.load(sys.argv[1], allow_pickle=True)
        fig = draw({k: d[k] for k in d.files})
    else:
        fig = placeholder()
    fig.savefig(os.path.join(OUT, "qualitative.pdf"))
    print("written")
