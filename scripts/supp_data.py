"""Data for the supplement figures.

STATUS: held-out status trade-offs (Supp. Fig. status_achieved).
These values were RECOVERED FROM THE VECTOR GEOMETRY of the group's original
figures/status_achieved.pdf (accurate to about +-0.2 points; achieved recall
matches tables/status_joint_v6.tex to 0.1). Replace with the analysis output
when available. Keys: route -> coverage-target index (0=81%, 1=90%, 2=98%).
"""
TARGETS = ["81% coverage target", "90% coverage target", "98% coverage target"]
STATUS = {
 "Fit comparator": {
  "0": {
   "recall": [
    31.5,
    40.9,
    47.0,
    99.4
   ],
   "offtarget_fv": [
    54.9,
    54.9,
    54.9,
    0.2
   ],
   "shear_fn": [
    42.7,
    45.9,
    49.2,
    87.7
   ]
  },
  "1": {
   "recall": [
    41.4,
    46.9,
    99.4
   ],
   "offtarget_fv": [
    54.9,
    54.9,
    0.2
   ],
   "shear_fn": [
    46.9,
    49.2,
    87.7
   ]
  },
  "2": {
   "recall": [
    41.4,
    47.0,
    99.4
   ],
   "offtarget_fv": [
    61.0,
    54.9,
    0.2
   ],
   "shear_fn": [
    46.9,
    49.2,
    87.7
   ]
  }
 },
 "Original 28": {
  "0": {
   "recall": [
    29.3,
    47.0,
    54.2,
    69.6,
    80.7
   ],
   "offtarget_fv": [
    52.2,
    47.2,
    42.8,
    36.1,
    21.2
   ],
   "shear_fn": [
    10.3,
    13.6,
    16.1,
    23.6,
    34.6
   ]
  },
  "1": {
   "recall": [
    29.3,
    46.9,
    54.1,
    69.6,
    80.6
   ],
   "offtarget_fv": [
    64.9,
    52.2,
    50.5,
    42.8,
    33.9
   ],
   "shear_fn": [
    10.3,
    13.6,
    16.1,
    23.6,
    34.6
   ]
  },
  "2": {
   "recall": [
    29.3,
    47.0,
    54.1,
    69.6,
    80.7
   ],
   "offtarget_fv": [
    72.1,
    59.3,
    52.2,
    43.9,
    35.0
   ],
   "shear_fn": [
    10.3,
    13.6,
    16.1,
    23.6,
    34.6
   ]
  }
 },
 "Original 28 + fit": {
  "0": {
   "recall": [
    28.2,
    46.4,
    51.9,
    69.1,
    80.1
   ],
   "offtarget_fv": [
    54.4,
    47.7,
    43.9,
    36.7,
    21.2
   ],
   "shear_fn": [
    11.9,
    16.1,
    18.4,
    24.9,
    35.9
   ]
  },
  "1": {
   "recall": [
    28.2,
    46.4,
    51.9,
    69.0,
    80.1
   ],
   "offtarget_fv": [
    66.0,
    54.4,
    52.2,
    43.3,
    34.5
   ],
   "shear_fn": [
    11.9,
    16.1,
    18.4,
    24.9,
    35.9
   ]
  },
  "2": {
   "recall": [
    28.2,
    46.4,
    51.9,
    69.1,
    80.1
   ],
   "offtarget_fv": [
    73.2,
    59.9,
    54.4,
    44.4,
    35.6
   ],
   "shear_fn": [
    11.9,
    16.1,
    18.4,
    24.9,
    35.9
   ]
  }
 },
 "Original 7": {
  "0": {
   "recall": [
    37.0,
    48.1,
    62.4,
    68.5,
    81.8
   ],
   "offtarget_fv": [
    35.6,
    30.6,
    26.2,
    22.3,
    15.1
   ],
   "shear_fn": [
    13.2,
    16.5,
    19.7,
    23.6,
    34.9
   ]
  },
  "1": {
   "recall": [
    37.0,
    48.1,
    62.4,
    68.5,
    81.8
   ],
   "offtarget_fv": [
    58.2,
    46.1,
    35.6,
    29.5,
    20.7
   ],
   "shear_fn": [
    13.2,
    16.5,
    19.7,
    23.6,
    34.9
   ]
  },
  "2": {
   "recall": [
    37.0,
    48.1,
    62.4,
    68.5,
    81.8
   ],
   "offtarget_fv": [
    62.7,
    49.9,
    39.5,
    32.3,
    22.9
   ],
   "shear_fn": [
    13.2,
    16.5,
    19.7,
    23.6,
    34.9
   ]
  }
 },
 "Wide relaxed 28": {
  "0": {
   "recall": [
    36.5,
    49.2,
    59.7,
    78.5,
    85.1
   ],
   "offtarget_fv": [
    47.2,
    38.9,
    35.0,
    25.1,
    17.3
   ],
   "shear_fn": [
    10.6,
    14.5,
    21.3,
    31.4,
    43.3
   ]
  },
  "1": {
   "recall": [
    36.5,
    49.2,
    59.7,
    78.4,
    85.1
   ],
   "offtarget_fv": [
    61.6,
    49.4,
    41.7,
    32.3,
    21.8
   ],
   "shear_fn": [
    10.6,
    14.5,
    21.3,
    31.4,
    43.3
   ]
  },
  "2": {
   "recall": [
    36.5,
    49.2,
    59.7,
    78.4,
    85.1
   ],
   "offtarget_fv": [
    67.6,
    54.4,
    47.7,
    35.6,
    25.1
   ],
   "shear_fn": [
    10.6,
    14.5,
    21.3,
    31.4,
    43.3
   ]
  }
 },
 "Wide strict 28": {
  "0": {
   "recall": [
    41.4,
    51.9,
    63.5,
    79.0,
    87.3
   ],
   "offtarget_fv": [
    43.3,
    37.8,
    31.7,
    20.7,
    14.0
   ],
   "shear_fn": [
    14.2,
    18.1,
    24.9,
    32.0,
    45.6
   ]
  },
  "1": {
   "recall": [
    41.4,
    51.9,
    63.5,
    79.0,
    87.3
   ],
   "offtarget_fv": [
    54.9,
    47.7,
    37.8,
    28.4,
    19.6
   ],
   "shear_fn": [
    14.2,
    18.1,
    24.9,
    32.0,
    45.6
   ]
  },
  "2": {
   "recall": [
    41.4,
    51.9,
    63.5,
    79.0,
    87.3
   ],
   "offtarget_fv": [
    61.0,
    49.9,
    41.1,
    30.6,
    19.6
   ],
   "shear_fn": [
    14.2,
    18.1,
    24.9,
    32.0,
    45.6
   ]
  }
 },
 "Wide strict 7": {
  "0": {
   "recall": [
    39.8,
    51.4,
    63.5,
    80.7,
    85.1
   ],
   "offtarget_fv": [
    38.3,
    27.8,
    20.1,
    12.9,
    9.1
   ],
   "shear_fn": [
    19.1,
    20.7,
    23.9,
    37.2,
    43.7
   ]
  },
  "1": {
   "recall": [
    39.8,
    51.4,
    63.5,
    80.6,
    85.1
   ],
   "offtarget_fv": [
    49.9,
    38.3,
    33.9,
    17.9,
    12.9
   ],
   "shear_fn": [
    19.1,
    20.7,
    23.9,
    37.2,
    43.7
   ]
  },
  "2": {
   "recall": [
    39.8,
    51.4,
    63.5,
    80.7,
    85.1
   ],
   "offtarget_fv": [
    58.8,
    45.5,
    36.1,
    17.9,
    13.5
   ],
   "shear_fn": [
    19.1,
    20.7,
    23.9,
    37.2,
    43.7
   ]
  }
 }
}

# PAIRED: paired 3 mm hit-rate changes (points, 95% patient-cluster CI),
# from tables/primary_contrasts.tex.
PAIRED_ROWS = ["Diversify at 28", "Cap 7\u219228, direct scorer", "Cap 7\u219228, SAM scorer", "Wider lattice at cap 28"]
PAIRED = {
    "staging":   [(9.1, 6.0, 12.2), (6.1, 3.6, 9.1), (-1.1, -3.6, 1.4), (-0.2, -2.8, 2.1)],
    "screening": [(12.0, 7.5, 16.4), (9.1, 6.0, 12.3), (-1.0, -5.5, 3.3), (0.6, -1.9, 3.2)],
}
