"""Results figures: budget sweep, reach/selection decomposition, accuracy vs latency."""
import sys, os
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(__file__))
import style as S
from data import N, BUDGETS, SWEEP, DECOMP, SPEED

S.apply()
OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
TITLES = {"staging": "Staging", "screening": "Screening"}


def pct(v, cohort):
    return 100.0 * np.asarray(v) / N[cohort]


def fig_budget():
    fig, axes = plt.subplots(1, 2, figsize=(S.COL_W, 1.95), sharey=True)
    x = np.arange(len(BUDGETS))
    for ax, c in zip(axes, ["staging", "screening"]):
        d = SWEEP[c]
        ax.axhline(pct(d["spline"], c), color=S.SPLINE, lw=1.0, ls=(0, (1, 1.5)), zorder=1)
        ax.plot(x, pct(d["ungated_reach"], c), color=S.OURS, lw=1.2, ls="--", zorder=2)
        ax.plot(x, pct(d["ungated_hits"], c), color=S.OURS, marker="o", ms=3.2, zorder=3,
                mec="white", mew=0.6)
        ax.plot(x, pct(d["strict_hits"], c), color=S.ALT, marker="s", ms=3.0, zorder=3,
                mec="white", mew=0.6)
        # fit-only prefix at 28 and exhaustive (raw lattice)
        ax.plot([2], [pct(d["fitonly28"][0], c)], marker="D", ms=4, color=S.INK2, ls="none",
                mec="white", mew=0.6, zorder=4)
        ax.plot([6], [pct(d["exhaustive"][0], c)], marker="^", ms=4.2, color=S.INK2,
                ls="none", mec="white", mew=0.6, zorder=4)
        ax.set_xticks(list(x) + [6])
        ax.set_xticklabels(BUDGETS + ["Exh."])
        ax.set_xlim(-0.3, 6.3)
        ax.set_ylim(40, 100)
        ax.set_title(TITLES[c], loc="left")
        ax.set_xlabel("Candidate budget $K$")
        ax.grid(axis="x", visible=False)
    axes[0].set_ylabel("Tracks within 3 mm (%)")
    from matplotlib.lines import Line2D
    h = [Line2D([], [], color=S.OURS, marker="o", ms=3, label="Diverse, no gates: hits"),
         Line2D([], [], color=S.OURS, ls="--", label="Diverse, no gates: reach"),
         Line2D([], [], color=S.ALT, marker="s", ms=3, label="Wide strict: hits"),
         Line2D([], [], color=S.INK2, marker="D", ls="none", ms=3.5, label="Fit-only 28"),
         Line2D([], [], color=S.INK2, marker="^", ls="none", ms=3.5, label="Exhaustive"),
         Line2D([], [], color=S.SPLINE, ls=(0, (1, 1.5)), lw=1, label="B-spline hits")]
    fig.legend(handles=h, loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.06),
               handlelength=1.8, columnspacing=0.9)
    fig.tight_layout(w_pad=0.6)
    fig.subplots_adjust(bottom=0.36)
    fig.savefig(os.path.join(OUT, "budget_reach.pdf"))
    plt.close(fig)


