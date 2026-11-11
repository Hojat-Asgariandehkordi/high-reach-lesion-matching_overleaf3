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
        ("Cap 7→28, direct", 33, -6),  # 33 new; shared 192->186 -> +27
        ("Cap 7→28, SAM", 10, -15),    # 10 new; shared 144->129 -> -5
    ],
    "screening": [
        ("Diversify at 28", 41, -4),        # -> +37
        ("Cap 7→28, direct", 23, 5),   # shared 167->172 -> +28
        ("Cap 7→28, SAM", 14, -17),    # shared 121->104 -> -3
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
