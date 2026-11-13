"""Method overview (Fig. 2) from the detailed BioRender illustration.

BioRender's generator delivers the figure as one flat image whose lettering is drawn as
pixels in a sans-serif face (its PowerPoint export would be that same single picture).
This script therefore
  1. removes every lettered region from figures/biorender/overview_detailed.png,
  2. fixes what the generator got wrong in panel C (a second ground-truth star with its
     leader line; 11 instead of 12 diverse candidates) and draws the corrected leader,
  3. saves the cleaned artwork as figures/biorender/overview_clean.png, and
  4. typesets every label from the single LAYOUT table below:
       - figures/overview.pdf / .png for the paper (Times via TeX Gyre Termes), and
       - figures/overview.pptx, an editable slide with Times New Roman text boxes
         over the cleaned artwork (scripts/make_overview_pptx.py).
Coordinates are in a 2000 x 1116 frame (the artwork is 2752 x 1536 px).
"""
import os
import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(__file__))

ROOT = os.path.join(os.path.dirname(__file__), "..")
SRC = os.path.join(ROOT, "figures", "biorender", "overview_detailed.png")
CLEAN = os.path.join(ROOT, "figures", "biorender", "overview_clean.png")
FW, FH = 2000, 1116
K = 12                                    # candidate budget drawn in panel C
TOP = 92                                  # rows above this (the old title banner) are cropped away

# Font sizes in points at paper size (figure width = 6.875 in).
TITLE, HEAD, LAB, SUB = 12.5, 8.4, 6.4, 5.8

# (x, y, text, size, options). Options: b=bold, i=italic, ha, rot.
# Inline $...$ marks an italic math symbol.
LAYOUT = [
    # panel heads
    (52, 130, "A. Initial Alignment", HEAD, dict(b=1, ha="left")),
    (797, 130, "B. Candidate Generation & Ranking", HEAD, dict(b=1, ha="left")),
    (1386, 130, "D. Lesion Scoring", HEAD, dict(b=1, ha="left")),
    (52, 647, "C. Candidate Selection Comparison", HEAD, dict(b=1, ha="left")),
    (1393, 699, "E. Outcome Distinction", HEAD, dict(b=1, ha="left")),
    # A
    (196, 184, "Current Scan", LAB, dict(b=1)),
    (587, 184, "Earlier Scan", LAB, dict(b=1)),
    (398, 330, "Affine\nAlignment", LAB, dict(b=1)),
    (102, 527, "Current Lesion", LAB, dict(ha="left")),
    (385, 524, "Residual\nDisplacement", LAB, {}),
    (617, 524, "Offset (reference point\nhidden from algorithm)", LAB, {}),
    # B
    (1199, 190, "Fit Octants", LAB, dict(ha="left")),
    (1172, 234, "Witness Octants", LAB, dict(ha="left")),
    (1252, 294, "Lesion-Excluded\nCentral Region", LAB, {}),
    (1190, 433, "Fit Cost", SUB, dict(rot=90)),
    (1252, 514, "Witness Cost\nContribution", LAB, {}),
    (907, 541, "Translation Lattice", LAB, dict(ha="left")),
    # D
    (1441, 191, "Retained\nCandidates", LAB, {}),
    (1639, 208, "Frozen\nLogistic-Regression\nLesion Scorer", LAB, dict(b=1)),
    (1617, 362, "Lesion Appearance\nFeatures", 5.3, {}),
    (1625, 578, "Soft Anatomical-Fit\nPenalty\n(witness costs)", SUB, {}),
    (1870, 266, "Highest-Scoring\nCandidate", LAB, {}),
    (1870, 521, "Predicted\nEarlier Lesion\nLocation", LAB, {}),
    # C
    (338, 701, "Conventional Top-K Selection", LAB + 0.3, dict(b=1)),
    (1020, 688, "Proposed Fit-Ordered Diverse Selection", LAB + 0.3, dict(b=1)),
    (1020, 721, "(Minimum Distance $r$ = 2.1 mm)", LAB + 0.3, {}),
    (579, 797, "Better Fit", SUB, dict(rot=90)),
    (579, 962, "Worse Fit", SUB, dict(rot=90)),
    (1259, 797, "Better Fit", SUB, dict(rot=90)),
    (1259, 962, "Worse Fit", SUB, dict(rot=90)),
    (708, 842, "Fit Ranking\nUnchanged", LAB + 0.3, {}),
    (340, 1054, "Misses\n3 mm Circle", LAB, {}),
    (544, 1054, "Ground-Truth\n(Evaluation Only)", LAB, {}),
    (832, 1054, "Spatially Diverse\nCandidates", LAB, {}),
    (1028, 1054, "One Candidate\ninside 3 mm Circle", LAB, {}),
    (1223, 1054, f"Same Candidate\nBudget ($K$ = {K})", LAB, {}),
    # E
    (1527, 748, "Reach", LAB + 0.6, dict(b=1)),
    (1817, 748, "Hit", LAB + 0.6, dict(b=1)),
    (1527, 909, "3 mm", SUB, {}),
    (1817, 909, "3 mm", SUB, {}),
    (1527, 999, "Is any candidate\nwithin 3 mm?", LAB, {}),
    (1527, 1039, "YES", LAB, dict(b=1)),
    (1817, 999, "Is the final selected\ncandidate within 3 mm?", LAB, {}),
    (1817, 1039, "YES (Hit)", LAB, dict(b=1)),
    (1672, 1071, "Reach does not guarantee Hit", SUB, dict(i=1)),
]

