# Revision notes (applied to the group's Overleaf project)

`submission.tex` builds the compact CVPR version (the main text ends on page 7, 8 pages with references). `main.tex` builds the long version that includes the `*_expanded.tex` blocks. Like the original long version, it runs past 8 pages, so submit `submission.tex`.

The supplement (`supplement.tex`) is unchanged and still compiles. The revision only adds packages to the shared `preamble.tex`.

## Files changed
| File | Change |
|---|---|
| `preamble.tex` | Added packages: cuted, caption, multirow, algorithm, algpseudocode. Added macros `\TODO`, `\ours`, `\T`, `\Ss` and `\argmax` |
| `abstract.tex` | Rewritten to lead with the idea; about 6 numbers instead of about 15 |
| `intro_findings.tex` | Rewritten: problem, prior approaches, clumping observation, reach/selection framing, contribution list |
| `intro_expanded.tex` | Shortened to the compute paragraph (the reach material moved into the core intro) |
| `main.tex` | Teaser strip on page 1; related work rewritten (adds learned registration and NMS / diversity; SAM disambiguated); method rewritten with Algorithm 1, the residual, coverage and decomposition equations in the core paper, the 8 scorer features named, and a new route-definition table; evaluation tightened |
| `method_expanded.tex` | Keeps only the residual-support details; the equations moved into the core method |
| `evaluation_expanded.tex` | Removed sentences that are now in the core text |
| `results_text.tex` | Built around one main table; adds the qualitative figure and new plots; compact and expanded switches kept |
| `discussion.tex` | Split into discussion, limitations (now includes the exact-mark diagnostic) and conclusion |
| `refs.bib` | 6 new references appended at the end, with a comment marking them |
| `tables/main_results.tex` | **New.** All methods × Hit@2/3/4, Reach@3 and time, for both cohorts |
| `figures/teaser.pdf`, `method_overview.pdf`, `budget_reach.pdf`, `reach_selection.pdf`, `accuracy_latency.pdf`, `qualitative.pdf` | **New** figures |
| `scripts/` | **New.** Python scripts that regenerate every new figure; numbers are in `scripts/data.py` with source tables |

The old figure files are left in `figures/` so nothing breaks. In the main paper, `cohort_transfer`, `method_schematic`, `candidate_budget`, `reach_attribution`, `matching_time` and `fixed_budget_cost` are no longer used. `query_sensitivity` is still used in the long version.

Unused after the revision: `tables/tolerance_effects.tex` (its numbers now appear in `tables/main_results.tex` and the text).

## Open decisions for the group
1. **Qualitative figure is a placeholder** (red TODO). Export patches as described in `scripts/qualitative.py`, then run `python scripts/qualitative.py cases.npz`.
2. **Timing replays disagree.** Exhaustive staging time is 0.956 s in Supp. Tab. S15 and 0.265 s in Tab. S16. Choose the canonical replay.
3. **Limitations wording** on the exact-mark diagnostic (Supp. Tab. S7). Keep it as written or soften it, but agree as a group.
4. **LLM usage statement:** check it against the CVPR 2027 policy, and mention the AI help used for this revision.
5. **Verify the 6 new references** at the end of `refs.bib`.
6. **Optional:** add a learned-registration baseline (e.g. uniGradICON).
7. Before submitting, uncomment `\renewcommand{\TODO}[1]{}` in `preamble.tex`.
