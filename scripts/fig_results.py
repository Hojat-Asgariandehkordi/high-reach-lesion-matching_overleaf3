"""Results figures: budget sweep, reach/selection decomposition, accuracy vs latency."""
import sys, os
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(__file__))
import style as S
from data import N, BUDGETS, SWEEP, DECOMP, SPEED, FOREST, BAND, BANDS, DECOMP_CI

S.apply()
OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
TITLES = {"staging": "Staging", "screening": "Screening"}


def pct(v, cohort):
    return 100.0 * np.asarray(v) / N[cohort]


def fig_budget():
    fig, axes = plt.subplots(1, 2, figsize=(S.COL_W, 2.2), sharey=True)
    x = np.arange(len(BUDGETS))
    for ax, c in zip(axes, ["staging", "screening"]):
        d = SWEEP[c]
        ax.axhline(pct(d["spline"], c), color=S.SPLINE, lw=1.0, ls=(0, (1, 1.5)), zorder=1)
        ax.plot(x, pct(d["ungated_reach"], c), color=S.OURS, lw=1.6, ls="--", zorder=2)
        ax.text(5.1, pct(d["ungated_reach"][-1], c) + 1.5, "reach", fontsize=6, color=S.OURS, ha="right", va="bottom")
        ax.text(5.1, pct(d["ungated_hits"][-1], c) - 2.0, "hits", fontsize=6, color=S.OURS, ha="right", va="top")
        ax.plot(x, pct(d["ungated_hits"], c), color=S.OURS, marker="o", ms=4.2, lw=1.8, zorder=3,
                mec="white", mew=0.6)
        ax.plot(x, pct(d["strict_hits"], c), color=S.ALT, marker="s", ms=3.8, lw=1.6, zorder=3,
                mec="white", mew=0.6)
        # fit-only prefix at 28 and exhaustive (raw lattice)
        ax.plot([2], [pct(d["fitonly28"][0], c)], marker="D", ms=5.5, color=S.INK, ls="none",
                mec="white", mew=0.6, zorder=4)
        ax.plot([6], [pct(d["exhaustive"][0], c)], marker="^", ms=6, color=S.INK,
                ls="none", mec="white", mew=0.6, zorder=4)
        ax.set_xticks(list(x) + [6])
        ax.set_xticklabels(BUDGETS + ["Exh."])
        ax.set_xlim(-0.3, 6.3)
        ax.set_ylim(40, 100)
        ax.set_title(TITLES[c], loc="left")
        ax.set_xlabel("Candidate budget $K$")
        ax.grid(axis="x", visible=False)
    axes[0].set_ylabel("Lesions within 3 mm (%)")
    from matplotlib.lines import Line2D
    h = [Line2D([], [], color=S.OURS, marker="o", ms=3, label="Diverse $K$: hits"),
         Line2D([], [], color=S.OURS, ls="--", label="Diverse $K$: reach"),
         Line2D([], [], color=S.ALT, marker="s", ms=3, label="Gated $K$: hits"),
         Line2D([], [], color=S.INK, marker="D", ls="none", ms=4.5, label="Fit-only 28"),
         Line2D([], [], color=S.INK, marker="^", ls="none", ms=4.5, label="Exhaustive"),
         Line2D([], [], color=S.SPLINE, ls=(0, (1, 1.5)), lw=1, label="B-spline: hits")]
    fig.legend(handles=h, loc="lower center", ncol=3, bbox_to_anchor=(0.5, 0.0),
               handlelength=1.8, columnspacing=0.9)
    fig.tight_layout(w_pad=0.6)
    fig.subplots_adjust(bottom=0.36)
    fig.savefig(os.path.join(OUT, "budget_reach.pdf"))
    plt.close(fig)


