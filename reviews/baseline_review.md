# Review: "High-Reach Candidate Search for Longitudinal Lung Lesion Matching"

## 1. Summary

The paper addresses point-query longitudinal lung lesion correspondence: given a lesion location in the current CT and a globally (affine) aligned earlier CT, find the same lesion in the earlier scan. Following the hypothesis-and-verify paradigm (LRR-style), candidate translations on a 3D lattice are ranked by an HU-based anatomical fit cost computed on an outer shell around the lesion, and a frozen lesion scorer (8-feature logistic regression plus a soft fit penalty, Eq. 4) picks one. The core proposal is to replace "top-K by fit" with a greedy minimum-distance (NMS-style) walk down the fit-ordered list (Alg. 1, r = 2.1 mm), which yields a covering bound (Eq. 3), plus a reach/selection accounting (Eqs. 5-6) that attributes hit changes to candidate coverage versus scorer choices. On 440 metastases from an independent staging cohort and 309 LUNA25/NLST screening nodules, the complete diversified list reaches 65.7% / 79.0% hits at 3 mm versus 55.2% / 68.3% for a lesion-inclusive B-spline (Tab. 1), and diversification alone at K=28 adds +9.1 / +12.0 points over fit-only top-28 (Tab. 2), with roughly 19x lower prepared-crop latency than the spline.

## 2. Strengths

- **Clear, well-posed observation.** The point that top-K by fit collapses onto near-duplicates of one mode (Fig. 1b, Sec. 3.3) is intuitive and well illustrated, and the fix is simple, cheap and easy to reproduce.
- **Careful statistical practice.** Patient-clustered paired bootstrap intervals (Sec. 4), success criteria and primary contrasts fixed before inference (lines 394-400, 358-362), all failures kept in the denominator, and robustness checks (equal patient weight, native-mm evaluation, Fig. 3 top) are better than is typical for this application area.
- **The reach/selection decomposition is useful for diagnosis.** Tab. 2 and Fig. 7 make it clear *where* gains come from, e.g. that enlarging the cap helps the direct scorer through reach but SAM loses more on shared lesions than it gains (lines 514-522). This is a good analysis habit that others could adopt.
- **Two cohorts with different populations** (metastases vs. screening nodules, different sources), with consistent direction of effect at every tolerance (Fig. 3).
- **Honest limitations section.** The authors themselves report the query-sensitivity result (screening advantage shrinks from 33 to 4 hits with the true mark, lines 477-483; Tab. S7), that end-to-end time is dominated by chest alignment (lines 540-545), and that learned registration was not compared (line 570).

## 3. Weaknesses (most important first)

1. **Limited methodological novelty for CVPR.** The proposed selection rule is greedy non-maximum suppression with a fixed radius on a score-ordered list (the paper itself says so, line 58 and Sec. 2 "Diversity in candidate generation"). The coverage guarantee in Eq. 3 is the standard r-net/covering property of greedy NMS and follows in two lines. The decomposition in Eq. 6 is an identity that holds for *any* two methods (hits are only possible on reachable lesions); only the *interpretation* of the selection term depends on the scorer property discussed at lines 278-283. Calling it "an exact reach/selection decomposition" as a contribution (lines 080-082) overstates it. The contribution is mainly an empirical finding for one application pipeline, which is a better fit for MICCAI / MedIA than for CVPR unless a broader lesson is shown.

2. **The headline gain over the spline is not mainly due to diversification, and the paper's own numbers show that.** Exhaustive scoring of all 4,851 translations beats Diverse search on staging at every tolerance (277/297/311 vs 259/289/306, Tab. 1; +1.8 [0.2, 3.5] at 3 mm, lines 461-464) and costs only 0.265 s vs 0.194 s. So at full budget, diversification is a ~1.4x compute saving at a small but significant accuracy cost, and the "+10.5 over B-spline" is a property of the lattice + fit + scorer pipeline, not of the proposed rule. The abstract and contributions bundle these two claims together; the cleanly attributable effect of the contribution is the fixed-budget K=28 result (+9.1 / +12.0), where Diverse 28 (245) merely ties the spline (243).

