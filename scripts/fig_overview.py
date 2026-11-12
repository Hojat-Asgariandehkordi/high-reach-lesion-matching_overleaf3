"""Method overview (Fig. 2), laid out after the authors' sketch.

Top row: A (initial alignment), B (candidate generation & ranking), D (lesion scoring).
Bottom row: C (candidate selection comparison), E (outcome distinction).
Panels A, B, D, E use text-free BioRender art (figures/biorender/ov_*.{png,jpg}; a PNG export
with the same canvas replaces the JPEG preview automatically). Panel C is drawn here with the
actual greedy rule so both sides have exactly the same candidate budget.
The fit/witness shell in B surrounds the lesion (23-28 mm ring), not the whole lungs.
All text is typeset in Times by this script.
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
from matplotlib.lines import Line2D
sys.path.insert(0, os.path.dirname(__file__))
import style as S

S.apply()
OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
BR = os.path.join(OUT, "biorender")
PW, PH = 1024, 572                       # BioRender preview canvas (crop boxes use these pixels)
BLUE, NAVY, ORANGE, INK = "#4a78d4", "#1d3f8f", "#e8792a", "#111111"
FS = 6.6                                 # body label size (pt)


def art(name, box):
    from PIL import Image
    for ext in ("png", "jpg"):
        f = os.path.join(BR, f"{name}.{ext}")
        if os.path.exists(f):
            im = Image.open(f).convert("RGB")
            sx, sy = im.width / PW, im.height / PH
            x0, y0, x1, y1 = box
            return np.asarray(im.crop((int(x0 * sx), int(y0 * sy), int(x1 * sx), int(y1 * sy))))
    raise FileNotFoundError(name)


def show(ax, name, box):
    x0, y0, x1, y1 = box
    ax.imshow(art(name, box), extent=[x0, x1, y1, y0], interpolation="lanczos")
    ax.set_xlim(x0, x1); ax.set_ylim(y1, y0); ax.axis("off")


def T(ax, x, y, s, **kw):
    kw.setdefault("fontsize", FS); kw.setdefault("ha", "center"); kw.setdefault("va", "center")
    kw.setdefault("color", INK); kw.setdefault("linespacing", 1.05)
    return ax.text(x, y, s, **kw)


def ftext(fig, x, y, s, **kw):
    kw.setdefault("fontsize", FS); kw.setdefault("ha", "center"); kw.setdefault("va", "center")
    kw.setdefault("color", INK); kw.setdefault("linespacing", 1.05)
    return fig.text(x, y, s, **kw)


def head(fig, x, y, s):
    fig.text(x, y, s, ha="left", va="top", fontsize=8.6, fontweight="bold", color=INK)


def arrow(fig, a, b, style="-|>", ms=7, lw=0.7):
    fig.add_artist(FancyArrowPatch(a, b, transform=fig.transFigure, arrowstyle=style,
                                   mutation_scale=ms, lw=lw, color=INK, shrinkA=0, shrinkB=0))


def line(fig, a, b, lw=0.5):
    fig.add_artist(Line2D([a[0], b[0]], [a[1], b[1]], transform=fig.transFigure, color=INK, lw=lw))


# ----------------------------------------------------------------------------- panel C
LUNGS = ((-3.3, 2.9, 5.6), (3.3, 2.9, 5.6))


def in_lungs(p):
    return np.any([((p[:, 0] - cx) / a) ** 2 + (p[:, 1] / b) ** 2 <= 1.0 for cx, a, b in LUNGS], 0)


def gauss(p, m, s):
    return np.exp(-np.sum((p - m) ** 2, 1) / (2 * s ** 2))


WRONG, TRUE = np.array([-3.9, 0.6]), np.array([0.3, -0.2])


def fit_score(p):          # higher = better fit (shown darker green)
    return 1.0 * gauss(p, WRONG, 1.7) + 0.55 * gauss(p, TRUE, 1.1)


def greedy(P, order, r, K):
    kept = []
    for i in order:
        if all(np.linalg.norm(P[i] - P[j]) >= r for j in kept):
            kept.append(i)
            if len(kept) == K:
                break
    return kept


def panel_c(axL, axR, K=15, tau=1.5):
    g = np.round(np.arange(-7.0, 7.001, 0.35), 3)
    XX, YY = np.meshgrid(g, g)
    P = np.stack([XX.ravel(), YY.ravel()], 1)
    P = P[in_lungs(P) | (np.linalg.norm(P - TRUE, axis=1) < 2.0)]
    f = fit_score(P) + 0.1 * in_lungs(P)
    order = np.lexsort((np.linalg.norm(P - WRONG, axis=1), -f))
    top = list(order[:K])
    div = None
    for r in np.arange(3.2, 1.5, -0.05):
        cand = greedy(P, order, r, K)
        n_in = sum(np.linalg.norm(P[i] - TRUE) <= tau for i in cand)
        if len(cand) == K and n_in == 1:
            div = cand
            break
    assert div is not None and len(top) == len(div) == K
    assert not any(np.linalg.norm(P[i] - TRUE) <= tau for i in top)
    gx = np.linspace(-7.6, 7.6, 320)
    GX, GY = np.meshgrid(gx, gx)
    Q = np.stack([GX.ravel(), GY.ravel()], 1)
    lm = in_lungs(Q)
    img = (0.12 + 0.9 * fit_score(Q)) * lm + 0.35 * fit_score(Q) * (~lm)
    for ax, idx in ((axL, top), (axR, div)):
        ax.imshow(img.reshape(GX.shape), extent=[-7.6, 7.6, -7.6, 7.6], origin="lower",
                  cmap="Greens", vmin=-0.02, vmax=1.35, interpolation="bilinear")
        ax.add_patch(Circle(TRUE, tau, fill=False, ec="black", lw=1.0, zorder=4))
        ax.plot(*TRUE, marker="*", ms=11, color=ORANGE, mec="#9a4a12", mew=0.5, zorder=6)
        for i in idx:
            inside = np.linalg.norm(P[i] - TRUE) <= tau
            ax.plot(*P[i], "o", ms=5.0, color=BLUE, mec=NAVY, mew=1.6 if inside else 0.6, zorder=5)
        ax.set_xlim(-7.6, 7.6); ax.set_ylim(-7.6, 7.6); ax.set_aspect("equal")
        ax.set_xticks([]); ax.set_yticks([])
        for s_ in ax.spines.values():
            s_.set_color("#444444"); s_.set_linewidth(0.7)
    return top, div, P, tau


# ----------------------------------------------------------------------------- figure
def main():
    W, H = S.PAGE_W, 4.6
    fig = plt.figure(figsize=(W, H))
    ftext(fig, 0.5, 0.99, "LONGITUDINAL PULMONARY CT CORRESPONDENCE PIPELINE", va="top", fontsize=12.5)
    gray = dict(transform=fig.transFigure, color="#9a9a9a", lw=0.6)
    fig.add_artist(Line2D([0.352, 0.352], [0.565, 0.91], **gray))
    fig.add_artist(Line2D([0.662, 0.662], [0.565, 0.91], **gray))
    fig.add_artist(Line2D([0.01, 0.99], [0.553, 0.553], **gray))
    fig.add_artist(Line2D([0.685, 0.685], [0.03, 0.54], **gray))

    # ---------------- A. Initial alignment
    head(fig, 0.01, 0.92, "A. Initial Alignment")
    aA1 = fig.add_axes([0.012, 0.635, 0.118, 0.23])
    aA2 = fig.add_axes([0.228, 0.635, 0.118, 0.23])
    show(aA1, "ov_A_align", (32, 125, 250, 440))
    show(aA2, "ov_A_align", (553, 125, 771, 440))
    # arrow from the current lesion to its affine-mapped location
    a0 = fig.transFigure.inverted().transform(aA1.transData.transform((135, 325)))
    a1 = fig.transFigure.inverted().transform(aA2.transData.transform((659, 325)))
    arrow(fig, (a0[0] + 0.008, a0[1]), (a1[0] - 0.009, a1[1]), ms=10, lw=1.6)
    ftext(fig, 0.179, 0.80, "Affine\nAlignment")
    ftext(fig, 0.179, 0.665, "Residual\nDisplacement")
    fig.add_artist(Line2D([0.018], [0.605], marker="o", ms=5.0, color=BLUE, mec=NAVY, mew=0.8,
                          transform=fig.transFigure))
    ftext(fig, 0.028, 0.605, "Current Lesion", ha="left")
    ftext(fig, 0.287, 0.598, "Offset (reference point\nhidden from algorithm)", fontsize=FS - 0.3)

    # ---------------- B. Candidate generation & ranking
    head(fig, 0.36, 0.92, "B. Candidate Generation & Ranking")
    aB = fig.add_axes([0.443, 0.615, 0.14, 0.245])
    box = (262, 46, 758, 524)
    show(aB, "ov_B_shell", box)
    cx, cy = 510, 285
    for rad in np.linspace(122, 200, 4):                  # sampled shell voxels (right half)
        for th in np.linspace(-80, 80, int(rad / 10)):
            t = np.deg2rad(th)
            aB.plot(cx + rad * np.cos(t), cy - rad * np.sin(t), "o", ms=1.3, color="#2b4f9e", zorder=4)

    def P_B(px, py):
        return fig.transFigure.inverted().transform(aB.transData.transform((px, py)))

    ftext(fig, 0.513, 0.875, "Eight-Octant Anatomical Shell")
    ftext(fig, 0.395, 0.82, "Fit\nOctants");      line(fig, (0.41, 0.80), P_B(345, 165))
    ftext(fig, 0.395, 0.715, "Witness\nOctants"); line(fig, (0.42, 0.715), P_B(320, 320))
    ftext(fig, 0.395, 0.63, "Fit Octants");      line(fig, (0.42, 0.635), P_B(440, 440))
    ftext(fig, 0.513, 0.578, "Lesion-Excluded\nCentral Region"); line(fig, (0.513, 0.6), P_B(510, 360))
    ftext(fig, 0.625, 0.86, "Witness\nOctants"); line(fig, (0.607, 0.85), P_B(690, 225))
    ftext(fig, 0.625, 0.735, "Fit Cost\nRanking")
    ftext(fig, 0.625, 0.61, "Witness Cost\nContribution")
    arrow(fig, (0.625, 0.825), (0.625, 0.765))
    arrow(fig, (0.625, 0.705), (0.625, 0.645))

    # ---------------- D. Lesion scoring
    head(fig, 0.67, 0.92, "D. Lesion Scoring")
    sx, y0, hD = 3.3e-4, 0.615, 0.225          # fig-x per art pixel, bottom, height
    xl, gap = 0.672, 0.07
    aDl = fig.add_axes([xl, y0, (268 - 100) * sx, hD])
    xr = xl + (268 - 100) * sx + gap
    aDr = fig.add_axes([xr, y0, (955 - 385) * sx, hD])
    show(aDl, "ov_D_scorer", (100, 85, 268, 520))
    show(aDr, "ov_D_scorer", (385, 85, 955, 520))
    fy = lambda py: y0 + hD * (520 - py) / 435
    fxr = lambda px: xr + (px - 385) * sx
    arrow(fig, (xr - gap, fy(285)), (xr + 0.002, fy(285)), ms=7, lw=0.7)
    gx = xr - gap / 2
    ftext(fig, gx, fy(285) + 0.05, "Lesion\nAppearance\nFeatures", fontsize=FS - 0.6)
    ftext(fig, gx, fy(285) - 0.065, "Soft\nAnatomical-\nFit Penalty\n(witness\ncosts)", fontsize=FS - 0.6)
    ftext(fig, xl + (160 - 100) * sx, fy(95), "Retained\nCandidates", va="bottom")
    ftext(fig, fxr(505), fy(150), "Frozen\nLogistic-Regression\nLesion Scorer", va="bottom")
    ftext(fig, 0.95, fy(185), "Highest-Scoring\nCandidate", va="bottom")
    ftext(fig, 0.95, fy(390), "Predicted Earlier\nLesion Location", va="top")

    # ---------------- C. Candidate selection comparison
    head(fig, 0.01, 0.535, "C. Candidate Selection Comparison")
    aCl = fig.add_axes([0.09, 0.075, 0.195, 0.37])
    aCr = fig.add_axes([0.392, 0.075, 0.195, 0.37])
    top, div, P, tau = panel_c(aCl, aCr)
    for ax in (aCl, aCr):     # fit-cost colour bars, as in the sketch
        bb = ax.get_position()
        cb = fig.add_axes([bb.x1 + 0.007, bb.y0, 0.011, bb.height])
        cb.imshow(np.linspace(1, 0, 100)[:, None], aspect="auto", cmap="Greens", vmin=-0.1, vmax=1.2)
        cb.set_xticks([]); cb.set_yticks([])
        for s_ in cb.spines.values():
            s_.set_color("#444444"); s_.set_linewidth(0.6)
        ax.text(0.5, 0.03, "Same Candidate Budget", transform=ax.transAxes, ha="center",
                va="bottom", fontsize=FS, zorder=8)

    def to_fig(ax, x, y):
        return fig.transFigure.inverted().transform(ax.transData.transform((x, y)))

    ftext(fig, 0.188, 0.468, "Conventional Top-K Selection", fontsize=FS + 0.4)
    ftext(fig, 0.49, 0.475, "Proposed Fit-Ordered Diverse Selection\n(Minimum Distance $r$ = 2.1 mm)",
          fontsize=FS + 0.4)
    # left: clustered / misses
    cl = np.mean(P[top], axis=0)
    ftext(fig, 0.045, 0.31, "Clustered\nCandidates")
    arrow(fig, (0.075, 0.31), to_fig(aCl, cl[0] - 1.6, cl[1]), ms=6, lw=0.6)
    ftext(fig, 0.045, 0.125, "Misses 3\nmm Circle")
    arrow(fig, (0.07, 0.14), to_fig(aCl, -6.4, -5.2), ms=6, lw=0.6)
    aCl.annotate("3 mm\nEvaluation\nCircle", xy=(TRUE[0] + tau * 0.72, TRUE[1] - tau * 0.72),
                 xytext=(TRUE[0] + 3.4, TRUE[1] - 3.4), fontsize=FS, ha="center", va="center",
                 linespacing=1.05, arrowprops=dict(arrowstyle="-", lw=0.5, color=INK))
    # ground truth leaders to both stars
    ftext(fig, 0.341, 0.395, "Ground-Truth\n(Evaluation Only)", fontsize=FS - 0.6)
    for ax, x0 in ((aCl, 0.31), (aCr, 0.372)):
        line(fig, (x0, 0.375), to_fig(ax, *TRUE))
    arrow(fig, (0.31, 0.245), (0.386, 0.245), style="<|-|>", ms=7, lw=0.8)
    ftext(fig, 0.348, 0.285, "Fit Ranking\nUnchanged")
    # right: spread / one inside
    ftext(fig, 0.645, 0.33, "Spatially\nDiverse\nCandidates")
    arrow(fig, (0.62, 0.33), (0.578, 0.33), ms=6, lw=0.6)
    sel = [i for i in div if np.linalg.norm(P[i] - TRUE) <= tau][0]
    ftext(fig, 0.645, 0.15, "One\nCandidate\ninside 3 mm\nCircle")
    sx, sy = to_fig(aCr, *P[sel])
    arrow(fig, (0.623, 0.165), (sx + 0.006, sy - 0.006), ms=6, lw=0.6)

    # ---------------- E. Outcome distinction
    head(fig, 0.697, 0.535, "E. Outcome Distinction")
    aE1 = fig.add_axes([0.70, 0.155, 0.142, 0.255])
    aE2 = fig.add_axes([0.852, 0.155, 0.142, 0.255])
    show(aE1, "ov_E_reachhit", (350, 125, 670, 450))
    show(aE2, "ov_E_reachhit", (688, 125, 1008, 450))
    ftext(fig, 0.771, 0.46, "Reach", fontsize=FS + 3)
    ftext(fig, 0.923, 0.46, "Hit", fontsize=FS + 3)
    T(aE1, 465, 215, "3 mm")
    T(aE2, 800, 215, "3 mm")
    ftext(fig, 0.771, 0.075, "Is any candidate\nwithin 3 mm?")
    ftext(fig, 0.771, 0.032, "YES", fontweight="bold")
    ftext(fig, 0.923, 0.075, "Is the final selected\ncandidate within 3 mm?")
    ftext(fig, 0.923, 0.032, "YES (Hit)", fontweight="bold")
    ftext(fig, 0.79, 0.14, "Reach does not guarantee Hit", fontsize=FS - 0.4, style="italic")
    tx, ty = to_fig(aE1, 405, 399)        # selected (ringed) candidate outside the circle
    arrow(fig, (0.725, 0.148), (tx - 0.002, ty - 0.012), ms=6, lw=0.6)

    fig.savefig(os.path.join(OUT, "overview.pdf"))
    fig.savefig(os.path.join(OUT, "overview.png"), dpi=220)
    plt.close(fig)
    print("wrote figures/overview.pdf; K =", len(top), len(div))


if __name__ == "__main__":
    main()
