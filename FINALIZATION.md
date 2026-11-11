# FINALIZATION — High-Reach Candidate Search (CVPR 2027), expanded working draft

Worktree: `Final_CVPR2027_HighReach_v1` (branch `final/CVPR2027_HighReach_v1`, from `main@e28aea2`). The original `main` branch is untouched.
Reviewer instructions: `reviews/REVIEW_RUBRIC.md`. The master prompt's Part C was missing from the upload, so this neutral rubric substitutes for it (agreed with the author).

## Working thesis
For point-query lesion matching after a chest alignment, *which* local hypotheses reach the scorer matters as much as how they are scored: ordering translations by anatomical fit and enforcing a minimum spacing turns a fixed candidate budget into coverage. This produces a ~10-point gain over lesion-inclusive B-spline refinement at ~19x lower local cost, and an exact reach/selection decomposition shows where the gain comes from.

## Contributions (2-4)
1. Fit-ordered diverse search: a parameter-light allocation rule with a lattice coverage bound (Eq. coverage).
2. Exact reach/selection decomposition for comparing candidate lists under a list-invariant scorer.
3. A controlled two-cohort study (independent staging + retrospective screening) isolating spatial allocation at fixed budget, scorer capacity (direct vs SAM) and compute.

## Claim-to-source map (central claims)
| Claim | Value | Source |
|---|---|---|
| Staging hits vs spline at 3 mm | 289 vs 243 / 440, +10.5 [3.6, 17.6] | draft Tab. 1, Supp. S10, tables/tolerance_effects.tex |
| Screening hits vs spline | 244 vs 211 / 309, +10.7 [5.8, 15.4] | same |
| Diversify at K=28 | 205→245 (+9.1 [6.0, 12.2]); 175→212 (+12.0 [7.5, 16.4]) | tables/primary_contrasts.tex |
| Reach decomposition (diversify, staging) | +45 new, −1 lost, −4 shared = +40 | draft Sec. 5.2 |
| Coverage of the complete list | 348/351, 289/290; ~365/360 kept of 4,851 | Supp. S9/S10 |
| Local speed | 0.194 vs 3.617 s (staging, S15); 0.185 vs 3.866 s (screening, S14) | Supp. S14/S15 |
| Cap 7→28: direct vs SAM | +6.1 vs −1.1 (staging); difference 7.3 [4.4, 10.4] | primary_contrasts, draft 5.3, Supp. S5 |
| Exact-mark diagnostic | spline 211→239, ours 244→243 (screening) | tables/current_mark_diagnostic.tex |
| Query bands (≤1.5 mm) | +10.2 [2.1, 18.4]; +10.8 [5.8, 16.0] | draft text; bands 2-3 CIs **recovered from vector figure** |
| Qualitative cases | errors per column | scripts/cases.npz, cases.json |
| Status figure (supp) | rule-level points | **recovered from vector figure** |

## Action ledger
(see cycles below)

## Independent review history
| Snapshot | Digest (main.pdf sha256, first 12) | Score (range) | Notes |
|---|---|---|---|

## Material unresolved items
- Exhaustive staging timing conflict: 0.956 s (S15) vs 0.265 s (S16).
- Recovered CIs/points (query bands 2-3; supp status figure) need confirmation from analysis output.
- No learned-registration baseline (would need new runs).
- LLM statement policy check; BioRender high-res export; official BioRender citation at camera-ready.

## Compression map
(filled at delivery)
