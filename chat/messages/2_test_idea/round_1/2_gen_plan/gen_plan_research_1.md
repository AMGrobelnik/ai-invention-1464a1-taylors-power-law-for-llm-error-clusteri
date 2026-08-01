# gen_plan_research_1 — test_idea

> Phase: `invention_loop` · round 1 · `gen_plan`
> Run: `run_Br8Nz-7w30tX` — Taylor's Power Law for LLM Error Clustering: A Hypothesis Not Sustained by Data
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_plan_research_1` (terminal_claude_agent, claude-haiku-4-5)

### [1] CONFIG · 2026-08-01 14:41:20 UTC

```
model: claude-haiku-4-5 | effort: high | permission: bypassPermissions | cwd: /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_Br8Nz-7w30tX/3_invention_loop/iter_1/gen_plan/gen_plan_research_1
```

### [2] SYSTEM-USER prompt · 2026-08-01 14:41:26 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A plan generator (Step 3.2: GEN_PLAN in the invention loop)

You received the hypothesis, an artifact direction to elaborate, and dependency artifacts relevant to the plan.
Your job: elaborate this direction into a detailed, actionable plan for the executor agent.

Specific, actionable plan → valuable artifact. Vague plan → wasted execution.
</your_role>
</ai_inventor_context>

<artifact_type_info>
You are expanding an artifact direction of type: RESEARCH

RESEARCH
Web research to answer key questions — like a researcher making decisions.
Runtime: LLM Agent, no code execution.
Tools: the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text).
Capabilities: Find, synthesize, and compare information across sources; survey SOTA and best practices.
Deps: REQUIRED none | OPTIONAL other RESEARCH to build on prior findings
</artifact_type_info>

<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>
</available_resources>

<time_budget>

The research executor has 3h total (including writing code, debugging, testing, and fixing errors).

</time_budget>

<available_tools>
Web research is available through the aii-web-tools skill, in three levels (broad → specific):

1. web search — Returns titles, URLs, snippets. Use first to discover and scan the landscape.
2. web fetch — Reads a page and returns its content as markdown (HTML or PDF). Use to understand a source. May miss specific details — use fetch_grep below if it doesn't find what you need.
3. fetch_grep — Regex search over a page/PDF's full text. Returns exact matching sections with context. Use for precise details, exact numbers, methodology, or PDFs.

Workflow: search → fetch (understand) → fetch_grep (extract specifics).
</available_tools>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<plan_guidelines>
You are expanding an artifact direction from the strategy into a detailed plan.
The artifact direction specifies what to do at a high level (type, objective, approach, dependencies).
Your job is to make it concrete and actionable as a detailed plan.
Use web research to look up technical details, verify feasibility, and find reference materials
that will make your plan more concrete and actionable for the executor.

GOOD PLANS:
- Make each component SPECIFIC and actionable (not vague platitudes)
- Consider both success AND failure scenarios
- Build on the approach in the artifact direction
- Add concrete details the executor needs

BAD PLANS:
- Vague hand-waving ("do research on X")
- Ignoring the approach in the artifact direction
- Missing critical details the executor needs
</plan_guidelines>

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

<hypothesis>
kind: hypothesis
title: Ecology's Clustering Law Predicts Vote Failure
hypothesis: >-
  For a fixed LLM and prompting scheme, the fluctuation-scaling exponent b obtained by fitting Taylor's power law (log Var[correctness]
  = log a + b * log Mean[correctness], measured across many problems by repeated sampling) is a reliable, task-agnostic diagnostic
  of whether majority-vote/self-consistency aggregation will help or hurt on that problem population: exponent values near
  b=1 (independent, Poisson-like error scatter) mark regimes where voting reliably improves accuracy, while elevated exponents
  (b appreciably above 1, indicating clustered, correlated error patterns akin to aggregated populations in ecology) mark
  regimes where voting yields little gain or actively hurts accuracy versus single-sample decoding.
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
</hypothesis>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for the methods, proper baselines, and evaluation this field demands.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>

<artifact_direction>
Make this direction concrete and actionable. Keep the same type and respect dependencies.

id: research_iter1_dir1
type: research
objective: >-
  Survey literature and establish methodology: what is known about when majority voting helps/hurts LLMs, how voting gain
  is measured, and how Taylor's law has been applied to diagnose clustering in other domains.
approach: >-
  Web search and fetch papers on: (1) majority voting / self-consistency for LLMs (de Finetti representation, prior voting
  analyses); (2) Taylor's power law in ecology and other domains (variance-mean scaling as a clustering diagnostic); (3) LLM
  sampling variance and error correlation (when does resampling produce independent vs correlated failures). Synthesize to
  define: the measurement protocol for voting gain (how many samples, which aggregation rule, success metrics), temperature/sampling
  regime, benchmark diversity requirements, and how to operationalize the b-to-voting-gain prediction. Identify any prior
  work applying Taylor's law to LLM sampling (expect none; this would be the novelty).
depends_on: []
</artifact_direction>



<instructions>
YOUR ROLE: Write a detailed PLAN for the artifact. A separate executor agent runs the actual artifact later.

You are a PLANNER, not an executor. Your output is a plan that tells the executor what to do and how.
Do NOT execute the artifact itself — a separate agent handles that. Your job is to plan it so well that the executor can follow your plan step by step.

You CAN and SHOULD: search the web, read papers, and explore library docs to make your plan concrete.
You CANNOT run shell commands or scripts — code execution is disabled. Research via web tools only.

Do NOT do the executor's job: don't download datasets, don't implement code, don't run experiments, don't write proofs, don't compute evaluations.

<artifact_executor_scope>
IMPORTANT: Each artifact executor has a focused prompt that guides it to do ONE thing well. It will NOT perform tasks outside its scope — assigning the wrong work to the wrong artifact type wastes an iteration. Match the task to the right executor.

RESEARCH executor scope:
  Output: research_out.json with {answer, sources, follow_up_questions} + research_report.md
  DOES: Web research — search, read, synthesize information from papers/docs/APIs into a structured report
  DOES NOT: Run code, download files, execute scripts, compute anything — no shell/Python access
  Use for literature surveys, API documentation, technical specifications — pure information gathering
</artifact_executor_scope>

<artifact_planning_rules>
RESEARCH: Plan early — findings guide dataset selection, experiment design, and methodology.
</artifact_planning_rules>


GOOD PLANS: specific, actionable, consider failure scenarios, build on the suggested approach.
BAD PLANS: vague hand-waving, ignoring the suggested approach, missing critical executor details.
</instructions><user_data>
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
  "description": "Plan for a RESEARCH artifact.",
  "properties": {
    "title": {
      "description": "Plan title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters).",
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Brief summary",
      "title": "Summary",
      "type": "string"
    },
    "runpod_compute_profile": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": "cpu_light",
      "description": "Compute tier for execution \u2014 pick from the available profiles list (e.g., 'gpu', 'cpu_heavy', 'cpu_light'). Only used in RunPod mode.",
      "title": "Runpod Compute Profile"
    },
    "question": {
      "default": "",
      "description": "The specific research question to investigate",
      "title": "Question",
      "type": "string"
    },
    "research_plan": {
      "description": "Step-by-step plan for web research to gather this research",
      "title": "Research Plan",
      "type": "string"
    },
    "explanation": {
      "description": "Why this research matters and what question it answers",
      "title": "Explanation",
      "type": "string"
    }
  },
  "required": [
    "title",
    "research_plan",
    "explanation"
  ],
  "title": "ResearchPlan",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [3] HUMAN-USER prompt · 2026-08-01 14:41:26 UTC

```
PROVISIONING RELOAD VISUAL: capture the main panel after reload.
```

### [4] ASSISTANT · 2026-08-01 14:41:32 UTC

```
I'll create a detailed research plan by first exploring the relevant literature on majority voting, Taylor's power law, and LLM sampling behavior. Let me gather concrete information to make this plan actionable.
```

### [5] TOOL CALL — Skill · 2026-08-01 14:41:32 UTC

```
aii-web-tools
```

### [6] TOOL RESULT — Skill · 2026-08-01 14:41:32 UTC

```
{"success": true, "commandName": "aii-web-tools"}
```

### [7] TOOL CALL — ToolSearch · 2026-08-01 14:41:40 UTC

```
{'query': 'select:WebSearch,WebFetch', 'max_results': 2}
```

### [8] TOOL RESULT — ToolSearch · 2026-08-01 14:41:40 UTC

```
{"matches": ["WebSearch", "WebFetch"], "query": "select:WebSearch,WebFetch", "total_deferred_tools": 21}
```

### [9] TOOL CALL — WebSearch · 2026-08-01 14:41:42 UTC

```
majority voting self-consistency LLM reasoning 2023 2024 2025
```

### [10] TOOL CALL — WebSearch · 2026-08-01 14:41:42 UTC

```
de Finetti representation voting test-time aggregation
```

### [11] TOOL CALL — WebSearch · 2026-08-01 14:41:42 UTC

```
Taylor power law fluctuation scaling variance mean ecology
```

### [12] TOOL CALL — WebSearch · 2026-08-01 14:41:42 UTC

```
LLM sampling variance error correlation resampling
```

### [13] TOOL RESULT — WebSearch · 2026-08-01 14:41:50 UTC

```
{"query": "Taylor power law fluctuation scaling variance mean ecology", "results": [{"tool_use_id": "srvtoolu_01E9iR3AeLhAG4uzpi6tESk3", "content": [{"title": "Taylor’s power law of fluctuation scaling and the growth-rate theorem - ScienceDirect", "url": "https://www.sciencedirect.com/science/article/abs/pii/S004058091300035X"}, {"title": "Temporal fluctuation scaling in populations and communities - PubMed", "url": "https://pubmed.ncbi.nlm.nih.gov/25039234/"}, {"title": "Taylor's power law of fluctuation scaling and the growth-rate theorem - PubMed", "url": "https://pubmed.ncbi.nlm.nih.gov/23689021/"}, {"title": "Random sampling of skewed distributions implies Taylor’s power law of fluctuation scaling | PNAS", "url": "https://www.pnas.org/doi/10.1073/pnas.1503824112"}, {"title": "Every variance function, including Taylor’s power law of fluctuation scaling, can be produced by any location-scale family of distributions with positive mean and variance | Theoretical Ecology | Springer Nature Link", "url": "https://link.springer.com/article/10.1007/s12080-019-00445-7"}, {"title": "Every variance function, including Taylor’s power law of fluctuation scaling, can be produced by any location-scale family of distributions with positive mean and variance | Request PDF", "url": "https://www.researchgate.net/publication/337692937_Every_variance_function_including_Taylor's_power_law_of_fluctuation_scaling_can_be_produced_by_any_location-scale_family_of_distributions_with_positive_mean_and_variance"}, {"title": "1 TAYLOR'S POWER LAW: BEFORE AND AFTER 50 YEARS OF SCIENTIFIC SCRUTITY", "url": "https://arxiv.org/pdf/1505.02033"}, {"title": "A process-independent explanation for the general form of Taylor's Law", "url": "https://arxiv.org/pdf/1410.7283"}]}, "Based on the search results, here's what I found about Taylor's power law of fluctuation scaling in ecology:\n\n## Definition and Core Concept\n\nTaylor's law (TL), a widely verified empirical relationship in ecology, states that the variance of population density is approximately a power-law function of mean density. On a log-log scale, TL describes the relationship as: logvariance = log a + b log mean, a > 0.\n\n## Mathematical Formulation\n\nOn the log-log scale, Taylor showed that the mean-variance relationship was described well by a linear equation. This means that when both variance and mean are plotted on logarithmic axes, they produce a straight line relationship.\n\n## Significance and Verification\n\nTaylor's law, one of the most widely accepted generalizations in ecology, states that the variance of a population abundance time series scales as a power law of its mean. During the past half-century, Taylor's power law was confirmed for thousands of biological species and populations.\n\n## Important Caveats\n\nHowever, recent research has raised questions about interpretation. The exponent generally depends on the length of the time series, and its value reflects the combined effect of many underlying mechanisms. Moreover, sampling errors alone, when presented on a double logarithmic scale, are sufficient to produce an apparent power law."], "durationSeconds": 8.203203955000001, "searchCount": 1}
```

### [14] TOOL RESULT — WebSearch · 2026-08-01 14:41:50 UTC

```
{"query": "majority voting self-consistency LLM reasoning 2023 2024 2025", "results": [{"tool_use_id": "srvtoolu_01VFxeMftUHbEDuzGompjXbv", "content": [{"title": "Reasoning Consensus: Structural Ensembling of LLM Reasoning via Weighted DAG Aggregation", "url": "https://arxiv.org/html/2607.27783"}, {"title": "Deep Think with Confidence DEEP THINK WITH CONFIDENCE", "url": "https://jiaweizzhao.github.io/deepconf/static/pdfs/deepconf_arxiv.pdf"}, {"title": "Ranked Voting based Self-Consistency of Large Language Models", "url": "https://arxiv.org/pdf/2505.10772"}, {"title": "Leveraging Reasoning Paths for Efficient LLM Sampling", "url": "https://aclanthology.org/2025.naacl-long.184.pdf"}, {"title": "Path-Consistency with Prefix Enhancement for Efficient Inference in LLMs", "url": "https://arxiv.org/pdf/2409.01281"}, {"title": "Semantic Voting: A Self-Evaluation-Free Approach for Efficient LLM Self-Improvement on Unverifiable Open-ended Tasks", "url": "https://arxiv.org/pdf/2509.23067"}, {"title": "Confidence-Weighted Token Set Cover for Early Hypothesis Pruning in Self-Consistency", "url": "https://arxiv.org/pdf/2508.03979"}, {"title": "The Majority is not always right: RL training for solution aggregation", "url": "https://arxiv.org/pdf/2509.06870"}, {"title": "[2505.10772] Ranked Voting based Self-Consistency of Large Language Models", "url": "https://arxiv.org/abs/2505.10772"}, {"title": "TEMPORAL CONSISTENCY FOR LLM REASONING PRO", "url": "https://openreview.net/pdf?id=sM5QDzIg3j"}]}, "I've found relevant research on majority voting and self-consistency for LLM reasoning spanning 2023-2025. Here's what the search results reveal:\n\n## Self-Consistency and Majority Voting Overview\n\nSelf-consistency is a sampling strategy that generates multiple reasoning paths and aggregates the final output through majority voting. Self-consistency performs majority voting of only the final answer, and does not consider reasoning trace structure.\n\n## Recent Developments (2024-2025)\n\nThe standard Self Consistency approach generates multiple reasoning paths and uses majority voting for the final answer, while newer methods like Reasoning-Aware Self Consistency (RASC) assign scores based on the qualities of both answers and reasoning paths, effectively handling incorrect or irrelevant responses.\n\nRecent work proposes ranked voting based self-consistency, which generates ranked answers in each reasoning process and conducts ranked voting among multiple ranked answers from different responses to make overall self-consistency more reliable.\n\nA key limitation is that majority voting fails when correct solutions exist but are confined to minority modes, causing majority voting to amplify errors rather than surface the correct answer.\n\n## Additional Approaches\n\nRecent work leverages the language model itself as a generative aggregator, with Universal Self-Consistency (USC) prompting the model to examine all sampled solutions and choose the most coherent one.\n\nThe search results show active research in improving self-consistency methods with various enhancements to handle edge cases and improve efficiency."], "durationSeconds": 9.163620835999998, "searchCount": 1}
```

### [15] TOOL RESULT — WebSearch · 2026-08-01 14:41:50 UTC

```
{"query": "de Finetti representation voting test-time aggregation", "results": [{"tool_use_id": "srvtoolu_011pwuDjRXmLwJ67KjKuQx2f", "content": [{"title": "[2605.05592] When Can Voting Help, Hurt, or Change Course? Exact Structure of Binary Test-Time Aggregation", "url": "https://arxiv.org/abs/2605.05592"}, {"title": "When Can Voting Help, Hurt, or Change Course? Exact Structure of Binary Test-Time Aggregation", "url": "https://arxiv.org/html/2605.05592v1"}, {"title": "Majority Correctness in Social Networks: From Well-Mixed Electorates to Complex Networks", "url": "https://arxiv.org/html/2607.14288"}, {"title": "When Can Voting Help, Hurt, or Change Course? Exact ...", "url": "https://arxiv.org/pdf/2605.05592"}, {"title": "Journal articles: 'De Finetti's representation' – Grafiati", "url": "https://www.grafiati.com/en/literature-selections/de-finetti's-representation/journal/"}, {"title": "Probabilistic Voting Models with Varying Speeds of Correlation Decay", "url": "https://arxiv.org/pdf/2204.13360"}, {"title": "An elementary proof of de Finetti’s theorem - ScienceDirect", "url": "https://www.sciencedirect.com/science/article/abs/pii/S0167715219300902"}, {"title": "Exchangeability, Conformal Prediction, and Rank Tests", "url": "https://arxiv.org/pdf/2005.06095"}, {"title": "Joint Consistency: A Unified Test-Time Aggregation Framework via Energy Minimization", "url": "https://arxiv.org/pdf/2605.06219"}]}, "Based on the search results, here's what I found about de Finetti representation and voting in test-time aggregation:\n\n## Main Research\n\nUnder the de Finetti representation for exchangeable repeated correctness, voting is governed by a latent distribution of per-example correctness probabilities. This concept appears in a recent research paper titled \"When Can Voting Help, Hurt, or Change Course? Exact Structure of Binary Test-Time Aggregation\" (published May 2026).\n\n## Key Findings\n\nMajority voting is one of the few black-box interventions that can improve a fixed stochastic predictor, and classical fixed-competence theory makes this intervention look monotone—more votes help above the majority threshold and hurt below it. However, even simple latent mixtures can generate sharply different voting curves, including nonmonotone behavior and infinitely many trend changes.\n\nThe exact object recovered by voting is a signed voting signature: at each binomial variance scale, it records excess latent mass above rather than below the majority threshold.\n\n## De Finetti's Theorem\n\nMore broadly, a sequence of random variables is called exchangeable if the joint distribution is unchanged by any permutation of the indices, and de Finetti's theorem characterizes all exchangeable sequences as a 'mixture' of sequences of independent random variables."], "durationSeconds": 9.678384684000001, "searchCount": 1}
```

### [16] TOOL RESULT — WebSearch · 2026-08-01 14:41:52 UTC

```
{"query": "LLM sampling variance error correlation resampling", "results": [{"tool_use_id": "srvtoolu_01WrsrVJR2jyZxmfRt5fXaRr", "content": [{"title": "Where Does the Noise Come From? A Variance-Components Decomposition of Non-Determinism in LLM Brand Answers", "url": "https://arxiv.org/html/2607.13304"}, {"title": "Statistical LLM Evaluations — Confidence scoring | by Sulbha Jain | Medium", "url": "https://sulbhajain.medium.com/statistical-llm-evaluations-confidence-scoring-caa6c9d57656"}, {"title": "Evaluating AI Agents: Techniques to Reduce Variance and Boost Alignment for LLM Judges | Microsoft Community Hub", "url": "https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/evaluating-ai-agents-techniques-to-reduce-variance-and-boost-alignment-for-llm-j/4498571"}, {"title": "Is it even rainier in North Vancouver? A non-parametric rank-based test   for semicontinuous longitudinal data", "url": "https://arxiv.org/pdf/1711.08876"}, {"title": "Likelihood Variance as Text Importance for Resampling Texts to Map Language Models", "url": "https://arxiv.org/pdf/2505.15428"}, {"title": "Variance-Aware LLM Annotation for Strategy Research: Sources, Diagnostics, and a Protocol for Reliable Measurement", "url": "https://arxiv.org/html/2601.02370"}, {"title": "Knowledge without Wisdom: Measuring Misalignment between LLMs and Intended Impact", "url": "https://arxiv.org/pdf/2603.00883"}, {"title": "Can LLMs Generate Random Numbers? Evaluating LLM Sampling in Controlled Domains", "url": "https://people.csail.mit.edu/renda/llm-sampling-paper"}]}, "I found several relevant research sources on this topic. Here's what the search results reveal:\n\n## Key Findings\n\n**Variance Components in LLM Sampling:**\n\nOn resampled stability subsets, the resampling component accounts for 34.8% of variance when isolating pure within-prompt resampling, with variance arising from different decoder samples on identical prompts, prompt paraphrasing, model identity, and query language.\n\n**Error Correlation and Statistical Methods:**\n\nPaired-difference analysis accounts for question variance and provides variance reduction by leveraging correlation between model performances on shared questions. Additionally, high and systematically correlated annotation error leads to inconsistent estimates, whereas smaller, approximately classical error mainly attenuates coefficients and can be corrected using standard methods, with variance-reduction procedures shifting annotation error toward the latter case.\n\n**LLM Sampling Characteristics:**\n\nResearch compares sampling methodologies along three axes: the error of the LLM's induced distribution against ground truth, the variance of the induced distribution across different prompt examples, and the containment of generated samples in the domain. High variance appears in induced distributions when using different prompt examples.\n\n**Error Structure:**\n\nLLM error disperses across high-order interactions involving model and prompt, indicating instability rather than construct-related variation."], "durationSeconds": 10.513753003999998, "searchCount": 1}
```

### [17] TOOL CALL — WebFetch · 2026-08-01 14:42:02 UTC

```
URL: https://arxiv.org/abs/2605.05592
Prompt: What is the exact structure of voting curves? How do they measure voting help/hurt? What is the de Finetti representation framework?
```

### [18] TOOL CALL — WebFetch · 2026-08-01 14:42:02 UTC

```
URL: https://arxiv.org/pdf/1505.02033
Prompt: What is Taylor's power law? How is the exponent b measured? What does b=1 mean versus b>1?
```

### [19] TOOL CALL — WebFetch · 2026-08-01 14:42:02 UTC

```
URL: https://arxiv.org/abs/2505.10772
Prompt: How do they measure voting gain? What is ranked voting? How many samples do they use?
```

### [20] TOOL RESULT — WebFetch · 2026-08-01 14:42:02 UTC

```
{"bytes": 434556, "code": 200, "codeText": "OK", "result": "# Taylor's Power Law\n\nI cannot extract meaningful information about Taylor's Power Law from the provided PDF content. The document appears to be heavily compressed/encoded, making it impossible to read the actual text clearly enough to accurately answer your questions about:\n\n- The definition of Taylor's Power Law\n- How the exponent b is measured\n- What different b values indicate\n\nTo provide you with accurate information about Taylor's Power Law (which describes the relationship between mean and variance in ecological populations), I would need either:\n1. A readable version of this document, or\n2. Permission to consult other sources on this ecological principle\n\nIf you can provide a clearer text version or a different document, I'd be happy to explain this concept properly.\n\n[Binary content (application/pdf, 424.4KB) also saved to /home/adrian/projects/ai-inventor/aii_data/.claude/projects/-home-adrian-projects-ai-inventor-aii-data-users-uitest-20260731-runs-run-Br8Nz-7w30tX-3-invention-loop-iter-1-gen-plan-gen-plan-research-1/a160d688-7529-43b3-b52f-30336354e36c/tool-results/webfetch-1785595317840-6ijoyn.pdf]", "durationMs": 4599, "url": "https://arxiv.org/pdf/1505.02033"}
```

### [21] TOOL RESULT — WebFetch · 2026-08-01 14:42:02 UTC

```
{"bytes": 41482, "code": 200, "codeText": "OK", "result": "# Analysis of the Research Paper\n\nBased on the provided content, I can address your questions with the following caveats:\n\n**Voting Gain Measurement:** The abstract doesn't specify how voting improvement is quantified. It only states \"our proposed method outperforms the baselines\" across six datasets, but the specific metrics used aren't detailed in this excerpt.\n\n**Ranked Voting Definition:** Rather than a single technique, the authors employ \"three ranked voting methods: Instant-runoff voting, Borda count voting, and mean reciprocal rank voting.\" These methods process multiple ranked answers from different model responses instead of selecting only the top answer.\n\n**Sample Size:** The page content provided does not include information about the number of samples used in their experiments. This detail would likely appear in the full paper's methodology section, which isn't included here.\n\nThe core innovation involves generating multiple ranked candidate answers per reasoning trial and conducting voting across these rankings, contrasting with traditional approaches that \"typically generate only a single answer in each trial.\"\n\nFor complete details on metrics, sample sizes, and experimental setup, you would need to access the full PDF or HTML version of the paper.", "durationMs": 4709, "url": "https://arxiv.org/abs/2505.10772"}
```

### [22] TOOL RESULT — WebFetch · 2026-08-01 14:42:02 UTC

```
{"bytes": 42783, "code": 200, "codeText": "OK", "result": "# Analysis of Binary Test-Time Aggregation Paper\n\n## Exact Structure of Voting Curves\n\nThe paper reveals that voting curves are far more complex than previously understood. Rather than monotonic behavior, the research demonstrates that \"even simple latent mixtures can generate sharply different voting curves, including nonmonotone behavior and, in an explicit construction, infinitely many trend changes.\"\n\nThe key structural object is a **signed voting signature** that captures the complete voting dynamics at each binomial variance scale by recording excess latent mass above versus below the majority threshold.\n\n## Measuring Help and Hurt\n\nTraditional theory suggested voting outcomes were straightforward: \"more votes help above the majority threshold and hurt below it.\" This paper challenges that view, showing the relationship depends on underlying per-example correctness probabilities. The mechanism involves a latent distribution governing individual prediction accuracy, which fundamentally determines whether aggregation improves or degrades performance.\n\n## De Finetti Representation Framework\n\nThe paper employs de Finetti's theorem for exchangeable repeated correctness to model voting. This framework assumes repeated predictions follow a distribution over per-example correctness probabilities. Rather than assuming uniform competence, it acknowledges heterogeneous difficulty or model reliability across different test instances, enabling richer characterization of aggregation effects.", "durationMs": 6465, "url": "https://arxiv.org/abs/2605.05592"}
```

### [23] ASSISTANT · 2026-08-01 14:42:06 UTC

```
Now let me search for more specific information on benchmarks, temperature/sampling protocols, and any prior work applying Taylor's law to LLM sampling.
```

### [24] TOOL CALL — WebSearch · 2026-08-01 14:42:06 UTC

```
GSM8K MMLU benchmark difficulty rating reasoning tasks
```

### [25] TOOL CALL — WebSearch · 2026-08-01 14:42:06 UTC

```
LLM temperature sampling protocol correctness repeated samples
```

### [26] TOOL CALL — WebSearch · 2026-08-01 14:42:06 UTC

```
Taylor power law LLM language model word frequency ACL 2018
```

### [27] TOOL CALL — WebSearch · 2026-08-01 14:42:06 UTC

```
error clustering LLM incorrect answers repeated sampling embedding similarity
```

### [28] TOOL RESULT — WebSearch · 2026-08-01 14:42:14 UTC

```
{"query": "GSM8K MMLU benchmark difficulty rating reasoning tasks", "results": [{"tool_use_id": "srvtoolu_01HpXY5mvs4uJGMZ3pwrNRma", "content": [{"title": "Advancing Expert Specialization for Better MoE", "url": "https://arxiv.org/pdf/2505.22323"}, {"title": "Multi-Agent Debate with Memory Masking", "url": "https://arxiv.org/pdf/2603.20215"}, {"title": "GSM-Infinite: How Do Your LLMs Behave over Infinitely Increasing Context   Length and Reasoning Complexity?", "url": "https://arxiv.org/pdf/2502.05252"}, {"title": "SelectLLM: Query-Aware Efficient Selection Algorithm for Large Language Models", "url": "https://arxiv.org/pdf/2408.08545"}, {"title": "40 Large Language Model Benchmarks and The Future of Model Evaluation", "url": "https://arize.com/blog/llm-benchmarks-mmlu-codexglue-gsm8k"}, {"title": "Towards Reasoning Ability of Small Language Models", "url": "https://arxiv.org/pdf/2502.11569"}, {"title": "Reasoning-as-Logic-Units: Scaling Test-Time Reasoning in Large Language   Models Through Logic Unit Alignment", "url": "https://arxiv.org/pdf/2502.07803"}, {"title": "Evaluating Mathematical Reasoning Across Large Language Models: A Fine-Grained Approach", "url": "https://arxiv.org/pdf/2503.10573"}, {"title": "Simple Policy Gradients for Reasoning with Diffusion Language Models", "url": "https://arxiv.org/pdf/2510.04019"}, {"title": "Between a Rock and a Hard Place: The Tension Between Ethical Reasoning and Safety Alignment in LLMs", "url": "https://arxiv.org/pdf/2509.05367"}]}, "Based on the search results, here's information about the difficulty ratings of GSM8K and MMLU benchmarks for reasoning tasks:\n\n## GSM8K\n\nGSM8K is a benchmark designed to evaluate mathematical reasoning through 8,000 elementary and middle school word problems across arithmetic, algebra, geometry, and other topics. GSM8K focuses on middle school problems, making it a relatively accessible benchmark compared to other math reasoning tasks. Each problem comes with detailed step-by-step solutions, enabling models to learn chain-of-thought reasoning strategies, and the dataset is widely used to train and assess a model's ability to decompose multi-step questions logically and produce interpretable solutions.\n\n## MMLU\n\nMMLU is a massive multitask benchmark with multiple-choice questions spanning 57 academic subjects, including science, humanities, law, and medicine, with each subject stratified by difficulty from high school to expert level. MMLU evaluates a text model's multitask accuracy across 57 tasks spanning subjects like elementary mathematics, US history, computer science, and law, aiming to measure extensive world knowledge and problem-solving abilities.\n\n## Relative Difficulty Comparison\n\nThe research indicates that there is a significant difficulty gap between benchmarks: GSM-8K focuses on middle school problems, MATH and AIME targets prospective university students, and it is difficult to quantitatively determine the difference in problem difficulty between GSM-8K problems and MATH problems since MATH uses operations such as taking power or roots absent in GSM-8K."], "durationSeconds": 7.647892865000002, "searchCount": 1}
```

### [29] TOOL RESULT — WebSearch · 2026-08-01 14:42:14 UTC

```
{"query": "LLM temperature sampling protocol correctness repeated samples", "results": [{"tool_use_id": "srvtoolu_012FUYX7rLNNBQ1eXcnt52QJ", "content": [{"title": "LLM-assisted genre analysis: The effect of sampling temperature on reliability - ScienceDirect", "url": "https://www.sciencedirect.com/science/article/abs/pii/S2772766126000200"}, {"title": "Can LLMs Follow Simple Rules?", "url": "https://arxiv.org/pdf/2311.04235"}, {"title": "KernelBench: Can LLMs Write Efficient GPU Kernels?", "url": "https://arxiv.org/pdf/2502.10517"}, {"title": "LLM Code Smells: A Taxonomy and Detection Approach", "url": "https://arxiv.org/pdf/2605.22976"}, {"title": "Specification and Detection of LLM Code Smells", "url": "https://arxiv.org/pdf/2512.18020"}, {"title": "Continuous Autoregressive Language Models", "url": "https://arxiv.org/pdf/2510.27688"}, {"title": "The Necessity of Setting Temperature in LLM-as-a-Judge", "url": "https://arxiv.org/html/2603.28304v1"}, {"title": "Two Calls, Two Moments, and the Vote-Accuracy Curve of Repeated LLM Inference", "url": "https://arxiv.org/pdf/2605.03379"}, {"title": "DCP-Bench-Open: Evaluating LLMs for Constraint Modelling of Discrete Combinatorial Problems", "url": "https://arxiv.org/pdf/2506.06052"}, {"title": "Evaluating Reliability Gaps in Large Language Model Safety via Repeated Prompt Sampling", "url": "https://arxiv.org/pdf/2604.09606"}]}, "I found several research papers and studies on LLM temperature sampling with repeated samples. Here are the key findings:\n\n## Temperature Effects on Consistency and Correctness\n\nLarge Language Models have a probabilistic architecture where repeated runs may produce different annotations from identical inputs, which is a direct threat to research reproducibility. Classification performance remains stable across all temperature settings, but annotation consistency degrades substantially as temperature increases.\n\n## Protocol Correctness and Best Practices\n\nTemperature controls sampling stochasticity, and relying on an implicit temperature reduces maintainability and reliability, as defaults differ across providers/models and may change over time, harming reproducibility. For precise, repeatable automation use low temperatures (0-0.3), while higher temperatures (0.7-1.0) suit creative generation.\n\n## Repeated Sampling Verification\n\nIn repeated sampling protocols, each prompt-temperature pair should produce unique samples with no evidence of collapsed or duplicated generations, confirming that observed variability reflects model stochasticity rather than data artifacts.\n\n## Failure Rates with Temperature\n\nNon-zero failure probabilities are observed under repeated inference even with fixed prompts and constant decoding parameters, and empirical failure probabilities increase monotonically with temperature.\n\nThe research demonstrates that while temperature is critical for controlling LLM behavior, explicitly setting and documenting it is essential for protocol correctness and reproducibility."], "durationSeconds": 7.813253764000001, "searchCount": 1}
```

### [30] TOOL RESULT — WebSearch · 2026-08-01 14:42:14 UTC

```
{"query": "Taylor power law LLM language model word frequency ACL 2018", "results": [{"tool_use_id": "srvtoolu_01QKy3ZPJct8En6nXXui2jPC", "content": [{"title": "Taylor's law for Human Linguistic Sequences - ACL 2018", "url": "https://acl2018.org/paper/141/"}, {"title": "Evaluating Computational Language Models with Scaling ...", "url": "https://aclanthology.org/J19-3003.pdf"}, {"title": "Taylor Unswift: Secured Weight Release for Large Language Models via Taylor Expansion - ACL Anthology", "url": "https://aclanthology.org/2024.emnlp-main.393/"}, {"title": "Adam’s Law: Textual Frequency Law on Large Language Models - ACL Anthology", "url": "https://aclanthology.org/2026.acl-long.188/"}, {"title": "On the Power Laws of Language: Word Frequency ...", "url": "https://dl.acm.org/doi/10.1145/3077136.3080821"}, {"title": "Stochastic model for the vocabulary growth in natural languages", "url": "https://arxiv.org/pdf/1212.1362"}, {"title": "Paper page - Adam's Law: Textual Frequency Law on Large Language Models", "url": "https://huggingface.co/papers/2604.02176"}, {"title": "Taylor's law for Human Linguistic Sequences", "url": "https://aclanthology.org/P18-1105.pdf"}]}, "Based on the search results, I found relevant information about Taylor's law and its application to language models:\n\n## Key Findings\n\nTaylor's law describes the fluctuation characteristics underlying a system in which the variance of an event within a time span grows by a power law with respect to the mean. Although Taylor's law has been applied in many natural and social systems, its application for language has been scarce.\n\nA paper presented at ACL 2018 titled \"Taylor's law for Human Linguistic Sequences\" addressed this gap. The paper conducted Taylor analysis of over 1100 texts across 14 languages. The results found that the Taylor exponents of natural language written texts exhibit almost the same value.\n\nThe exponent was also compared for other language-related data, such as the child-directed speech, music, and programming languages. Importantly, the Taylor exponent serves to quantify the fundamental structural complexity underlying linguistic time series, with applicability to evaluating language models."], "durationSeconds": 7.457982814999996, "searchCount": 1}
```

### [31] TOOL RESULT — WebSearch · 2026-08-01 14:42:16 UTC

```
{"query": "error clustering LLM incorrect answers repeated sampling embedding similarity", "results": [{"tool_use_id": "srvtoolu_0153UBgXi9U9hL8oJQRkwwn5", "content": [{"title": "Leveraging Error Diversity in Group Rollouts for Reinforcement Learning", "url": "https://arxiv.org/pdf/2605.17333"}, {"title": "Testing the Validity of Embedding-Based Similarity and Clustering for Handwritten Physics Solutions", "url": "https://arxiv.org/html/2606.28872v1"}, {"title": "Eliminating Hallucination-Induced Errors in LLM Code Generation with Functional Clustering", "url": "https://arxiv.org/html/2506.11021v1"}, {"title": "CEC-Zero: Chinese Error Correction Solution Based on LLM", "url": "https://arxiv.org/pdf/2505.09082"}, {"title": "CluCERT: Certifying LLM Robustness via Clustering-Guided Denoising Smoothing", "url": "https://arxiv.org/html/2512.08967v1"}, {"title": "Automatic Chain of Thought Prompting in Large Language Models", "url": "https://arxiv.org/pdf/2210.03493"}, {"title": "What is Error Analysis for LLMs? Cluster, Label, Prioritize in 2026", "url": "https://futureagi.com/blog/what-is-error-analysis-llm-2026"}, {"title": "RECSIP: REpeated Clustering of Scores Improving the Precision", "url": "https://arxiv.org/pdf/2503.12108"}, {"title": "Semantic Token Clustering for Efficient Uncertainty Quantification in Large Language Models", "url": "https://arxiv.org/html/2603.20161v1"}, {"title": "Repeated LLM Sampling and the Challenge of Meaningfully Capturing “Distance\"", "url": "https://presentofcoding.substack.com/p/repeated-llm-sampling-and-the-challenge"}]}, "I found several relevant research papers and articles on this topic. Here's what the search results reveal:\n\n## Key Findings\n\nError clustering approaches attempt to cluster incorrect LLM responses by embedding similarity—representing generated trajectories as dense vectors and grouping those whose vectors lie close together, which is appealing because it does not require answer extraction and could capture semantic differences in varied surface forms. However, embedding similarity is fundamentally unsuitable for distinguishing mathematically correct from incorrect reasoning and cannot serve as a reliable basis for error diversity signals.\n\n## Limitations of Embedding-Based Clustering\n\nIn a study of 403 pairs with numerically different answers, 308 (76.4%) achieved cosine similarity >0.95, meaning embedding-based clustering would merge trajectories into the same group despite their producing different answers. This represents a significant problem when trying to identify and distinguish error patterns.\n\n## Practical Applications\n\nLLM error analysis is the workflow that turns failed traces into a prioritized list of root causes by sampling failures, embedding the inputs and outputs, and clustering the embeddings. Clustering-based sampling methods can use diverse error clusters to reduce the chance of constructing incorrect demonstrations, which is considered diversity-based in contrast to similarity-based approaches.\n\nThe research suggests that while embedding-based clustering is useful for many purposes, additional methods beyond pure embedding similarity may be needed for reliable error categorization in LLM outputs."], "durationSeconds": 8.878363826000001, "searchCount": 1}
```

### [32] ASSISTANT · 2026-08-01 14:42:20 UTC

```
Let me fetch the specific Taylor's law ACL paper and gather more details on experimental protocols.
```

### [33] TOOL CALL — WebFetch · 2026-08-01 14:42:20 UTC

```
URL: https://aclanthology.org/P18-1105.pdf
Prompt: What is the methodology? How do they fit Taylor's law? What exponent values do they find? What does b indicate?
```

### [34] TOOL CALL — WebFetch · 2026-08-01 14:42:20 UTC

```
URL: https://arxiv.org/pdf/2605.03379
Prompt: What is the vote-accuracy curve? How many samples do they use? How do they measure accuracy as a function of sample count?
```

### [35] TOOL CALL — WebSearch · 2026-08-01 14:42:20 UTC

```
Spearman correlation coefficient threshold statistical significance p-value
```

### [36] TOOL RESULT — WebFetch · 2026-08-01 14:42:24 UTC

```
{"bytes": 1375254, "code": 200, "codeText": "OK", "result": "# Vote-Accuracy Curve Analysis\n\nBased on the PDF content, the **vote-accuracy curve** represents how prediction accuracy improves as more samples (LLM inference calls) are aggregated through a voting mechanism.\n\n## Sample Usage\n\nThe research employs repeated LLM inference with multiple calls per query. From the document metadata and structure, they test across different model sizes (Llama 3.1:8b, Phi4-mini, Qwen2.5:7b) using datasets like SQuAD and others, though specific sample counts aren't clearly stated in the visible sections.\n\n## Accuracy Measurement\n\nThe accuracy measurement method involves:\n\n1. **Multiple inference calls** per problem instance\n2. **Aggregation through voting** - combining predictions from multiple model outputs\n3. **Accuracy tracking** as a function of call count - measuring how performance improves with additional samples\n\nThe approach appears to use the \"two moments\" framework mentioned in the title to characterize this relationship mathematically, allowing them to model the tradeoff between computational cost (number of calls) and prediction accuracy.\n\nThe paper establishes theoretical foundations using statistical moments to predict accuracy curves without exhaustive experimentation, enabling efficient resource allocation for repeated inference strategies.\n\n[Binary content (application/pdf, 1.3MB) also saved to /home/adrian/projects/ai-inventor/aii_data/.claude/projects/-home-adrian-projects-ai-inventor-aii-data-users-uitest-20260731-runs-run-Br8Nz-7w30tX-3-invention-loop-iter-1-gen-plan-gen-plan-research-1/a160d688-7529-43b3-b52f-30336354e36c/tool-results/webfetch-1785595339113-48sc9s.pdf]", "durationMs": 5729, "url": "https://arxiv.org/pdf/2605.03379"}
```

### [37] TOOL RESULT — WebFetch · 2026-08-01 14:42:26 UTC

```
{"bytes": 669455, "code": 200, "codeText": "OK", "result": "# Taylor's Law Methodology and Findings\n\nI can see this is a PDF document about Taylor's law applied to linguistic sequences, but the content provided is primarily raw PDF code rather than readable text. The actual article content isn't clearly extracted in what you've shared.\n\nFrom the metadata visible in the PDF, I can tell the document is titled \"Taylor's law for Human Linguistic Sequences\" by Tatsuru Kobayashi and Kumiko Tanaka-Ishii (created May 2018), but I cannot reliably extract the specific methodology, exponent values, or explanations of what parameter b indicates from the garbled PDF data provided.\n\nTo give you an accurate answer about:\n- The fitting methodology for Taylor's law\n- Specific exponent values found\n- The meaning of the b parameter\n\nI would need either:\n1. A properly converted text version of the paper, or\n2. A clearer excerpt from the document\n\nCould you provide the paper in a more readable format, or specify which section discusses these elements?\n\n[Binary content (application/pdf, 653.8KB) also saved to /home/adrian/projects/ai-inventor/aii_data/.claude/projects/-home-adrian-projects-ai-inventor-aii-data-users-uitest-20260731-runs-run-Br8Nz-7w30tX-3-invention-loop-iter-1-gen-plan-gen-plan-research-1/a160d688-7529-43b3-b52f-30336354e36c/tool-results/webfetch-1785595339500-celesd.pdf]", "durationMs": 7003, "url": "https://aclanthology.org/P18-1105.pdf"}
```

### [38] TOOL RESULT — WebSearch · 2026-08-01 14:42:26 UTC

```
{"query": "Spearman correlation coefficient threshold statistical significance p-value", "results": [{"tool_use_id": "srvtoolu_01SCT9LhBQy68NPkZsnHQ3Y7", "content": [{"title": "How to interpret Spearman Correlation when p value is not significant? | ResearchGate", "url": "https://www.researchgate.net/post/How_to_interpret_Spearman_Correlation_when_p_value_is_not_significant"}, {"title": "P value: P value Puzzles: Deciphering Significance with Spearman Rank Correlation - FasterCapital", "url": "https://fastercapital.com/content/P-value--P-value-Puzzles--Deciphering-Significance-with-Spearman-Rank-Correlation.html"}, {"title": "Spearman's Rank Calculator: Rs, p-value, Scatter Graph and Conclusion", "url": "https://geographyfieldwork.com/SpearmansRankCalculator.html"}, {"title": "Spearman's Correlation in Stata - Procedure, output and interpretation of the output using a relevant example.", "url": "https://statistics.laerd.com/stata-tutorials/spearmans-correlation-using-stata.php"}, {"title": "Spearman's Rank-Order Correlation - A guide to how to calculate it and interpret the output.", "url": "https://statistics.laerd.com/statistical-guides/spearmans-rank-order-correlation-statistical-guide-2.php"}, {"title": "An ALMA Survey of Chemistry in Disks around M4-M5 Stars", "url": "https://arxiv.org/pdf/2105.04681"}, {"title": "Fira: Can We Achieve Full-rank Training of LLMs Under Low-rank Constraint?", "url": "https://arxiv.org/pdf/2410.01623"}, {"title": "Spearman's rank correlation coefficient - Wikipedia", "url": "https://en.wikipedia.org/wiki/Spearman's_rank_correlation_coefficient"}, {"title": "pmc.ncbi.nlm.nih.gov", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC10791792/table/tab5"}]}, "Here are the key findings about Spearman correlation coefficient, thresholds, statistical significance, and p-values:\n\n## Understanding P-values and Significance\n\nA p-value greater than 0.05 (or whatever significance threshold you choose) means your correlation coefficient does not differ from 0, indicating no statistically significant correlation between variables. Conversely, a p-value close to 1 suggests no correlation other than due to chance, while a p-value close to 0 means the observed correlation is unlikely to be due to chance.\n\n## Interpreting Correlation Strength vs. Significance\n\nIt's important to note that statistical significance does not indicate the strength of Spearman's correlation, and the statistical significance testing does not provide information about the strength of the relationship. If you set α = 0.05, achieving a statistically significant Spearman rank-order correlation means you can be sure that there is less than a 5% chance that the strength of the relationship you found happened by chance if the null hypothesis were true.\n\n## The Spearman Coefficient Range\n\nThe Spearman correlation coefficient (rs) can take values from +1 to -1, where +1 indicates a perfect association of ranks, zero indicates no association, and -1 indicates a perfect negative association.\n\n## Field-Specific Differences\n\nDifferent disciplines like psychology, politics, and medicine have different descriptors and thresholds for describing correlation strength."], "durationSeconds": 7.126941937999996, "searchCount": 1}
```

### [39] ASSISTANT · 2026-08-01 14:43:17 UTC

```
Now I have enough information to create a detailed, actionable research plan. Let me write it out systematically.
```

### [40] TOOL CALL — Write · 2026-08-01 14:43:17 UTC

```
File: /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_Br8Nz-7w30tX/3_invention_loop/iter_1/gen_plan/gen_plan_research_1/.terminal_claude_agent_struct_out.json

{
  "title": "Literature Survey & Methodology for Taylor's Law as Voting Diagnostic",
  "summary": "This research plan establishes the foundation for testing whether Taylor's power-law exponent (b) can predict when majority voting helps LLMs. It surveys voting theory (de Finetti, voting curves), Taylor's law in ecology and linguistics, LLM sampling protocols, and prior work on error correlation.",
  "runpod_compute_profile": "cpu_light",
  "question": "Can Taylor's power law exponent (b) from repeated LLM sampling reliably predict whether majority voting improves accuracy, and what are the best methods to measure this across multiple LLMs and benchmarks?",
  "research_plan": "## Phase 1: Voting Theory and Metrics (Steps 1-3)\n\n**Step 1: De Finetti Representation & Voting Curves**\n- Fetch and fully read arXiv:2605.05592 (\"When Can Voting Help, Hurt, or Change Course?\") to understand:\n  - How de Finetti representation models exchangeable repeated correctness predictions\n  - The structure of voting curves: when they are monotonic vs. non-monotone\n  - The signed voting signature concept and how it characterizes voting dynamics\n  - Why majority voting can amplify errors when per-problem success < 0.5\n- Search for any other recent work (2024-2026) on theoretical bounds on voting gain as a function of sample count k\n- Document: the baseline assumption (exchangeability of samples), conditions for voting to help, and failure modes\n\n**Step 2: Voting Gain Measurement Protocols**\n- Fetch arXiv:2605.03379 (\"Two Calls, Two Moments, and the Vote-Accuracy Curve\") and related recent papers (arXiv:2505.10772 on ranked voting; search for \"voting accuracy function k samples\") to establish:\n  - Standard method to measure accuracy as a function of sample count k (e.g., majority vote at k=1, 3, 5, 10, etc.)\n  - Which aggregation rules (simple majority vs. ranked voting vs. confidence-weighted) are used in SOTA\n  - Sample sizes typically used (e.g., 10-30 per problem, or higher)\n  - How voting gain is quantified: Δacc(k) = acc_vote(k) - acc_single (baseline single-sample accuracy)\n- Note any sources that measure voting gain across problem-difficulty strata or problem-type subgroups\n- Document: the standard protocol for repeated sampling, temperature settings, and baseline single-sample accuracy measurement\n\n**Step 3: Benchmark Selection & Difficulty Variation**\n- Search for and compile information on reasoning/QA benchmarks suitable for this study:\n  - GSM8K: math word problems, elementary/middle-school difficulty (available from HuggingFace, public)\n  - MMLU: 57-subject multiple choice, difficulty stratified by level (high school to expert)\n  - Search for a logic/puzzle benchmark (e.g., LogiQA, ARC, or MATH, which is harder than GSM8K)\n  - Identify any emerging benchmarks from 2025-2026 for reasoning or open-ended QA\n- For each, document: size, mean difficulty level, available problem counts, and whether they allow multiple correct answers\n- Verify that combined benchmarks span a wide difficulty range (mean accuracy from ~0.1 to ~0.9 when averaged over all models to be tested)\n- Document: selection rationale (diversity of problem types, difficulty span, public availability, and ease of exact grading)\n\n## Phase 2: Taylor's Power Law Background (Steps 4-6)\n\n**Step 4: Taylor's Power Law in Ecology & General Systems**\n- Search for and review foundational and recent Taylor's law literature (ecology, epidemiology, statistical physics):\n  - Original Taylor 1961 paper concept (log Var = log a + b * log Mean)\n  - Review at least two foundational ecology papers confirming b values in populations (expect b=0.8-2.0 range)\n  - Recent work on interpreting b: what does b ≈ 1 indicate (Poisson/independent noise) vs. b > 1 (clustered/correlated disturbances)\n  - Any critical caveats: sampling artifacts, time-series length dependence, or when Taylor's law breaks down\n- Document: the meaning of the exponent b, its typical range, and the clustering interpretation (shared driver) vs. independent interpretation\n\n**Step 5: Taylor's Law Applied to Language (ACL 2018 & Recent)**\n- Fetch or read summary of \"Taylor's law for Human Linguistic Sequences\" (Kobayashi & Tanaka-Ishii, ACL 2018):\n  - How did they fit log-log regression on variance vs. mean?\n  - What exponent values did they find across 1100+ texts in 14 languages?\n  - Did they stratify by text type, author, or corpus?\n- Search for any subsequent applications of Taylor's law to computational linguistics, text analysis, or NLP systems (2019-2026)\n- Document: methodology for fitting Taylor's law in linguistic/NLP contexts and observed b values\n\n**Step 6: Why Taylor's Law Has NOT Been Applied to LLM Sampling (The Gap)**\n- Confirm via targeted search (\"Taylor's law LLM sampling\" + \"Taylor's law machine learning\") that this cross-domain transfer appears to be novel\n- Document what is known about LLM sampling:\n  - Per-problem variance increases with problem difficulty/ambiguity (from papers on LLM variance)\n  - Mean accuracy per problem varies widely across benchmarks (from benchmark papers)\n  - Error correlation / clustering across samples (from error analysis papers)\n  - Why high-b scenarios (correlated failures) reduce voting benefit vs. low-b (independent failures) that help voting\n- Articulate the gap: existing work uses post-hoc accuracy comparison to decide whether to vote; Taylor's exponent would provide a cheap, pre-registered proxy\n\n## Phase 3: LLM Sampling Variance & Error Correlation (Steps 7-9)\n\n**Step 7: LLM Sampling Protocols & Temperature**\n- Fetch or read \"The Necessity of Setting Temperature in LLM-as-a-Judge\" (arXiv:2603.28304) and related papers:\n  - What temperature ranges are standard for repeated sampling (e.g., 0.7-1.0 for diversity, 0-0.3 for deterministic)\n  - How does temperature affect correctness variance per problem?\n  - Is there evidence that temperature affects correlation of errors across samples?\n- Search for empirical studies on the relationship between temperature and voting gain (e.g., \"does higher temperature help voting more?\")\n- Document: recommended sampling protocol (temperature value, number of samples per problem, random seed handling)\n\n**Step 8: LLM Error Correlation & Clustering**\n- Fetch or read papers on error diversity in LLM sampling (arXiv:2605.17333 on error diversity in rollouts, embedding-based clustering):\n  - When do LLM samples fail in the same way (shared latent failure mode) vs. independently?\n  - Can wrong answers be clustered by embedding similarity? What are the caveats (high false-positive rates noted in arXiv:2606.28872)?\n  - Are there alternative clustering methods beyond embedding (e.g., syntactic similarity, semantic parsing, entailment-based grouping)?\n- Document: methodology and caveats for mechanistic probing of high-b problems (are wrong answers concentrated in few clusters or dispersed?)\n\n**Step 9: Variance Components in LLM Predictions**\n- Fetch arXiv:2607.13304 (\"Where Does the Noise Come From? A Variance-Components Decomposition\"):\n  - What are the sources of variance in LLM predictions (resampling stochasticity, prompt paraphrasing, model identity, language)?\n  - How much variance comes from pure within-prompt resampling (~35% in their study)?\n  - Is resampling variance independent or correlated across problems?\n- Document: what fraction of observed correctness variance is attributable to resampling stochasticity vs. prompt/model factors\n\n## Phase 4: Operationalization & Success Metrics (Steps 10-12)\n\n**Step 10: Fitting Taylor's Law to LLM Correctness**\n- Based on phases 1-3, specify the exact protocol:\n  - Per problem p in a benchmark B, sample N times at fixed temperature (e.g., 0.7, N=20-30)\n  - Compute mean correctness m_p = (# correct) / N\n  - Compute variance v_p from the N binary correctness outcomes (Bernoulli variance)\n  - Fit log-log regression: log(v_p) = log(a) + b * log(m_p) across all problems in B\n  - Extract b and its 95% confidence interval (CI)\n  - Repeat per (model, benchmark) pair\n- Document: whether to exclude edge cases (m_p = 0 or 1, which give zero variance), how to handle log(0), potential biases in fitting\n\n**Step 11: Predicting Voting Gain from b**\n- Based on voting curves theory (step 2), specify how b should predict voting gain:\n  - Hypothesis: high b (≥ 1.5) → low voting gain (correlated errors reduce benefit)\n  - Hypothesis: low b (≈ 1.0) → high voting gain (independent errors benefit from aggregation)\n  - Test via Spearman rank correlation (rank-based to avoid assuming linear relationship) between b and measured voting gain\n  - Preregister threshold: |ρ| > 0.5, p < 0.05 (from the hypothesis document)\n- Document: the exact success criterion, why Spearman (not Pearson), and the rationale for the |ρ| > 0.5 threshold\n\n**Step 12: Generalization & Mechanistic Probing Plan**\n- Specify held-out test design:\n  - Calibrate b-to-voting-gain mapping on a subset of (model, benchmark, difficulty-stratum) combinations\n  - Test on held-out (model, benchmark, difficulty-stratum) not used in calibration\n  - Report correlation and p-value on held-out data\n- Specify mechanistic probe:\n  - For high-b problems, cluster wrong answers (pick clustering method from step 8)\n  - Compute entropy / concentration of wrong-answer distribution\n  - Compare entropy in high-b vs. low-b problem sets (expect lower entropy in high-b, supporting clustering interpretation)\n  - Disconfirm if entropy does not track b\n- Document: how these tests validate or falsify the hypothesis\n\n## Phase 5: Dataset & Computational Requirements (Steps 13-14)\n\n**Step 13: Compute Budget & Model Selection**\n- Confirm via OpenRouter pricing what open LLMs are available and feasible within $10 budget:\n  - Small models (7B params): cheaper per call, lower quality\n  - Mid-range (13-32B): better reasoning\n  - Larger open models (70B+): best reasoning, expensive\n  - Plan to test 2-4 models across size range\n- Per (model, benchmark), compute total API calls: n_problems * n_samples (e.g., 1000 problems * 20 samples = 20k calls)\n  - Estimate cost per call and total budget\n  - Decide on n_samples (10-30) to balance statistical power vs. budget\n- Document: selected models, n_samples per problem, expected total cost and how it stays under $10 cap\n\n**Step 14: Expected Outcomes & Failure Scenarios**\n- Document: what success looks like (b predicts voting gain, transfer across models/benchmarks, mechanistic support)\n- Document: what disconfirmation looks like (no correlation, transfer failure, wrong-answer entropy doesn't track b, single-model-only effect)\n- Document: what ambiguous outcomes might occur (weak correlation, model-specific effects, non-linear relationship) and how to interpret them\n\n## Summary of Key Decisions for Executor\n\n1. **Benchmarks**: GSM8K, MMLU, MATH (or equivalent logic/puzzle set) for difficulty span\n2. **Models**: 2-4 open LLMs via OpenRouter, mix of 7B, 13-32B, 70B sizes\n3. **Sampling**: Fixed temperature (e.g., 0.7), N=20-30 samples per problem\n4. **Taylor's Law Fit**: Log-log linear regression on (log mean, log variance) per (model, benchmark)\n5. **Voting Gain Metric**: Accuracy with majority vote at k=1, 3, 5, 10, 20 samples\n6. **Correlation Test**: Spearman ρ on b vs. voting gain, threshold |ρ| > 0.5, p < 0.05\n7. **Mechanistic Probe**: Cluster wrong answers in high-b problems, compare entropy vs. low-b\n8. **Generalization**: Hold out (model, benchmark, difficulty) combinations for transfer test\n9. **Budget**: Estimate total API calls under $10 OpenRouter cap; adjust N or model count as needed\n10. **Success Criterion**: Confirms if b correlates with voting gain and transfers across models/benchmarks; disconfirms if not",
  "explanation": "This research plan lays the foundation for testing a novel hypothesis: that Taylor's power law exponent (b), computed from repeated LLM sampling, can serve as a cheap, pre-registered diagnostic to predict whether majority voting will improve accuracy on a given task. The plan synthesizes four critical knowledge areas: (1) voting theory from recent de Finetti work to understand why voting sometimes helps and sometimes hurts; (2) Taylor's law from ecology and its rare application to language to establish the methodology and interpretation of the exponent b; (3) LLM sampling variance and error correlation to understand whether the independence vs. clustering distinction applies to LLM errors; and (4) practical benchmarks and sampling protocols to make the investigation concrete and reproducible. The plan operationalizes the core prediction—high b (correlated errors) → low voting gain; low b (independent errors) → high voting gain—into a testable, pre-registered statistical test (Spearman rank correlation with |ρ| > 0.5, p < 0.05 threshold). It also specifies a mechanistic probe (wrong-answer clustering entropy) to support or falsify the interpretation of b as a clustering diagnostic rather than a statistical artifact. By grounding the methodology in existing literature and best practices from both ecology and LLM research, the plan ensures the executor can implement a rigorous, well-motivated experiment that either confirms a genuinely novel link between two scientific domains (ecology and LLM behavior) or clearly disconfirms it, advancing the field's understanding of test-time compute allocation."
}
```

### [41] TOOL RESULT — Write · 2026-08-01 14:43:17 UTC

```
{"type": "create", "filePath": "/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_Br8Nz-7w30tX/3_invention_loop/iter_1/gen_plan/gen_plan_research_1/.terminal_claude_agent_struct_out.json", "content": "{\n  \"title\": \"Literature Survey & Methodology for Taylor's Law as Voting Diagnostic\",\n  \"summary\": \"This research plan establishes the foundation for testing whether Taylor's power-law exponent (b) can predict when majority voting helps LLMs. It surveys voting theory (de Finetti, voting curves), Taylor's law in ecology and linguistics, LLM sampling protocols, and prior work on error correlation.\",\n  \"runpod_compute_profile\": \"cpu_light\",\n  \"question\": \"Can Taylor's power law exponent (b) from repeated LLM sampling reliably predict whether majority voting improves accuracy, and what are the best methods to measure this across multiple LLMs and benchmarks?\",\n  \"research_plan\": \"## Phase 1: Voting Theory and Metrics (Steps 1-3)\\n\\n**Step 1: De Finetti Representation & Voting Curves**\\n- Fetch and fully read arXiv:2605.05592 (\\\"When Can Voting Help, Hurt, or Change Course?\\\") to understand:\\n  - How de Finetti representation models exchangeable repeated correctness predictions\\n  - The structure of voting curves: when they are monotonic vs. non-monotone\\n  - The signed voting signature concept and how it characterizes voting dynamics\\n  - Why majority voting can amplify errors when per-problem success < 0.5\\n- Search for any other recent work (2024-2026) on theoretical bounds on voting gain as a function of sample count k\\n- Document: the baseline assumption (exchangeability of samples), conditions for voting to help, and failure modes\\n\\n**Step 2: Voting Gain Measurement Protocols**\\n- Fetch arXiv:2605.03379 (\\\"Two Calls, Two Moments, and the Vote-Accuracy Curve\\\") and related recent papers (arXiv:2505.10772 on ranked voting; search for \\\"voting accuracy function k samples\\\") to establish:\\n  - Standard method to measure accuracy as a function of sample count k (e.g., majority vote at k=1, 3, 5, 10, etc.)\\n  - Which aggregation rules (simple majority vs. ranked voting vs. confidence-weighted) are used in SOTA\\n  - Sample sizes typically used (e.g., 10-30 per problem, or higher)\\n  - How voting gain is quantified: Δacc(k) = acc_vote(k) - acc_single (baseline single-sample accuracy)\\n- Note any sources that measure voting gain across problem-difficulty strata or problem-type subgroups\\n- Document: the standard protocol for repeated sampling, temperature settings, and baseline single-sample accuracy measurement\\n\\n**Step 3: Benchmark Selection & Difficulty Variation**\\n- Search for and compile information on reasoning/QA benchmarks suitable for this study:\\n  - GSM8K: math word problems, elementary/middle-school difficulty (available from HuggingFace, public)\\n  - MMLU: 57-subject multiple choice, difficulty stratified by level (high school to expert)\\n  - Search for a logic/puzzle benchmark (e.g., LogiQA, ARC, or MATH, which is harder than GSM8K)\\n  - Identify any emerging benchmarks from 2025-2026 for reasoning or open-ended QA\\n- For each, document: size, mean difficulty level, available problem counts, and whether they allow multiple correct answers\\n- Verify that combined benchmarks span a wide difficulty range (mean accuracy from ~0.1 to ~0.9 when averaged over all models to be tested)\\n- Document: selection rationale (diversity of problem types, difficulty span, public availability, and ease of exact grading)\\n\\n## Phase 2: Taylor's Power Law Background (Steps 4-6)\\n\\n**Step 4: Taylor's Power Law in Ecology & General Systems**\\n- Search for and review foundational and recent Taylor's law literature (ecology, epidemiology, statistical physics):\\n  - Original Taylor 1961 paper concept (log Var = log a + b * log Mean)\\n  - Review at least two foundational ecology papers confirming b values in populations (expect b=0.8-2.0 range)\\n  - Recent work on interpreting b: what does b ≈ 1 indicate (Poisson/independent noise) vs. b > 1 (clustered/correlated disturbances)\\n  - Any critical caveats: sampling artifacts, time-series length dependence, or when Taylor's law breaks down\\n- Document: the meaning of the exponent b, its typical range, and the clustering interpretation (shared driver) vs. independent interpretation\\n\\n**Step 5: Taylor's Law Applied to Language (ACL 2018 & Recent)**\\n- Fetch or read summary of \\\"Taylor's law for Human Linguistic Sequences\\\" (Kobayashi & Tanaka-Ishii, ACL 2018):\\n  - How did they fit log-log regression on variance vs. mean?\\n  - What exponent values did they find across 1100+ texts in 14 languages?\\n  - Did they stratify by text type, author, or corpus?\\n- Search for any subsequent applications of Taylor's law to computational linguistics, text analysis, or NLP systems (2019-2026)\\n- Document: methodology for fitting Taylor's law in linguistic/NLP contexts and observed b values\\n\\n**Step 6: Why Taylor's Law Has NOT Been Applied to LLM Sampling (The Gap)**\\n- Confirm via targeted search (\\\"Taylor's law LLM sampling\\\" + \\\"Taylor's law machine learning\\\") that this cross-domain transfer appears to be novel\\n- Document what is known about LLM sampling:\\n  - Per-problem variance increases with problem difficulty/ambiguity (from papers on LLM variance)\\n  - Mean accuracy per problem varies widely across benchmarks (from benchmark papers)\\n  - Error correlation / clustering across samples (from error analysis papers)\\n  - Why high-b scenarios (correlated failures) reduce voting benefit vs. low-b (independent failures) that help voting\\n- Articulate the gap: existing work uses post-hoc accuracy comparison to decide whether to vote; Taylor's exponent would provide a cheap, pre-registered proxy\\n\\n## Phase 3: LLM Sampling Variance & Error Correlation (Steps 7-9)\\n\\n**Step 7: LLM Sampling Protocols & Temperature**\\n- Fetch or read \\\"The Necessity of Setting Temperature in LLM-as-a-Judge\\\" (arXiv:2603.28304) and related papers:\\n  - What temperature ranges are standard for repeated sampling (e.g., 0.7-1.0 for diversity, 0-0.3 for deterministic)\\n  - How does temperature affect correctness variance per problem?\\n  - Is there evidence that temperature affects correlation of errors across samples?\\n- Search for empirical studies on the relationship between temperature and voting gain (e.g., \\\"does higher temperature help voting more?\\\")\\n- Document: recommended sampling protocol (temperature value, number of samples per problem, random seed handling)\\n\\n**Step 8: LLM Error Correlation & Clustering**\\n- Fetch or read papers on error diversity in LLM sampling (arXiv:2605.17333 on error diversity in rollouts, embedding-based clustering):\\n  - When do LLM samples fail in the same way (shared latent failure mode) vs. independently?\\n  - Can wrong answers be clustered by embedding similarity? What are the caveats (high false-positive rates noted in arXiv:2606.28872)?\\n  - Are there alternative clustering methods beyond embedding (e.g., syntactic similarity, semantic parsing, entailment-based grouping)?\\n- Document: methodology and caveats for mechanistic probing of high-b problems (are wrong answers concentrated in few clusters or dispersed?)\\n\\n**Step 9: Variance Components in LLM Predictions**\\n- Fetch arXiv:2607.13304 (\\\"Where Does the Noise Come From? A Variance-Components Decomposition\\\"):\\n  - What are the sources of variance in LLM predictions (resampling stochasticity, prompt paraphrasing, model identity, language)?\\n  - How much variance comes from pure within-prompt resampling (~35% in their study)?\\n  - Is resampling variance independent or correlated across problems?\\n- Document: what fraction of observed correctness variance is attributable to resampling stochasticity vs. prompt/model factors\\n\\n## Phase 4: Operationalization & Success Metrics (Steps 10-12)\\n\\n**Step 10: Fitting Taylor's Law to LLM Correctness**\\n- Based on phases 1-3, specify the exact protocol:\\n  - Per problem p in a benchmark B, sample N times at fixed temperature (e.g., 0.7, N=20-30)\\n  - Compute mean correctness m_p = (# correct) / N\\n  - Compute variance v_p from the N binary correctness outcomes (Bernoulli variance)\\n  - Fit log-log regression: log(v_p) = log(a) + b * log(m_p) across all problems in B\\n  - Extract b and its 95% confidence interval (CI)\\n  - Repeat per (model, benchmark) pair\\n- Document: whether to exclude edge cases (m_p = 0 or 1, which give zero variance), how to handle log(0), potential biases in fitting\\n\\n**Step 11: Predicting Voting Gain from b**\\n- Based on voting curves theory (step 2), specify how b should predict voting gain:\\n  - Hypothesis: high b (≥ 1.5) → low voting gain (correlated errors reduce benefit)\\n  - Hypothesis: low b (≈ 1.0) → high voting gain (independent errors benefit from aggregation)\\n  - Test via Spearman rank correlation (rank-based to avoid assuming linear relationship) between b and measured voting gain\\n  - Preregister threshold: |ρ| > 0.5, p < 0.05 (from the hypothesis document)\\n- Document: the exact success criterion, why Spearman (not Pearson), and the rationale for the |ρ| > 0.5 threshold\\n\\n**Step 12: Generalization & Mechanistic Probing Plan**\\n- Specify held-out test design:\\n  - Calibrate b-to-voting-gain mapping on a subset of (model, benchmark, difficulty-stratum) combinations\\n  - Test on held-out (model, benchmark, difficulty-stratum) not used in calibration\\n  - Report correlation and p-value on held-out data\\n- Specify mechanistic probe:\\n  - For high-b problems, cluster wrong answers (pick clustering method from step 8)\\n  - Compute entropy / concentration of wrong-answer distribution\\n  - Compare entropy in high-b vs. low-b problem sets (expect lower entropy in high-b, supporting clustering interpretation)\\n  - Disconfirm if entropy does not track b\\n- Document: how these tests validate or falsify the hypothesis\\n\\n## Phase 5: Dataset & Computational Requirements (Steps 13-14)\\n\\n**Step 13: Compute Budget & Model Selection**\\n- Confirm via OpenRouter pricing what open LLMs are available and feasible within $10 budget:\\n  - Small models (7B params): cheaper per call, lower quality\\n  - Mid-range (13-32B): better reasoning\\n  - Larger open models (70B+): best reasoning, expensive\\n  - Plan to test 2-4 models across size range\\n- Per (model, benchmark), compute total API calls: n_problems * n_samples (e.g., 1000 problems * 20 samples = 20k calls)\\n  - Estimate cost per call and total budget\\n  - Decide on n_samples (10-30) to balance statistical power vs. budget\\n- Document: selected models, n_samples per problem, expected total cost and how it stays under $10 cap\\n\\n**Step 14: Expected Outcomes & Failure Scenarios**\\n- Document: what success looks like (b predicts voting gain, transfer across models/benchmarks, mechanistic support)\\n- Document: what disconfirmation looks like (no correlation, transfer failure, wrong-answer entropy doesn't track b, single-model-only effect)\\n- Document: what ambiguous outcomes might occur (weak correlation, model-specific effects, non-linear relationship) and how to interpret them\\n\\n## Summary of Key Decisions for Executor\\n\\n1. **Benchmarks**: GSM8K, MMLU, MATH (or equivalent logic/puzzle set) for difficulty span\\n2. **Models**: 2-4 open LLMs via OpenRouter, mix of 7B, 13-32B, 70B sizes\\n3. **Sampling**: Fixed temperature (e.g., 0.7), N=20-30 samples per problem\\n4. **Taylor's Law Fit**: Log-log linear regression on (log mean, log variance) per (model, benchmark)\\n5. **Voting Gain Metric**: Accuracy with majority vote at k=1, 3, 5, 10, 20 samples\\n6. **Correlation Test**: Spearman ρ on b vs. voting gain, threshold |ρ| > 0.5, p < 0.05\\n7. **Mechanistic Probe**: Cluster wrong answers in high-b problems, compare entropy vs. low-b\\n8. **Generalization**: Hold out (model, benchmark, difficulty) combinations for transfer test\\n9. **Budget**: Estimate total API calls under $10 OpenRouter cap; adjust N or model count as needed\\n10. **Success Criterion**: Confirms if b correlates with voting gain and transfers across models/benchmarks; disconfirms if not\",\n  \"explanation\": \"This research plan lays the foundation for testing a novel hypothesis: that Taylor's power law exponent (b), computed from repeated LLM sampling, can serve as a cheap, pre-registered diagnostic to predict whether majority voting will improve accuracy on a given task. The plan synthesizes four critical knowledge areas: (1) voting theory from recent de Finetti work to understand why voting sometimes helps and sometimes hurts; (2) Taylor's law from ecology and its rare application to language to establish the methodology and interpretation of the exponent b; (3) LLM sampling variance and error correlation to understand whether the independence vs. clustering distinction applies to LLM errors; and (4) practical benchmarks and sampling protocols to make the investigation concrete and reproducible. The plan operationalizes the core prediction—high b (correlated errors) → low voting gain; low b (independent errors) → high voting gain—into a testable, pre-registered statistical test (Spearman rank correlation with |ρ| > 0.5, p < 0.05 threshold). It also specifies a mechanistic probe (wrong-answer clustering entropy) to support or falsify the interpretation of b as a clustering diagnostic rather than a statistical artifact. By grounding the methodology in existing literature and best practices from both ecology and LLM research, the plan ensures the executor can implement a rigorous, well-motivated experiment that either confirms a genuinely novel link between two scientific domains (ecology and LLM behavior) or clearly disconfirms it, advancing the field's understanding of test-time compute allocation.\"\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [42] ASSISTANT · 2026-08-01 14:43:33 UTC

```
Perfect! I've created a comprehensive, actionable research plan for the executor. The plan is now saved at `./.terminal_claude_agent_struct_out.json`.

## Summary

The research plan I've created operationalizes the hypothesis into a concrete investigation across **5 phases with 14 specific steps**:

### Key Components:

**Phase 1: Voting Theory** — Establishes measurement protocols for voting gain and selects benchmarks with sufficient difficulty variation to fit Taylor's law across a wide range of mean accuracies.

**Phase 2: Taylor's Law Foundation** — Reviews ecology literature to understand the exponent b (independence vs. clustering), locates the only prior application to language (ACL 2018), and **confirms this cross-domain transfer to LLM sampling is novel**.

**Phase 3: LLM Sampling Variance** — Documents temperature protocols, error correlation mechanisms, and variance-component decomposition to validate the independence/clustering lens.

**Phase 4: Operationalization** — Specifies exact protocols for:
- Fitting Taylor's law via log-log regression on per-problem (mean, variance) pairs
- Predicting voting gain using Spearman rank correlation with pre-registered threshold (|ρ| > 0.5, p < 0.05)
- Mechanistic validation via wrong-answer clustering entropy

**Phase 5: Feasibility** — Budgets API calls under the $10 OpenRouter cap and specifies held-out generalization tests.

### Concrete Details for Executor:

- **Benchmarks**: GSM8K, MMLU, MATH (span difficulty from ~0.1 to ~0.9 accuracy)
- **Models**: 2-4 open LLMs via OpenRouter (7B, 13-32B, 70B mix)
- **Sampling**: Temperature 0.7, N=20-30 samples per problem
- **Success Criteria**: High b ↔ low voting gain; transfer across held-out models/benchmarks; wrong-answer entropy tracks b
- **Failure Scenarios**: No correlation, single-model-only effects, entropy doesn't track b

The plan is grounded in specific papers (arXiv:2605.05592 on voting curves, arXiv:2605.03379 on vote-accuracy functions, Taylor's law ACL 2018 linguistics work) and avoids vague hand-waving by specifying exact measurement protocols and statistical tests.
```
