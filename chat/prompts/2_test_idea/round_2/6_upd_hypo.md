# upd_hypo — test_idea

> Phase: `invention_loop` · round 2 · `upd_hypo`
> Run: `run_Br8Nz-7w30tX` — Taylor's Power Law for LLM Error Clustering: A Hypothesis Not Sustained by Data
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `upd_hypo` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-08-01 15:20:37 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A hypothesis reviser (Step 3.6: UPD_HYPO in the invention loop)

You received the current hypothesis, all artifacts, and the paper draft.
Revise the hypothesis based on what the evidence supports.

Honest revision → focused research. Inflated confidence → wasted iteration.
</your_role>
</ai_inventor_context>

You are revising a research hypothesis based on empirical evidence gathered
during an iterative invention loop. Your role is internal reflection — honest
assessment of what the evidence supports.

SCOPE: Your ONLY output is the revised hypothesis text. You do NOT run code,
produce artifacts, fix bugs, or otherwise act on the evidence yourself — the
next iteration of the invention loop will spawn fresh artifacts based on your
revised hypothesis. Reflect on the evidence and rewrite the hypothesis;
nothing else.

PRINCIPLES:
- Ground every revision in specific artifacts and results
- Treat negative and null results as valuable contributions. If the original
  approach failed, the null result IS often the contribution — frame it as
  such (e.g. "X does not improve Y under conditions Z"). Only pivot to a
  different positive claim when the evidence actually supports one; never
  fabricate a positive narrative to mask a failed approach.
- Increase specificity as evidence accumulates
- Don't inflate confidence without strong evidence
- Preserve the core AII prompt unless evidence clearly contradicts it
- Revise hypothesis text only — never attempt to address feedback by running
  code, proposing fixes, or producing artifacts; the next loop iteration
  handles all artifact generation

<current_hypothesis>
The hypothesis as it stands. Revise it based on the evidence below.

kind: hypothesis
title: Ecology's Clustering Law Predicts Vote Failure
hypothesis: >-
  For a fixed LLM and prompting scheme, the fluctuation-scaling exponent b obtained by fitting Taylor's power law (log Var[correctness]
  = log a + b * log Mean[correctness], measured across many problems by repeated sampling) is a reliable, task-agnostic diagnostic
  of whether majority-vote/self-consistency aggregation will help or hurt on that problem population: exponent values near
  b=1 (independent, Poisson-like error scatter) mark regimes where voting reliably improves accuracy, while elevated exponents
  (b appreciably above 1, indicating clustered, correlated error patterns akin to aggregated populations in ecology) mark
  regimes where voting yields little gain or actively hurts accuracy versus single-sample decoding. This claim remains UNTESTED
  empirically as of this iteration -- only a literature synthesis and a benchmark dataset (GSM8K, MMLU, ARC-Challenge) exist
  so far, with no sampling, fitting, or voting-gain code executed -- so all specific numeric predictions below are provisional
  targets for the next iteration's experiment, not established results. Three refinements from this iteration's review must
  shape that experiment: (1) the exponent must be validated against a noise floor -- before trusting any fitted b, the next
  iteration must show, via a null simulation of purely independent Bernoulli problems at the same per-problem sample count
  N (~20-30) and problem count, that the real data's b is not explainable by binomial sampling noise alone, and must justify
  (or relax) excluding m_p in {0,1} rather than discarding exactly the easy/hard extremes where voting's known failure mode
  (per-problem success <0.5 amplifying errors) is most diagnostic; (2) the practical decision rule (b thresholds) must be
  scoped explicitly to the accuracy range actually tested (roughly 60-95%) and not claimed as general until a low-accuracy
  (<50% per-problem success) benchmark is added to test the mapping in the error-amplification regime; (3) the novelty claim
  relative to the two-call/second-moment theory (which already argues the second moment of the latent correctness distribution
  determines voting gain) must be sharpened by showing Taylor's b either needs fewer samples for comparable predictive power
  than the two-call estimator, or captures cross-stratum/cross-benchmark comparability that a raw second-moment estimate does
  not -- otherwise it is a relabeling, not a new diagnostic.
motivation: >-
  Practitioners currently decide whether to spend extra inference compute on self-consistency/majority-voting largely by trial
  and error per task, because current theory (e.g. de Finetti/voting-curve analyses) explains WHY voting can be non-monotone
  in the abstract but gives no cheap, measurable statistic a practitioner can compute from a small calibration sample to decide,
  for a NEW task or model, whether voting is worth the extra API spend. Taylor's power law is one of the most extensively
  validated empirical regularities for diagnosing whether variability in a population is driven by independent individual-level
  noise (b near 1) versus shared, correlated disturbances that cluster individuals together (b greater than 1) - exactly the
  same clustering-versus-independence distinction that determines whether repeated LLM samples behave like independent draws
  (voting helps) or like correlated draws sharing one latent failure mode (voting cannot help, since resampling just re-elects
  the same wrong answer). If the exponent transfers, it gives a cheap, single-number, pre-registered stopping rule for test-time
  compute allocation.
assumptions:
- >-
  Per-problem correctness across repeated LLM samples at fixed temperature can be treated as a set of exchangeable Bernoulli-like
  draws whose problem-to-problem mean and variance can be estimated from a modest number of repeated samples (e.g. 10-30)
  per problem.
- >-
  A benchmark or problem population exists with enough graded variation in difficulty/ambiguity that mean accuracy per problem
  spans a wide range (near 0 to near 1), which is required to fit a variance-mean power law across problems.
- >-
  The scaling relationship is approximately log-linear over the accessible mean-accuracy range, as is empirically true for
  Taylor's law in most tested biological and non-biological systems.
- >-
  The mechanism generating elevated b (shared systematic failure modes: e.g. a consistent misreading of the prompt, a memorized-but-wrong
  fact, a flawed heuristic the model always reaches for) is distinguishable in effect from independent stochastic slips, even
  though both are observed only through sampling variance.
investigation_approach: >-
  Using several open LLMs served via OpenRouter and several reasoning/QA benchmarks spanning a wide difficulty range (e.g.
  GSM8K-style arithmetic, MMLU-style factual QA, and a logic/puzzle set), sample each problem N times (~20-30) at a fixed
  temperature to estimate per-problem mean and variance of correctness. Fit Taylor's power law (log-log regression of variance
  on mean) per (model, benchmark) pair to obtain the exponent b and its confidence interval. Independently measure the actual
  gain or loss from majority voting (accuracy at k samples via majority vote minus accuracy at 1 sample) as a function of
  k, for the same (model, benchmark) pairs. Test the hypothesis by checking whether b predicts the sign and magnitude of the
  voting gain across (model, benchmark, and problem-difficulty-stratified subset) combinations, including held-out combinations
  not used to calibrate the b-to-voting-gain mapping. As a mechanistic probe, for a sample of high-b problems, cluster the
  wrong answers produced across repeated samples (e.g. by embedding similarity) to check whether they collapse onto one or
  few dominant wrong answers (consistent with a shared latent failure mode) versus scattering diffusely (which would falsify
  the clustering interpretation of high b).
success_criteria: >-
  Confirms if: (1) b reliably separates voting-helps versus voting-hurts/no-gain regimes across held-out (model, benchmark,
  difficulty-stratum) combinations with a statistically significant correlation (e.g. Spearman rho with a preregistered threshold,
  such as |rho| > 0.5, p < 0.05) between b and the measured voting gain; and (2) the wrong-answer clustering probe shows that
  high-b problem sets have systematically more concentrated (lower-entropy) wrong-answer distributions than low-b problem
  sets, supporting the mechanistic interpretation rather than b being a spurious statistical artifact. Disconfirms if b shows
  no consistent relationship to voting gain across models/benchmarks, if the relationship only holds within a single model
  or benchmark and fails to transfer, or if wrong-answer clustering does not track b.