3. **The fixed-budget baseline is a straw man; obvious alternatives are missing.** The only fixed-budget comparator is fit-only top-K, which by construction spends its budget on neighbours one voxel apart. Natural alternatives that also spread a budget are not evaluated: a uniform coarse sub-lattice (e.g. stride ~2-3 voxels, which provides the same r-cover without fit ordering), top-K from a coarse-to-fine lattice, farthest-point sampling restricted to a fit threshold, random subsampling from the top fraction, or local-minima (mode) extraction of the fit-cost map. Without these, it is unclear whether fit ordering matters or simply spatial spreading. There is also no sensitivity analysis on r in the main paper, although r = 2.1 mm vs τ = 3 mm directly determines the coverage bound.

4. **Weak and possibly under-configured comparators.** (a) The B-spline is a 3x3x4 control mesh within 22 mm, *initialized from the best exhaustive translation on the smaller original lattice* (lines 371-375). It is therefore not independent of the discrete search, and its initialization cannot exceed ±4.2 mm, which helps explain its 3/43 hits for queries >3 mm off (Tab. S6). (b) SAM standalone gets 99/440 hits at 3 mm while its similarity field reaches 396 (Tab. 1). That gap is large enough to suggest a domain or preprocessing mismatch (the checkpoint was trained on NIH Lymph Node, lines 377-379), so the conclusion that "a general anatomical embedding does not benefit from extra candidates" (lines 553-556) rests on a possibly mis-adapted model. (c) No learned registration (VoxelMorph, uniGradICON) and no lesion-tracking method (DLT, TLT, LRR) is run; the justification (line 129-133, Sec. S3) is about missing weights, but a re-implementation or at least LRR-style candidate generation would be expected.

5. **A large share of the gain is robustness to a simulated query.** The query is synthetic (jitter up to 2.5 mm plus a blob detector within 6 mm, lines 169-177). With the true mark, the screening advantage over the spline drops from 33 hits to 4 (lines 477-483, Tab. S7). Fig. 5 shows the staging gain concentrated in the >3 mm query-error band (+~20 points, n=43). The practical value therefore depends strongly on how realistic the query-error distribution is, and no real detector outputs or reader clicks are evaluated.

6. **The replication cohort is not truly held out.** The screening patients "had been inspected earlier in the project" (lines 367-370), and the development set is small (145 tracks from 100 patients). The paper is transparent about this, but it weakens the "replicate" framing, leaving one independent cohort with 72 patients.

7. **The compute claim is local-only.** "About 19 times faster" (abstract, line 026) refers to the prepared-crop step; end-to-end native time is 29.36 s vs 32.87 s per query (lines 540-543), i.e. ~11% faster. The abstract should say so.

8. **Evaluation granularity.** Hit@3 mm on centroids is applied uniformly to lesions of very different sizes (Fig. 4, rightmost failure is a large lesion). No breakdown by lesion size, lesion growth/shrinkage, or location (juxtapleural vs. central) is given, even though the fit cost deliberately excludes the lesion and the scorer uses lesion appearance. Resolved or new lesions are excluded by design (lines 557-559).

## 4. Clarity and presentation

- **Writing.** The introduction and Sec. 3.1-3.5 are mostly readable, and Figs. 1-2 convey the idea well. However, the paper uses a large, inconsistent taxonomy of internal configuration names ("Original 7", "Original 28 + fit", "Wide strict", "Strict K", "Relaxed K", "Cap 7→28, direct", "gates", "Wide relaxed 28 + Siamese", ...). Sec. 3.6 and especially the "Residual support details" paragraph (lines 337-346: "strided centers", "safe shell centers", "a subset of the original 824 samples per sector") are close to unreadable without the supplement and read like lab notes. The supplement is even more so. Much of this can be cut or moved, since the main story needs only Fit-only K, Diverse K, Diverse search, and Exhaustive.
- **Naming inconsistency.** Fig. 3 labels "Cap 7→28, direct/SAM" correspond to Tab. 2 "Strict 7→28, direct/SAM"; Fig. 6 uses "Wide strict", which is never defined under that name in the main text.
- **Math.** Eqs. 1-6 are simple and correct. Eq. 4's normalizers F and W are described only as "residual limits fitted on development data" (lines 276-277) without values in the main text. The 1.5 coefficient is unexplained. Eq. 2's weight is fine but would benefit from one sentence on why these constants.
- **Table 1** mixes timing sources (direct timings, fixed-budget replays marked †, and a GPU forward pass for SAM marked ‡) in one column. This makes the column not directly comparable, and the SAM time in particular should not sit next to CPU times. "22 / 25" candidates for the Siamese row is unexplained in the main text.
- **Table 2** is dense; the "+/−" column is useful but unlabeled in the header beyond the caption.
- **Fig. 6** is informative, but the reach-vs-hit distinction relies on dashed vs solid lines at small size; the "Exh." triangles and the fit-only diamond are hard to see.
- **Fig. 8** is the weakest figure: the "28"/"All" annotations are tiny, the diverse-K curve is compressed into a small region at the left of a log axis, and the single B-spline point is far right. A table or a linear inset would communicate this better.
- **Fig. 4** is good qualitatively but would benefit from showing the fit-only top-K candidates alongside the diversified ones, which is the paper's actual point.
- **Redundancy.** The same numbers (+10.5, +9.1/+12.0, 19x, one-thirteenth) are repeated in the abstract, contributions, Sec. 5, Sec. 6 and the conclusion; some of this could be trimmed in favour of the missing analyses.

