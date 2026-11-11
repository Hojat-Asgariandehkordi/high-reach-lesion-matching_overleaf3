"""Supplement figures: paired candidate/scorer effects and held-out status trade-offs."""
import sys, os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
sys.path.insert(0, os.path.dirname(__file__))
import style as S
from supp_data import STATUS, TARGETS, PAIRED, PAIRED_ROWS

S.apply()
OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
COHORT = {"staging": "Staging (independent, n=440)", "screening": "Screening (retrospective, n=309)"}


def fig_paired():
    fig, axes = plt.subplots(1, 2, figsize=(S.PAGE_W * 0.96, 1.55), sharey=True)
    y = np.arange(len(PAIRED_ROWS))[::-1]
    for ax, c in zip(axes, ["staging", "screening"]):
        ax.axvline(0, color=S.INK2, lw=0.7, zorder=1)
        ax.axvline(3, color=S.INK2, lw=0.7, ls=(0, (2, 2)), zorder=1)
        ax.axhspan(y[0] - 0.45, y[0] + 0.45, color="#f3f2ee", lw=0, zorder=0)
        for yi, (est, lo, hi) in zip(y, PAIRED[c]):
            col = S.OURS if lo > 0 else S.MUTED
            ax.errorbar([est], [yi], xerr=[[est - lo], [hi - est]], fmt="o", ms=4.5, color=col,
                        ecolor=col, elinewidth=1.4, capsize=3, capthick=1.4, mec="white", mew=0.6,
                        zorder=3)
            ax.text(28.6, yi, f"{est:+.1f} [{lo:.1f}, {hi:.1f}]", va="center", ha="right",
                    fontsize=6, color=S.INK2)
        ax.set_xlim(-7, 29)
        ax.set_xticks([-5, 0, 5, 10, 15])
        ax.set_title(COHORT[c], loc="left")
        ax.grid(axis="y", visible=False)
        ax.tick_params(axis="y", length=0)
    axes[0].set_yticks(y)
    axes[0].set_yticklabels(PAIRED_ROWS)
    axes[0].set_ylim(-0.6, len(PAIRED_ROWS) - 0.4)
    fig.supxlabel("Paired change in hit rate at 3 mm (points), 95% patient-cluster CI",
                  fontsize=7, color=S.INK2, y=0.03)
    h = [Line2D([], [], color=S.OURS, marker="o", lw=1.4, ms=4, label="Interval above zero"),
         Line2D([], [], color=S.MUTED, marker="o", lw=1.4, ms=4, label="Interval includes zero"),
         Line2D([], [], color=S.INK2, lw=0.7, ls=(0, (2, 2)), label="+3 point margin")]
    fig.legend(handles=h, loc="upper center", ncol=3, bbox_to_anchor=(0.6, 1.08), fontsize=6.5)
    fig.tight_layout(w_pad=1.0)
    fig.savefig(os.path.join(OUT, "paired_effects.pdf"))
    plt.close(fig)


# Status figure: colour = route family, marker/line = candidate cap.
FAMILY = {
    "Original 7": (S.SPLINE, "o", (0, (3, 1.5))),
    "Original 28": (S.SPLINE, "s", "-"),
    "Original 28 + fit": (S.SPLINE, "^", (0, (1, 1))),
    "Wide strict 7": (S.OURS, "o", (0, (3, 1.5))),
    "Wide strict 28": (S.OURS, "s", "-"),
    "Wide relaxed 28": (S.ALT, "D", "-"),
    "Fit comparator": (S.INK2, "v", "-"),
}


def fig_status():
    fig, axes = plt.subplots(2, 3, figsize=(S.PAGE_W * 0.96, 3.6), sharex=True, sharey="row")
    for k in range(3):
        for name, (col, mk, ls) in FAMILY.items():
            d = STATUS[name][str(k)]
            for r, key in enumerate(["offtarget_fv", "shear_fn"]):
                ax = axes[r, k]
                ax.plot(d["recall"], d[key], color=col, ls=ls, lw=1.1, marker=mk,
                        ms=4.2 if mk != "D" else 3.8, mec="white", mew=0.5,
                        alpha=1.0 if name != "Fit comparator" else 0.85, zorder=3)
        axes[0, k].set_title(f"{'ABC'[k]}  {TARGETS[k]}", loc="left")
        axes[1, k].set_xlabel("")
        for r in range(2):
            axes[r, k].set_xlim(25, 102)
            axes[r, k].set_xticks([30, 50, 70, 90])
    axes[0, 0].set_ylim(-3, 80)
    axes[1, 0].set_ylim(-3, 95)
    axes[0, 0].set_ylabel("Off-target false visible (%)")
    axes[1, 0].set_ylabel("Shear false new (%)")
    fig.supxlabel("Achieved incident recall on absent controls (%)", fontsize=7, color=S.INK2,
                  y=0.11)
    h = [Line2D([], [], color=c, marker=m, ls=l, lw=1.1, ms=4, mec="white", label=n)
         for n, (c, m, l) in FAMILY.items()]
    fig.legend(handles=h, loc="lower center", ncol=4, bbox_to_anchor=(0.5, -0.01),
               fontsize=6.5, handlelength=2.4, columnspacing=1.2)
    fig.tight_layout(h_pad=0.8, w_pad=0.6)
    fig.subplots_adjust(bottom=0.17)
    fig.savefig(os.path.join(OUT, "status_achieved.pdf"))
    plt.close(fig)


if __name__ == "__main__":
    fig_paired()
    fig_status()
    print("done")
