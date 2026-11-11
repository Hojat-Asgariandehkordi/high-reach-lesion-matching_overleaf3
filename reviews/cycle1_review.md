# Review: "High-Reach Candidate Search for Longitudinal Lung Lesion Matching"

## 1. Summary

The paper looks at the local step of longitudinal lesion matching. After a global affine chest alignment, a query lesion in the current CT has to be found again in the earlier CT within a small residual window. Hypothesis-based matchers rank candidate translations by anatomical fit and pass the top-K to a lesion scorer. The authors argue that these top-K lists collapse onto a single fit mode. They propose "fit-ordered diverse search": greedy minimum-distance (r = 2.1 mm) suppression over the fit-sorted translation lattice (Alg. 1). Run to completion, this gives an r-net covering the lattice with about 365 of 4,851 translations (Eq. 3). Reach/selection accounting (Eqs. 5-6) splits the change in hits into a coverage term and a choice term. The evidence comes from two cohorts: an independent melanoma staging cohort (440 links) and a retrospective LUNA25/NLST screening cohort (309 tracks). At K = 28, diversification adds +9.1 and +12.0 points at 3 mm, and the whole gain comes from reach (Tab. 1, Fig. 4). The complete diversified list comes within 1.8 points of exhaustive scoring. It beats a lesion-inclusive B-spline by +10.5 / +10.7 points while running the local step about 19x faster (Tab. 2).

## 2. Strengths

- **Clear, well-isolated question.** The paper separates candidate allocation from candidate scoring, which is a real and under-examined design variable in hypothesis-based correspondence. Fig. 1 states the failure mode (fit-ranked top-K collapsing onto one mode) quickly and convincingly.
- **Useful reach/selection accounting.** Eq. 6 is trivially an identity, as the authors admit. Combined with the list-invariance property of Eq. 4 (Sec. 3.4, l. 283-288), it makes the decomposition interpretable. Fig. 4 and Tab. 3 use it well. The SAM result is the clearest example: its field reaches 396/440 but selects only 99, so a general embedding cannot exploit extra coverage.
- **Unusually careful evaluation hygiene.** Contrasts, margins and criteria were fixed before inference (l. 391-397). Paired patient-cluster bootstrap CIs are used throughout. All failures stay in the denominators. There is a native-mm and equal-patient-weight sensitivity analysis (Fig. 5) and an audit of reference centroids (l. 354-356). The paper is open about the screening cohort having been inspected earlier (l. 363-367).
- **A simple, cheap mechanism with a guarantee.** The covering bound in Eq. 3 is elementary but correct and practically meaningful. Every reference within 0.9 mm of the lattice is guaranteed a kept candidate within 3 mm.
- **Numbers are internally consistent.** I spot-checked about 20 figures across the abstract, Tabs. 1-3 and Secs. 5.1-5.6, and they all agree (e.g., 289 = 226 + 63; 45 - 1 - 4 = 40; the Table 3 rows sum to 440/309; the 18.6x and 20.9x speed ratios).
- **Honest limitations section** (Sec. 6), including the shrinking screening advantage when the query is the exact mark.

## 3. Weaknesses (most important first)

1. **The headline B-spline comparison is confounded and does not isolate the contribution.** Three things favor the proposed matcher over the spline independently of diversification:
   - (a) Diverse search ends with a *lesion scorer* that snaps to a lesion-like structure, whereas the spline maps the (perturbed) query point. When the exact mark is used as the query, the spline rises from 211 to 239 on screening while Diverse search stays at 243 (Sec. 5.4; Tab. S7). The advantage drops from 33 to 4 hits.
   - (b) The spline is initialized from the best translation on the *original* lattice (±4.2 mm), while Diverse search uses the *wide* lattice (±7 mm). The ">3 mm query error" band in Fig. 7 / Tab. S6 (spline 3/43 vs 12/43 hits) reflects search extent as much as method.
   - (c) Exhaustive scoring beats the spline by even more (Tab. 2). So the gain over registration comes from "lattice + lesion scorer", not from diversification. A "spline + local lesion-scorer refinement" comparator, or a spline initialized on the wide lattice, is needed before the +10 points can be attributed to the proposed design.
   The abstract and conclusion ("improves on lesion-inclusive B-spline registration by about 10 points") present this comparison as the main practical result without these caveats.
