"""Teaser and method-overview figures.

The left panels are a 2D *illustration*: a synthetic fit-cost landscape with
two modes, on which we run the real greedy rule (Alg. 1). No patient data.
A real CT slice can replace the gray background
once patches are exported."""
import sys, os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, FancyArrowPatch
sys.path.insert(0, os.path.dirname(__file__))
import style as S
from data import HEADLINE, N

S.apply()
OUT = os.path.join(os.path.dirname(__file__), "..", "figures")

# ---- synthetic landscape on the wide lattice (0.7 mm, +-7 mm) -------------
g = np.round(np.arange(-7, 7.01, 0.7), 2)
XX, YY = np.meshgrid(g, g)
P = np.stack([XX.ravel(), YY.ravel()], 1)
WRONG, TRUE = np.array([-2.1, 1.4]), np.array([2.8, -2.1])
Y_REF = np.array([3.0, -2.4])
rng = np.random.default_rng(3)


def gauss(p, m, s):
    return np.exp(-np.sum((p - m) ** 2, 1) / (2 * s ** 2))


fit = -(1.0 * gauss(P, WRONG, 2.0) + 0.65 * gauss(P, TRUE, 1.3)) + 0.03 * rng.standard_normal(len(P))
order = np.lexsort((np.linalg.norm(P, axis=1), fit))


def diverse(order, r=2.1, K=np.inf):
    kept = []
    for i in order:
        if all(np.linalg.norm(P[i] - P[j]) >= r for j in kept):
            kept.append(i)
            if len(kept) >= K:
                break
    return kept


def landscape(ax, alpha=1.0):
    gg = np.linspace(-7.6, 7.6, 200)
    GX, GY = np.meshgrid(gg, gg)
    Q = np.stack([GX.ravel(), GY.ravel()], 1)
    F = -(1.0 * gauss(Q, WRONG, 2.0) + 0.65 * gauss(Q, TRUE, 1.3))
    ax.contourf(GX, GY, F.reshape(GX.shape), levels=9, cmap="Greys_r", alpha=0.32 * alpha)
    ax.set_xlim(-7.6, 7.6); ax.set_ylim(-7.6, 7.6)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(True); s.set_color(S.MUTED); s.set_linewidth(0.6)


def truth(ax, tau=3.0):
    ax.add_patch(Circle(Y_REF, tau, fill=False, ls=(0, (2, 1.5)), lw=0.9, color=S.SPLINE))
    ax.plot(*Y_REF, marker="*", ms=8, color=S.SPLINE, mec="white", mew=0.5, zorder=6)


BR = os.path.join(OUT, "biorender")


def biorender(name, crop):
    """Load BioRender art (high-res PNG export preferred, JPEG preview as fallback).
    crop = (left, top, right, bottom) as fractions of the image size."""
    from PIL import Image
    for ext in ("png", "jpg"):
        f = os.path.join(BR, f"{name}.{ext}")
        if os.path.exists(f):
            im = Image.open(f).convert("RGB")
            w, h = im.size
            l, t, r, b = crop
            return np.asarray(im.crop((int(l * w), int(t * h), int(r * w), int(b * h))))
    return None


