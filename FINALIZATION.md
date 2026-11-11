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

### Cycle 1 candidates (scores: P(help) / benefit 1-3 / P(harm) / downside 1-3 / cost 1-5)
| ID | Concern (baseline review) | Change | Evidence | P(help) | Ben | P(harm) | Down | Cost | Priority | Decision |
|---|---|---|---|---|---|---|---|---|---|---|
| A | W1, W2, W7, fix 1-2, 5: claims bundle pipeline vs. rule; contributions oversold; local-only speed | Rewrite abstract, intro contributions, Sec. 5.1 lead and discussion around two separated, precisely scoped findings: (i) allocation at fixed budget (+9.1/+12.0); (ii) the full fit-ordered pipeline vs. spline, with exhaustive as an explicit upper bound (diverse = 348/351 reach, 289/297 hits at 7.5% of positions). Present Eq. 3 as the NMS covering property and Eq. 6 as an accounting identity whose interpretation rests on list invariance. State local vs end-to-end speed. Add a compact "where misses come from" table (Supp. Tab. S3: unreachable vs reachable-misselected) | primary_contrasts; Supp S3, S10, S14-16 | high | 3 | low | 1 | 3 | (0.8x3-0.1x1)/3 = 0.77 | execute |
| B | Clarity 4: route taxonomy, lab-note paragraph, Tab. 1 timing mix, F/W undefined, Siamese "22/25" | One naming scheme (Fit-only K, Diverse K, Diverse search, Exhaustive, Gated K strict/relaxed) across text, tables and figures; move "Residual support details" to the supplement; split Tab. 1 time column note (CPU vs GPU), explain candidate counts; give F, W values | Supp S3 (F=76.958, W=99.541 HU) | high | 2 | low | 1 | 3 | (0.8x2-0.1)/3 = 0.50 | execute |
| C | Figs 6 and 8 hard to read | Redesign Fig. 8 (accuracy-latency) with a linear time axis inset and direct labels; enlarge markers and reach/hit distinction in Fig. 6 | existing data | med-high | 2 | low | 1 | 2 | (0.7x2-0.1)/2 = 0.65 | execute |
| D | Fig. 4 should show fit-only candidates | Add fit-only top-K overlay | cases.npz lacks fit-only lists | — | 2 | — | — | 4 | — | reject (data unavailable) |
| E | W3: spread baselines, r sweep | Uniform sub-lattice / local-minima / r sweep | needs new runs | — | 3 | — | — | 5 | — | defer (next research task) |

Predicted benefit of cycle 1: clarity +1, novelty framing more defensible (no score promise).

**Cycle 1 outcome:** overall score unchanged (4, range 3-5); clarity 4→5; the reviewer judged numbers consistent and Fig. 1 and the miss-mode table effective, and raised no new factual problems. Decision: **keep** (meaningful clarity gain, no regression).