def fig_decomp():
    fig, axes = plt.subplots(1, 2, figsize=(S.COL_W, 1.6), sharey=True)
    for ax, c in zip(axes, ["staging", "screening"]):
        rows = DECOMP[c]
        y = np.arange(len(rows))[::-1]
        h = 0.3
        for k, (yi, (lab, reach, sel)) in enumerate(zip(y, rows)):
            rp, sp = 100 * reach / N[c], 100 * sel / N[c]
            ax.barh(yi + h / 2 + 0.03, rp, height=h, color=S.OURS, edgecolor="none")
            ax.barh(yi - h / 2 - 0.03, sp, height=h, color=S.MUTED, edgecolor="none",
                    hatch="//////", lw=0)
            net = rp + sp
            lo, hi = DECOMP_CI[c][k]
            ax.errorbar([net], [yi], xerr=[[net - lo], [hi - net]], fmt="D", ms=4.2,
                        color=S.INK, ecolor=S.INK, elinewidth=1.1, capsize=2.6, capthick=1.1,
                        mec="white", mew=0.6, zorder=5)
        ax.axvline(0, color=S.INK2, lw=0.6)
        ax.set_yticks(y)
        ax.set_yticklabels([r[0] for r in rows])
        ax.set_xlim(-8, 17)
        ax.set_xticks([-5, 0, 5, 10, 15])
        ax.set_title(TITLES[c], loc="left")
        ax.grid(axis="y", visible=False)
        ax.tick_params(axis="y", length=0)
    import matplotlib.patches as mp
    from matplotlib.lines import Line2D
    hd = [mp.Patch(color=S.OURS, label="Reach component"),
          mp.Patch(facecolor=S.MUTED, hatch="//////", edgecolor="white", label="Selection component"),
          Line2D([], [], marker="D", color=S.INK, ls="-", lw=1.1, ms=3.5, label="Net, 95% CI")]
    fig.legend(handles=hd, loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.02),
               handlelength=1.4, columnspacing=0.8)
    fig.supxlabel("Change in hit rate at 3 mm (points)", fontsize=7, color=S.INK2, y=0.15)
    fig.tight_layout(w_pad=0.5)
    fig.subplots_adjust(bottom=0.33)
    fig.savefig(os.path.join(OUT, "reach_selection.pdf"))
    plt.close(fig)


def fig_forest():
    labels = list(FOREST["staging"].keys())
    n_sp = 5
    rows, ypos, yy = [], [], 0.0
    for i, lab in enumerate(labels):
        if i == 0:
            rows.append(("Diverse search vs. B-spline", yy, True)); yy += 1
        if i == n_sp:
            yy += 0.3
            rows.append(("Changes to the candidate list", yy, True)); yy += 1
        rows.append(("  " + lab.replace("vs spline, ", ""), yy, False))
        ypos.append(yy); yy += 1
    ypos = -np.array(ypos)
    fig, ax = plt.subplots(figsize=(S.COL_W, 2.85))
    ax.axvline(0, color=S.INK2, lw=0.7, zorder=1)
    ax.axvline(3, color=S.INK2, lw=0.7, ls=(0, (2, 2)), zorder=1)
    style = {"staging": (S.OURS, "o", 0.17), "screening": (S.ALT, "s", -0.17)}
    for c in ["staging", "screening"]:
        col, mk, off = style[c]
        for i, lab in enumerate(labels):
            v = FOREST[c][lab]
            if v is None:
                continue
            est, lo, hi = v
            ax.errorbar([est], [ypos[i] + off], xerr=[[est - lo], [hi - est]], fmt=mk, ms=3.6,
                        color=col, ecolor=col, elinewidth=1.2, capsize=2.2, capthick=1.2,
                        mec="white", mew=0.4, zorder=3)
    ax.set_yticks([-r[1] for r in rows])
    ax.set_yticklabels([r[0] for r in rows])
    for t, r in zip(ax.get_yticklabels(), rows):
        if r[2]:
            t.set_fontweight("bold"); t.set_color(S.INK)
    ax.set_ylim(ypos[-1] - 0.7, 0.6)
    ax.set_xlim(-7, 23)
    ax.set_xticks([0, 5, 10, 15, 20])
    ax.set_xlabel("Paired difference in hit rate (points), 95% CI")
    ax.grid(axis="y", visible=False)
    ax.tick_params(axis="y", length=0)
    from matplotlib.lines import Line2D
    h = [Line2D([], [], color=S.OURS, marker="o", ms=3.5, lw=1.2, label="Staging"),
         Line2D([], [], color=S.ALT, marker="s", ms=3.5, lw=1.2, label="Screening"),
         Line2D([], [], color=S.INK2, ls=(0, (2, 2)), lw=0.7, label="+3 pt margin")]
    ax.legend(handles=h, loc="lower center", bbox_to_anchor=(0.42, 1.0), ncol=3, fontsize=6,
              handlelength=1.6, columnspacing=1.0)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "paired_forest.pdf"))
    plt.close(fig)


