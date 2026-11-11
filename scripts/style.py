"""Shared figure style for the paper (CVPR column = 3.25 in, page = 6.875 in)."""
import matplotlib as mpl

COL_W = 3.25
PAGE_W = 6.875

# Validated categorical slots 1-3 (all-pairs safe) + neutrals
OURS = "#2a78d6"      # Diverse search
SPLINE = "#eb6834"    # B-spline baseline
ALT = "#1baf7a"       # strict / alternative route
SAMC = "#6250d6"      # SAM (only appears in bar charts, never next to ALT)
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#8a8985"
GRID = "#e4e3df"
SURF = "#fcfcfb"


def apply():
    mpl.rcParams.update({
        "font.family": "serif",
        # Times New Roman if installed; otherwise metric-compatible Times clones
        "font.serif": ["Times New Roman", "TeX Gyre Termes", "Liberation Serif", "Nimbus Roman", "Times"],
        "mathtext.fontset": "stix",
        "font.size": 7,
        "axes.titlesize": 7.5,
        "axes.titleweight": "bold",
        "axes.labelsize": 7,
        "axes.labelcolor": INK2,
        "axes.edgecolor": MUTED,
        "axes.linewidth": 0.6,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": GRID,
        "grid.linewidth": 0.5,
        "xtick.color": INK2,
        "ytick.color": INK2,
        "xtick.labelsize": 6.5,
        "ytick.labelsize": 6.5,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "legend.fontsize": 6.5,
        "legend.frameon": False,
        "lines.linewidth": 1.5,
        "lines.markersize": 4,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
        "pdf.fonttype": 42,
    })
