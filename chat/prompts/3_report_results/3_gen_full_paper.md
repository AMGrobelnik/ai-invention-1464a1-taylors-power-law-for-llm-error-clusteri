# gen_full_paper — report_results

> Phase: `gen_paper_repo` · `gen_full_paper`
> Run: `run_Br8Nz-7w30tX` — Taylor's Power Law for LLM Error Clustering: A Hypothesis Not Sustained by Data
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_full_paper` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-08-01 15:34:23 UTC

````
<research_methodology>
Write like an experienced academic. Reviewers judge both the science and the writing.

- Claims must be proportional to evidence. Choose verbs carefully — "demonstrate," "observe," and "hypothesize" mean different things.
- Every result needs: what was measured, on what data, the numbers, and what they mean.
- Methodology must be specific enough to reproduce. Related work must be organized by theme, not a literature dump.
- State limitations honestly. Avoid both overclaiming and excessive hedging.
</research_methodology>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

<workspace>
Your workspace: `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_Br8Nz-7w30tX/4_gen_paper_repo/_4_assemble_paper/paper/workspace`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_Br8Nz-7w30tX/4_gen_paper_repo/_4_assemble_paper/paper/workspace/`:
GOOD: `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_Br8Nz-7w30tX/4_gen_paper_repo/_4_assemble_paper/paper/workspace/file.py`, `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_Br8Nz-7w30tX/4_gen_paper_repo/_4_assemble_paper/paper/workspace/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>

<task>
Create a publication-ready top-conference LaTeX paper with BibTeX from <paper_text> and <available_figures>, compile to PDF.
</task>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<paper_text>
title: 'Taylor''s Power Law for LLM Error Clustering: A Hypothesis Not Sustained by Data'
abstract: >-
  We test whether Taylor's power law—a principle from ecology relating population variance to mean through variance = a ×
  mean^b—can serve as a cheap diagnostic for predicting when majority-vote aggregation benefits large language models. The
  hypothesis is appealing: the exponent b indicates clustering (b > 1) versus independence (b ≈ 1) in error distributions,
  directly mirroring the vote-help-versus-hurt distinction. We design an experiment to measure b from repeated LLM sampling
  and correlate it with voting gain across 90 problems spanning GSM8K, MMLU, and ARC-Challenge. Our findings are negative:
  (1) the fitted exponent b does not distinguish the null hypothesis (independent Bernoulli) from the clustering hypothesis
  at p < 0.05 across any model-benchmark pair (minimum p = 0.18); (2) within-benchmark correlations between a per-problem
  overdispersion proxy and voting gain range from ρ = 0.16 to 0.28, all non-significant (p > 0.33); (3) the meta-analytic
  pooled correlation is ρ = 0.21 (95% CI: 0.03–0.38), below the pre-registered success threshold of |ρ| > 0.5. These results
  suggest that either (a) the clustering signal is too weak to detect at the sample sizes we used, or (b) Taylor's exponent,
  while a valid clustering statistic in ecology, does not capture the structure of LLM error correlation relevant to voting.
  We detail why this null result is informative: the noise floor under binomial sampling is substantial, the accuracy range
  we tested (60–95%) avoids the <50% regime where voting actively harms, and a direct comparison with Liu's competing second-moment
  theory remains unperformed. This paper contributes by documenting a hypothesis that didn't work and clarifying the methodological
  barriers to cheap test-time-compute diagnostics for LLMs.
paper_text: |
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

  Because the number of problems per model-benchmark pair (10–14) is too small to fit a robust log-log regression for exponent b (a power-law fit requires many more data points), we instead used per-problem overdispersion od_p as a local proxy for clustering: od_p ≈ 1 indicates independent Bernoulli; od_p > 1 indicates clustering \footnote{Code: \url{https://github.com/AMGrobelnik/ai-invention-1464a1-taylors-power-law-for-llm-error-clusteri/tree/main/round-2/evaluation-1}}.

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

  Key result: **Zero of five tested (model, benchmark) combos rejected the independence null at p < 0.05.** Minimum p-value = 0.18. This indicates that the observed exponent values are statistically indistinguishable from what we would expect if errors were purely independent. Per the pre-registered plan, this noise-floor gate means the hypothesis is not established as distinguishable from sampling noise at this scale .

  ### 2. Within-Benchmark Correlations: Weak and Non-Significant

  Despite the noise-floor result, we computed per-problem overdispersion od_p as a local clustering proxy and tested correlation with voting gain within each benchmark :

  - **ARC-Challenge** (n=14 problems): Spearman ρ = 0.28, p = 0.33, 95% CI: [−0.04, 0.58].
  - **GSM8K** (n=10 problems): Spearman ρ = 0.16, p = 0.66, 95% CI: [−0.33, 0.53].
  - **MMLU** (n=14 problems): Spearman ρ = 0.25, p = 0.38, 95% CI: [−0.06, 0.55].

  All correlations are non-significant. The correlation magnitude (ρ ~0.16–0.28) is well below the pre-registered threshold of |ρ| > 0.5. Across all k values (3, 5, 10), the pattern holds .

  ### 3. Meta-Analytic Pooling: No Systematic Signal

  Using DerSimonian-Laird random-effects meta-analysis across all estimated correlations, the pooled Spearman ρ = 0.21, 95% CI: [0.03, 0.38], with zero heterogeneity (I² = 0, τ² = 0). This pooled estimate is below the pre-registered success threshold and is driven primarily by ARC-Challenge, which shows the largest correlation. The zero heterogeneity indicates that the weak correlations are consistent across benchmarks—not a sign of hidden signal in a subset .

  ### 4. Effect Sizes: Small Across Benchmarks

  We computed Cohen's d comparing top- and bottom-quartile overdispersion groups:

  - **ARC-Challenge**: d = −0.16, small effect.
  - **GSM8K**: d = −0.12, negligible effect.
  - **MMLU**: d = −0.11, negligible effect.

  The small effect sizes reinforce the weak signal .

  ## Discussion

  ### Why the Hypothesis Failed

  Three factors likely explain the null result:

  **1. Noise Floor Under Binomial Sampling.** The Taylor exponent fitted on only 5 samples per problem suffers from substantial binomial sampling noise. Estimated variance m_p(1 − m_p) has sampling error ~1/√N; the ratio of two noisy quantities (variance and mean) compounds this error. The simulated null distribution showed that random Bernoulli data yields fitted exponents similar to our observed values, indicating the signal-to-noise ratio is unfavorable at this sample size .

  **2. Limited Accuracy Range.** Our tested benchmarks span mean per-problem success rates of 60–95%, a regime where voting generally helps. The critical regime where voting amplifies errors (per-problem success < 50%) is undocumented in our data. Taylor's exponent may behave differently in the error-amplification regime, making our findings inapplicable to the exact operational scenario where a cheap diagnostic would be most valuable .

  **3. Error Correlation Structure.** Recent work documents that LLM error correlation is non-uniform and structured: co-failure rates (all models wrong) far exceed predictions from pairwise correlation, imposing a ceiling on voting effectiveness [8]. This structured clustering (some problems inherently hard, others easy) may not decompose into a uniform clustering signal (high b) that Taylor's law measures. LLM errors may violate the assumptions underlying Taylor's law—specifically, that clustering is driven by a shared external stochastic factor, not by fundamental problem difficulty \footnote{Code: \url{https://github.com/AMGrobelnik/ai-invention-1464a1-taylors-power-law-for-llm-error-clusteri/tree/main/round-2/research-1}}.

  ### Novelty and Comparison with Liu's Theory

  A significant gap in our work is the lack of direct comparison with Liu's competing two-call theory [4]. Liu proposes that two labeled calls on each problem suffice to identify the second moment m₂ of the latent correctness distribution, which exactly determines voting-gain bounds for any budget. Taylor's exponent b also captures problem-level heterogeneity, but through a different parametrization .

  We did not empirically test whether b predicts voting gain more efficiently or accurately than m₂, or whether b transfers across (model, benchmark) pairs better than m₂. Without this comparison, we cannot claim novelty over Liu's theory—we can only claim novelty in domain (applying an ecology principle to LLMs), not in method.

  ### Implications for Test-Time Compute Allocation

  Our negative result highlights a fundamental challenge in developing cheap operational diagnostics for LLMs: the signal (error clustering) is subtle, the noise floor (binomial sampling variance) is high, and the solution (voting) is already computationally cheap relative to inference. For practitioners, this suggests:

  1. **Trial-and-error remains the operational standard.** Until a diagnostic shows strong transferability and signal-to-noise ratio >> 1, post-hoc evaluation on a held-out dev set remains the most reliable method.
  2. **Higher sample counts are needed.** Fitting a robust Taylor exponent requires N >> 5 samples per problem; the compute savings from avoiding costly per-problem sampling may not justify the cost savings from skipping unnecessary voting.
  3. **Structured error correlation may require different models.** The uniform clustering assumption underlying Taylor's law may not hold for LLMs; domain-specific models of error structure (e.g., problem difficulty, reasoning step count, co-failure patterns) may be more informative.

  ### Limitations

  **Sample size.** Our 90 problems and 5 samples per problem per model are at the lower end of what power-law estimation requires; 500+ problems and 20–30 samples per problem would provide more robust exponent estimates and improve statistical power .

  **Accuracy range.** The 60–95% regime tested is unrepresentative of the full landscape where voting decisions matter most (< 50% per-problem success, where voting harms). Extending to very-hard benchmarks or adversarial tasks is essential.

  **Model diversity.** We tested only three model sizes from the same family. Testing across diverse model families, architectures, and training regimes would clarify whether b is a model-universal signal or a model-specific property.

  **Mechanistic understanding.** We did not analyze the structure of wrong answers (e.g., via embedding clustering or syntactic analysis) to confirm the interpretation that high od_p reflects truly clustered, systematic errors versus random binomial variation.

  ### Methodological Contributions

  Despite the negative empirical result, this work contributes methodologically:

  1. **Noise-floor validation protocol.** We demonstrate a principled way to test whether a fitted exponent is distinguishable from the null hypothesis (i.i.d. Bernoulli), using per-combo null simulation and p-value gates .
  2. **Bibliography verification.** We identify and resolve gaps in the original hypothesis's citation chain, replacing unverifiable anonymous references with verified peer-reviewed sources .
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
summary: >-
  We test the hypothesis that Taylor's power law predicts whether majority voting improves LLM accuracy. Using repeated sampling
  on 90 problems across GSM8K, MMLU, and ARC-Challenge, we find that the fitted exponent does not distinguish clustering from
  independence at p < 0.05 (minimum p = 0.18). Within-benchmark correlations are weak (ρ = 0.16–0.28, all p > 0.3) and below
  the pre-registered success threshold (|ρ| > 0.5). Meta-analytic pooling yields ρ = 0.21 (95% CI: 0.03–0.38). The null result
  is explained by three factors: binomial sampling noise dominates at N=5 samples per problem, the tested accuracy range (60–95%)
  avoids the <50% regime where voting actively harms and exponent behavior is unknown, and LLM error correlation may be structured
  (co-failure patterns, problem difficulty) rather than uniform clustering. We conclude that Taylor's law, while well-validated
  in ecology, does not appear to capture the error-correlation structure relevant to LLM voting without substantial methodological
  refinement.
</paper_text>

<available_figures>
--- Item 1 ---
id: fig_noise_floor
title: 'Noise Floor: Exponent Indistinguishable from Independence'
caption: >-
  Null hypothesis test for each model-benchmark pair. The fitted Taylor exponent b from real data (red) is compared against
  the simulated null distribution (gray histogram) assuming i.i.d. Bernoulli correctness (true b=1). None of the five tested
  combos reject the null at p < 0.05 (minimum p = 0.18), indicating that observed exponents are statistically indistinguishable
  from random sampling noise.
image_gen_detailed_description: >-
  Five subplots arranged horizontally, one per model-benchmark combo (small_3b × GSM8K, small_3b × MMLU, small_3b × ARC-Challenge,
  mid_13b × MMLU, large_70b × ARC-Challenge). Each subplot has a histogram (gray, 0.8–1.5 range for b) showing the null distribution
  from 1000 simulations of independent Bernoulli problems at the same N and problem count. A vertical red line marks the observed
  b from real data. Y-axis: frequency (0–500). X-axis: Taylor exponent b (0.8–1.5). Title per subplot: combo name and p-value.
  Legend: 'Simulated null (independent errors)' gray, 'Observed b (real data)' red line. Sans-serif font, white background.
aspect_ratio: '21:9'
summary: >-
  Validation that observed exponents are not distinguishable from independence; all p-values > 0.05 indicate noise floor gate
  failure.
figure_path: figures/fig_noise_floor_v0.jpg
</available_figures>

<figure_requirements>
CRITICAL: Include ALL figures from <available_figures>. No exceptions.

- Every figure MUST use \includegraphics{figures/filename.jpg}
- Do NOT skip, convert to tables, or describe without inserting
- Each needs: \begin{figure*|figure}[placement], \includegraphics, \caption, \label, \end{...} — pick env + placement by the figure's `aspect_ratio` field (see PLACEMENT below). Constrain every \includegraphics with `width=\linewidth,height=0.4\textheight,keepaspectratio` (single-column) or `width=\textwidth,height=0.45\textheight,keepaspectratio` (figure*). Use exactly these option keys — `max height=` is NOT valid LaTeX
- Use the `caption` field from each figure for \caption{...} — do NOT invent new captions
- Place figures where their [FIGURE:fig_id] markers appear in paper_text
- VERIFICATION: paper.tex MUST have exact same number of \includegraphics as <available_figures>
- Do NOT generate new figure images (no matplotlib, no PIL, no image generation). Use ONLY the pre-generated figures from <available_figures>. They were already created by a previous pipeline step.

PLACEMENT BY ASPECT RATIO (use the `aspect_ratio` field on each figure):
- `21:9` (architecture diagrams / hero figures): \begin{figure*}[!t] (full two-column width, top of page). The hero architecture diagram should appear EARLY in the paper — typically at the top of page 2. Marker placement in paper_text already determines this; preserve it.
- `16:9` (comparisons, multi-panel results): \begin{figure*}[!t] for full-width or \begin{figure}[!htbp] for single-column.
- `4:3` / `1:1` / `3:2` / `3:4` / `9:16`: \begin{figure}[!htbp] (single-column).
</figure_requirements>

<artifact_links>
The paper_text contains \footnote{Code: \url{...}} references linking to artifact source code
on GitHub. Include \usepackage{hyperref} and \usepackage{url}.
Preserve these exactly as-is — do not remove, rewrite, or convert them to plain text.
The URLs will not resolve yet (the repo is deployed after compilation) — do NOT try to verify or fix them.
</artifact_links>

<headings>
NEVER use inline math (``$...$``) inside ``\section{...}`` / ``\subsection{...}`` / ``\subsubsection{...}`` arguments — hyperref's bookmark builder errors out (``Token not allowed in a PDF string``) and the PDF outline breaks. If a section heading needs a math-looking term, use the text equivalent (``d star`` not ``$d^*$``, ``alpha-equivalent`` not ``$\alpha$-equivalent``) or wrap it in ``\texorpdfstring{$math$}{plain}``. Inline math inside body paragraphs is fine.
</headings>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-paper-to-latex, aii-semscholar-bib.
TODO 2. Review <paper_text> and <available_figures>. Copy all figure images into ./figures/ in your workspace. Count figures — MUST include every one. Plan placements per section. Build `./references.bib` via aii_semscholar_bib__fetch — collect DOIs/ArXiv IDs from <paper_text> and batch-fetch all BibTeX in one call. Do NOT fabricate entries.
TODO 3. Create `./paper.tex` per aii-paper-to-latex skill's setup, write ALL sections, insert ALL figures from <available_figures>, include `./references.bib` via \bibliography. Compile to PDF per skill's process. Fix errors.
TODO 4. CRITICAL VERIFICATION: Run `grep -c 'includegraphics' paper.tex`, confirm count equals figures in <available_figures>. If not, add missing figures. Verify `./paper.pdf` was created.
TODO 5. VISUAL REVIEW: Write Python script to convert EVERY page of paper.pdf to PNG at 150 DPI (use pdf2image or pymupdf). Then read ALL page screenshots — each page image costs ~1,600 tokens so a 15-page paper is only ~24K tokens. You MUST read every page. The ONLY exception is if all page images would not fit in your remaining context — in that case, read as many as fit and state which pages you are skipping and why. Check every page for layout issues, overlapping figures, cut-off text, bad spacing, formatting problems. Fix issues and recompile.
TODO 6. FINAL READ: Check page count (`pdfinfo paper.pdf` or pymupdf). Read entire paper.pdf — check for missing sections, unclear explanations, inconsistencies, typos. Fix and recompile. The ONLY exception is if all pages would not fit in your remaining context — in that case, read as many pages as fit and state which pages you are skipping and why.
</todos>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "FullPaperExpectedFiles": {
      "description": "All expected output files from full paper generation.",
      "properties": {
        "paper_tex_path": {
          "description": "Path to LaTeX source file. Example: 'paper.tex'",
          "title": "Paper Tex Path",
          "type": "string"
        },
        "paper_pdf_path": {
          "description": "Path to compiled PDF. Example: 'paper.pdf'",
          "title": "Paper Pdf Path",
          "type": "string"
        },
        "references_bib_path": {
          "description": "Path to BibTeX bibliography file. Example: 'references.bib'",
          "title": "References Bib Path",
          "type": "string"
        },
        "figure_paths": {
          "description": "Paths to all figure image files. Example: ['figures/fig1_v0.jpg', 'figures/fig2_v0.jpg']",
          "items": {
            "type": "string"
          },
          "title": "Figure Paths",
          "type": "array"
        }
      },
      "required": [
        "paper_tex_path",
        "paper_pdf_path",
        "references_bib_path",
        "figure_paths"
      ],
      "title": "FullPaperExpectedFiles",
      "type": "object"
    }
  },
  "description": "Full paper \u2014 structured output from paper generation.",
  "properties": {
    "title": {
      "description": "Paper title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance. Aim for about 4-8 words (~40 characters).",
      "maxLength": 90,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "description": "Brief summary of the generated paper: sections written, figures included, compilation status",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/FullPaperExpectedFiles",
      "description": "All output files you created. Must include paper.tex, paper.pdf, references.bib, and paths to all figure files."
    }
  },
  "required": [
    "title",
    "summary",
    "out_expected_files"
  ],
  "title": "FullPaper",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [2] HUMAN-USER prompt · 2026-08-01 15:34:23 UTC

```
PROVISIONING RELOAD VISUAL: capture the main panel after reload.
```

### [3] SKILL-INPUT — aii-paper-to-latex · 2026-08-01 15:34:27 UTC

The agent loaded the **aii-paper-to-latex** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-paper-to-latex
description: LaTeX paper assembly and compilation. Covers document setup, figure inclusion from pre-generated JPEGs, compilation process, and output files. Use when assembling a paper from pre-written text and pre-generated figures into a compiled PDF.
---

## LaTeX Paper Assembly

Assembles a research paper from paper text, pre-generated figure JPEGs, and bibliography into a compiled PDF.

### Document Setup

```latex
\documentclass[11pt,letterpaper]{article}
\usepackage{graphicx, geometry, amsmath, hyperref, natbib, booktabs, xcolor, listings}
\geometry{margin=1in}
\hypersetup{colorlinks=true, linkcolor=black, citecolor=black, urlcolor=black}
```

### Figure Inclusion

CRITICAL: Include ALL figures. Every figure MUST appear in the paper.

```latex
\begin{figure}[!htbp]
  \centering
  \includegraphics[width=0.92\textwidth,keepaspectratio]{figures/filename.jpg}
  \caption{Descriptive caption.}
  \label{fig:label}
