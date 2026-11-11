# Review: "High-Reach Candidate Search for Longitudinal Lung Lesion Matching" (CVPR 2027 submission)

## 1. Summary

The paper studies hypothesis-based longitudinal lung lesion matching. After a global chest affine, a lesion marked in the current CT has to be found in the earlier CT by scoring candidate 3D translations on a ±7 mm voxel lattice (4,851 shifts). The authors argue that the usual design, which ranks shifts by an outer-shell anatomical fit cost and passes the top K to a lesion scorer, wastes its budget, because the top-K shifts are near-duplicates around one fit mode. They propose "fit-ordered diverse search" (Alg. 1): walk the fit-ranked list and keep a shift only if its proposed position is at least r = 2.1 mm from every kept position. This is greedy NMS / an r-net, and run to completion it keeps about 365 shifts. They split the change in hits between two lists into a "reach" term and a "selection" term (Eq. 6). Evidence comes from 440 lesions in an independent melanoma staging cohort and 309 LUNA25/NLST screening tracks, with patient-cluster bootstrap CIs and pre-specified criteria:
- At K=28, diversification raises 3 mm hits by +9.1 and +12.0 points over fit-only 28, and the accounting attributes the gain to reach.
- The complete diversified list comes within 1.8 points of exhaustive scoring.
- The full matcher beats a lesion-inclusive B-spline by about 10.5 points at 3 mm, with a local step about 19x faster.

## 2. Strengths

- **Clean problem framing.** Separating *which candidates reach the scorer* from *how they are scored* is a useful lens for hypothesis-based correspondence. The reach/selection identity (Eq. 6) is simple. Because the scorer's scores are invariant to list growth (Eq. 4, l.286-292), the selection term reflects real changes in choice rather than score reshuffling.
- **Careful statistics.** The evaluation is unusually disciplined for a CVPR paper:
  - patient-clustered paired bootstrap intervals;
  - primary contrasts, margins and the spline-comparison criterion fixed before inference (l.396-401);
  - all failures, including unsupported crops, kept in the denominators;
  - an independent cohort from a different clinical source and disease (melanoma staging) used as the primary test.
- **Honest internal controls.** The paper reports the cases where the story weakens:
  - exhaustive scoring beats the method on staging (297 vs 289);
  - widening the lattice at fixed cap 28 does nothing;
  - with the exact annotated mark, the screening advantage over the spline shrinks from 33 to 4 hits (l.547-553, l.609-612).
- **Interpretable failure analysis.** Table 3 (unreachable vs mis-selected) shows that the spline and SAM fail in opposite ways (reach vs selection). Fig. 7 (gain by query error) and Fig. 5 add useful diagnostics.
- **Simple, cheap method.** The covering guarantee (Eq. 3) is correct and easy to state. The method needs no training beyond a small logistic-regression scorer, and its compute is reported under two protocols (Table 4).
- **Numerical consistency.** I spot-checked about 20 numbers across the text, Tables 1-3 and supplement Tables S5, S6 and S10 (for example 205->245, 51/11, 289+92+59=440, 33 of 46 net gains in the <=1.5 mm band, 0.265-0.190 = 75 ms). All were consistent.

## 3. Weaknesses (most important first)

1. **Diversification is not what makes the matcher strong; the paper's own numbers show this.**
   - On staging, exhaustive scoring of all 4,851 shifts is more accurate than Diverse search (297 vs 289 hits; 277 vs 259 at 2 mm, Table 2). It costs only 75 ms more per query (0.265 vs 0.190 s, Table 4, fixed-budget replay; about 1.4x).
   - In the single-pass matched comparison the gap is 0.956 vs 0.194 s on staging (4.9x) and 0.256 vs 0.185 s on screening (1.4x), so the ratio depends on the protocol (l.583-586).
   - The fit cost must be computed for every shift anyway to produce the ordering, so the saving is only in scorer calls.
   - The gain over the B-spline (Sec. 5.3) therefore comes from a wide, lesion-aware search that exhaustive scoring also delivers, and the paper concedes this (l.507-523).
   - Diversification is a strong idea only in the fixed small-budget regime, against a fit-only top-K list that is close to a strawman (point 2). It matters for the stated motivation of an expensive learned scorer (l.486-489), but that regime is not tested: the scorer here is a logistic regression on 8 hand-crafted features. The title, abstract and contribution bullets put diversification at the centre, which over-sells it relative to the evidence.