def chest(ax, cx, lesion, title, query=None, window=None):
    from matplotlib.patches import Ellipse, Rectangle
    ax.add_patch(Ellipse((cx, 0), 8.6, 6.2, color="#c9c7c0", lw=0))
    ax.add_patch(Ellipse((cx - 2.0, 0.25), 3.1, 4.3, color="#3b3a37", lw=0))
    ax.add_patch(Ellipse((cx + 2.0, 0.25), 3.1, 4.3, color="#3b3a37", lw=0))
    ax.add_patch(Circle((cx, -2.35), 0.55, color="#f4f3ef", lw=0))
    ax.add_patch(Ellipse((cx + 0.35, 0.0), 1.3, 1.9, color="#a9a7a0", lw=0))
    ax.add_patch(Circle(lesion, 0.32, color="#efeee9", lw=0))
    ax.text(cx, 3.55, title, ha="center", fontsize=6.5, color=S.INK)
    if query is not None:
        ax.annotate("query $p$", xy=(query[0] + 0.3, query[1] + 0.25), xytext=(query[0] + 0.9, query[1] + 1.6),
                    fontsize=6, color="#8a7300", ha="left",
                    arrowprops=dict(arrowstyle="-|>", color="#ffd400", lw=1.0, mutation_scale=6))
    if window is not None:
        (wx, wy), w = window
        ax.add_patch(Rectangle((wx - w / 2, wy - w / 2), w, w, fill=False, ec="#ffd400",
                               lw=0.9, ls=(0, (2, 1.5)), zorder=5))


def teaser_drawn_a(ax):
    ax.set_xlim(-4.5, 15.3); ax.set_ylim(-4.0, 4.1); ax.set_aspect("equal")
    ax.axis("off")
    chest(ax, 0, (-2.6, 1.0), "Current CT", query=(-2.6, 1.0))
    chest(ax, 10.8, (10.8 - 2.25, 0.7), "Earlier CT, aligned",
          window=((10.8 - 2.6, 1.0), 2.4))
    ax.add_patch(FancyArrowPatch((4.6, 0.3), (6.2, 0.3), arrowstyle="-|>", mutation_scale=9,
                                 color=S.INK2, lw=0.9))
    ax.text(5.4, 0.75, "same\nframe", ha="center", fontsize=5.8, color=S.INK2)
    ax.text(10.8, -3.6, "zoomed in (b, c)", ha="center", fontsize=6, color="#b39400")
    ax.set_title("(a) Find the same lesion earlier", loc="left")


def teaser():
    K = 12
    fitonly = order[:K]
    div = diverse(order, K=K)
    fig = plt.figure(figsize=(S.COL_W, 1.12))
    gs = fig.add_gridspec(1, 3, width_ratios=[2.3, 1, 1], wspace=0.07,
                          left=0.005, right=0.995, top=0.86, bottom=0.13)
    # (a) the problem; (b), (c) the search window zoomed, all in one row
    ax = fig.add_subplot(gs[0])
    art = biorender("problem_notext", (0, 0.08, 1, 0.86))
    if art is not None:
        H, W = art.shape[:2]
        sx, sy = W / 1024.0, H / (572 * 0.78)          # preview pixel -> crop pixel
        y0 = 572 * 0.08
        Q = lambda x, y: (x * sx, (y - y0) * sy)
        ax.imshow(art, interpolation="lanczos")
        ax.axis("off")
        ax.set_title("(a) Task", loc="left", fontsize=6.5, pad=2)
        import matplotlib.patheffects as pe
        halo = [pe.withStroke(linewidth=1.8, foreground="black")]
        ax.text(*Q(218, 72), "Current CT", ha="center", va="center", fontsize=5.6, color=S.INK)
        ax.text(*Q(806, 72), "Earlier CT", ha="center", va="center", fontsize=5.6, color=S.INK)
        ax.text(*Q(102, 330), "query $p$", ha="center", va="top", fontsize=5.4, color="#ffe14a", path_effects=halo)
        ax.text(*Q(712, 418), "lesion", ha="center", va="top", fontsize=5.4,
                color="#ffa04d", path_effects=halo)
    else:
        teaser_drawn_a(ax)
    # (b) and (c): the search window, zoomed
    for k, (idx, title) in enumerate([(fitonly, f"(b) Top {K} by fit"),
                                      (div, f"(c) Diversified")]):
        ax = fig.add_subplot(gs[k + 1])
        landscape(ax)
        for sp in ax.spines.values():
            sp.set_color("#ffd400"); sp.set_linestyle((0, (2, 1.5))); sp.set_linewidth(0.9)
        if k == 1:
            for i in idx:
                ax.add_patch(Circle(P[i], 2.1 / 2, color=S.OURS, alpha=0.12, lw=0))
        ax.scatter(P[idx, 0], P[idx, 1], s=5, color=S.OURS if k else S.INK2,
                   edgecolor="white", linewidth=0.5, zorder=5)
        truth(ax)
        hit = [i for i in idx if np.linalg.norm(P[i] - Y_REF) <= 3.0]
        msg = "misses lesion" if not hit else "covers lesion"
        ax.text(0.5, -0.05, msg, transform=ax.transAxes, ha="center", va="top", fontsize=5.4,
                color=S.SPLINE if not hit else S.OURS, fontweight="bold")
        ax.set_title(title, loc="left", fontsize=6.5, pad=2)
    fig.savefig(os.path.join(OUT, "teaser.pdf"))
    plt.close(fig)
    return fitonly, div