def fig_decomp():
    fig, axes = plt.subplots(1, 2, figsize=(S.COL_W, 1.45), sharey=True)
    for ax, c in zip(axes, ["staging", "screening"]):
        rows = DECOMP[c]
        y = np.arange(len(rows))[::-1]
        h = 0.32
        for yi, (lab, reach, sel) in zip(y, rows):
            ax.barh(yi + h / 2 + 0.02, reach, height=h, color=S.OURS, edgecolor="none")
            ax.barh(yi - h / 2 - 0.02, sel, height=h, color=S.MUTED, edgecolor="none",
                    hatch="//////", lw=0)
            net = reach + sel
            ax.plot([net], [yi], marker="D", ms=4.2, color=S.INK, mec="white", mew=0.6, zorder=5)
            ax.text(max(reach, net, 0) + 4, yi, f"{net:+d}", va="center", fontsize=6.5,
                    color=S.INK, fontweight="bold")
        ax.axvline(0, color=S.INK2, lw=0.6)
        ax.set_yticks(y)
        ax.set_yticklabels([r[0] for r in rows])
        ax.set_xlim(-22, 58)
        ax.set_xticks([-20, 0, 20, 40])
        ax.set_title(TITLES[c], loc="left")
        ax.set_xlabel("Change in hits")
        ax.grid(axis="y", visible=False)
        ax.tick_params(axis="y", length=0)
    import matplotlib.patches as mp
    from matplotlib.lines import Line2D
    hd = [mp.Patch(color=S.OURS, label="Reach (new minus lost targets hit)"),
          mp.Patch(facecolor=S.MUTED, hatch="//////", edgecolor="white", label="Selection (shared targets)"),
          Line2D([], [], marker="D", color=S.INK, ls="none", ms=3.5, label="Net")]
    fig.legend(handles=hd, loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.1),
               handlelength=1.2, columnspacing=0.8)
    fig.tight_layout(w_pad=0.5)
    fig.subplots_adjust(bottom=0.36)
    fig.savefig(os.path.join(OUT, "reach_selection.pdf"))
    plt.close(fig)


def fig_speed():
    fig, axes = plt.subplots(1, 2, figsize=(S.COL_W, 1.75), sharey=True)
    for ax, c in zip(axes, ["staging", "screening"]):
        d = SPEED[c]
        div = [r for r in d["routes"] if r[0] in ("28", "56", "112", "All")]
        ax.plot([r[1] for r in div], pct([r[2] for r in div], c), color=S.OURS, marker="o",
                ms=3.2, mec="white", mew=0.6, zorder=3)
        for lab, t, h in div:
            if lab not in ("28", "All"):
                continue
            ax.annotate(lab, (t, 100 * h / N[c]), textcoords="offset points", xytext=(-4, 2),
                        ha="right", fontsize=5.8, color=S.INK2)
        for lab, mk in (("Fit-only 28", "D"), ("Exhaustive", "^")):
            r = [r for r in d["routes"] if r[0] == lab][0]
            ax.plot([r[1]], [100 * r[2] / N[c]], marker=mk, ms=4, color=S.INK2, ls="none",
                    mec="white", mew=0.6, zorder=4)
        st, sh = d["spline"]
        ax.plot([st], [100 * sh / N[c]], marker="o", ms=4.5, color=S.SPLINE, ls="none",
                mec="white", mew=0.6, zorder=4)
        ax.set_xscale("log")
        ax.set_xlim(0.07, 6)
        ax.set_xticks([0.1, 0.3, 1, 3])
        ax.set_xticklabels(["0.1", "0.3", "1", "3"])
        ax.minorticks_off()
        ax.set_ylim(35, 90)
        ax.set_title(TITLES[c], loc="left")
        ax.set_xlabel("Median local time (s, log)")
    axes[0].set_ylabel("Hits within 3 mm (%)")
    from matplotlib.lines import Line2D
    h = [Line2D([], [], color=S.OURS, marker="o", ms=3, label="Diverse search, cap $K$"),
         Line2D([], [], color=S.INK2, marker="D", ls="none", ms=3.5, label="Fit-only 28"),
         Line2D([], [], color=S.INK2, marker="^", ls="none", ms=3.5, label="Exhaustive"),
         Line2D([], [], color=S.SPLINE, marker="o", ls="none", ms=3.5, label="B-spline")]
    fig.legend(handles=h, loc="lower center", ncol=4, bbox_to_anchor=(0.5, -0.06),
               handlelength=1.4, columnspacing=0.8)
    fig.tight_layout(w_pad=0.6)
    fig.subplots_adjust(bottom=0.3)
    fig.savefig(os.path.join(OUT, "accuracy_latency.pdf"))
    plt.close(fig)


if __name__ == "__main__":
    fig_budget()
    fig_decomp()
    fig_speed()
    print("done")