2. **Missing obvious allocation baselines.**
   - Fit-only top-K is the only non-diverse list compared at fixed K. The natural alternatives are named only as future work (l.613-616):
     - a uniform sub-lattice of spacing about r;
     - local minima of the fit map;
     - random or stratified subsampling;
     - fit-ordered NMS with a sweep over r.
   - A stride-3 in-plane / stride-2 axial sub-lattice gives about 300 shifts with a covering radius comparable to r. It would show whether fit ordering matters at all for the complete list, or whether coverage alone explains the result, which the paper's own accounting suggests ("the entire gain comes from coverage", abstract l.014-016).
   - At fixed K, a uniform coarse lattice of K points is the obvious coverage-maximising competitor.
   - Without these, the claim of an "efficient allocation step" (l.522) is not established.

3. **The registration baseline is handicapped, and there are no learned baselines.**
   - The B-spline is initialised from the best translation on the *original* ±4.2 mm lattice, while Diverse search covers ±7 mm (l.507-511). Part of the gap is search extent, and the large-motion example in Fig. 6 illustrates exactly that.
   - A fair comparison would initialise the spline from the wide-lattice exhaustive best, or from the Diverse search output.
   - No learned registration (VoxelMorph, uniGradICON; both cited) is run. Deep Lesion Tracker and Transformer Lesion Tracker are excluded for lack of weights. The diffusion-guided tracker is excluded because it needs a coarse registration, which the paper itself has (the chest affine).
   - So the external comparison is one classical spline configuration plus SAM.

4. **The SAM comparison looks weak and its conclusion is overstated.**
   - Standalone SAM hits 99/440 at 3 mm despite 396/440 reach (Tables 2-3). The setup is a lymph-node checkpoint with 2 mm resampling and a coarse+fine similarity mean.
   - A pure anatomical embedding cannot be expected to tell a lesion from its anatomical look-alikes. "A general anatomical embedding fails to profit" (l.601-603) is close to tautological for an appearance-agnostic scorer.
   - Using SAM similarity as a feature inside the lesion scorer, or refining SAM's top modes, would be a more informative test.

5. **Query simulation drives a large part of the headline advantage.**
   - The query is the annotated mark plus up to 2.5 mm of uniform jitter, then a blob-detector refinement (l.176-184). With the exact mark, the screening hits for the spline rise from 211 to 239, while Diverse search stays at 243 (Table S7). The screening advantage then becomes 4 hits and is very likely non-significant.
   - The corresponding exact-mark rerun on the independent staging cohort is not reported in the main paper. It should be, because staging is the primary cohort.
   - The jitter model is not validated against real clicks or detector outputs (acknowledged in l.609-613). The claim that the gain is "largest when the query is imprecise" partly reflects how imprecision was synthesised.

6. **Limited novelty for CVPR.**
   - Minimum-distance greedy selection over a score-ranked list is classical NMS / an r-net / farthest-point-style coverage; the paper cites [3, 5, 17].
   - The covering bound (Eq. 3) is the standard r-net property.
   - The reach/selection split is an accounting identity (l.312-326). Its interpretive power rests on the list-invariance of Eq. 4, which holds by construction.
   - The contribution is mainly an application and analysis contribution in a narrow medical setting, with translation-only hypotheses, a specific hand-crafted fit cost and an 8-feature scorer. The claim that the lesson "transfers to other point-correspondence problems" (l.603-605) is not tested on any non-CT or non-lesion task.

7. **Cohort and design caveats.**
   - **Screening cohort was not held out.** Its patients "had been inspected earlier in the project" (l.367-371), so it is not a clean test.
   - **Small independent cohort.** The staging cohort has 72 patients (440 lesions, a mean of about 6 per patient). The bootstrap handles this correctly, but the effective sample size is small.
   - **Alignment failures dominate some patients.** In two patient pairs the chest affine fails, putting 28 lesions outside the crop (l.617-619). This is a reminder that end-to-end robustness is bounded by the affine.
   - **No analysis by lesion size or by size change.** The 3 mm centroid tolerance means something quite different for a 4 mm nodule and a 30 mm metastasis.
   - **End-to-end saving is small.** On native scans the shared alignment dominates: 29.36 vs 32.87 s per query, about 11% (l.587-591). The "19x faster" in the abstract refers to the local step only, which a careful reader will notice but a casual reader will not.