def method():
    top, bot = 0.12, 0.70
    art = biorender("pipeline_notext", (0, top, 1, bot))
    if art is None:
        return method_drawn()
    h, w = art.shape[:2]
    sx, sy = w / 1024.0, h / (572 * (bot - top))
    Q = lambda x, y: (x * sx, (y - 572 * top) * sy)
    fig = plt.figure(figsize=(S.PAGE_W, S.PAGE_W * h / w + 0.32))
    ax = fig.add_axes([0, 0.32 / (S.PAGE_W * h / w + 0.32), 1, 1 - 0.32 / (S.PAGE_W * h / w + 0.32)])
    ax.imshow(art, interpolation="lanczos")
    ax.axis("off")
    ax.text(*Q(80, 92), "current", ha="center", va="center", fontsize=7, color=S.INK)
    ax.text(*Q(225, 92), "earlier", ha="center", va="center", fontsize=7, color=S.INK)
    from matplotlib.patches import Rectangle
    for k, (lab, col) in enumerate((("fit", "#83a1df"), ("witness", "#81c9c5"))):
        x, y = Q(255, 196 + 26 * k)
        ax.add_patch(Rectangle((x, y - 9 * sy), 14 * sx, 14 * sy, color=col, lw=0))
        ax.text(x + 20 * sx, y - 2 * sy, lab, ha="left", va="center", fontsize=6.8, color=S.INK)
    ax.text(*Q(683, 286), "$r$", ha="center", va="bottom", fontsize=8, color=S.INK)
    ax.text(*Q(958, 262), "reference", ha="left", va="center", fontsize=6.4, color="#c0571c")
    labels = [(0.15, "1  Align, crop, fit/witness shell"), (0.42, "2  Rank shifts by fit $f_t$"),
              (0.665, "3  Keep if $\\geq r$ from kept"), (0.895, "4  Scorer selects $\\hat{t}$")]
    for x, t in labels:
        fig.text(x, 0.02, t, ha="center", va="bottom", fontsize=7.2, fontweight="bold", color=S.INK)
    fig.savefig(os.path.join(OUT, "method_overview.pdf"), dpi=600)
    plt.close(fig)