\end{figure}
```

Rules:
- ALWAYS use `[!htbp]` float placement (NOT `[t]` or `[h]` alone)
- ALWAYS constrain with `width` and `keepaspectratio` to prevent page takeover
- Every figure needs `\caption`, `\label`, and a `\ref` in the text
- Do NOT convert figures to tables or describe them without inserting the image
- Do NOT skip any figures

### Compilation Process

Run each command separately (do NOT chain with `&&` — pdflatex often exits non-zero on warnings, which would skip bibtex and leave citations as `??`):

```bash
pdflatex -interaction=nonstopmode paper.tex
bibtex paper
pdflatex -interaction=nonstopmode paper.tex
pdflatex -interaction=nonstopmode paper.tex
```

All four commands are required. Skipping bibtex causes `??` in all citations.
Fix any errors between runs. Verify `./paper.pdf` was created.

### Output Files

- `./paper.tex` — LaTeX source
- `./references.bib` — bibliography file
- `./paper.pdf` — compiled PDF
- `./figures/*.jpg` — all figure images (pre-generated, copied into workspace)
````

### [4] SKILL-INPUT — aii-semscholar-bib · 2026-08-01 15:34:27 UTC

The agent loaded the **aii-semscholar-bib** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-semscholar-bib
description: Build bibliographies using Semantic Scholar. Batch-fetch BibTeX for papers by DOI, ArXiv ID, or title. Use when writing papers, generating reference lists, or building .bib files.
---

## Tool: `aii_semscholar_bib__fetch`

Batch-fetch BibTeX entries from Semantic Scholar. Pass all references in a single call — the tool handles batching internally.

### How it works

1. **DOI/ArXiv refs** → batched into POST /paper/batch calls (up to 500 per API call, auto-chunked)
2. **Title-only refs** → individual GET /paper/search/match (1s delay between)
3. **Post-process** → fix entry type, fix citation key (AuthorYYYY), inject DOI

The ability server runs a single worker (`max_threads: 1`). Multiple concurrent tool calls are queued — each runs independently (no cross-request aggregation). Batching happens within each request.

### Input format

```json
{
  "references": [
    {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
    {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
    {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
  ]
}
```

Each reference object can have:
- `doi` — DOI string (ArXiv DOIs like `10.48550/arXiv.XXXX.XXXXX` auto-convert to ArXiv IDs)
- `arxiv` — ArXiv ID (e.g. `"2305.14325"`)
- `title` — Paper title (used for search/match when no DOI/ArXiv)
- `author` — First author last name (for cleaner citation key)
- `year` — Publication year (int, for citation key)

At least one of `doi`, `arxiv`, or `title` is required per reference.

### Output format

```json
{
  "success": true,
  "bib_text": "@inproceedings{Vaswani2017, ...}\n\n@article{Wei2022, ...}",
  "total": 3,
  "found": 3,
  "failed_count": 0,
  "entries": [{"citation_key": "Vaswani2017", "bibtex": "...", "title": "...", "doi": "...", "arxiv": ""}],
  "failed": []
}
```

### Workflow

1. Collect DOIs, ArXiv IDs, or titles for all papers you need to cite
2. Call `aii_semscholar_bib__fetch` with the full list in **one call**
3. Save `bib_text` from the response to your `references.bib` file
4. Check `failed` — for any missed papers, follow the **fallback procedure** below

### Fallback for failed references (MANDATORY)

NEVER fabricate BibTeX. For each failed reference:
1. **WebSearch** for `"Title" author year` (try `site:arxiv.org` too)
2. **WebFetch** the paper page → extract title, authors, year, venue, DOI/ArXiv ID
3. If DOI/ArXiv found → retry `aii_semscholar_bib__fetch` with it
4. Last resort: write BibTeX by hand using **only verified info from the actual paper page**

---

### CLI (for manual use / debugging)

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-semscholar-bib" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_semscholar_bib__fetch.py --refs '[
  {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
  {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
  {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
]'
```

`--json, -j` — output raw JSON instead of .bib text

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````