related_works:
- >-
  'When Can Voting Help, Hurt, or Change Course? Exact Structure of Binary Test-Time Aggregation' (arXiv 2605.05592) uses
  de Finetti representation theory to show voting curves can be non-monotone and that the curve alone cannot identify the
  underlying correctness-probability distribution; it is a structural/identifiability analysis, not a cheap empirical diagnostic
  a practitioner can compute from a calibration sample to decide whether to vote on a new task -- the proposed hypothesis
  supplies exactly that missing operational statistic (the Taylor exponent) and tests whether it transfers across models and
  tasks.
- >-
  Work on self-consistency and majority voting for LLM reasoning (the original self-consistency decoding method, and later
  analyses showing majority voting can amplify errors when per-problem success probability is below 0.5) establishes empirically
  that voting sometimes helps and sometimes hurts, but selects whether to vote using post-hoc accuracy comparison rather than
  a pre-registered, sampling-cheap summary statistic computed independent of ground-truth labels being available for the target
  task.
- >-
  Taylor's power law of fluctuation scaling (Taylor 1961 and its extensive ecological/statistical literature, including work
  confirming it across thousands of biological and non-biological populations) establishes the variance-mean exponent as a
  general diagnostic of aggregation/clustering versus independence in population counts; it has not previously been applied
  to LLM sampling variability as a test-time-compute allocation diagnostic, which is the cross-domain transfer this hypothesis
  makes concrete and falsifiable.
- >-
  'Taylor's law for Human Linguistic Sequences' (ACL 2018 / arXiv 1804.07893) applies Taylor's law to word-frequency fluctuation
  statistics within corpora as a description of linguistic structure; it studies static corpus statistics rather than an LLM's
  own repeated-sampling error correlation as a live, task-specific predictor of test-time aggregation gain, so its use of
  the exponent targets a different object (corpus word counts) and a different purpose (linguistic characterization, not compute-allocation
  decision-making).
inspiration: >-
  CONCEPTUAL: population ecology treats variance-to-mean scaling as a signature of whether individuals in a population fluctuate
  independently or are clustered by a shared external driver (weather, resource patches) -- the same lens reframes 'does resampling
  an LLM give independent tries or correlated tries pulled by one shared failure mode' as a directly measurable clustering
  question instead of a black-box property inferred only after building the whole voting pipeline. METHODOLOGICAL: the specific
  technique imported is Taylor's power law fitting itself (log-log regression of the variance of a quantity against its mean
  across many sub-populations, and reading the slope b as an aggregation index) -- a decades-validated, cheap, off-the-shelf
  statistical tool from ecology and epidemiology that has apparently never been pointed at LLM self-consistency sampling despite
  being a near-perfect fit for the independence-versus-correlation question that determines when voting works.
terms:
- term: Taylor's power law (fluctuation scaling)
  definition: >-
    An empirical relationship, first described in ecology, stating that the variance of a quantity measured across many sub-populations
    scales as a power-law function of its mean: Var = a * Mean^b. The exponent b indicates whether fluctuations are driven
    mostly by independent, individual-level randomness (b near 1, Poisson-like) or by shared, correlated disturbances that
    cause clustering (b appreciably greater than 1).
- term: Self-consistency / majority voting
  definition: >-
    A test-time compute technique where an LLM is sampled multiple times on the same problem (usually at nonzero temperature)
    and the most common answer across samples is taken as the final output, intended to average out random per-sample errors.
- term: Per-problem correctness mean and variance
  definition: >-
    For a single problem, the fraction of repeated LLM samples that are correct (the mean) and how much that correctness fluctuates
    across repeated samples and across repeated batches (the variance); measured empirically by sampling the same problem
    many times.
- term: Shared latent failure mode
  definition: >-
    A single underlying cause (e.g. a consistent misreading of the problem, a memorized wrong fact, a flawed default heuristic)
    that makes many or most of an LLM's repeated samples on a given problem land on the same wrong answer, as opposed to each
    sample failing for an unrelated, independent reason.
- term: Voting gain
  definition: >-
    The change in accuracy obtained by aggregating k repeated samples via majority vote compared to using a single sample,
    measured as a function of k for a given model and problem set.
summary: >-
  This hypothesis proposes importing Taylor's power law -- ecology's standard variance-mean scaling exponent for telling independent
  from clustered population fluctuations -- as a cheap, pre-registered diagnostic that predicts, from a small calibration
  sample, whether majority-vote/self-consistency test-time compute will help or hurt on a given LLM-and-task combination.
_relation_rationale: >-
  Same core claim, now scoped as untested pending real experiments; added noise-floor, range, and novelty conditions
_confidence_delta: decreased
_key_changes:
- >-
  Flagged that no experiment (sampling, exponent fitting, voting-gain measurement, entropy probe) has actually been run; only
  literature review and dataset prep exist -- all Results-section numbers in the paper draft were fabricated and must be removed
  until traceable to real code output
- >-
  Added a required noise-floor validation step: simulate independent-Bernoulli null data at matching N and problem count and
  show real b is not explainable by sampling noise alone
- >-
  Added a requirement to justify or relax exclusion of m_p in {0,1}, since those are the problems most informative about voting's
  known failure regime (success probability <0.5)
- >-
  Scoped the practical decision rule's claimed validity to the tested accuracy range (~60-95%) rather than presenting it as
  general, pending a low-accuracy benchmark test
- >-
  Added a novelty-sharpening requirement: show Taylor's b is cheaper or more transferable than the existing two-call second-moment
  estimator, not just a relabeling of it
- >-
  Confidence decreased because the reviewer found the entire empirical section was unsupported by any executed artifact
relation_type: evolution
</current_hypothesis>

<all_artifacts>
Complete set of research artifacts across all iterations.

--- Item 1 ---
id: art_PyaRZoyCdMFV
type: research
title: 'Taylor''s Law as Voting Diagnostic: Comprehensive Literature Review & Methodology'
summary: |-
  This research synthesizes five critical knowledge domains to establish theoretical and methodological foundations for testing whether Taylor's power-law exponent (b), computed from repeated LLM sampling, can serve as a diagnostic for when majority voting helps LLM accuracy.

  **Voting Theory Foundation (de Finetti & Non-Monotone Curves):** Classical voting theory assumed monotone behavior, but recent work shows voting can help, hurt, or reverse direction depending on latent correctness distribution. De Finetti representation for exchangeable repeated correctness reveals voting curves determined by per-example success-probability distribution. Signed voting signatures uniquely characterize voting behavior. Critical finding: when per-problem correctness < 0.5, majority voting amplifies errors. Two-call theory predicts voting gain from just mean and second moment without large-scale sampling [1, 2].

  **Taylor's Law in Ecology & Universality:** Taylor's power law (Var = a * Mean^b) from 1961 ecology relates population variance to mean through power law. Exponent b ∈ [0.8, 2.0] typically; b ≈ 1 indicates Poisson/independence; b > 1 indicates clustering from shared drivers. Confirmed across hundreds of species. In linguistics, applied to 1100+ texts across 14 languages yielding universal b ≈ 0.58 for written text, 0.63 adult speech, 0.68 child speech, 0.79 code/music [3, 4, 5]. Cross-domain consistency suggests Taylor's law captures fundamental system properties [5].

  **LLM Error Correlation (Non-Independence):** LLM errors are NOT independent—they are substantially correlated, with accurate models showing higher correlation than weaker ones [6]. This violates Poisson assumptions underlying classical voting theory. Variance decomposes into within-prompt resampling (~35%), prompt paraphrase, model identity, language choice; systematic factors dominate [7]. Temperature affects consistency/diversity but not per-call accuracy [8, 9]. Standard sampling protocol: fixed temperature 0.7-0.8, N=20-30 samples per problem [19, 20].

  **Error Diversity Predicts Voting Benefit:** Intra-group error diversity (how dispersed wrong answers are) strongly predicts voting gain—problems with diverse wrong answers benefit more from aggregation [10]. Embedding-based clustering has known limitations (anisotropy, low geometric separation, semantic ambiguity) but alternative methods exist (syntactic, entailment-based) [11, 12]. For mechanistic validation, entropy of wrong-answer distribution should track Taylor's exponent: high-b problems (clustered errors) should show lower entropy [10].

  **Voting Aggregation Methods & Metrics:** Two-call theory yields distribution-free voting accuracy intervals at any budget k (k=3, 5, 10) with width ≤ 1/8 [2]. Ranked voting offers modest gains over plurality [13]. Confidence-weighted voting best when calibrated [13]. Advanced methods (Optimal Weight, Inverse Surprising Popularity) leverage higher-order information and provably exceed majority voting [13]. Voting saturates quickly; pass@k continues improving [1, 2].

  **Benchmarks & Difficulty Stratification:** GSM8K (8.5K problems, easy 91.2% accuracy, hard 66.7%) [14]; MMLU (57 domains, 4-level difficulty) [14]; MATH (competition-level, hardest Level 5) [14]. Combined span 66.7%-91.2% accuracy, enabling difficulty-stratified testing [14]. All available on HuggingFace with open licenses [21].

  **Computational Budget & Model Selection:** OpenRouter offers 300+ models [16]. Budget for $10: 1,000 problems × 20-30 samples ≈ $5-7.50 cost. Recommended mix: 1× small (7B), 1× mid (13-32B), 1× large (70B+) for transfer testing [16].

  **Taylor's Law Operationalization:** Log-log regression on (log mean, log variance) across problems yields exponent b with 95% CI [17]. Bernoulli variance v_p = m_p(1 - m_p) where m_p = correctness mean [18]. Edge case handling: exclude m_p = 0 or 1 (zero variance); log(0) carefully [17].

  **Hypothesis & Success Criterion:** High b (≥ 1.5) proxies correlated errors → low voting gain. Low b (≈ 1.0) proxies independent errors → high voting gain. Spearman ρ test: |ρ| > 0.5, p < 0.05 [1, 2]. Must transfer to held-out (model, benchmark, difficulty) combinations. Mechanistic probe: entropy of wrong answers in high-b problems should be lower than low-b [10].

  **Novel Gap:** No published work applies Taylor's law to LLM sampling to predict voting gain. This cross-domain hypothesis offers a cheap, pre-registered diagnostic (compute b once, predict voting benefit) vs. post-hoc voting comparison.
