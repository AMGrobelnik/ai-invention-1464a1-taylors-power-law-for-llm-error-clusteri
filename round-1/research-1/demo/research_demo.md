# Taylor's Law as Voting Diagnostic: Comprehensive Literature Review & Methodology

## Summary

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

## Research Findings

## Overview of Research Landscape

This investigation establishes the theoretical and empirical foundations for testing a novel hypothesis: that Taylor's power-law exponent (b), computed from repeated LLM sampling of problem correctness, can predict whether majority voting will improve accuracy on a task. The research spans five interconnected domains: voting theory, Taylor's law from ecology, LLM sampling behavior, error clustering analysis, and benchmark selection methodology.

## Part 1: Voting Theory Under De Finetti Representation

**Classical Theory Overturned:**
Classical majority voting assumes monotone behavior: more votes always help above majority threshold, always hurt below. Yi Liu's 2026 work (arXiv:2605.05592) completely invalidates this picture [1]. Under de Finetti representation for exchangeable repeated correctness, voting is governed by a latent distribution of per-example success probabilities—a hidden structure that determines whether voting helps, hurts, or changes course [1].

**Voting Curves Are Non-Monotone:**
Voting curves (accuracy vs. number of votes) can have infinitely many trend reversals and sharply different shapes even for simple latent mixtures [1]. The signed voting signature—which records the distribution of per-problem correctness probabilities above vs. below 0.5—uniquely characterizes the voting curve via Hausdorff moments [1]. This mathematical result establishes that voting behavior is determined by the latent correctness distribution, not by naive ensemble theory [1].