### Cycle 2 candidates
| ID | Concern (cycle-1 review) | Change | Evidence | P(help) | Ben | P(harm) | Down | Cost | Priority | Decision |
|---|---|---|---|---|---|---|---|---|---|---|
| A2 | W1, W2, W5, fix 1-2 | Attribute the spline gain precisely where it is stated (abstract, intro, 5.3, conclusion): wider search extent plus lesion-aware selection; put the exact-mark result (33→4 on screening) next to the headline; say why small budgets bind (per-candidate scoring cost, multi-lesion workloads) | Supp. S7, S14-S16 | high | 3 | low | 1 | 2 | 1.15 | execute |
| B2 | W8, Tab. 2 and Fig. 8 mix timing protocols | Remove timing from Tab. 2; new one-column timing table with both protocols side by side (matched comparison vs fixed-budget replay), including the exhaustive discrepancy; Fig. 8 uses one protocol only; text states speed ratios per protocol | Supp. S14, S15, S16 | high | 2 | low | 1 | 2 | 0.75 | execute |
| D2 | Naming mismatch with supplement; redundancy | Add a name-mapping table at the top of the supplement and a scope note before the status-protocol sections; remove duplicated interval lists from Tab. 2 caption | supplement | med | 2 | low | 1 | 2 | 0.65 | execute |
| E2 | W3 uniform sub-lattice; r sweep; wide-initialized spline | needs runs | — | — | 3 | — | — | 5 | — | defer (next research tasks) |
| F2 | Fig. 6 markers overlap | larger markers / zoom insets | spec fixed by group (PROMPT.md) | med | 1 | med | 1 | 2 | 0.25 | reject (conflicts with group's figure spec) |



## Independent review history
| Snapshot | Digest (main.pdf sha256, first 12) | Score (range) | Notes |
|---|---|---|---|
| baseline main@e28aea2 | de17d686a67b | 4/10 (3-5), conf 4 | novelty 3, soundness 6, evidence 5, clarity 4, figs 6. Main issues: claims bundle pipeline gain with diversification; Eq.3/6 oversold; taxonomy; Tab.1 timing; Fig.8; missing spread baselines (needs runs) |
| cycle 1 @66a52ad | 14ce67264aed | 4/10 (3-5), conf 4 | novelty 3, soundness 6, evidence 5, clarity 5 (+1), figs 6. Fig.1 'excellent', Tab.3 'clear and effective'. Remaining: spline comparison confounded (lesion snapping, lattice extent), timing protocols mixed, naming vs supplement, redundancy of Fig.5, uniform sub-lattice ablation (needs runs) |
| cycle 2 @a9ae09b | d4f98a988404 | 4/10 (3-5), conf 4 | novelty 3, soundness 6, evidence 6 (+1), clarity 6 (+1), figs 6. Tab. 3 'best table'; numbers consistent. Remaining: diversification vs exhaustive value, missing allocation baselines, spline extent confound, exact-mark staging rerun, layout gaps p10-11 |
| final @(see STATE) | unscored | — | layout-only correction after the cycle-2 review (float placement; removes blank bands on pp. 10-11). No text or number changes. The cycle-2 score is historical for this snapshot. |

## Material unresolved items
- Exhaustive staging timing conflict: 0.956 s (S15) vs 0.265 s (S16).
- Recovered CIs/points (query bands 2-3; supp status figure) need confirmation from analysis output.
- No learned-registration baseline (would need new runs).
- LLM statement policy check; BioRender high-res export; official BioRender citation at camera-ready.

## Compression map
(filled at delivery)

**Cycle 2 outcome:** overall score unchanged (4, range 3-5); clarity 5→6 and evidence 5→6 on the reviewer's sub-scores. No factual regressions were found. Decision: **keep**. MAX_CYCLES=2 reached; stopped.

**Post-review correction (unscored):** the cycle-2 reviewer flagged blank bands on pp. 10-11 caused by a float barrier. I removed it and moved three floats earlier. Only layout changed; the text and numbers are identical to the reviewed snapshot.

## Assessment of the score ceiling
All three independent reviews agree (4/10, novelty 3). The remaining bottlenecks cannot be fixed by writing or presentation: they need new evidence. Next research tasks, ranked by expected reviewer impact:
1. Allocation baselines at matched K and at completion: a uniform sub-lattice with spacing about r, fit-map local minima, random/stratified subsampling, plus an r sweep (1.4-4.2 mm). These decide whether fit ordering matters beyond coverage. Runs on existing crops; cheap.
2. Fairer registration comparator: a B-spline initialized from the wide-lattice best translation (or from the Diverse-search output); one learned registration model (uniGradICON has public weights).
3. Exact-mark rerun on the staging cohort (the analogue of Supp. Tab. S7), and ideally real queries (detector outputs or reader clicks).
4. A heavier learned scorer (e.g. the Siamese scorer over the full lattice) to demonstrate the regime where diversification, not exhaustive scoring, is the right choice.
5. A breakdown by lesion diameter and interval size change.

## Material unresolved items (carried)
- Timing: exhaustive staging 0.956 s (matched comparison, single pass) vs 0.265 s (fixed-budget replay). Now reported transparently in Tab. 4, but the group should confirm which is representative.
- Recovered values (query-band CIs for bands 2-3; supplement status figure) need confirmation from the analysis output.
- The 1.5 weight in Eq. 4: no rationale was found in the sources; the paper now states it as fixed.
- LLM statement policy check; BioRender high-res exports and the official citation at camera-ready.

## Compression map (expanded draft ≈ 9.6 pages of body → 8)
| Cut | Saves (pages) |
|---|---|
| Move Tab. 4 (timing protocols) and Fig. 8 (accuracy-latency) to the supplement; keep the speed ratios in the text | 0.45 |
| Drop Fig. 5 (forest); intervals already appear in the text and Tab. 1 | 0.35 |
| Fold Sec. 5.5 (scorer capacity) into Sec. 5.1 (the decomposition figure already shows it) | 0.2 |
| Remove the `evaluation_expanded` paragraphs (reference geometry, shared inputs, matched workloads) via the compact build switch | 0.4 |
| Trim Sec. 3.1 notation and Related work by about 25% | 0.3 |
| Shorten Discussion to one paragraph plus Limitations | 0.15 |
| **Total** | **≈1.85** |