workspace_path: >-
  /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_Br8Nz-7w30tX/3_invention_loop/iter_1/gen_art/gen_art_research_1
out_expected_files:
- research_out.json

--- Item 2 ---
id: art_-jn9Gvt0zmil
type: dataset
title: 'Three Reasoning Benchmarks: Math, Knowledge, Science'
summary: >-
  Standardized dataset of three complementary reasoning benchmarks downloaded from HuggingFace Hub: GSM8K (openai/gsm8k, config=main,
  split=test, 1,319 grade-school arithmetic word problems requiring 2-8 step reasoning, free-response numeric answers), MMLU
  (cais/mmlu, config=all, split=test, 14,042 multiple-choice questions spanning 57 subjects across STEM/social sciences/humanities),
  and ARC-Challenge (allenai/ai2_arc, config=ARC-Challenge, split=test, 1,172 multiple-choice grade-school science reasoning
  questions). All three are established, high-download (>150k-900k+ downloads), well-documented HuggingFace benchmarks with
  clear dataset cards, confirmed provenance, and published baseline accuracies (~60-70%), giving orthogonal reasoning modes
  (arithmetic, factual/multidisciplinary recall, science logic) with the difficulty variation the downstream power-law-fit
  experiment needs. Total 16,533 examples across the three datasets. Output schema follows exp_sel_data_out.json: a top-level
  object with a `datasets` array, each entry `{dataset: <name>, examples: [...]}`; every example has `input` (question text,
  with lettered A/B/C/D choices appended inline for MC datasets) and `output` (ground-truth answer: final numeric answer string
  for GSM8K, choice letter for MMLU/ARC-Challenge), plus flat `metadata_*` fields per example (metadata_row_index, metadata_task_type,
  metadata_question_length_chars, and dataset-specific fields like metadata_subject for MMLU, metadata_reasoning_steps/metadata_full_solution
  for GSM8K, metadata_problem_id/metadata_choice_texts/metadata_n_classes for ARC-Challenge). Six candidate datasets (GSM8K,
  MMLU, ARC-Challenge, HellaSwag, CommonsenseQA, OpenBookQA) were downloaded, previewed, and standardized; the final three
  were selected as the best match for the artifact plan's explicit criteria (orthogonal reasoning modes + documented difficulty
  spread for a power-law fit), dropping HellaSwag/CommonsenseQA/OpenBookQA as redundant commonsense-reasoning coverage outside
  the plan's named triad. data.py (a uv inline-script, stdlib+loguru only) reproduces the full pipeline from temp/datasets/
  raw HuggingFace downloads to full_data_out.json. Output validated against the exp_sel_data_out.json schema (PASSED). full_data_out.json
  is 16MB, well under the 100MB split threshold, so no splitting was needed. mini_data_out.json (9 examples, 3 per dataset)
  and preview_data_out.json (same 9 examples, strings truncated to 200 chars) are provided for quick inspection. pyproject.toml
  pins the single runtime dependency (loguru==0.7.3) for reproducibility. Downstream steps can load full_data_out.json directly
  to get per-example question/answer pairs with rich metadata for difficulty stratification, sampling, and evaluation.
workspace_path: >-
  /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_Br8Nz-7w30tX/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json

--- Item 3 ---
id: art_mBThrQVRQRjk
type: evaluation
title: Does Voting Gain Follow the Taylor Exponent?
summary: >-
  This evaluation loads the real EXPERIMENT artifact output (gen_art_experiment_1/method_out.json: 3 models x 3 benchmarks
  x 10 problems x 5 repeated samples = 90 problems, 450 raw samples) and tests whether the Taylor power-law exponent b predicts
  self-consistency voting gain. Because the EXPERIMENT only fits b at the (model, benchmark) granularity (9 combos, 3 with
  a degenerate/null fit from too few valid problems in this budget-scaled run), two complementary analyses are reported: (1)
  combo_level_spearman -- the literal plan-specified test of fitted b vs. aggregate voting gain across the 5 valid (model,
  benchmark) combos (rho=-0.90, p=0.037, but n=5 is severely underpowered, flagged explicitly); (2) a per-problem analysis
  using od_p = v_p_empirical/(m_p(1-m_p)), the real per-problem overdispersion ratio (the finest-grained analog of b available,
  since true per-problem b is undefined), against real per-problem voting gains recomputed from raw correctness_samples via
  majority vote. On this n=90 basis the evaluation implements the full artifact plan: within-benchmark Spearman rho with 10k-iteration
  bootstrap CIs at k=5 (and secondary k=3,10), a 60/40 stratified calibration/holdout linear-regression transfer test with
  attenuation factor, cross-benchmark transfer (train on GSM8K, test on MMLU/ARC-Challenge), difficulty-stratified (low/medium/high
  m_p tercile) correlations with Holm-Bonferroni FWER correction, a noise-floor gate using the EXPERIMENT's own per-combo
  null-simulation p-values, DerSimonian-Laird random-effects meta-analytic pooling of all rho estimates with tau^2/I^2/Q heterogeneity,
  Cohen's d effect sizes (top vs bottom od_p quartile), and scatter/histogram visualizations with regression bands by benchmark
  and stratum. Key real finding: 0 of 5 testable (model, benchmark) combos rejected the i.i.d.-Bernoulli null at p<0.05 (min
  p=0.181) -- per the plan's own stated logic, this means the exponent-based diagnostic is not established as distinguishable
  from sampling noise at this experiment's scale, so all downstream correlation estimates (within-benchmark rho ~0.16-0.28,
  pooled meta-analytic rho=0.21 with near-zero heterogeneity) should be read as directional/exploratory rather than confirmatory.
  All code paths are fully general (no hard-coded results) and will produce statistically meaningful, adequately-powered output
  if the EXPERIMENT is rerun at a larger N.
workspace_path: >-
  /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_Br8Nz-7w30tX/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json

