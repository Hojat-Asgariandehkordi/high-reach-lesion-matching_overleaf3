"""All plotted numbers, transcribed from the manuscript and supplement.
Each block cites its source table so values can be re-checked."""

N = {"staging": 440, "screening": 309}

# Budget sweep (Supp. Tab. S10 staging, Tab. S9 screening), 3 mm.
BUDGETS = ["7", "14", "28", "56", "112", "All"]
SWEEP = {
    "staging": {
        "ungated_hits":  [197, 221, 245, 270, 278, 289],
        "ungated_reach": [211, 246, 274, 306, 322, 348],
        "strict_hits":   [192, 208, 219, 229, 230, 232],
        "strict_reach":  [202, 226, 241, 255, 257, 259],
        "fitonly28": (205, 221),      # hits, reach (wide ungated, undiversified 28)
        "exhaustive": (297, 351),
        "spline": 243,
    },
    "screening": {
        "ungated_hits":  [170, 190, 212, 223, 232, 244],
        "ungated_reach": [189, 219, 242, 262, 271, 289],
        "strict_hits":   [167, 183, 195, 198, 199, 198],
        "strict_reach":  [185, 207, 220, 227, 229, 229],
        "fitonly28": (175, 189),
        "exhaustive": (242, 290),
        "spline": 211,
    },
}

# Reach/selection decomposition (main text Sec. 5.2-5.3, Supp. Tab. S5).
# (label, reach component, selection component); net = sum.
DECOMP = {
    "staging": [
        ("Diversify at 28", 44, -4),        # 45 gained - 1 lost; shared -4 -> +40
        ("Gated, K 7→28 (direct)", 33, -6),  # 33 new; shared 192->186 -> +27
        ("Gated, K 7→28 (SAM)", 10, -15),    # 10 new; shared 144->129 -> -5
    ],
    "screening": [
        ("Diversify at 28", 41, -4),        # -> +37
        ("Gated, K 7→28 (direct)", 23, 5),   # shared 167->172 -> +28
        ("Gated, K 7→28 (SAM)", 14, -17),    # shared 121->104 -> -3
    ],
}

# Accuracy vs. latency (Supp. Tab. S16 fixed-budget replay; spline from Tab. S15/S14).
SPEED = {
    "staging": {
        "routes": [("Fit-only 28", 0.098, 205), ("28", 0.120, 245), ("56", 0.131, 270),
                   ("112", 0.142, 278), ("All", 0.190, 289), ("Exhaustive", 0.265, 297)],
        "spline": (3.617, 243),
    },
    "screening": {
        "routes": [("Fit-only 28", 0.101, 175), ("28", 0.120, 212), ("56", 0.132, 223),
                   ("112", 0.144, 232), ("All", 0.190, 244), ("Exhaustive", 0.265, 242)],
        "spline": (3.866, 211),
    },
}

# Headline (Tab. 1 / Supp. S9-S10), 3 mm hits.
HEADLINE = {
    "staging":   {"B-spline": 243, "Fit-only 28": 205, "Diverse 28": 245, "Diverse search": 289},
    "screening": {"B-spline": 211, "Fit-only 28": 175, "Diverse 28": 212, "Diverse search": 244},
}

# Paired differences in points with patient-cluster 95% CIs.
# Diverse search vs spline: Tab. 1 of the draft (tables/tolerance_effects.tex).
# Search changes: tables/primary_contrasts.tex. Robustness rows: draft Sec. 5.1.
FOREST = {
    "staging": {
        "vs spline, 2 mm": (13.6, 5.6, 21.7),
        "vs spline, 3 mm": (10.5, 3.6, 17.6),
        "vs spline, 4 mm": (8.9, 1.7, 16.2),
        "vs spline, equal patient weight": (9.6, 3.7, 15.9),
        "vs spline, native mm": (11.4, 4.1, 18.9),
        "Diversify at 28": (9.1, 6.0, 12.2),
        "Gated, K 7→28 (direct)": (6.1, 3.6, 9.1),
        "Gated, K 7→28 (SAM)": (-1.1, -3.6, 1.4),
        "Gated 28, wider lattice": (-0.2, -2.8, 2.1),
        "Relaxed, 28→all": (6.1, 3.3, 9.1),
        "Remove gates, all": (5.7, 2.3, 9.1),
        "Diverse search→exhaustive": (1.8, 0.2, 3.5),
    },
    "screening": {
        "vs spline, 2 mm": (12.0, 6.1, 17.6),
        "vs spline, 3 mm": (10.7, 5.8, 15.4),
        "vs spline, 4 mm": (7.8, 3.2, 12.6),
        "vs spline, equal patient weight": None,
        "vs spline, native mm": None,
        "Diversify at 28": (12.0, 7.5, 16.4),
        "Gated, K 7→28 (direct)": (9.1, 6.0, 12.3),
        "Gated, K 7→28 (SAM)": (-1.0, -5.5, 3.3),
        "Gated 28, wider lattice": (0.6, -1.9, 3.2),
        "Relaxed, 28→all": (4.2, 2.0, 6.7),
        "Remove gates, all": (8.7, 5.4, 12.1),
        "Diverse search→exhaustive": (-0.6, -3.1, 1.7),
    },
}

# Query-error bands, Diverse search minus spline at 3 mm (points, 95% CI).
# Point estimates from Supp. tables query_external / query_luna (hits per band).
# Band 1 CIs are in the draft text; bands 2-3 CIs were read from the vector
# geometry of the draft's Fig. 3 -- CONFIRM against the analysis output.
BANDS = ["≤1.5 mm", "1.5–3 mm", ">3 mm"]
BAND = {
    "staging":   {"n": [322, 72, 43], "d": [(10.2, 2.1, 18.4), (5.6, -5.3, 16.0), (20.9, 9.4, 34.0)]},
    "screening": {"n": [194, 68, 47], "d": [(10.8, 5.8, 16.0), (16.2, 5.0, 27.3), (2.1, -13.2, 16.7)]},
}

# Net-change CIs for the decomposition rows (points), from primary_contrasts.
DECOMP_CI = {
    "staging":   [(6.0, 12.2), (3.6, 9.1), (-3.6, 1.4)],
    "screening": [(7.5, 16.4), (6.0, 12.3), (-5.5, 3.3)],
}
