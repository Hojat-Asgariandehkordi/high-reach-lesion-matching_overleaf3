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


def teaser():
    K = 12
    fitonly = order[:K]
    div = diverse(order, K=K)
    fig = plt.figure(figsize=(S.PAGE_W, 2.05))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1.45], wspace=0.25)
    for k, (idx, title) in enumerate([(fitonly, f"Top {K} by fit"),
                                      (div, f"Top {K}, diversified")]):
        ax = fig.add_subplot(gs[k])
        landscape(ax)
        if k == 1:
            for i in idx:
                ax.add_patch(Circle(P[i], 2.1 / 2, color=S.OURS, alpha=0.12, lw=0))
        ax.scatter(P[idx, 0], P[idx, 1], s=14, color=S.OURS if k else S.INK2,
                   edgecolor="white", linewidth=0.5, zorder=5)
        truth(ax)
        hit = [i for i in idx if np.linalg.norm(P[i] - Y_REF) <= 3.0]
        msg = "no candidate within 3 mm" if not hit else f"{len(hit)} candidates within 3 mm"
        ax.text(0.5, -0.07, msg, transform=ax.transAxes, ha="center", va="top", fontsize=6.5,
                color=S.SPLINE if not hit else S.OURS, fontweight="bold")
        ax.set_title(("(a) " if k == 0 else "(b) ") + title, loc="left")
    # (c) results
    ax = fig.add_subplot(gs[2])
    names = ["B-spline", "Fit-only 28", "Diverse 28", "Diverse search"]
    cols = [S.SPLINE, S.MUTED, S.OURS, S.OURS]
    hatches = ["", "", "//////", ""]
    w = 0.19
    for gi, c in enumerate(["staging", "screening"]):
        for j, n in enumerate(names):
            v = 100 * HEADLINE[c][n] / N[c]
            x = gi + (j - 1.5) * (w + 0.02)
            ax.bar(x, v, width=w, color=cols[j] if not hatches[j] else "white",
                   edgecolor=cols[j], hatch=hatches[j], lw=0.8 if hatches[j] else 0)
            ax.text(x, v + 1.2, f"{v:.0f}", ha="center", fontsize=5.8, color=S.INK2)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Staging (n=440)", "Screening (n=309)"])
    ax.set_ylim(0, 108)
    ax.set_yticks([0, 20, 40, 60, 80])
    ax.set_ylabel("%")
    ax.grid(axis="x", visible=False)
    ax.set_title("(c) Hits within 3 mm, same scorer", loc="left")
    import matplotlib.patches as mp
    hd = [mp.Patch(facecolor=cols[j] if not hatches[j] else "white", edgecolor=cols[j],
                   hatch=hatches[j], label=names[j]) for j in range(4)]
    ax.legend(handles=hd, loc="upper left", ncol=2, fontsize=5.8, handlelength=1.2,
              columnspacing=0.7, bbox_to_anchor=(0.0, 1.03))
    fig.savefig(os.path.join(OUT, "teaser.pdf"))
    plt.close(fig)
    return fitonly, div


def method():
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
