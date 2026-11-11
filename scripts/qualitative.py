"""Qualitative figure: six axial CT pairs from the staging cohort.

Usage (from the project root):
    python scripts/qualitative.py                # reads scripts/cases.npz
    python scripts/qualitative.py path/to/cases.npz

Writes figures/qualitative.pdf and figures/qualitative.png (200 dpi).
Reads only cases.npz; all coordinates are voxel (z, y, x) on the shared
current-frame grid with spacing (1.5, 0.7, 0.7) mm.
"""
import os
import sys

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "figures")

WINDOW = (-950, 80)            # lung window, HU
TOL_MM = 3.0                   # hit tolerance
CAND_SLAB_MM = 1.6             # show candidates within this axial distance
TITLE_COLOR = "#b86a3d"
COL = {
    "query": "white",
    "cand": "#e4e4e4",
    "affine": "#9ad0ff",
    "ref": "#ffe14a",
    "diverse": "#58cbff",
    "spline": "#ffb05c",
    "sam": "#75e9a8",
}


def load(path):
    d = np.load(path, allow_pickle=False)
    data = {k: d[k] for k in d.files}
    assert data["current"].shape[0] == 6 and data["prior"].shape[0] == 6, "expected 6 columns"
    assert float(data["half_mm"]) == 16.0, "half_mm must be 16"
    assert np.allclose(data["spacing_zyx"], [1.5, 0.7, 0.7]), "spacing must be [1.5, 0.7, 0.7]"
    return data


def show_slice(ax, vol, z, center_yx, dz, dy, dx, half):
    img = vol[int(z)].astype(np.float32)          # (y, x), not modified in place
    ny, nx = img.shape
    extent = [-dx / 2, (nx - 0.5) * dx, -dy / 2, (ny - 0.5) * dy]
    ax.imshow(img, cmap="gray", vmin=WINDOW[0], vmax=WINDOW[1], interpolation="nearest",
              origin="lower", extent=extent)
    cy, cx = center_yx[0] * dy, center_yx[1] * dx
    ax.set_xlim(cx - half, cx + half)
    ax.set_ylim(cy - half, cy + half)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    return cy, cx


def mm(p, dy, dx):
    """voxel (z, y, x) -> plot (x_mm, y_mm)."""
    return p[2] * dx, p[1] * dy


def main(path):
    d = load(path)
    dz, dy, dx = (float(v) for v in d["spacing_zyx"])
    half = float(d["half_mm"])
    labels = [str(s) for s in d["labels"]]

    plt.rcParams.update({"font.family": "DejaVu Sans", "pdf.fonttype": 42})
    fig, axes = plt.subplots(2, 6, figsize=(7.0, 2.62),
                             gridspec_kw=dict(wspace=0.03, hspace=0.03,
                                              left=0.005, right=0.995, top=0.915, bottom=0.115))
    for i in range(6):
        # --- top: current CT with the query
        a0 = axes[0, i]
        show_slice(a0, d["current"][i], d["current_slice"][i], d["current_center_yx"][i],
                   dz, dy, dx, half)
        qx, qy = mm(d["query"][i], dy, dx)
        a0.plot(qx, qy, marker="+", ms=9, mew=1.4, color=COL["query"], ls="none")
        a0.set_title(labels[i], fontsize=8, fontweight="bold", color=TITLE_COLOR, pad=2.5)

        # --- bottom: earlier CT
        a1 = axes[1, i]
        z = int(d["earlier_slice"][i])
        show_slice(a1, d["prior"][i], z, d["earlier_center_yx"][i], dz, dy, dx, half)
        n = int(d["candidate_n"][i])
        cand = d["candidates"][i, :n]
        keep = np.abs(cand[:, 0] - z) * dz <= CAND_SLAB_MM
        a1.plot(cand[keep, 2] * dx, cand[keep, 1] * dy, ls="none", marker="o", ms=2,
                mfc=COL["cand"], mec="none", alpha=0.9)
        rx, ry = mm(d["reference"][i], dy, dx)
        a1.add_patch(Circle((rx, ry), TOL_MM, fill=False, ec="white", lw=0.9, ls=(0, (1, 1.3))))
        a1.plot(qx, qy, marker="x", ms=6, mew=1.3, color=COL["affine"], ls="none")
        a1.plot(rx, ry, marker="*", ms=9, color=COL["ref"], mec="black", mew=0.3, ls="none")
        for key, mk, ms in (("diverse", "o", 8), ("spline", "^", 8), ("sam", "s", 7)):
            px, py = mm(d[key][i], dy, dx)
            a1.plot(px, py, marker=mk, ms=ms, mfc="none", mec=COL[key], mew=1.4, ls="none")

    # 5 mm scale bar, lower-left of the first current panel
    a0 = axes[0, 0]
    x0, x1 = a0.get_xlim(); y0, y1 = a0.get_ylim()
    bx, by = x0 + 2.0, y0 + 2.4
    a0.plot([bx, bx + 5.0], [by, by], color="white", lw=2.0, solid_capstyle="butt")
    a0.text(bx + 2.5, by + 0.9, "5 mm", color="white", fontsize=6.5, ha="center", va="bottom")

    handles = [
        Line2D([], [], ls="none", marker="+", ms=7, mew=1.3, color="black", label="query"),
        Line2D([], [], ls="none", marker="*", ms=8, color=COL["ref"], mec="black", mew=0.4,
               label="reference"),
        Line2D([], [], ls=(0, (1, 1.3)), lw=1.0, color="black", label="3 mm"),
        Line2D([], [], ls="none", marker="o", ms=3, mfc="#9a9a9a", mec="none",
               label="kept candidates"),
        Line2D([], [], ls="none", marker="o", ms=6, mfc="none", mec="#2a9fd6", mew=1.3,
               label="Diverse search"),
        Line2D([], [], ls="none", marker="^", ms=6, mfc="none", mec="#e08a2e", mew=1.3,
               label="B-spline"),
        Line2D([], [], ls="none", marker="s", ms=5.5, mfc="none", mec="#2fb36e", mew=1.3,
               label="SAM"),
        Line2D([], [], ls="none", marker="x", ms=5.5, mew=1.3, color="#4a90d9",
               label="chest-affine query"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=8, frameon=False, fontsize=6.6,
               handlelength=1.6, handletextpad=0.35, columnspacing=0.9,
               bbox_to_anchor=(0.5, -0.005))

    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, "qualitative.pdf"))
    fig.savefig(os.path.join(OUT, "qualitative.png"), dpi=200)
    plt.close(fig)
    print("wrote figures/qualitative.pdf and figures/qualitative.png")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "cases.npz"))