2. **Practical value over exhaustive scoring is thin.** Exhaustive scoring is the most accurate method on staging: +8 hits at 3 mm and +18 at 2 mm, with the interval [0.2, 3.5] excluding zero (Sec. 5.2, Tab. 2). It costs only about 0.07 s more per query in the replay timing (0.265 vs 0.194 s, Tab. S16). That is roughly 1.4x, while the paper emphasises scoring "7.5% of the shifts". End-to-end per-query time is dominated by the shared alignment (29.36 vs 32.87 s vs spline, Sec. 5.6). The case for diversification therefore rests on small fixed budgets (K ≤ 112). There the result is solid but expected, and the paper never motivates why such budgets are binding in practice.
3. **Missing the most natural ablation: a uniform sub-lattice.** Run to completion, an r-net over a dense lattice is close to a regular grid of spacing about r. The fit ordering only chooses which representative stands in for each ball. The authors list "a coarse sub-lattice" as future work (l. 589-590), but without it one cannot tell whether *fit-ordering* contributes anything at completion, or at K = 28 compared with a fit-agnostic stratified sample. This directly affects the novelty claim in contribution 1.
4. **Limited methodological novelty for CVPR.** Greedy minimum-distance suppression is NMS / farthest-point / r-net covering, which the paper itself cites (Sec. 2, l. 137-149). Its application to a fit-ranked shortlist is natural, and its benefit at small K is largely predictable once Fig. 1b is observed. The analysis contribution (Eq. 6) is an accounting identity. The paper's strength is careful empirical engineering for one clinical sub-task rather than a new technique of broad vision interest. The claimed transfer to "other point-correspondence problems" (l. 577-579) is untested.
5. **Simulated query drives much of the effect.** The query is the annotated mark jittered by up to 2.5 mm and then moved by a blob filter (l. 172-180). On screening the advantage almost disappears with the exact mark (Tab. S7), and the staging cohort is not rerun with exact marks (only screening is in Tab. S7). Neither cohort uses real clicks or detector outputs. The query model's fidelity therefore determines the size of the headline effect.
6. **Baselines are thin.** There is no learned registration (VoxelMorph/uniGradICON, cited in Sec. 2) and no reimplementation of LRR [23], which the paper calls the closest design (l. 100). The SAM checkpoint is trained on lymph-node CT, not tuned for lung, so its weak standalone result (99/440) is not very informative about embedding-based matching in general. The frozen Siamese scorer is the authors' own.
7. **Many hand-tuned constants, no sensitivity analysis on r.** Eq. 2 and Eq. 4 contain fixed constants (98 HU clip, 420 HU cap, 860/490 weighting, F = 76.958, W = 99.541, weight 1.5, shell 23-28 mm, r = 2.1 mm). r is the method's only real hyperparameter, yet there is no r sweep (deferred, l. 590-591). The covering bound suggests a direct tolerance/r trade-off that should be shown.
8. **Timing measurements are inconsistent across protocols.** Tab. 2 mixes times from the matched prepared-crop comparison and the fixed-budget replay (dagger rows). In the supplement, exhaustive scoring on staging is 0.956 s in Tab. S15 but 0.265 s in Tab. S16, a 3.6x discrepancy, and Diverse search p90 is 0.458 vs 0.199 s. The 18.6x speed claim uses the S15 protocol, while the exhaustive comparison uses S16. Fig. 8 likewise combines spline timing from one protocol with the others from another.
9. **Evaluation scope.** The staging cohort is 440 links from only 72 patients (about 6 per patient), drawn from one source. Hits are measured on centroids at 3 mm with no stratification by lesion size or growth/shrinkage, even though the paper motivates the task by lesion change (l. 194-196). 28 staging lesions fail before local search because of affine failure (Sec. 6, Tab. S7 text). That is fine for the denominators, but it caps all methods equally.

## 4. Clarity and presentation