8. **Hand-tuned constants and many variants.**
   - Eq. 4 uses F = 76.958 HU and W = 99.541 HU (three-decimal "fitted" scales) and a fixed weight of 1.5.
   - Eq. 2 uses a 420 HU cap, ±98 HU clipping, and weight breakpoints at -860 and -370 HU. The shell is 23-28 mm.
   - Sensitivity to r is not reported in the main paper, even though r is *the* parameter of the method.
   - The Gated / Relaxed / Fit-only / Diverse / Exhaustive variants and their supplement aliases ("Wide strict", "Original 28 + fit", "Wide ungated, diversified all", "Escalation") make the experimental space hard to navigate.

## 4. Clarity and presentation

- **Main text.** Generally clearly written and logically organised around four questions (Sec. 5). Notation is light and mostly consistent, and Eqs. 1-6 and Algorithm 1 are readable. Eq. 4's "minimum over the list" normalisation, and the reason it gives list invariance, is explained well.
- **Weak-point patterns.**
  - Sec. 3.6 introduces four list families (Fit-only, Diverse, Gated, Relaxed) plus Exhaustive. Gated/Relaxed carry several thresholds described only in prose ("24 HU worse than the best", "loosens the fit limit by 20 HU and the slack to 40 HU"). A small table of list definitions would help.
  - Numbers are often given to excess precision (three-decimal HU scales), which reads as over-fitting rather than rigour.
- **Redundancy.** The same paired differences appear four times: Table 1, Fig. 4, Fig. 5 (bottom) and supplement Fig. S1. Fig. 5's bottom panel and Fig. S1 overlap almost entirely with Table 1. I would keep Table 1 plus one figure.
- **Layout.** Page 10 has a large empty band below Fig. 6, and page 11 has a large blank block in the Discussion column. This suggests float placement problems in the expanded draft.

**Figures and tables:**
- **Figure 1:** Effective teaser. Panels (b, c) on a synthetic 2D landscape communicate the idea immediately.
- **Figure 2:** Good pipeline schematic.
- **Figure 3:**
  - Informative, but the legend mixes line styles, markers and a dotted B-spline reference across two panels, and the in-plot "reach" / "hits" labels collide with the curves.
  - "Exh." on a categorical K axis next to "All" is confusing.
  - Gated K (green) is shown only for hits, not reach.
- **Figure 4:** Hard to read.
  - The selection component (hatched grey) is tiny, and in the SAM row it overlaps the net marker.
  - Row labels such as "Gated, K 7->28 (direct)" depend on Sec. 3.6 jargon.
  - The figure is small for the amount of information it carries.
- **Figure 5:** Clear, but redundant with Table 1 and Fig. S1, as noted above. Mixing the "Diverse search vs. B-spline" rows and the "changes to the candidate list" rows on one axis invites cross-comparison of unrelated contrasts.
- **Figure 6:** The qualitative examples are useful, but the bottom-row markers (circle, triangle, square, cross, star) overlap heavily at this size, and the dense grey candidate dots obscure the anatomy. Larger crops, or showing fewer markers per panel, would help. The "large motion" column is where the spline-extent confound shows, and it deserves a caption comment.
- **Figure 7:** Clear.
- **Figure 8:** Clear, but omitting the B-spline because it was "timed in a separate protocol" leaves out the main comparator. A broken axis or an inset would fix this.
- **Table 2:** Good. "Siamese scorer, Relaxed 28" with "22/25*" is understandable.
- **Table 3:** Very informative and the best table in the paper.
- **Table 4:** Confusing. It merges two timing protocols with "–" fillers, and the same method (Diverse search, Exhaustive) has different times in the two halves (0.956 vs 0.265 s for Exhaustive on staging). This partly undercuts the cost argument.
- **Supplement:** Dense and hard to follow.
  - It uses a different naming scheme from the main paper, mitigated by a mapping table.
  - It includes a full "status protocol" study (S5, S6) that the paper says is not used in the main paper.
  - It contains many idiosyncratic details (hash orders, seeds, archive byte ranges). This is padding from the main paper's perspective.
