"""Method overview (Fig. 2) from the detailed BioRender illustration.

BioRender's generator draws lettering as pixels in a sans-serif face, so this script
(1) removes every lettered region from figures/biorender/overview_detailed.png,
(2) fixes the two scientific details the generator got wrong in panel C
    (a second ground-truth star; 11 instead of 12 candidates on the diverse side), and
(3) typesets every label in Times (TeX Gyre Termes, the metric Times clone used by the
    paper body) as real, selectable PDF text.
Coordinates below are in a 2000 x 1116 frame (the image is 2752 x 1536).
"""
import os
import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
sys.path.insert(0, os.path.dirname(__file__))
import style as S

S.apply()
plt.rcParams.update({"pdf.fonttype": 42, "font.family": "serif",
                     "font.serif": ["Times New Roman", "TeX Gyre Termes", "Nimbus Roman", "Times"]})
ROOT = os.path.join(os.path.dirname(__file__), "..")
SRC = os.path.join(ROOT, "figures", "biorender", "overview_detailed.png")
FW, FH = 2000, 1116
K = 12                                            # candidate budget drawn in panel C

img = cv2.imread(SRC)                             # BGR, 2752 x 1536
SC = img.shape[1] / FW


def px(*v):
    return [int(round(a * SC)) for a in v]


# ---------------------------------------------------------------- pixel edits
def blank(box, pad=0):
    """Fill a box with the median colour of its border (white card, tinted box, ...)."""
    x0, y0, x1, y1 = px(box[0] - pad, box[1] - pad, box[2] + pad, box[3] + pad)
    ring = np.concatenate([img[y0, x0:x1], img[y1, x0:x1], img[y0:y1, x0], img[y0:y1, x1]])
    img[y0:y1, x0:x1] = np.median(ring, axis=0)


def inpaint(mask_fn, radius=6):
    global img
    m = np.zeros(img.shape[:2], np.uint8)
    mask_fn(m)
    img = cv2.inpaint(img, m, radius, cv2.INPAINT_NS)


rgb = img[:, :, ::-1].astype(int)
R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]
orange = (R > 200) & (G > 90) & (G < 190) & (B < 100)


def kill_extra_star(m):
    x0, y0, x1, y1 = px(448, 912, 498, 966)
    sub = orange[y0:y1, x0:x1].astype(np.uint8) * 255
    m[y0:y1, x0:x1] = cv2.dilate(sub, np.ones((15, 15), np.uint8))
    # the leader line that pointed at it (from the label up to the star)
    cv2.line(m, tuple(px(530, 1030)), tuple(px(476, 946)), 255, px(12)[0])


inpaint(kill_extra_star, radius=9)

# every lettered region: (box in 2000x1116 frame)
BOXES = [
    (140, 12, 1860, 82),                                   # banner
    (45, 106, 350, 154), (790, 106, 1330, 154), (1380, 106, 1655, 154),
    (45, 622, 590, 672), (1388, 676, 1742, 722),           # panel heads
    (108, 166, 284, 200), (506, 166, 668, 200),            # A
    (326, 292, 470, 368),
    (98, 510, 262, 544), (314, 493, 468, 554), (492, 493, 744, 554),
    (1194, 174, 1312, 206), (1167, 218, 1338, 250), (1166, 264, 1338, 324),   # B
    (1175, 392, 1206, 478), (1180, 486, 1324, 545), (902, 525, 1106, 558),
    (1378, 161, 1505, 220), (1528, 163, 1752, 247), (1530, 332, 1708, 380),   # D
    (1534, 546, 1716, 618), (1778, 236, 1962, 296), (1790, 478, 1950, 564),
    (1376, 568, 1506, 624),
    (150, 683, 527, 720), (770, 670, 1270, 706), (824, 703, 1216, 739),       # C
    (563, 748, 594, 848), (563, 912, 594, 1012), (1243, 748, 1274, 848), (1243, 912, 1274, 1012),
    (634, 810, 784, 874), (270, 1024, 410, 1084), (455, 1024, 634, 1084),
    (742, 1024, 924, 1084), (927, 1024, 1130, 1084), (1134, 1024, 1314, 1084),
    (1484, 731, 1572, 765), (1790, 731, 1845, 765),        # E
    (1493, 895, 1562, 924), (1783, 895, 1852, 924),
    (1378, 983, 1668, 1086), (1676, 983, 1958, 1074),
]
for b in BOXES:
    blank(b)

# ---------------------------------------------------------------- figure
W = S.PAGE_W
fig = plt.figure(figsize=(W, W * FH / FW))
ax = fig.add_axes([0, 0, 1, 1])
ax.imshow(img[:, :, ::-1], extent=[0, FW, FH, 0], interpolation="lanczos")
ax.set_xlim(0, FW); ax.set_ylim(FH, 0); ax.axis("off")
U = 72 * W / FW                                     # points per frame unit
INK = "#141414"