--- Item 4 ---
id: art_bgXM6FEsKofI
type: research
title: 'Taylor''s Law Voting: Verified Citations, Novelty Gap, and Scope Limits'
summary: |-
  This research artifact systematically verifies the Taylor's Law voting hypothesis through exhaustive bibliography searches, direct comparison with Liu's two-call moment theory, and scope analysis of tested accuracy ranges.

  **Core Findings:**

  1. **Bibliography Verification (COMPLETE):** The three primary citations are verified as authentic peer-reviewed work: Liu 2605.05592 (de Finetti representation of voting), Liu 2605.03379 (two-call second-moment theory), and Tanaka-Ishii 1804.07893 (Taylor's law on word frequencies in 1100+ texts). However, Tanaka-Ishii applies Taylor's law to corpus linguistics (word frequency distributions), not LLM error correlation—this is a critical distinction that may limit the evidential chain.

  2. **Anonymous Reference Status (INCOMPLETE):** Five anonymous references (3, 5, 6, 8, 10) could not be independently verified as published works despite extensive searches across arXiv, Semantic Scholar, ACL Anthology, and peer-reviewed databases. Refs 8 and 10 may be non-peer-reviewed sources (Medium, Digital Commons) that should be replaced with established methodology papers (Xiao et al. 2011 on allometric power laws, Clauset et al. 2009 on MLE, Lin & Newberry 2023 on noise in power laws). Ref 6 (claimed prior application of Taylor exponent to LLM) could not be located, potentially indicating this IS a novel contribution but with a broken citation chain.

  3. **Novelty vs. Liu's Theory (REQUIRES CLARIFICATION):** Liu 2605.03379 proposes that two labeled calls can identify the second moment m_2 of the latent correctness distribution, which exactly determines voting-gain bounds for any budget. Taylor's exponent b captures clustering via log(V) = log(a) + b·log(M). Both measure heterogeneity in problem-level correctness, but through different parametrizations. The hypothesis does not demonstrate whether b provides DISTINCT advantages (sample efficiency, transferability, interpretability) over m_2, or is merely a relabeling. This is the central novelty question and is unresolved.

  4. **Scope Limitations (SEVERE):** Tested accuracy ranges span GSM8K (40–97%), MMLU (78–90%), ARC Challenge (25–93%). Critically, no published work documents voting behavior in the <50% accuracy regime, where majority voting amplifies error and becomes harmful. If the hypothesis fitted Taylor exponent b only on problems in the 60–95% range, the exponent's validity for predicting voting harm at <50% is untested. This is a fundamental gap, as the decision rule's utility depends on coverage of the full spectrum.

  5. **Methodology Soundness (PARTIALLY VALIDATED):** Log-log OLS regression is acceptable under multiplicative error (confirmed by Xiao et al. 2011 re-analysis of 471 datasets), but MLE is more robust. Critical gap: No characterization of the noise floor under binomial sampling. If problems are sampled k times each (k calls per problem for correctness measurement), the fitted exponent b depends on k and noise level. The hypothesis should validate that b converges to a stable value as k increases, and characterize the null distribution under independence (b ≈ 1 in Poisson case).

  **Verified Sources:** Liu papers verified via arXiv (2026-05-07 submission dates). Tanaka-Ishii verified via ACL Anthology and arXiv. Power-law methodology verified via Xiao et al. 2011 (Ecology), Clauset et al. 2009 (general power law), and Lin & Newberry 2023 (noise sensitivity). Error correlation in voting verified via papers on co-failure ceilings and correlated LLM errors across 67 frontier models.

  **Confidence and Uncertainty:** High confidence in verification of primary citations; high confidence in identifying anonymous reference gaps; medium confidence in novelty assessment (lacks direct m_2 vs. b comparison); low confidence in scope validation (insufficient detail in published materials on exact accuracy ranges used in hypothesis).
workspace_path: >-
  /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_Br8Nz-7w30tX/3_invention_loop/iter_2/gen_art/gen_art_research_1
out_expected_files:
- research_out.json
</all_artifacts>

<new_artifacts_this_iteration>
These 2 artifacts were created THIS iteration.

id: art_mBThrQVRQRjk
type: evaluation
title: Does Voting Gain Follow the Taylor Exponent?
summary: >-
  This evaluation loads the real EXPERIMENT artifact output (gen_art_experiment_1/method_out.json: 3 models x 3 benchmarks
  x 10 problems x 5 repeated samples = 90 problems, 450 raw samples) and tests whether the Taylor power-law exponent b predicts
  self-consistency voting gain. Because the EXPERIMENT only fits b at the (model, benchmark) granularity (9 combos, 3 with
  a degenerate/null fit from too few valid problems in this budget-scaled run), two complementary analyses are reported: (1)
  combo_level_spearman -- the literal plan-specified test of fitted b vs. aggregate voting gain across the 5 valid (model,
  benchmark) combos (rho=-0.90, p=0.037, but n=5 is severely underpowered, flagged explicitly); (2) a per-problem analysis
  using od_p = v_p_empirical/(m_p(1-m_p)), the real per-problem overdispersion ratio (the finest-grained analog of b available,
  since true per-problem b is undefined), against real per-problem voting gains recomputed from raw correctness_samples via
  majority vote. On this n=90 basis the evaluation implements the full artifact plan: within-benchmark Spearman rho with 10k-iteration
  bootstrap CIs at k=5 (and secondary k=3,10), a 60/40 stratified calibration/holdout linear-regression transfer test with
  attenuation factor, cross-benchmark transfer (train on GSM8K, test on MMLU/ARC-Challenge), difficulty-stratified (low/medium/high
  m_p tercile) correlations with Holm-Bonferroni FWER correction, a noise-floor gate using the EXPERIMENT's own per-combo
  null-simulation p-values, DerSimonian-Laird random-effects meta-analytic pooling of all rho estimates with tau^2/I^2/Q heterogeneity,
  Cohen's d effect sizes (top vs bottom od_p quartile), and scatter/histogram visualizations with regression bands by benchmark
  and stratum. Key real finding: 0 of 5 testable (model, benchmark) combos rejected the i.i.d.-Bernoulli null at p<0.05 (min
  p=0.181) -- per the plan's own stated logic, this means the exponent-based diagnostic is not established as distinguishable
  from sampling noise at this experiment's scale, so all downstream correlation estimates (within-benchmark rho ~0.16-0.28,
  pooled meta-analytic rho=0.21 with near-zero heterogeneity) should be read as directional/exploratory rather than confirmatory.
  All code paths are fully general (no hard-coded results) and will produce statistically meaningful, adequately-powered output
  if the EXPERIMENT is rerun at a larger N.
workspace_path: >-
  /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_Br8Nz-7w30tX/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json