- **LLM usage statement.** The statement is present and specific: Codex assisted with study design through manuscript drafting. I do not penalise this, but readers will appreciate that the numerical results are traceable to recorded analysis.

## 5. Questions for the authors

1. How does a uniform sub-lattice with spacing about r (or K evenly spaced shifts) compare with Diverse K and with complete Diverse search, under the same scorer? Does fit ordering contribute anything beyond coverage?
2. What happens to the B-spline comparison if the spline is initialised from the best wide-lattice translation (or from the Diverse-search output) instead of the ±4.2 mm original lattice?
3. What are the staging-cohort results with the exact annotated current mark as the query (the analogue of Table S7)? Is the 10.5-point gain over the spline retained?
4. How sensitive are reach and hits to r (for example 1.4, 2.1, 2.8, 3.5 mm) at fixed K and for the complete list?
5. Given that exhaustive scoring is only about 75 ms slower and is more accurate on staging, in what concrete setting do you expect diversification to be necessary? Can you show it with a heavier learned scorer, for example the frozen Siamese network scored over the full lattice?
6. How do results vary with lesion diameter and with interval size change? Is the 3 mm centroid tolerance meaningful for large metastases?

## 6. Most impactful fixable changes

**Using existing results and writing only (ranked):**
1. **Reframe the contribution honestly.** Make the main claim the wide lesion-aware candidate search (exhaustive or diversified), and present diversification as the efficient allocation for small budgets. State explicitly in the abstract and introduction that exhaustive scoring is more accurate on staging at about 1.4x the local cost. Qualify "19x faster" as local-step only, with an end-to-end saving of about 11%.
2. **State the search-extent confound up front.** Do this in Sec. 5.3 and in the abstract claim against the B-spline, and report the spline's results restricted to lesions whose reference lies within ±4.2 mm (computable from existing outputs).
3. **Move the exact-mark diagnostic into the main paper.** Bring Table S7 in, add a staging row if it is available, and soften "largest when the query is imprecise" to reflect the synthetic jitter.
4. **Remove redundancy and fix layout.** Keep Table 1 and one of Fig. 4 / Fig. 5. Drop Fig. S1 and S5-S6 from the supplement. Fix the empty space on pp. 10-11. Add a compact table defining all list variants and their thresholds. Use a single naming scheme in the main paper and the supplement.
5. **Fix Table 4 and Fig. 8.** Present one timing protocol in the main table and the other in the supplement. Add the B-spline to Fig. 8 via a broken axis. Round the fitted constants in Eq. 4.

**Requiring new experiments (up to 3):**
1. Uniform sub-lattice, random subsampling and fit-map local-minima baselines at matched K, plus an r sweep.
2. A fairer and broader registration comparison: a B-spline initialised from the wide lattice, at least one learned registration (uniGradICON or VoxelMorph), and SAM similarity used as a scorer feature.
3. Real queries (radiologist clicks or detector outputs), and a heavier learned scorer, to show the regime where diversification, not exhaustive scoring, is the right choice.

## 7. Scores

- **Overall:** 4 / 10 (plausible range 3-5). This is a careful, honest and statistically rigorous application study with a useful reach/selection lens. However:
  - the methodological novelty is small (greedy NMS over a translation lattice);
  - the central component, diversification, is outperformed or matched by exhaustive scoring at modest extra cost;
  - key allocation baselines are missing, and the registration comparison is confounded by search extent;
  - the scope (translation-only, one organ, hand-crafted scorer) is narrow for CVPR.

  It would fit better at MICCAI/IPMI or in a medical imaging journal, unless the generality claim is demonstrated.
- **Sub-scores:**

| Criterion | Score (1-10) |
|---|---|
| Novelty | 3 |
| Technical soundness | 6 |
| Experimental evidence | 6 |
| Clarity | 6 |
| Figures and tables | 6 |

- **Confidence:** 4 / 5
