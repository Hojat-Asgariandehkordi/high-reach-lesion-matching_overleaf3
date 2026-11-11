"""Method overview (Fig. 2): BioRender art for panels A, B, D, E plus a code-drawn panel C.

All text is typeset here in Times; the BioRender art contains no text.
Art lives in figures/biorender/ov_*.{png,jpg}; a high-res PNG export with the same
canvas replaces the JPEG preview automatically. Panel C runs the actual greedy rule
(Alg. 1) on a synthetic 2D fit landscape with K = 12 on both sides.
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle
sys.path.insert(0, os.path.dirname(__file__))
import style as S
import fig_schematic as F            # synthetic landscape + greedy rule

S.apply()
OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
BR = os.path.join(OUT, "biorender")
PREVIEW_W, PREVIEW_H = 1024, 572     # coordinates below refer to the preview canvas

BLUE, TEAL, ORANGE = "#3f6fd1", "#3fb8a8", "#e8792a"


def art(name, box):
    """Crop box (x0, y0, x1, y1) given in preview pixels; works for any export size."""
    from PIL import Image
    for ext in ("png", "jpg"):
        f = os.path.join(BR, f"{name}.{ext}")
        if os.path.exists(f):
            im = Image.open(f).convert("RGB")
            sx, sy = im.width / PREVIEW_W, im.height / PREVIEW_H
            x0, y0, x1, y1 = box
            return np.asarray(im.crop((int(x0 * sx), int(y0 * sy), int(x1 * sx), int(y1 * sy)))), (x0, y0, x1, y1)
    raise FileNotFoundError(name)


def show(ax, name, box):
    img, (x0, y0, x1, y1) = art(name, box)
    ax.imshow(img, extent=[x0, x1, y1, y0], interpolation="lanczos")   # preview pixel coords
    ax.set_xlim(x0, x1); ax.set_ylim(y1, y0)
    ax.axis("off")
    return ax


def title(ax, s, y=0.965):
    x = ax.get_position().x0
    ax.figure.text(x, y, s, ha="left", va="top", fontsize=8, fontweight="bold")


def T(ax, x, y, s, **kw):
    kw.setdefault("fontsize", 6.8)
    kw.setdefault("ha", "center")
    kw.setdefault("va", "center")
    kw.setdefault("color", S.INK)
    ax.text(x, y, s, **kw)


def panel_c(ax_l, ax_r):
    K = 12
    fit_idx = F.order[:K]
    div_idx = F.diverse(F.order, K=K)
    gg = np.linspace(-7.6, 7.6, 220)
    GX, GY = np.meshgrid(gg, gg)
    Q = np.stack([GX.ravel(), GY.ravel()], 1)
    FIT = -(1.0 * F.gauss(Q, F.WRONG, 2.0) + 0.65 * F.gauss(Q, F.TRUE, 1.3))
    for ax, idx, ring in ((ax_l, fit_idx, False), (ax_r, div_idx, True)):
        ax.imshow(-FIT.reshape(GX.shape), extent=[-7.6, 7.6, -7.6, 7.6], origin="lower",
                  cmap="Greens", vmin=-0.25, vmax=1.6, interpolation="bilinear")
        if ring:
            for i in idx:
                ax.add_patch(Circle(F.P[i], 2.1 / 2, color=BLUE, alpha=0.15, lw=0))
        ax.add_patch(Circle(F.Y_REF, 3.0, fill=False, ec="black", lw=0.9))
        ax.plot(*F.Y_REF, marker="*", ms=10, color=ORANGE, mec="white", mew=0.5, zorder=6)
        hit = [i for i in idx if np.linalg.norm(F.P[i] - F.Y_REF) <= 3.0]
        for i in idx:
            ax.plot(*F.P[i], "o", ms=4.6, color=BLUE, mec="#1d3f8f" if i in hit else "white",
                    mew=1.3 if i in hit else 0.5, zorder=5)
        ax.set_xlim(-7.6, 7.6); ax.set_ylim(-7.6, 7.6); ax.set_aspect("equal")
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(True); s.set_color(S.MUTED); s.set_linewidth(0.6)
        assert len(idx) == K
    return fit_idx, div_idx


def main():
    W = S.PAGE_W
    fig = plt.figure(figsize=(W, 3.55))
    # ---------------- row 1: A, B, D ----------------
    r1 = 0.545
    aA = fig.add_axes([0.005, r1, 0.37, 0.36])
    aB = fig.add_axes([0.395, r1, 0.17, 0.36])
    aD = fig.add_axes([0.62, r1, 0.375, 0.36])
    show(aA, "ov_A_align", (28, 112, 996, 460))
    title(aA, "A  Global alignment")
    T(aA, 250, 478, "current CT", va="top")
    T(aA, 773, 478, "earlier CT", va="top")
    T(aA, 512, 240, "chest\naffine", fontsize=6.5, color=S.INK2, linespacing=1.0)
    T(aA, 150, 362, "query $p$", fontsize=6.5, color="white")
    T(aA, 660, 362, "true lesion?", fontsize=6.5, color="white")

    show(aB, "ov_B_shell", (258, 41, 766, 530))
    title(aB, "B  Fit / witness shell")
    for k, (lab, col, hatch) in enumerate((("fit", "#8aa6ea", None), ("witness", "#6fd2c3", None),
                                           ("lesion core", "#d9d9d9", "////"))):
        y = 600 + 52 * k
        aB.add_patch(Rectangle((280, y - 16), 34, 32, facecolor=col, edgecolor=S.INK2, lw=0.4,
                               hatch=hatch, clip_on=False))
        T(aB, 330, y, lab, ha="left", fontsize=6.5)
    aB.set_ylim(745, 41)

    show(aD, "ov_D_scorer", (100, 100, 955, 505))
    title(aD, "D  Lesion scoring")
    T(aD, 160, 525, "kept candidates", va="top")
    T(aD, 506, 140, "frozen scorer $s(t)$", fontsize=6.6)
    T(aD, 506, 425, "lesion features $\\ell_t$ + soft fit penalty", va="top", fontsize=6.0,
      color=S.INK2)
    T(aD, 850, 400, "selected $\\hat{x}$", va="top")
    aD.set_ylim(545, 100)

    # ---------------- row 2: C, E ----------------
    r2 = 0.075
    aCl = fig.add_axes([0.03, r2, 0.2, 0.33])
    aCr = fig.add_axes([0.305, r2, 0.2, 0.33])
    fit_idx, div_idx = panel_c(aCl, aCr)
    fig.text(0.005, 0.475, "C  Same budget ($K{=}12$), different allocation", ha="left",
             va="top", fontsize=8, fontweight="bold")
    aCl.text(0.5, 1.03, "top 12 by fit", transform=aCl.transAxes, ha="center", va="bottom",
             fontsize=6.8)
    aCr.text(0.5, 1.03, "fit-ordered diverse ($\\geq r$ apart)", transform=aCr.transAxes,
             ha="center", va="bottom", fontsize=6.8)
    aCl.text(0.5, -0.04, "no candidate within 3 mm", transform=aCl.transAxes, ha="center",
             va="top", fontsize=6.6, color="#b4471b")
    n_in = sum(np.linalg.norm(F.P[i] - F.Y_REF) <= 3.0 for i in div_idx)
    aCr.text(0.5, -0.04, f"{n_in} candidates within 3 mm", transform=aCr.transAxes, ha="center",
             va="top", fontsize=6.6, color="#1d3f8f")
    fig.add_artist(FancyArrowPatch((0.236, r2 + 0.18), (0.299, r2 + 0.18),
                                   transform=fig.transFigure, arrowstyle="<|-|>",
                                   mutation_scale=7, color=S.INK2, lw=0.8))
    fig.text(0.2675, r2 + 0.205, "same fit\norder", ha="center", va="bottom", fontsize=6.2,
             color=S.INK2, linespacing=1.0)

    aE = fig.add_axes([0.545, r2, 0.45, 0.33])
    show(aE, "ov_E_reachhit", (10, 110, 1014, 462))
    fig.text(0.545, 0.475, "E  Reach and hit at tolerance $\\tau = 3$ mm", ha="left",
             va="top", fontsize=8, fontweight="bold")
    for x, lab, sub in ((173, "unreachable", "no candidate inside"),
                        (512, "reachable, missed", "wrong one selected"),
                        (851, "hit", "selected one inside")):
        T(aE, x, 100, lab, va="bottom", fontsize=7)
        T(aE, x, 474, sub, va="top", fontsize=6.3, color=S.INK2)
    aE.set_ylim(500, 70)
    fig.text(0.997, 0.005, "black ring = selected candidate; star = reference (evaluation only)",
             ha="right", va="bottom", fontsize=6.0, color=S.INK2)

    fig.add_artist(plt.Line2D([0.005, 0.995], [0.505, 0.505], transform=fig.transFigure,
                              color=S.GRID, lw=0.8))
    fig.savefig(os.path.join(OUT, "overview.pdf"))
    fig.savefig(os.path.join(OUT, "overview.png"), dpi=220)
    plt.close(fig)
    print("wrote figures/overview.pdf")


if __name__ == "__main__":
    main()