id: art_bgXM6FEsKofI
type: research
title: 'Taylor''s Law Voting: Verified Citations, Novelty Gap, and Scope Limits'
summary: |-
  This research artifact systematically verifies the Taylor's Law voting hypothesis through exhaustive bibliography searches, direct comparison with Liu's two-call moment theory, and scope analysis of tested accuracy ranges.

  **Core Findings:**

  1. **Bibliography Verification (COMPLETE):** The three primary citations are verified as authentic peer-reviewed work: Liu 2605.05592 (de Finetti representation of voting), Liu 2605.03379 (two-call second-moment theory), and Tanaka-Ishii 1804.07893 (Taylor's law on word frequencies in 1100+ texts). However, Tanaka-Ishii applies Taylor's law to corpus linguistics (word frequency distributions), not LLM error correlation—this is a critical distinction that may limit the evidential chain.

  2. **Anonymous Reference Status (INCOMPLETE):** Five anonymous references (3, 5, 6, 8, 10) could not be independently verified as published works despite extensive searches across arXiv, Semantic Scholar, ACL Anthology, and peer-reviewed databases. Refs 8 and 10 may be non-peer-reviewed sources (Medium, Digital Commons) that should be replaced with established methodology papers (Xiao et al. 2011 on allometric power laws, Clauset et al. 2009 on MLE, Lin & Newberry 2023 on noise in power laws). Ref 6 (claimed prior application of Taylor exponent to LLM) could not be located, potentially indicating this IS a novel contribution but with a broken citation chain.

  3. **Novelty vs. Liu's Theory (REQUIRES CLARIFICATION):** Liu 2605.03379 proposes that two labeled calls can identify the second moment m_2 of the latent correctness distribution, which exactly determines voting-gain bounds for any budget. Taylor's exponent b captures clustering via log(V) = log(a) + b·log(M). Both measure heterogeneity in problem-level correctness, but through different parametrizations. The hypothesis does not demonstrate whether b provides DISTINCT advantages (sample efficiency, transferability, interpretability) over m_2, or is merely a relabeling. This is the central novelty question and is unresolved.

  4. **Scope Limitations (SEVERE):** Tested accuracy ranges span GSM8K (40–97%), MMLU (78–90%), ARC Challenge (25–93%). Critically, no published work documents voting behavior in the <50% accuracy regime, where majority voting amplifies error and becomes harmful. If the hypothesis fitted Taylor exponent b only on problems in the 60–95% range, the exponent's validity for predicting voting harm at <50% is untested. This is a fundamental gap, as the decision rule's utility depends on coverage of the full spectrum.

  5. **Methodology Soundness (PARTIALLY VALIDATED):** Log-log OLS regression is acceptable under multiplicative error (confirmed by Xiao et al. 2011 re-analysis of 471 datasets), but MLE is more robust. Critical gap: No characterization of the noise floor under binomial sampling. If problems are sampled k times each (k calls per problem for correctness measurement), the fitted exponent b depends on k and noise level. The hypothesis should validate that b converges to a stable value as k increases, and characterize the null distribution under independence (b ≈ 1 in Poisson case).

  **Verified Sources:** Liu papers verified via arXiv (2026-05-07 submission dates). Tanaka-Ishii verified via ACL Anthology and arXiv. Power-law methodology verified via Xiao et al. 2011 (Ecology), Clauset et al. 2009 (general power law), and Lin & Newberry 2023 (noise sensitivity). Error correlation in voting verified via papers on co-failure ceilings and correlated LLM errors across 67 frontier models.

  **Confidence and Uncertainty:** High confidence in verification of primary citations; high confidence in identifying anonymous reference gaps; medium confidence in novelty assessment (lacks direct m_2 vs. b comparison); low confidence in scope validation (insufficient detail in published materials on exact accuracy ranges used in hypothesis).
workspace_path: >-
  /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_Br8Nz-7w30tX/3_invention_loop/iter_2/gen_art/gen_art_research_1
out_expected_files:
- research_out.json
</new_artifacts_this_iteration>

<current_paper>
The paper draft from this iteration — represents the current state of the research story.

# Introduction

Majority voting and self-consistency decoding are established test-time compute techniques for improving LLM accuracy. The method is conceptually simple: sample the model multiple times at nonzero temperature, aggregate the samples via majority vote, and return the modal answer. Yet practitioners face a persistent operational question: for a given task or model, is the extra compute cost of voting justified? Trial-and-error evaluation on held-out test data answers this post-hoc, but requires labeled examples, wastes compute on tasks where voting provides no benefit, and does not transfer to new models or domains.

Recent voting theory provides structural insight into this problem. Liu's de Finetti analysis shows that voting curves are non-monotone and determined by the latent distribution of per-problem correctness [1]. Critically, when per-problem success probability falls below 50%, majority voting actively amplifies errors [1]. This means voting's effectiveness depends on whether the LLM's repeated samples fail independently or cluster on a common wrong answer—a distinction that current practice cannot measure cheaply before committing to the voting pipeline.

We explored whether Taylor's power law—a principle from population ecology—could bridge this gap. Taylor's law relates population variance to mean through a power-law relationship: Var = a × Mean^b. In ecology, the exponent b is a clustering diagnostic: b ≈ 1 indicates Poisson-like independence; b > 1 indicates clustered, correlated disturbances [2]. We hypothesized that if LLM error correlation exhibits similar variance-mean scaling, the exponent could serve as a cheap, pre-registered diagnostic for predicting voting gain.

This paper reports a negative result: we find that Taylor's exponent, computed from repeated LLM sampling on 90 problems across three benchmarks, does not correlate significantly with measured voting gain. We detail the evidence, discuss why this null finding is methodologically instructive, and identify the barriers to developing cheap test-time-compute diagnostics for LLMs.

## Related Work

**Voting and Test-Time Aggregation.** Self-consistency decoding, introduced by Wang et al., empirically showed that majority voting over chain-of-thought samples improves reasoning [3]. However, this approach requires post-hoc evaluation on labeled data. Recent work by Liu reveals that voting curves are non-monotone under de Finetti representation and that per-problem success probability determines voting behavior [1]. Liu's two-call theory proposes that the second moment of the latent correctness distribution suffices to predict voting gain without large-scale sampling, but this requires knowledge of latent success probability—still unavailable for a new task without labels [4].

**Error Correlation in LLMs.** Diversity metrics are widely proposed as predictors of voting gain, but recent audits show they fail to predict voting benefit [5]. The root cause is that LLM errors are substantially correlated, not independent [6, 7]. More accurate models show even higher error correlation than weaker models [7]. This violates classical voting assumptions and explains why diversity alone cannot predict voting gain. Recent work documents that error correlation is structured: co-failure rates (all models wrong on the same problem) far exceed predictions from pairwise error correlation, imposing a ceiling on voting effectiveness [8].

**Taylor's Power Law and Clustering.** Taylor's law, originated by Taylor in 1961 [9], has been extensively validated across hundreds of biological species and non-biological systems [10]. The exponent b captures clustering: b ≈ 1 for Poisson/independent processes; b > 1 for correlated, clustered disturbances. In linguistics, Tanaka-Ishii and Kobayashi applied Taylor's law to word-frequency distributions in over 1,100 texts across 14 languages, finding universal exponents [11]. However, this work focused on corpus structure, not on live error correlation in machine-learning systems.

**LLM Sampling Variance.** Temperature affects consistency and diversity but not single-call accuracy [12]. Variance in LLM outputs decomposes into within-prompt resampling (~35%), prompt paraphrase, model identity, and language choice; systematic factors dominate [13]. These findings establish that LLM sampling exhibits both stochastic and systematic variation—potentially exhibiting power-law structure.

## Methodology

### Hypothesis and Success Criterion

We hypothesized that the Taylor's power-law exponent b, computed from repeated LLM sampling on a set of problems, would reliably predict whether majority voting improves accuracy. Specifically:

**High b (≥ 1.5)** → errors are clustered (shared failure modes) → voting provides little gain.

**Low b (≈ 1.0)** → errors are independent (Poisson-like) → voting provides substantial gain.

**Pre-registered success criterion:** Spearman rank correlation |ρ| > 0.5, p < 0.05 between b (or a proxy overdispersion measure) and measured voting gain across tested problems.

### Experimental Design

We conducted an experiment on three benchmarks spanning 90 problems:

- **GSM8K** (10 problems): Grade-school arithmetic, stratified by reasoning difficulty.
- **MMLU** (14 problems): Multidisciplinary knowledge questions.
- **ARC-Challenge** (14 problems): Science logic reasoning.

Problems were sampled from each benchmark's test split. For each problem, we sampled three models (a 3B, a mid-size 13-32B, and a 70B+ model) at fixed temperature τ = 0.7, with 5 repeated samples per problem per model.

### Operationalization: Computing Variance-Mean Structure

For each problem p and model m:

1. Sample the model N = 5 times at fixed temperature.
2. Count correct samples: c_p ∈ [0, 5].
3. Compute per-problem mean correctness: m_p = c_p / 5.
4. Compute Bernoulli variance: v_p = m_p × (1 − m_p).
5. Across all problems in a benchmark, compute the overdispersion ratio: od_p = v_p / (m_p(1 − m_p)).

Because the number of problems per model-benchmark pair (10–14) is too small to fit a robust log-log regression for exponent b (a power-law fit requires many more data points), we instead used per-problem overdispersion od_p as a local proxy for clustering: od_p ≈ 1 indicates independent Bernoulli; od_p > 1 indicates clustering [ARTIFACT:art_mBThrQVRQRjk].

### Voting Gain Measurement

For each problem, we independently measured voting gain:

1. Compute single-sample accuracy: acc_1 (k=1).
2. Compute majority-vote accuracy at k = 3, 5, 10.
3. Compute voting gain: Δ_k = acc_vote(k) − acc_1.

## Results

[FIGURE:fig_noise_floor]

Our experiment yielded three key findings:

### 1. Noise Floor: Exponent Not Distinguishable from Null

We fitted Taylor exponent b at the (model, benchmark) level, aggregating all problems per combination (5 valid combos with N ≥ 5 problems; 4 combos excluded due to degenerate m_p or insufficient data). We then conducted a null-hypothesis simulation for each combo: generate synthetic problems with i.i.d. Bernoulli correctness (independent errors, true b = 1) at the same N and problem count, fit the exponent, and compare the fitted b distribution to the observed b.

Key result: **Zero of five tested (model, benchmark) combos rejected the independence null at p < 0.05.** Minimum p-value = 0.18. This indicates that the observed exponent values are statistically indistinguishable from what we would expect if errors were purely independent. Per the pre-registered plan, this noise-floor gate means the hypothesis is not established as distinguishable from sampling noise at this scale [ARTIFACT:art_mBThrQVRQRjk].

### 2. Within-Benchmark Correlations: Weak and Non-Significant

Despite the noise-floor result, we computed per-problem overdispersion od_p as a local clustering proxy and tested correlation with voting gain within each benchmark [ARTIFACT:art_mBThrQVRQRjk]:

- **ARC-Challenge** (n=14 problems): Spearman ρ = 0.28, p = 0.33, 95% CI: [−0.04, 0.58].
- **GSM8K** (n=10 problems): Spearman ρ = 0.16, p = 0.66, 95% CI: [−0.33, 0.53].
- **MMLU** (n=14 problems): Spearman ρ = 0.25, p = 0.38, 95% CI: [−0.06, 0.55].

All correlations are non-significant. The correlation magnitude (ρ ~0.16–0.28) is well below the pre-registered threshold of |ρ| > 0.5. Across all k values (3, 5, 10), the pattern holds [ARTIFACT:art_mBThrQVRQRjk].

### 3. Meta-Analytic Pooling: No Systematic Signal

Using DerSimonian-Laird random-effects meta-analysis across all estimated correlations, the pooled Spearman ρ = 0.21, 95% CI: [0.03, 0.38], with zero heterogeneity (I² = 0, τ² = 0). This pooled estimate is below the pre-registered success threshold and is driven primarily by ARC-Challenge, which shows the largest correlation. The zero heterogeneity indicates that the weak correlations are consistent across benchmarks—not a sign of hidden signal in a subset [ARTIFACT:art_mBThrQVRQRjk].

### 4. Effect Sizes: Small Across Benchmarks

We computed Cohen's d comparing top- and bottom-quartile overdispersion groups:

- **ARC-Challenge**: d = −0.16, small effect.
- **GSM8K**: d = −0.12, negligible effect.
- **MMLU**: d = −0.11, negligible effect.

The small effect sizes reinforce the weak signal [ARTIFACT:art_mBThrQVRQRjk].

## Discussion

### Why the Hypothesis Failed

Three factors likely explain the null result:

**1. Noise Floor Under Binomial Sampling.** The Taylor exponent fitted on only 5 samples per problem suffers from substantial binomial sampling noise. Estimated variance m_p(1 − m_p) has sampling error ~1/√N; the ratio of two noisy quantities (variance and mean) compounds this error. The simulated null distribution showed that random Bernoulli data yields fitted exponents similar to our observed values, indicating the signal-to-noise ratio is unfavorable at this sample size [ARTIFACT:art_mBThrQVRQRjk].

**2. Limited Accuracy Range.** Our tested benchmarks span mean per-problem success rates of 60–95%, a regime where voting generally helps. The critical regime where voting amplifies errors (per-problem success < 50%) is undocumented in our data. Taylor's exponent may behave differently in the error-amplification regime, making our findings inapplicable to the exact operational scenario where a cheap diagnostic would be most valuable [ARTIFACT:art_mBThrQVRQRjk].

**3. Error Correlation Structure.** Recent work documents that LLM error correlation is non-uniform and structured: co-failure rates (all models wrong) far exceed predictions from pairwise correlation, imposing a ceiling on voting effectiveness [8]. This structured clustering (some problems inherently hard, others easy) may not decompose into a uniform clustering signal (high b) that Taylor's law measures. LLM errors may violate the assumptions underlying Taylor's law—specifically, that clustering is driven by a shared external stochastic factor, not by fundamental problem difficulty [ARTIFACT:art_bgXM6FEsKofI].

### Novelty and Comparison with Liu's Theory

A significant gap in our work is the lack of direct comparison with Liu's competing two-call theory [4]. Liu proposes that two labeled calls on each problem suffice to identify the second moment m₂ of the latent correctness distribution, which exactly determines voting-gain bounds for any budget. Taylor's exponent b also captures problem-level heterogeneity, but through a different parametrization [ARTIFACT:art_bgXM6FEsKofI].

We did not empirically test whether b predicts voting gain more efficiently or accurately than m₂, or whether b transfers across (model, benchmark) pairs better than m₂. Without this comparison, we cannot claim novelty over Liu's theory—we can only claim novelty in domain (applying an ecology principle to LLMs), not in method.

### Implications for Test-Time Compute Allocation

Our negative result highlights a fundamental challenge in developing cheap operational diagnostics for LLMs: the signal (error clustering) is subtle, the noise floor (binomial sampling variance) is high, and the solution (voting) is already computationally cheap relative to inference. For practitioners, this suggests:

1. **Trial-and-error remains the operational standard.** Until a diagnostic shows strong transferability and signal-to-noise ratio >> 1, post-hoc evaluation on a held-out dev set remains the most reliable method.
2. **Higher sample counts are needed.** Fitting a robust Taylor exponent requires N >> 5 samples per problem; the compute savings from avoiding costly per-problem sampling may not justify the cost savings from skipping unnecessary voting.
3. **Structured error correlation may require different models.** The uniform clustering assumption underlying Taylor's law may not hold for LLMs; domain-specific models of error structure (e.g., problem difficulty, reasoning step count, co-failure patterns) may be more informative.

### Limitations

**Sample size.** Our 90 problems and 5 samples per problem per model are at the lower end of what power-law estimation requires; 500+ problems and 20–30 samples per problem would provide more robust exponent estimates and improve statistical power [ARTIFACT:art_mBThrQVRQRjk].

**Accuracy range.** The 60–95% regime tested is unrepresentative of the full landscape where voting decisions matter most (< 50% per-problem success, where voting harms). Extending to very-hard benchmarks or adversarial tasks is essential.

**Model diversity.** We tested only three model sizes from the same family. Testing across diverse model families, architectures, and training regimes would clarify whether b is a model-universal signal or a model-specific property.

**Mechanistic understanding.** We did not analyze the structure of wrong answers (e.g., via embedding clustering or syntactic analysis) to confirm the interpretation that high od_p reflects truly clustered, systematic errors versus random binomial variation.

### Methodological Contributions

Despite the negative empirical result, this work contributes methodologically:

1. **Noise-floor validation protocol.** We demonstrate a principled way to test whether a fitted exponent is distinguishable from the null hypothesis (i.i.d. Bernoulli), using per-combo null simulation and p-value gates [ARTIFACT:art_mBThrQVRQRjk].
2. **Bibliography verification.** We identify and resolve gaps in the original hypothesis's citation chain, replacing unverifiable anonymous references with verified peer-reviewed sources [ARTIFACT:art_bgXM6FEsKofI].
3. **Honest reporting of null results.** We document a hypothesis that did not survive empirical testing, providing a template for reporting negative results in LLM research and clarifying the barriers to cheap diagnostics.

## Conclusion

We tested whether Taylor's power law could serve as a cheap diagnostic for predicting when majority voting improves LLM accuracy. The hypothesis was not supported: the fitted exponent does not distinguish clustering from independence at our sample size, within-benchmark correlations are weak (ρ < 0.28, all p > 0.3), and the meta-analytic pooled correlation (ρ = 0.21) falls short of the pre-registered threshold (|ρ| > 0.5).

This negative result is informative. It reveals fundamental barriers to developing cheap test-time-compute diagnostics for LLMs: the binomial sampling noise is substantial, the signal we sought (uniform clustering of errors via a power-law exponent) may not align with how LLM errors actually cluster (structured by problem difficulty, co-failure patterns), and a direct comparison with Liu's competing second-moment theory remains unmade.

For the community, this work underscores that cross-domain transfer of statistical principles—even well-validated ones like Taylor's law—requires careful validation against domain-specific assumptions. The clustering behavior that drives Taylor's law in ecology (shared environmental stressors) may not map cleanly onto the error-correlation structure in LLMs.

Future work should: (1) test Taylor's law at larger sample sizes (20–30 samples per problem), (2) extend to the <50% per-problem-success regime where voting actively harms, (3) compare b against Liu's second-moment m₂ empirically, and (4) develop mechanistic probes of LLM error structure beyond variance-mean scaling (e.g., co-failure matrices, problem-difficulty embeddings).

## Bibliography

[1] Liu, Y. When Can Voting Help, Hurt, or Change Course? Exact Structure of Binary Test-Time Aggregation. *arXiv preprint* arXiv:2605.05592, 2026.

[2] Taylor, L.R. Aggregation, Variance and the Mean. *Nature*, 189, 732–735 (1961).

[3] Wang, X., Wei, J., Schuurmans, D., et al. Self-Consistency Improves Chain of Thought Reasoning in Language Models. *arXiv preprint* arXiv:2203.11171, 2022.

[4] Liu, Y. Two Calls, Two Moments, and the Vote-Accuracy Curve of Repeated LLM Inference. *arXiv preprint* arXiv:2605.03379, 2026.

[5] Anonymous. Are Diversity Metrics Measuring Diversity? A Capability-Controlled Audit of Majority-Vote Gain in LLM Ensembles. *arXiv preprint* arXiv:2607.20768, 2026.

[6] Taori, R., Gulrajani, I., Zhang, T., et al. Stanford Alpaca: An Instruction-following LLaMA Model. *GitHub Repository*, 2023. https://github.com/tatsu-lab/stanford_alpaca

[7] Anonymous. Where Does the Noise Come From? A Variance-Components Decomposition of Non-Determinism in LLM Brand Answers. *arXiv preprint* arXiv:2607.13304, 2026.

[8] Anonymous. When Does Combining Language Models Help? A Co-Failure Ceiling on Routing, Voting, and Mixture-of-Agents Across 67 Frontier Models. *arXiv preprint* arXiv:2606.27288, 2026.

[9] Taylor, L.R. Aggregation, Variance and the Mean. *Nature*, 189, 732–735 (1961).

[10] Riordan, B. Population Ecology and Environmental Variance: Taylor's Law. *Oikos*, 2020.

[11] Tanaka-Ishii, K., & Kobayashi, S. Taylor's law for Human Linguistic Sequences. In *Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics* (pp. 1141-1151). *arXiv preprint* arXiv:1804.07893, 2018.

[12] Holtzman, A., Buys, J., Du, L., Forbes, M., & Choi, Y. The Curious Case of Neural Text Degeneration. *arXiv preprint* arXiv:1910.14599, 2019.

[13] Ouyang, L., Wu, J., Jiang, X., et al. Training Language Models to Follow Instructions with Human Feedback. *arXiv preprint* arXiv:2203.02155, 2022.

</current_paper>

<reviewer_feedback>
Feedback from the paper reviewer this iteration.

- [MAJOR] (rigor) Reference [6] (Taori, Gulrajani, Zhang et al., 'Stanford Alpaca: An Instruction-following LLaMA Model,' GitHub repo, 2023) is cited to support the claim 'LLM errors are substantially correlated, not independent [6, 7]' and again in the Related Work sentence 'More accurate models show even higher error correlation than weaker models [7]' (the latter correctly cites only [7], but [6] is used for the general correlated-errors claim in the same sentence). The Stanford Alpaca repository documents an instruction-tuning recipe and released model weights; it contains no analysis of error correlation across repeated samples or across models. This is a citation used to support a claim it does not make.
  Action: Remove ref [6] from that sentence and replace it with a citation that actually reports LLM error correlation/non-independence (e.g., the co-failure-ceiling paper already cited as [8], or another verifiable source found via a targeted search for 'LLM sample correlation majority voting non-independence'). Verify every citation-claim pairing in the paper by re-reading the cited source's abstract/results before finalizing, not just checking that a citation with a plausible-looking arXiv ID exists.
- [MAJOR] (evidence) The evaluation artifact (art_mBThrQVRQRjk) reports a combo-level Spearman correlation between the fitted Taylor exponent b and aggregate voting gain of rho=-0.90, p=0.037 (n=5 combos) — this is the literal pre-registered test specified in Methods ('Spearman rank correlation |rho|>0.5, p<0.05 between b ... and measured voting gain') and it nominally satisfies both thresholds (|rho|=0.90>0.5, p=0.037<0.05). The paper's Results and Conclusion sections never mention this number; they report only the secondary per-problem od_p proxy analysis (rho=0.16-0.28, all non-significant) as if that were the primary test, and conclude 'the hypothesis was not supported.' The combo-level result is flagged in the artifact as severely underpowered (n=5), which is a legitimate reason to distrust it, but the paper does not disclose the result or explain the reasoning for deprioritizing it — this reads as switching the primary endpoint after seeing which one supported the desired conclusion.
  Action: Explicitly report the combo-level b-vs-voting-gain correlation in the Results section, state clearly that it nominally meets the pre-registered criterion but is disqualified by n=5 severe underpowering (e.g., show the confidence interval width or a power calculation), and only then justify pivoting to the per-problem od_p analysis as the paper's actual basis for its conclusion. This must be stated in the paper body, not left implicit in the supplementary artifact only.
- [MINOR] (clarity) The Methodology section states three benchmarks with 10, 14, and 14 problems respectively (summing to 38 unique problems), while the Results section and artifact description refer to '90 problems' (3 models x 3 benchmarks x 10 problems x 5 samples). These are inconsistent: 90 appears to be problem-model instances rather than unique problems, and the per-benchmark problem counts used for the Spearman tests (n=14, n=10, n=14 in Results item 2) do not match the Methodology's per-benchmark breakdown structure or explain how 3 models collapse into single n values per benchmark.
  Action: Add one sentence clarifying the units precisely: e.g., 'we sample 10/14/14 unique problems per benchmark, each evaluated on 3 models, yielding 90 problem-model correctness vectors; within-benchmark Spearman tests pool across the 3 models per problem, giving n=10/14/14 per benchmark.' Ensure the same unit convention is used everywhere the counts appear.
- [MAJOR] (novelty) The paper's Discussion explicitly states 'we cannot claim novelty over Liu's theory — we can only claim novelty in domain (applying an ecology principle to LLMs), not in method,' and this gap is carried unresolved into the Conclusion as future work. This is the same gap flagged in the prior review round and it remains unaddressed empirically; only a qualitative discussion of the two parametrizations is given.
  Action: Given that the underlying dataset (90 problem-model correctness vectors with 5 repeats) is already collected, compute Liu's second-moment m2 estimator on the same data and report its correlation with voting gain alongside od_p/b, using the same Spearman/meta-analysis pipeline already built for the Taylor exponent. This is a bounded, already-scoped addition given the existing artifact and would resolve the paper's own stated central open question.
- [MINOR] (rigor) References [5], [7], and [8] are attributed to 'Anonymous' authors on arXiv preprints; arXiv does not permit anonymous public preprints, so these cannot be independently located or verified by a reader from the citation alone, even though a title and arXiv ID are given. The paper's own supplementary research artifact (art_bgXM6FEsKofI) reports that five such references could not be independently verified across arXiv/Semantic Scholar/ACL Anthology searches, and recommends replacing two of them (used for the log-log regression methodology claims) with established sources (Xiao et al. 2011, Clauset et al. 2009, Lin & Newberry 2023) — but the paper as written still cites the unverified 'Anonymous' sources for its core error-correlation and co-failure-ceiling claims.
  Action: Either resolve the true author names for refs [5], [7], [8] via a direct arXiv ID lookup (fetch each arXiv page directly) and correct the byline, or drop these three claims/citations from the argument and rely only on the paper's own verified primary sources (Liu, Taylor, Tanaka-Ishii, Wang et al.) plus the well-established methodology references identified in the verification artifact.
- [MINOR] (scope) This concern was raised in the previous review and remains only partially addressed: the tested accuracy range (60-95% per the paper's Discussion) still never reaches the <50% per-problem-success regime where voting is known to actively harm accuracy — precisely the regime where a cheap pre-voting diagnostic would matter most. The current draft does at least foreground this in the Discussion ('Limited Accuracy Range' subsection) rather than burying it, which is an improvement, but the practical implications section still speaks generally about 'test-time compute allocation' without re-scoping the claim to the tested range.
  Action: This is now adequately flagged as a limitation and does not need further empirical work to be acceptable for a negative-result paper, but the 'Implications' subsection should add one explicit sentence restricting all three numbered recommendations to the 60-95% regime tested, since a reader skimming only that subsection could otherwise over-generalize the conclusions.
</reviewer_feedback>



<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for the field's landscape, prior work, crowded lanes, and the novelty bar — consult it while revising so the updated hypothesis stays genuinely novel and well-positioned.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>

<task>
IMPORTANT: Your ONLY output is the revised hypothesis text. Do NOT run code, produce artifacts,
fix bugs, or attempt to address the evidence yourself — the next iteration of the invention loop
will generate fresh artifacts based on your revised hypothesis. Reflect and rewrite; nothing else.

Do NOT generate a completely new hypothesis. Take the current hypothesis and REVISE it
to incorporate new evidence. Keep the core idea — refine, narrow, or strengthen it.

1. Does the evidence support the hypothesis? Narrow or broaden scope as needed.
2. Which claims now have strong evidence? Which are still unsupported?
3. Should the hypothesis become more specific based on what we've learned?
4. If reviewer feedback is provided, address the critiques directly.

STABILITY IS OK: If progress is good and evidence supports the current direction, keep the
hypothesis similar or identical. Only make substantive changes when evidence clearly calls for
them — e.g., contradictory results, fundamental reviewer critiques, or findings that refine scope.

You must also classify two kinds of edges in the research trace:

(A) The H↔H edge — how does this revised hypothesis relate to the previous one?
    Set `relation_type` (Moulines's structuralist typology) to one of:
    - "evolution": refining specialised claims, same conceptual frame
    - "embedding": previous hypothesis is now a special case of a broader frame
    - "replacement": rejecting the previous frame entirely (Kuhnian shift)
    Set `relation_rationale` to a brief justification (≤120 chars).

(B) The A↔A edges — for each artifact created THIS iteration, classify each of its
    `in_dependencies` (predecessor → dependent) using MultiCite's citation-function
    typology (Lauscher et al., NAACL 2022) — emit one entry in `artifact_relations`
    per (predecessor, dependent) pair. Predecessors are ALWAYS artifacts from EARLIER
    iterations — artifacts within one iteration run in parallel and cannot depend on
    each other, so never emit a relation between two same-iteration artifacts (it
    will be dropped):
    - "background": predecessor is treated as background context
    - "motivation": predecessor motivated this artifact's research
    - "uses": this artifact uses the predecessor's data, method, or output
    - "extends": this artifact extends the predecessor
    - "similarities": this artifact's results agree with the predecessor's
    - "differences": this artifact's results disagree with the predecessor's
    Each `relation_rationale` must be ≤120 characters.

Output the COMPLETE revised hypothesis (with the H↔H relation fields) AND the full
list of A↔A `artifact_relations` for this iteration's new artifacts.
</task><user_data>
User-provided reference materials are available at `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_Br8Nz-7w30tX/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ArtifactRelation": {
      "description": "One typed A\u2194A edge between a dependent artifact and one of its in_dependencies.\n\nMultiCite citation-function typology (Lauscher et al., NAACL 2022),\nreduced to 6 plain-English types.",
      "properties": {
        "from_id": {
          "description": "ID of the predecessor artifact (the one being depended on)",
          "title": "From Id",
          "type": "string"
        },
        "to_id": {
          "description": "ID of the dependent artifact (the new artifact this iteration)",
          "title": "To Id",
          "type": "string"
        },
        "relation_type": {
          "description": "MultiCite citation-function type for the predecessor\u2192dependent edge: 'background' \u2014 predecessor is treated as background context; 'motivation' \u2014 predecessor motivated this artifact's research; 'uses' \u2014 this artifact uses the predecessor's data, method, or output; 'extends' \u2014 this artifact extends the predecessor; 'similarities' \u2014 this artifact's results agree with the predecessor's; 'differences' \u2014 this artifact's results disagree with the predecessor's.",
          "enum": [
            "background",
            "motivation",
            "uses",
            "extends",
            "similarities",
            "differences"
          ],
          "title": "Relation Type",
          "type": "string"
        },
        "relation_rationale": {
          "description": "Brief rationale for this relation type (one short line, max 120 characters).",
          "maxLength": 120,
          "title": "Relation Rationale",
          "type": "string"
        }
      },
      "required": [
        "from_id",
        "to_id",
        "relation_type",
        "relation_rationale"
      ],
      "title": "ArtifactRelation",
      "type": "object"
    }
  },
  "description": "Revised hypothesis after reviewing iteration results.\n\nOutput matches the hypothesis dict structure so it can replace the\noriginal hypothesis in subsequent iterations.",
  "properties": {
    "title": {
      "description": "Revised hypothesis title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters); may be unchanged if still accurate.",
      "title": "Title",
      "type": "string"
    },
    "hypothesis": {
      "description": "Revised hypothesis statement \u2014 what we now believe based on evidence",
      "title": "Hypothesis",
      "type": "string"
    },
    "relation_rationale": {
      "description": "Brief rationale for the H\u2194H revision type (one short line, max 120 characters).",
      "maxLength": 120,
      "title": "Relation Rationale",
      "type": "string"
    },
    "confidence_delta": {
      "description": "How confidence changed: 'increased', 'decreased', or 'unchanged'",
      "title": "Confidence Delta",
      "type": "string"
    },
    "key_changes": {
      "description": "Bullet list of specific changes made to the hypothesis",
      "items": {
        "type": "string"
      },
      "title": "Key Changes",
      "type": "array"
    },
    "relation_type": {
      "description": "Moulines's structuralist typology of this hypothesis revision: 'evolution' \u2014 refining specialised claims while keeping the same conceptual frame; 'embedding' \u2014 the previous hypothesis is now a special case of a broader frame; 'replacement' \u2014 rejecting the previous frame entirely (incommensurable, Kuhnian revolution).",
      "enum": [
        "evolution",
        "embedding",
        "replacement"
      ],
      "title": "Relation Type",
      "type": "string"
    },
    "artifact_relations": {
      "description": "Typed A\u2194A edges for this iteration's new artifacts. Emit one entry per (predecessor \u2192 dependent) edge for every in_dependency on each artifact produced this iteration.",
      "items": {
        "$ref": "#/$defs/ArtifactRelation"
      },
      "title": "Artifact Relations",
      "type": "array"
    }
  },
  "required": [
    "title",
    "hypothesis",
    "relation_rationale",
    "confidence_delta",
    "key_changes",
    "relation_type"
  ],
  "title": "RevisedHypothesis",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [2] HUMAN-USER prompt · 2026-08-01 15:20:37 UTC

```
PROVISIONING RELOAD VISUAL: capture the main panel after reload.
```

### [3] SYSTEM-USER prompt · 2026-08-01 15:21:19 UTC

```
<validation-feedback>
Attempt 1 failed validation.

Schema validation found 1 problem — fix ALL of them at once:
  - at `relation_rationale`: 'Same core claim; first test underpowered/noise-floor-failed, not falsified -- narrowed to require scale-up before adjudication' is too long (at most 120 characters, got 126)
Every required field must be present and every field type must match the schema.

Produce `.terminal_claude_agent_struct_out.json` again so it contains corrected JSON that matches the schema. Do not invent new fields.
</validation-feedback>
```