def fig_bands():
    fig, axes = plt.subplots(1, 2, figsize=(S.COL_W, 1.55), sharey=True)
    y = np.arange(3)[::-1]
    for ax, c in zip(axes, ["staging", "screening"]):
        ax.axvline(0, color=S.INK2, lw=0.7)
        for yi, (est, lo, hi), n in zip(y, BAND[c]["d"], BAND[c]["n"]):
            ax.errorbar([est], [yi], xerr=[[est - lo], [hi - est]], fmt="o", ms=4,
                        color=S.OURS, ecolor=S.INK, elinewidth=1.1, capsize=2.6,
                        capthick=1.1, mec="white", mew=0.5, zorder=3)
            ax.text(est, yi + 0.3, f"n={n}", fontsize=5.6, color=S.INK2, va="bottom", ha="center")
        ax.set_xlim(-16, 37)
        ax.set_xticks([-10, 0, 10, 20, 30])
        ax.set_title(TITLES[c], loc="left")
        ax.grid(axis="y", visible=False)
        ax.tick_params(axis="y", length=0)
    axes[0].set_yticks(y)
    axes[0].set_yticklabels(BANDS)
    axes[0].set_ylabel("Query error")
    axes[0].set_ylim(-0.5, 2.85)
    fig.supxlabel("Diverse search \u2212 B-spline at 3 mm (points), 95% CI", fontsize=7, color=S.INK2, y=0.02)
    fig.tight_layout(w_pad=0.5)
    fig.savefig(os.path.join(OUT, "query_bands.pdf"))
    plt.close(fig)


def fig_speed():
    fig, axes = plt.subplots(1, 2, figsize=(S.COL_W, 1.9), sharey=True)
    for ax, c in zip(axes, ["staging", "screening"]):
        d = SPEED[c]
        div = [r for r in d["routes"] if r[0] in ("28", "56", "112", "All")]
        ax.plot([r[1] for r in div], pct([r[2] for r in div], c), color=S.OURS, marker="o",
                ms=4.5, lw=1.8, mec="white", mew=0.6, zorder=3)
        offs = {"28": (4, -10), "112": (-8, 5), "All": (0, 5)}
        for lab, t, h in div:
            if lab not in offs:
                continue
            ax.annotate("K=" + lab if lab != "All" else "all", (t, 100 * h / N[c]),
                        textcoords="offset points", xytext=offs[lab], ha="center",
                        fontsize=5.8, color=S.OURS)
        for lab, mk, off in (("Fit-only 28", "D", (14, -10)), ("Exhaustive", "^", (0, 5))):
            r = [r for r in d["routes"] if r[0] == lab][0]
            ax.plot([r[1]], [100 * r[2] / N[c]], marker=mk, ms=5.5, color=S.INK, ls="none",
                    mec="white", mew=0.6, zorder=4)
            ax.annotate(lab,
                        (r[1], 100 * r[2] / N[c]), textcoords="offset points", xytext=off,
                        ha="center", fontsize=5.8, color=S.INK)
        ax.set_xlim(0.07, 0.30)
        ax.set_xticks([0.1, 0.15, 0.2, 0.25, 0.3])
        ax.set_ylim(35, 92)
        ax.set_title(TITLES[c], loc="left")
    axes[0].set_ylabel("Hits within 3 mm (%)")
    fig.supxlabel("Median local time per query (s)", fontsize=7, color=S.INK2, y=0.02)
    fig.tight_layout(w_pad=0.6)
    fig.savefig(os.path.join(OUT, "accuracy_latency.pdf"))
    plt.close(fig)


if __name__ == "__main__":
    fig_budget()
    fig_decomp()
    fig_speed()
    fig_forest()
    fig_bands()
    print("done")