def method_drawn():
    fig, axes = plt.subplots(1, 4, figsize=(S.PAGE_W, 1.95))
    plt.subplots_adjust(wspace=0.32)
    # (1) shared frame: shell with alternating fit / witness octants
    ax = axes[0]
    ax.set_xlim(-10, 10); ax.set_ylim(-10, 10); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(True); s.set_color(S.MUTED); s.set_linewidth(0.6)
    for k in range(8):
        col = S.OURS if k % 2 == 0 else S.ALT
        ax.add_patch(Wedge((0, 0), 8.4, 45 * k, 45 * (k + 1), width=1.6, color=col,
                           alpha=0.55 if k % 2 == 0 else 0.35, lw=0))
    ax.add_patch(Circle((0, 0), 2.1, color=S.INK2, alpha=0.35, lw=0))
    ax.plot(0, 0, marker="+", ms=7, mew=1.2, color=S.INK)
    ax.text(0, -3.4, "query $p$", ha="center", fontsize=6, color=S.INK)
    ax.text(-9.4, -9.4, "fit", fontsize=6, color=S.OURS, fontweight="bold")
    ax.text(-6.6, -9.4, "witness", fontsize=6, color="#0f7d57", fontweight="bold")
    ax.set_title("1  Shared frame", loc="left")
    ax.text(0.5, -0.07, "outer shell: fit / witness octants", transform=ax.transAxes,
            ha="center", va="top", fontsize=6, color=S.INK2)

    # (2) fit order
    ax = axes[1]
    landscape(ax, alpha=0.6)
    rank = np.empty(len(P)); rank[order] = np.arange(len(P))
    sc = ax.scatter(P[:, 0], P[:, 1], c=rank, cmap="Blues_r", s=4, vmin=0, vmax=len(P) * 0.6,
                    lw=0, zorder=3)
    ax.set_title("2  Rank by fit $f_t$", loc="left")
    ax.text(0.5, -0.07, "darker = better anatomical fit", transform=ax.transAxes,
            ha="center", va="top", fontsize=6, color=S.INK2)

    # (3) diversification
    ax = axes[2]
    landscape(ax, alpha=0.6)
    kept = diverse(order)
    ax.scatter(P[:, 0], P[:, 1], s=2, color=S.MUTED, alpha=0.35, lw=0, zorder=2)
    for i in kept:
        ax.add_patch(Circle(P[i], 2.1 / 2, color=S.OURS, alpha=0.10, lw=0))
    ax.scatter(P[kept, 0], P[kept, 1], s=7, color=S.OURS, edgecolor="white", lw=0.4, zorder=4)
    ax.set_title("3  Diversify ($r$)", loc="left")
    ax.text(0.5, -0.07, "kept if $\\geq r$ from all kept", transform=ax.transAxes,
            ha="center", va="top", fontsize=6, color=S.INK2)

    # (4) scoring
    ax = axes[3]
    landscape(ax, alpha=0.6)
    lesion = gauss(P[kept], Y_REF + np.array([0.2, 0.3]), 1.2)
    score = lesion - 0.25 * (fit[kept] - fit[kept].min())
    sel = kept[int(np.argmax(score))]
    ax.scatter(P[kept, 0], P[kept, 1], s=4 + 40 * (score - score.min()) / np.ptp(score),
               color=S.OURS, alpha=0.75, edgecolor="white", lw=0.4, zorder=4)
    truth(ax)
    ax.add_patch(Circle(P[sel], 0.75, fill=False, color=S.INK, lw=1.1, zorder=7))
    ax.set_title("4  Score, select $\\hat{t}$", loc="left")
    ax.text(0.5, -0.07, "size = score $s(t)$; star = reference", transform=ax.transAxes,
            ha="center", va="top", fontsize=6, color=S.INK2)

    for k in range(3):
        a0 = axes[k].get_position(); a1 = axes[k + 1].get_position()
        fig.add_artist(FancyArrowPatch((a0.x1 + 0.004, (a0.y0 + a0.y1) / 2),
                                       (a1.x0 - 0.004, (a1.y0 + a1.y1) / 2),
                                       transform=fig.transFigure, arrowstyle="-|>",
                                       mutation_scale=8, color=S.INK2, lw=0.8))
    fig.savefig(os.path.join(OUT, "method_overview.pdf"))
    plt.close(fig)


if __name__ == "__main__":
    f, d = teaser()
    print("fit-only min dist to ref:", min(np.linalg.norm(P[i] - Y_REF) for i in f))
    print("diverse min dist to ref:", min(np.linalg.norm(P[i] - Y_REF) for i in d))
    method()
    print("kept total:", len(diverse(order)))