## 5. Questions for the authors

1. How does Diverse K compare with a uniform sub-lattice of matching size (e.g. stride chosen so that the cell count is about K), and with extracting local minima of the fit-cost map? Does fit ordering matter beyond spatial spreading?
2. How sensitive are reach and hits to r (e.g. 1.4, 2.1, 2.8, 3.5 mm) at fixed K and for the complete list? Was r = 2.1 mm chosen on development data?
3. Given that Exhaustive is significantly better than Diverse search on staging (+1.8 points) at only ~70 ms extra, in what operating regime do you recommend the complete diversified list over exhaustive scoring?
4. Why is the B-spline initialized from the original (±4.2 mm) lattice rather than the wide lattice, and how does a spline initialized from the wide-lattice best translation (or from Diverse search's output) perform?
5. Can you explain the SAM standalone result (99 hits vs 396 reach)? Did you check SAM's preprocessing and the coarse-to-fine matching on a few cases, and would a SAM variant trained on chest CT change the conclusion in lines 553-556?
6. Do you have any real-query data (detector outputs or reader clicks), even on a subset, to validate the simulated query-error distribution that drives much of the gain?

## 6. Most impactful fixable changes

**Without new experiments (ranked):**
1. Reframe the claims to separate the two results: (a) diversification gives +9-12 points at a fixed budget over fit-only top-K, and (b) the lattice+scorer pipeline beats this particular spline. State plainly in the abstract that exhaustive scoring is slightly better at full budget, and that the speedup is local-only (~11% end-to-end).
2. Downgrade Eq. 3 and Eq. 6 from "contributions" to "analysis tools", acknowledging that Eq. 3 is the standard greedy-NMS covering property and that Eq. 6 is an identity whose selection-term interpretation relies on the scorer property.
3. Collapse the configuration taxonomy in Sec. 3.6, Tab. 2 and Figs. 3/6/7 to a few consistently named variants; move "Residual support details" to the supplement.
4. Fix Table 1's timing column (separate CPU and GPU timings, single timing protocol or a clear footnote) and explain the Siamese "22 / 25" candidates.
5. Move the query-sensitivity result (Tab. S7, Fig. 5) and the B-spline initialization caveat more prominently into the main results discussion, since they qualify the headline comparison.

**Needing new experiments (ranked):**
1. Fixed-budget baselines that also spread candidates (uniform sub-lattice, fit-map local minima, FPS within a fit threshold) plus an r sweep.
2. Stronger, independent comparators: a learned registration model (e.g. uniGradICON, which has public weights), a spline initialized independently of the discrete search, and an LRR-style re-implementation.
3. Evaluation with real queries (detector outputs or reader clicks) and a breakdown by lesion size and location.

## 7. Scores

- **Overall: 4 / 10** (plausible range 3-5). A carefully evaluated, honest, but incremental application study. The proposed rule is standard NMS with a trivial covering bound; the main accuracy claim over the spline is not attributable to it; comparators are weak; and a sizable part of the gain comes from robustness to a simulated query. It is better suited to a medical imaging venue in its current form.
- **Novelty:** 3
- **Technical soundness:** 6 (statistics and accounting are sound; baseline construction and attribution of claims are the problems)
- **Experimental evidence:** 5
- **Clarity:** 4
- **Figures and tables:** 6
- **Confidence:** 4