**When Voting Fails (Critical Finding):**
When per-problem correctness < 0.5 (harder problems, ambiguous tasks), majority voting amplifies errors rather than correcting them [1, 2]. This is because the majority of samples are already wrong; combining them increases the likelihood that the wrong answer dominates [1, 2]. This failure mode is central to the hypothesis: problems with high error correlation (proxied by high Taylor's exponent b) are more likely to have <0.5 per-sample correctness and to suffer from voting [1, 2].

**Two-Call Theory for Voting Prediction:**
ArXiv:2605.03379 (Yi Liu, 2026) shows that mean and second moment of the latent correctness distribution fully determine voting gain, distribution-free [2]. One labeled call identifies the mean m; two calls identify the second moment m₂ and hence the same-example correctness correlation (which separates stable errors from recoverable randomness) [2]. From these two moments, every majority-vote budget k has a sharp distribution-free confidence interval [2]. The three-vote rule has a closed-form accuracy bound with width ≤ 1/8 [2]. This theoretical result is powerful: even limited empirical data can predict voting gain, supporting the feasibility of using Taylor's exponent as a cheap diagnostic [2].

## Part 2: Taylor's Power Law—Ecology to General Systems

**Foundational Concept (1961):**
Taylor's power law, Var = a * Mean^b, originated in Lionel Roy Taylor's ecological work in 1961 [3]. The law relates variance of population counts (or event frequencies) to the mean through a power-law relationship [3]. The exponent b is interpreted as an aggregation index: how much spatial or temporal clustering is present [3]. The law has been confirmed for hundreds of species across ecology and has been extended to epidemiology, physics, finance, and human dynamics [5].

**Exponent Interpretation:**
When b ≈ 1: the data follows Poisson distribution, indicating random, independent events [3]. When b > 1 (typical range 1.5-2.5): indicates clustering or aggregation; organisms/events are spatially or temporally concentrated rather than uniformly distributed, often from shared environmental drivers [3]. As a concrete example, forest disturbances show b ≈ 2.19-2.23, indicating extreme clustering: as mean disturbance rates increase, temporal variability increases dramatically, creating pulses of concentrated damage [3].

This interpretation maps directly to LLM errors: high b → errors cluster around shared failure modes → reducing error diversity → reducing voting benefit [10]. Low b → errors are independent → high diversity → voting helps [1, 2].

**Fundamental Property or Artifact?**
The consistency of Taylor's law across ecology, physics, and finance (found in >1000 species and systems) suggests it captures a genuine phenomenon rather than sampling artifact [3, 5]. This universality motivates testing whether it applies to LLM correctness distributions.

## Part 3: Taylor's Law in Computational Linguistics (ACL 2018)

**Kobayashi & Tanaka-Ishii Landmark Study:**
The ACL 2018 paper (Kobayashi & Tanaka-Ishii) applied Taylor's law to 1,100+ texts across 14 languages, finding that Taylor exponents of natural language written texts are universally consistent at b ≈ 0.58 [4, 5]. This universality—identical exponent across English, Chinese, Arabic, Japanese, and other structurally different languages—is striking and suggests Taylor's law captures fundamental structure of language [4, 5].

**Comparative Exponent Values Across Domains:**
The study extended to non-text domains with revealing results [5]:
- Written natural language: b ≈ 0.58 (universal across 14 languages) [5]
- Adult speech: b ≈ 0.63 [5]
- Child-directed speech (more structured): b ≈ 0.68 [5]
- Programming language code (rigid syntax): b ≈ 0.79 [5]
- Music (highly structured): b ≈ 0.79 [5]
- LSTM-generated text: b ≈ 0.50 (showing limitation of neural models in capturing co-occurrence structure vs. real text at 0.58) [5]

The progression suggests Taylor's exponent reflects linguistic structure and constraint: more structured domains (code, music, child speech) have higher b; pure language modeling (LSTM) undershapes the exponent [5].

**Methodology for Text Analysis:**
The approach: (1) segment text into fixed-size windows, (2) compute variance and mean of word/character frequency within windows, (3) fit log-log regression on (log mean, log variance) points, (4) extract slope b with standard regression confidence intervals [4, 5]. This methodology transfers directly to LLM correctness: treat each problem as an "event," sample correctness N times, compute mean and Bernoulli variance, fit log-log regression [5, 17].

## Part 4: LLM Sampling Variance & Error Correlation

**Temperature & Sampling Diversity (Not Accuracy):**
Empirical research on 4 LLM models and 1,000 multiple-choice questions confirms: changing temperature in range 0.0–1.0 has NO statistically significant effect on per-call accuracy [8]. However, temperature DOES control consistency vs. diversity: temperature 0.0 is highly repetitive; temperature 1.0 is diverse but noisier [8, 9]. For repeated sampling to maximize diversity while maintaining quality, standards practice uses 0.7-0.8 [19, 20].

**Critical Finding: LLM Errors Are Correlated, Not Independent:**
ArXiv:2607.20768 (2026 audit of majority-vote gain in LLM ensembles) demonstrates LLM errors are substantially correlated, violating the independence assumption underlying classical voting theory [6]. More surprisingly, more accurate models show HIGHER error correlation than weaker models—the opposite of naive ensemble intuition [6]. This correlation is the central problem: correlated errors mean samples fail on the same examples, reducing voting benefit [6].

The paper's key innovation: capability-controlled audit, comparing models at similar performance levels to isolate genuine error disagreement vs. capability differences [6]. Diversity metrics (embedding-based similarity, disagreement counts) do NOT reliably predict voting gain; error correlation and shared failure patterns matter more [6].

**Variance Components Decomposition:**
Using 12,933 LLM responses across 20 brands, 8 languages, and 3 models (GPT-5.2, Gemini 3 Flash, Perplexity), researchers partitioned total variance into four orthogonal sources [7]:
1. Within-prompt resampling stochasticity: ~35% [7]
2. Prompt paraphrase effects: [7]
3. Model identity (GPT vs. Gemini vs. Perplexity): [7]
4. Language choice: [7]

The critical insight: only ~35% of observed correctness variance comes from pure resampling randomness [7]. The remaining ~65% is systematic (model/prompt structure) [7]. This suggests many high-variance problems achieve high variance from systematic factors (ambiguous prompt, multi-faceted task) rather than from true independence [7]. High-variance problems may naturally have high Taylor's exponent b, but for different reasons than pure clustering [7].

**Standard Sampling Protocol:**
Empirical best practice (synthesized from multiple 2025-2026 sources): [19, 20]
- Fixed temperature: 0.7-0.8 (0.8 yields highest accuracy for code; 0.7 standard for general tasks) [19, 20]
- Number of samples per problem: N = 20-30 [1, 2, 19, 20]
- Random seed: varies (enables diversity) [19, 20]
- Max tokens per sample: task-dependent (for reasoning: typically 1000-2000) [19, 20]

## Part 5: Error Diversity & Clustering

**Error Diversity Predicts Voting Benefit:**
RLVR (Reinforcement Learning from Verifiable Rewards) research (arXiv:2605.17333, 2026) shows intra-group error diversity—how dispersed wrong answers are within a sample set—is a strong predictor of training/voting success [10]. Problems eliciting diverse wrong answers (many different incorrect solutions) train better and likely vote better than homogeneous-failure problems (all samples converge on same wrong answer) [10].

Proposed method EDAS (Error Diversity Advantage Shaping): modulates advantage signals based on error diversity—amplifies penalties for dominant repeated errors (homogeneous failure, bad for voting) and attenuates penalties for rare errors (good exploration) [10]. This directly supports the hypothesis: high-b problems should have homogeneous errors (low diversity), low voting gain [10].

**Embedding-Based Clustering Limitations:**
LLM embedding spaces have well-documented issues [11, 12]:
- Anisotropy: embeddings concentrate in narrow high-dimensional cones [11, 12]
- Low geometric separation: semantically different concepts can be embedded close together [11]
- Semantic ambiguity: singular vs. plural forms ("gas" vs. "gases") map to different embeddings despite semantic similarity [11]
- Potential high false-positive rates in clustering [11, 12]

These issues suggest embedding-based clustering of wrong answers may produce unreliable entropy estimates [11, 12]. Alternatives to explore [11, 12]:
- Syntactic similarity: edit distance, token overlap
- Semantic entailment-based grouping: using entailment models to detect if one answer "subsumes" another
- LLM-driven topic clustering: using a language model to label clusters thematically

For mechanistic validation of the hypothesis, multiple clustering methods should be tested [11, 12].

## Part 6: Voting Aggregation Methods & Measurement Protocols

**Standard Voting Accuracy Protocol:**
Repeated sampling yields N samples per problem at fixed temperature [1, 2]. For each sample count k ∈ {1, 3, 5, 10, 20}, compute majority-vote accuracy: acc_vote(k) = proportion of problems where ≥ ceil(k/2) samples are correct [1, 2]. Voting gain: Δacc(k) = acc_vote(k) - acc_single, where acc_single is baseline single-sample accuracy [1, 2]. The vote-accuracy curve plots Δacc(k) vs. k; typically shows rapid initial gain then saturation [1, 2].

**Two-Call Prediction:**
From just two labeled calls, one can derive distribution-free confidence intervals for any k without assuming a parametric distribution (e.g., Beta-Binomial) [2]. The three-vote rule: when k=3, the confidence interval has width ≤ 1/8, providing certified guidance on whether voting at k=3 will help [2].

**Ranked & Weighted Voting:**
Recent methods (2025) show modest improvements over simple majority [13]:
- Instant runoff: eliminate lowest-ranked candidate iteratively [13]
- Borda count: assign points based on rank, sum across samples [13]
- Mean reciprocal rank: average inverse rank of correct answer [13]
- Confidence-weighted voting: weight each sample by model confidence (requires calibration) [13]

Advanced aggregation (Optimal Weight, Inverse Surprising Popularity) leverages first- and second-order information and provably mitigate majority-voting limitations [13].

**Saturation vs. Pass@k:**
Critical distinction: majority voting saturates—adding more votes beyond a threshold provides diminishing returns [1, 2]. Pass@k (does ANY sample give correct answer) continues improving linearly [1, 2]. For voting-gain prediction, saturation behavior is important: high-b problems may saturate at low k; low-b problems may continue improving [1, 2].

## Part 7: Benchmark Selection & Difficulty Stratification

**GSM8K (Grade School Math 8K):**
- 8,500 high-quality math word problems, elementary/middle-school level [14]
- Difficulty stratification: problems stratified by ground-truth solution steps [14]
  - Easy: 2-3 steps, ~91.2% accuracy (averaged across models) [14]
  - Medium: 4-5 steps, ~75% accuracy [14]
  - Hard: 6-11 steps, ~66.7% accuracy [14]
- Multi-step reasoning required; ground-truth step counts enable objective stratification [14]
- MIT license, available on HuggingFace at `openai/gsm8k` [21]
- Size: 7,473 train, 1,319 test (~2.7 MB) [21]

**MMLU (Massive Multitask Language Understanding):**
- 57 multiple-choice domains (math, science, humanities, social sciences) [14]
- Difficulty stratification: 4-level (high school, college, professional, expert) [14]
- Challenging and diverse; suitable for transfer testing across domains [14]
- Multiple versions: standard MMLU, MMLU-Pro (12K complex questions), MMMLU (multilingual translation) [14]
- Available on HuggingFace [14]

**MATH (Mathematics Benchmark):**
- Elementary through high-school mathematics, LaTeX-formatted [14]
- Difficulty stratified by subject (algebra, geometry, calculus, statistics) and level [14]
- Level 5 problems represent competition mathematics (hardest stratum) [14]
- Evaluates both answer correctness and solution quality [14]

**Combined Coverage:**
The three benchmarks span difficulty from ~66.7% (hard GSM8K) to ~91.2% (easy GSM8K) to expert-level (MMLU, MATH). This range is ideal for testing whether Taylor's exponent b correlates with voting gain across diverse difficulty strata [14]. Cross-benchmark testing enables transfer validation [1, 2].

## Part 8: Computational Infrastructure & Budget

**OpenRouter LLM Catalog (2026):**
OpenRouter provides unified API access to 300+ LLMs from multiple providers [16]. Pricing tiers [16]:
- Small models (7B params): ~$0.01-0.10 per million input tokens (e.g., DeepSeek 7B) [16]
- Mid-range (13-32B): ~$0.2-1 per million tokens [16]
- Large (70B+): ~$1-10 per million tokens [16]
- Free models: DeepSeek R1, Llama 3.3 70B, Gemma 3 (zero cost, rate-limited to 20 req/min, 200 req/day) [16]

Additional fees: 5.5% credit-card platform fee ($0.80 minimum) + 5% BYOK fee on requests >1M/month [16].

**Budget Estimation for $10 Cap:**
Assumptions: 1,000 problems in test set, N=20-30 samples per problem, ~500 tokens per problem/sample [16].

Cost calculation (mid-range model at $0.5/M tokens):
- 1,000 problems × 20 samples × 500 tokens = 10M tokens [16]
- Cost: 10M × ($0.5/M) = $5 [16]
- With 30 samples: 15M tokens ≈ $7.50 [16]
- Plus 5.5% fee: $7.50 × 1.055 = $7.91 [16]

Result: within $10 budget. Enables testing 2-4 models, with mix of sizes [16].

**Recommended Model Mix:**
- 1× small (7B, e.g., DeepSeek-7B or free Llama 3.3 if rate limit acceptable): tests scaling [16]
- 1× mid-range (13-32B, e.g., Qwen, Llama 3.1): standard reasoning capability [16]
- 1× large (70B+, e.g., GPT-4o or Claude Sonnet): best reasoning, transfer test [16]

This mix balances cost, capability, and transfer testing (cross-size generalization) [16].

## Part 9: Statistical Operationalization & Fitting Protocol

**Taylor's Law Fitting (Step-by-Step):**

1. **Per-problem sampling:** For each problem p in benchmark B, sample N times at fixed temperature (e.g., 0.7, N=20-30) [1, 2, 19, 20]

2. **Compute mean correctness:** m_p = (# correct samples) / N [18]

3. **Compute Bernoulli variance:** v_p = m_p × (1 - m_p) [18]
   - For small N, use unbiased estimate: v_p = Σ(x_i - m_p)² / (N-1) [18]
   - For N ≥ 15, both estimates converge [18]

4. **Handle edge cases:** Exclude problems with m_p = 0 or 1 (zero variance, make log-fitting undefined) [17, 18]
   - For remaining problems, create (log m_p, log v_p) pairs [17]

5. **Fit log-log regression:** log(v_p) = log(a) + b × log(m_p) [17]
   - Standard linear regression on log-transformed data [17]
   - Slope b is the Taylor exponent [17]
   - Extract 95% CI via standard regression errors [17]
   - Back-transform CI by exponentiating: [exp(CI_lower), exp(CI_upper)] [17]

6. **Output:** Per (model, benchmark) pair: b, 95% CI, R², N_problems_used [17]

**Bernoulli Variance Note:**
For binary correctness outcomes (right/wrong), sample variance is Binomial; MLE mean is m_p = successes/N, and unbiased variance is m_p(1-m_p) × N/(N-1) ≈ m_p(1-m_p) for N large [18]. For LLM correctness, each problem is a Bernoulli trial; across N samples, variance naturally equals m(1-m) [18].

**Spearman Rank Correlation Test (Primary Hypothesis):**

1. **Compute voting gain** per (model, benchmark): Δacc = majority-vote accuracy - single-sample accuracy at k=3 (or any fixed k) [1, 2]

2. **Rank Taylor exponents** (b values) and voting gains independently [17]

3. **Compute Spearman ρ** (rank-based correlation) between ranked b and ranked Δacc [17]

4. **Test significance:** H₀: ρ = 0; H₁: |ρ| > 0.5, p < 0.05 [1, 2]
   - Use permutation test or standard Spearman p-value [17]
   - One-sided test: b > 0 indicates clustering (expected direction) [1]

5. **Interpretation:**
   - |ρ| ≥ 0.5, p < 0.05: **SUCCESS**, Taylor's exponent predicts voting gain [1, 2]
   - |ρ| < 0.3, p > 0.05: **FAILURE**, exponent is not predictive [1, 2]
   - 0.3 ≤ |ρ| < 0.5, p < 0.1: **AMBIGUOUS**, weak relationship, may need larger sample or refined operationalization [1, 2]

**Why Spearman (not Pearson)?**
Spearman rank correlation is robust to outliers and does not assume linear relationship; appropriate for testing monotonic (not necessarily linear) association between b and voting gain [17]. Power-law relationships are naturally monotonic but non-linear in raw space [17].

## Part 10: Generalization & Mechanistic Validation

**Held-Out Test Design:**
To avoid overfitting and validate transfer:
1. Stratify (model, benchmark, difficulty-stratum) combinations into train (60%) and held-out (40%) [1, 2]
2. Compute b-to-voting-gain correlation on train set [1, 2]
3. Report correlation on held-out set separately [1, 2]
4. Transfer success: held-out ρ remains ≥ 0.5, p < 0.05 [1, 2]
5. Transfer failure: held-out ρ < 0.3 suggests model-specific or benchmark-specific effect [1, 2]

**Mechanistic Probe (Wrong-Answer Entropy):**
To validate that b proxies clustering (not just variance), analyze wrong-answer distributions in high-b vs. low-b problems [10]:

1. **Cluster wrong answers** for high-b problems (e.g., b > 75th percentile) [10, 11]
   - Try multiple methods: embedding similarity, syntactic similarity, entailment-based [11, 12]
   - Use HDBSCAN, KMeans, or LLM-driven clustering [11, 12]

2. **Compute entropy** of wrong-answer cluster distribution [10]
   - Low entropy: few dominant error clusters (high clustering) [10]
   - High entropy: many distinct error patterns (low clustering) [10]

3. **Compare** entropy in high-b vs. low-b problem sets [10]
   - Expectation: high-b has LOWER entropy (clustered errors) [10]
   - Disconfirmation: similar entropy → b captures variance, not clustering [10]

4. **Statistical test:** Mann-Whitney U test for entropy difference [10]
   - p < 0.05 supports clustering interpretation [10]

## Part 11: Expected Outcomes & Disconfirmation Criteria

**Success Scenario:**
- Spearman ρ between b and voting gain: |ρ| ≥ 0.5, p < 0.05 [1, 2]
- Transfer to held-out combinations: similar correlation [1, 2]
- Mechanistic probe: entropy lower in high-b problems, p < 0.05 [10]
- **Interpretation:** Taylor's exponent is a genuine predictor of voting benefit; clustering interpretation supported [1, 2, 10]

**Disconfirmation Scenarios:**
1. **No correlation:** |ρ| < 0.3, p > 0.05 across all (model, benchmark) pairs → Taylor's exponent does not predict voting gain; hypothesis rejected [1, 2]

2. **Transfer failure:** calibration ρ ≈ 0.5, but held-out ρ < 0.3 → overfitting or confounding by model/benchmark; effect is not general [1, 2]

3. **Entropy doesn't track b:** high-b and low-b problems have similar entropy distributions, p > 0.05 → clustering interpretation fails; b may capture other variance structure [10]

4. **Non-linear relationship:** low Spearman ρ but clear non-monotone pattern → polynomial or interaction model needed; simple power-law mapping fails [1, 2]

**Ambiguous Outcomes (Require Further Investigation):**
- **Weak correlation:** 0.3 < |ρ| < 0.5, p < 0.1 → plausible but underpowered; larger sample or refined operationalization needed [1, 2]
- **Model-specific effect:** ρ high for one model (e.g., Llama), low for another (GPT-4o) → Taylor's exponent depends on model-specific behavior, not universal property [1, 2]
- **Difficulty-dependent effect:** ρ high for easy/hard strata but low for medium → difficulty confounds relationship; exponent measurement may be scale-dependent [1, 2]

## Key Methodological Decisions for Executor

1. **Benchmarks:** GSM8K, MMLU, MATH (spans 66.7%-91.2% difficulty) [14, 21]
2. **Models:** 2-4 open LLMs via OpenRouter, mix of 7B / 13-32B / 70B sizes [16]
3. **Sampling:** Fixed temperature 0.7, N=20-30 samples per problem [19, 20]
4. **Taylor's law:** Log-log linear regression, extract b with 95% CI [17]
5. **Voting metric:** Majority vote at k=3, 5, 10; voting gain = vote_acc - single_acc [1, 2]
6. **Primary test:** Spearman ρ on b vs. voting gain, threshold |ρ| > 0.5, p < 0.05 [1, 2]
7. **Generalization:** Hold-out test on (model, benchmark, difficulty) combinations [1, 2]
8. **Mechanistic probe:** Cluster wrong answers in high-b vs. low-b, compare entropy [10, 11]
9. **Budget:** $10 OpenRouter cap; 1,000 problems × 20-30 samples ≈ $5-7.50 [16]
10. **Success:** Confirms if b correlates with voting gain AND transfers across models/benchmarks AND entropy tracks b; disconfirms if not [1, 2, 10]

## Sources

[1] [When Can Voting Help, Hurt, or Change Course? Exact Structure of Binary Test-Time Aggregation](https://arxiv.org/abs/2605.05592) — Yi Liu (2026) proves voting curves under de Finetti representation are non-monotone; signed voting signatures uniquely characterize behavior; voting hurts when per-problem correctness < 0.5.

[2] [Two Calls, Two Moments, and the Vote-Accuracy Curve of Repeated LLM Inference](https://arxiv.org/abs/2605.03379) — Yi Liu (2026) shows mean and second moment fully determine voting gain distribution-free; three-vote rule has closed-form bounds; enables prediction without large-scale empirical voting.

[3] [Taylor's law - Wikipedia](https://en.wikipedia.org/wiki/Taylor%27s_law) — Taylor's power law (Var=a*Mean^b) from 1961 ecology; b range [0.8-2.0]; b≈1 Poisson, b>1 clustering; confirmed across hundreds of species.

[4] [Taylor's law for Human Linguistic Sequences - ACL Anthology](https://aclanthology.org/P18-1105/) — Kobayashi & Tanaka-Ishii (ACL 2018) apply Taylor's law to 1100+ texts, 14 languages; universal b≈0.58 for written text; log-log regression methodology.

[5] [Taylor's law for Human Linguistic Sequences](https://arxiv.org/abs/1804.07893) — Full paper: written text b≈0.58, speech 0.63/0.68, code/music 0.79, LSTM-generated 0.50; universality across languages suggests fundamental property.

[6] [Are Diversity Metrics Measuring Diversity? A Capability-Controlled Audit of Majority-Vote Gain in LLM Ensembles](https://arxiv.org/abs/2607.20768) — LLM errors substantially correlated; accurate models show higher correlation; diversity metrics fail to predict voting gain; error correlation matters more than disagreement.

[7] [Where Does the Noise Come From? A Variance-Components Decomposition of Non-Determinism in LLM Brand Answers](https://arxiv.org/abs/2607.13304) — 12,933 responses decomposed: ~35% within-prompt resampling, remainder from prompt/model/language; systematic factors dominate pure stochasticity.

[8] [LLM Temperature and Sampling Strategies — Myths, Data, and Production Configurations](https://medium.com/@wasowski.jarek/temperature-0-0-generates-48x-more-repetition-loops-than-1-0-sampling-strategies-f0b8d7a3c850) — 4 models, 1000 questions: temperature 0.0-1.0 has no effect on accuracy; temperature 0 is repetitive, 1.0 diverse; temperature controls consistency not correctness.

[9] [LLM-assisted genre analysis: The effect of sampling temperature on reliability](https://sciencedirect.com/science/article/abs/pii/S2772766126000200) — Classification accuracy stable across temperatures; consistency degrades at high temperature; temperature affects diversity-consistency tradeoff in multi-call scenarios.

[10] [Leveraging Error Diversity in Group Rollouts for Reinforcement Learning](https://arxiv.org/abs/2605.17333) — Error diversity within sample groups predicts training success; diverse wrong answers benefit more than homogeneous failures; EDAS method amplifies rare errors.

[11] [Human-interpretable clustering of short text using large language models](https://pmc.ncbi.nlm.nih.gov/articles/PMC11750404/) — LLM embedding clustering limitations: anisotropy, low geometric separation, semantic ambiguity (singular/plural); frozen LLMs lack dataset-specific semantics.

[12] [Position: Uncertainty Quantification in LLMs is Just Unsupervised Clustering](https://arxiv.org/abs/2605.19220) — Embedding space issues: concentration in narrow cones, low-separation structure; alternative methods (syntactic, entailment-based) needed for robust clustering.

[13] [When Does Delegation Beat Majority? A Delegation-Based Aggregator for Multi-Sample LLM Inference](https://arxiv.org/abs/2606.08098) — Ranked voting (instant runoff, Borda, MRR) modest gains over plurality; confidence-weighted voting best when calibrated; advanced methods provably exceed majority voting.

[14] [Mathematical Reasoning Benchmarks | Giskard Documentation](https://docs.giskard.ai/start/glossary/llm-benchmarks/math-problems) — GSM8K: 8.5K problems, easy 91.2%, hard 66.7% accuracy; MMLU: 57 domains, 4-level difficulty; MATH: competition-level; all difficulty-stratified, HuggingFace available.

[15] [Tiny Recursive Reasoning with Mamba-2 Attention Hybrid](https://arxiv.org/abs/2602.12078) — Difficulty-stratified voting: hard inputs (correct-vote-share <15%) gain +4.9 points hybrid; easy gain +4.6 transformer; voting dynamics reverse across difficulty.

[16] [OpenRouter Pricing 2026: 300+ LLM Models](https://costgoat.com/pricing/openrouter) — OpenRouter: 300+ models; small <$0.1/M; mid $0.2-1/M; large $1-10/M; free models available; 5.5% credit-card + 5% BYOK fees; $10 budget enables 2-4 models.

[17] [On the use of log-transformation vs. nonlinear regression for analyzing biological power laws](https://digitalcommons.usu.edu/cgi/viewcontent.cgi?article=1351&context=biology_facpub) — Log-log regression for power-law fitting: slope=b; 95% CI via standard regression; log-transformation preferred for allometric data; back-transform CI by exponentiating.

[18] [8.3: Estimation in the Bernoulli Model - Statistics LibreTexts](https://stats.libretexts.org/Bookshelves/Probability_Theory/Probability_Mathematical_Statistics_and_Stochastic_Processes_(Siegrist)/08:_Set_Estimation/8.03:_Estimation_in_the_Bernoulli_Model) — Bernoulli variance=p(1-p); MLE of p=(# successes)/N; for LLM correctness, p=mean, variance=p(1-p); handles binary outcomes in repeated sampling.

[19] [Mastering LLM Temperature: A Step-by-Step Guide](https://medium.com/thinking-sand/mastering-llm-temperature-a-step-by-step-guide-81e9f27fef77) — Temperature 0.7-0.8 standard for repeated sampling; 0.8 highest accuracy for code; samples+ranking beats single high-temp output; multiple samples with temperature 0.8-1.2.

[20] [LLM Temperature Settings: A Complete Guide for Developers](https://tetrate.io/learn/ai/llm-temperature-guide) — Temperature 0.6-0.8 balances coherence & creativity; GPT-4 used 0.6 for free-response; little rigorous research on optimal settings; context-dependent best practice.

[21] [openai/gsm8k · Datasets at Hugging Face](https://huggingface.co/datasets/openai/gsm8k) — GSM8K: 8.5K grade-school math problems, MIT license; 7,473 train / 1,319 test; ~2.7 MB download; publicly available on HuggingFace.

## Follow-up Questions

- Can Taylor's exponent b computed from one model predict voting gain in other models? That is, does b capture model-independent problem structure, or is it model-specific (high b for GPT-4o on hard problems, low b for Llama on same problems)?
- What is the relationship between Taylor's exponent b and ground-truth problem difficulty or semantic ambiguity? Can b be validated as a proxy for intrinsic task difficulty independent of model, or does difficulty confound the b-to-voting-gain correlation?
- For the mechanistic probe of wrong-answer clustering entropy, which clustering method (embedding similarity, syntactic, entailment-based, LLM-driven) is most robust to low-signal embedding spaces and most predictive of voting gain—or do all methods converge on the same result?

---
*Generated by AI Inventor Pipeline*