- **Main paper.** The writing is generally clear and the problem framing (Sec. 1, Fig. 1) is strong. Sec. 3 reads well, and Alg. 1 and Eq. 3 are easy to follow. The math is light and readable. Eqs. 2 and 4 are cluttered by constants given to three decimals (F = 76.958 HU); these would read better as named, fitted scales.
- **Naming burden.** The paper juggles Fit-only K, Diverse K, Diverse search, Gated K, Relaxed K, Exhaustive, the "original" vs "wide" lattice, "direct" vs "SAM" scorer, "standalone" vs "crossing", and "routes". Tab. 1 rows such as "Gated, K 7→28 (SAM)" and "Gated 28, wider lattice" need several cross-references to decode. Sec. 4 "Matched workloads" mentions "fixed and adaptive search routes" (l. 432), which are never defined in the main paper.
- **Supplement mismatch.** The supplement uses a different vocabulary ("Original 7", "Wide strict", "Wide relaxed", "Wide ungated, diversified all", "Escalation", "archived route"), so mapping its tables to the main paper is laborious. It also contains large sections (S5, S6, Fig. S2, Tabs. S20-S24) on lesion-status / new-lesion detection protocols with insertion controls that the main paper never mentions. These look like residue from a different study and should be removed or explained.
- **Fig. 1** is excellent.
- **Fig. 2** is clear but schematic.
- **Fig. 3:** the inline "reach"/"hits" labels overlap the curves, and four series plus two reference markers in two small panels is crowded. It is still informative.
- **Fig. 4** is useful but small; the hatched selection bars are hard to read at print size.
- **Fig. 5** largely duplicates intervals already given in Tab. 1, the Tab. 2 caption and the text (and again in Fig. S1). This is redundancy rather than new information. One of Fig. 5 or Fig. 4 could be merged or cut.
- **Fig. 6:** the markers (circle, triangle, square, cross, star) overlap at this scale and are hard to tell apart in most columns. Zoomed insets or larger markers are needed. Only one failure case is shown.
- **Fig. 8** combines timing from two measurement protocols (caption), which undermines a single accuracy-latency plot.
- **Tab. 2** is the key table but mixes timing sources (daggers), uses "22 / 25*" mean-candidate notation, and the SAM GPU time is not comparable. Splitting accuracy and timing would help.
- **Tab. 3** is clear and effective.

## 5. Questions for the authors

1. How does a fit-agnostic uniform sub-lattice with spacing about r (a similar ~365 candidates, and a stratified 28-candidate version) compare with Diverse K and Diverse search? This determines whether fit-ordering matters at all.
2. What happens to the B-spline comparison if the spline is (a) initialized from the wide lattice, and (b) followed by a lesion-scorer refinement within a few mm of its mapped point? How much of the +10.5 points remains?
3. What are the staging-cohort results with the exact annotated mark as the query (the analogue of Tab. S7)?
4. Why do the exhaustive and Diverse-search timings differ so much between Tab. S15 and Tab. S16, and which protocol should readers trust for the 19x claim?
5. How do hits and the diversification gain vary with r (e.g., 1.4-4.2 mm) and with lesion diameter or interval volume change?
6. In what realistic deployment is a candidate budget of 7-28 binding, given that complete scoring of 4,851 translations costs about 0.27 s against about 29 s of shared alignment?

## 6. Most impactful fixable changes

**With existing results and writing only (ranked):**
1. Reframe the B-spline comparison honestly in the abstract, intro and conclusion. State that the gain partly comes from lesion snapping and wider search extent, and that exhaustive scoring beats the spline by more. Report the exact-mark result (33 → 4 hits on screening) next to the headline number, not only in Limitations.
2. Lead with the fixed-budget result (Tab. 1, Fig. 4) as the main contribution. Present Diverse search vs exhaustive as a modest accuracy/cost trade-off (about 1.4x faster, 1.8 points lower on staging) rather than "7.5% of the cost".
3. Make the timing consistent. Use one protocol in Tab. 2 and Fig. 8, or give both clearly, and reconcile the Tab. S15 / S16 discrepancy.
4. Unify naming between the main paper and the supplement (one mapping table). Remove or explicitly scope out the unrelated status-protocol material (S5, S6, Fig. S2, Tabs. S20-S24).
5. Cut redundancy: merge Fig. 5 into Fig. 4 or Tab. 1, and use the space for a larger Fig. 6 with more failure cases, and move the query-error stratification (Tab. S6) into the main text.

**Needing new experiments (ranked):**
1. A uniform / stratified sub-lattice baseline at matched K and at completion, plus an r sweep.
2. Stronger and fairer comparators: a wide-initialized spline with lesion-scorer refinement, a learned registration model (e.g., uniGradICON), and an LRR-style matcher.
3. Evaluation with real queries (radiologist clicks or detector outputs), including the staging cohort with exact marks.

## 7. Scores

- **Overall:** 4 / 10 (plausible range 3-5). The work is rigorous and transparent, with a clean diagnosis at small budgets. However, the technical novelty is modest, the main practical comparison is confounded, and the advantage over exhaustive scoring is small. In its current form it is below the CVPR bar. It might fit better at a medical-imaging venue after the comparator issues are addressed.
- **Novelty:** 3
- **Technical soundness:** 6
- **Experimental evidence:** 5
- **Clarity:** 5
- **Figures and tables:** 6
- **Confidence:** 4