# every lettered region in the BioRender art, (x0, y0, x1, y1) in the 2000 x 1116 frame
BOXES = [
    (140, 12, 1860, 82),                                   # banner
    (45, 106, 350, 154), (790, 106, 1330, 154), (1380, 106, 1655, 154),
    (45, 622, 590, 672), (1388, 676, 1742, 722),           # panel heads
    (108, 166, 284, 200), (506, 166, 668, 200),            # A
    (326, 292, 470, 368),
    (98, 510, 262, 544), (314, 493, 468, 554), (492, 493, 744, 554),
    (1194, 174, 1312, 206), (1167, 218, 1338, 250), (1166, 264, 1338, 324),   # B
    (1175, 392, 1206, 478), (1180, 486, 1324, 545), (902, 525, 1106, 558),
    (1378, 161, 1505, 220), (1534, 171, 1746, 247), (1530, 332, 1708, 380),   # D
    (1534, 546, 1716, 618), (1778, 236, 1962, 296), (1790, 478, 1950, 564),
    (1376, 568, 1506, 624),                                # misspelt duplicate label
    (150, 683, 527, 720), (770, 670, 1270, 706), (824, 703, 1216, 739),       # C
    (563, 748, 594, 848), (563, 912, 594, 1012), (1243, 748, 1274, 848), (1243, 912, 1274, 1012),
    (634, 810, 784, 874), (270, 1024, 410, 1084), (455, 1024, 634, 1084),
    (742, 1024, 924, 1084), (927, 1024, 1130, 1084), (1134, 1024, 1314, 1084),
    (1484, 731, 1572, 765), (1790, 731, 1845, 765),        # E
    (1499, 898, 1556, 922), (1789, 898, 1846, 922),
    (1378, 983, 1668, 1086), (1676, 983, 1958, 1074),
]


def build_clean():
    img = cv2.imread(SRC)
    sc = img.shape[1] / FW
    px = lambda *v: [int(round(a * sc)) for a in v]
    rgb = img[:, :, ::-1].astype(int)
    R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]

    # (a) second ground-truth star and the leader line pointing at it (panel C, left map)
    m = np.zeros(img.shape[:2], np.uint8)
    x0, y0, x1, y1 = px(448, 912, 498, 966)
    star = ((R > 200) & (G > 90) & (G < 190) & (B < 100))[y0:y1, x0:x1].astype(np.uint8) * 255
    m[y0:y1, x0:x1] = cv2.dilate(star, np.ones((15, 15), np.uint8))
    band = np.zeros_like(m)                                   # only the dark line pixels
    cv2.line(band, tuple(px(530, 1030)), tuple(px(476, 946)), 255, px(12)[0])
    dark = ((R + G + B) < 330).astype(np.uint8) * 255
    m |= cv2.dilate(band & dark, np.ones((5, 5), np.uint8))
    img = cv2.inpaint(img, m, 5, cv2.INPAINT_TELEA)

    # (b) remove all lettering: fill each box with the median colour of its border
    for b in BOXES:
        x0, y0, x1, y1 = px(*b)
        ring = np.concatenate([img[y0, x0:x1], img[y1, x0:x1], img[y0:y1, x0], img[y0:y1, x1]])
        img[y0:y1, x0:x1] = np.median(ring, axis=0)

    # (c) corrected leader to the ground-truth star, and the 12th diverse candidate
    aa = cv2.LINE_AA
    cv2.line(img, tuple(px(526, 1024)), tuple(px(437, 922)), (58, 58, 58), 2, aa)
    c = tuple(px(970, 911))
    halo = img.copy()
    cv2.circle(halo, c, px(15.5)[0], (255, 255, 255), -1, aa)
    img = cv2.addWeighted(halo, 0.55, img, 0.45, 0)
    cv2.circle(img, c, px(8.0)[0], (201, 119, 37), -1, aa)        # BGR of #2577c9
    cv2.circle(img, c, px(8.0)[0], (111, 65, 23), 2, aa)          # BGR of #17416f
    cv2.imwrite(CLEAN, img)
    return img


def split_math(s):
    """'Budget ($K$ = 12)' -> [('Budget (', False), ('K', True), (' = 12)', False)]"""
    parts = s.split("$")
    return [(p, i % 2 == 1) for i, p in enumerate(parts) if p]


def render_paper(img):
    import style as S
    S.apply()
    plt.rcParams.update({"pdf.fonttype": 42, "font.family": "serif",
                         "font.serif": ["Times New Roman", "TeX Gyre Termes", "Nimbus Roman", "Times"]})
    W = S.PAGE_W
    fig = plt.figure(figsize=(W, W * (FH - TOP) / FW))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(img[:, :, ::-1], extent=[0, FW, FH, 0], interpolation="lanczos")
    ax.set_xlim(0, FW); ax.set_ylim(FH, TOP); ax.axis("off")
    for x, y, s, size, o in LAYOUT:
        ax.text(x, y, s, fontsize=size, fontweight="bold" if o.get("b") else "normal",
                style="italic" if o.get("i") else "normal", ha=o.get("ha", "center"),
                va="center", rotation=o.get("rot", 0), color="#141414", linespacing=1.05)
    out = os.path.join(ROOT, "figures")
    fig.savefig(os.path.join(out, "overview.pdf"), dpi=400)
    fig.savefig(os.path.join(out, "overview.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    clean = build_clean()
    render_paper(clean)
    print("wrote figures/overview.pdf and figures/biorender/overview_clean.png")