def T(x, y, s, size=6.6, bold=False, ha="center", va="center", **kw):
    ax.text(x, y, s, fontsize=size, fontweight="bold" if bold else "normal", ha=ha, va=va,
            color=kw.pop("color", INK), linespacing=kw.pop("linespacing", 1.05), **kw)


HEAD, LAB, SUB = 8.7, 6.4, 5.8
T(1000, 47, "LONGITUDINAL PULMONARY CT CORRESPONDENCE PIPELINE", size=12.5)
for x, y, s in ((52, 130, "A. Initial Alignment"), (797, 130, "B. Candidate Generation & Ranking"),
                (1386, 130, "D. Lesion Scoring"), (52, 647, "C. Candidate Selection Comparison"),
                (1393, 699, "E. Outcome Distinction")):
    T(x, y, s, size=HEAD, bold=True, ha="left")

# A
T(196, 183, "Current Scan", LAB, bold=True)
T(587, 183, "Earlier Scan", LAB, bold=True)
T(404, 330, "Affine\nAlignment", LAB, bold=True)
T(102, 527, "Current Lesion", LAB, ha="left")
T(392, 523, "Residual\nDisplacement", LAB)
T(617, 523, "Offset (reference point\nhidden from algorithm)", LAB)
# B
T(1199, 190, "Fit Octants", LAB, ha="left")
T(1172, 234, "Witness Octants", LAB, ha="left")
T(1252, 294, "Lesion-Excluded\nCentral Region", LAB)
T(1190, 435, "Fit Cost", LAB, rotation=90)
T(1252, 514, "Witness Cost\nContribution", LAB)
T(907, 541, "Translation Lattice", LAB, ha="left")
# D
T(1441, 191, "Retained\nCandidates", LAB)
T(1639, 205, "Frozen\nLogistic-Regression\nLesion Scorer", LAB, bold=True)
T(1619, 356, "Lesion Appearance\nFeatures", SUB)
T(1625, 582, "Soft Anatomical-Fit\nPenalty\n(witness costs)", SUB)
T(1870, 266, "Highest-Scoring\nCandidate", LAB)
T(1870, 521, "Predicted\nEarlier Lesion\nLocation", LAB)
# C
T(338, 701, "Conventional Top-K Selection", LAB + 0.3, bold=True)
T(1020, 688, "Proposed Fit-Ordered Diverse Selection", LAB + 0.3, bold=True)
T(1020, 721, "(Minimum Distance $r$ = 2.1 mm)", LAB + 0.3)
for x in (579, 1259):
    T(x, 797, "Better Fit", SUB, rotation=90)
    T(x, 962, "Worse Fit", SUB, rotation=90)
T(708, 842, "Fit Ranking\nUnchanged", LAB + 0.3)
T(340, 1054, "Misses\n3 mm Circle", LAB)
T(544, 1054, "Ground-Truth\n(Evaluation Only)", LAB)
ax.plot([526, 437], [1024, 922], color="#3a3a3a", lw=0.55, solid_capstyle="round")
T(832, 1054, "Spatially Diverse\nCandidates", LAB)
T(1028, 1054, "One Candidate\ninside 3 mm Circle", LAB)
T(1223, 1054, f"Same Candidate\nBudget ($K$ = {K})", LAB)
# twelfth candidate on the diverse side (generator drew eleven)
ax.add_patch(Circle((970, 911), 15.5, color="white", alpha=0.55, lw=0, zorder=3))
ax.add_patch(Circle((970, 911), 8.0, facecolor="#2577c9", edgecolor="#17416f", lw=0.7, zorder=4))
# E
T(1527, 748, "Reach", LAB + 0.6, bold=True)
T(1817, 748, "Hit", LAB + 0.6, bold=True)
T(1527, 909, "3 mm", SUB)
T(1817, 909, "3 mm", SUB)
T(1527, 1006, "Is any candidate\nwithin 3 mm?", LAB)
T(1527, 1044, "YES", LAB, bold=True)
T(1817, 1006, "Is the final selected\ncandidate within 3 mm?", LAB)
T(1817, 1044, "YES (Hit)", LAB, bold=True)
T(1672, 1073, "Reach does not guarantee Hit", SUB, style="italic")

OUT = os.path.join(ROOT, "figures")
fig.savefig(os.path.join(OUT, "overview.pdf"), dpi=400)
fig.savefig(os.path.join(OUT, "overview.png"), dpi=300)
plt.close(fig)
print("wrote figures/overview.pdf")
