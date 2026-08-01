# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru"]
# ///
"""Standardize 6 reasoning benchmarks (GSM8K, MMLU, ARC-Challenge, HellaSwag,
CommonsenseQA, OpenBookQA) from temp/datasets/ into exp_sel_data_out.json schema."""

import json
import re
import sys
from pathlib import Path
from string import ascii_uppercase

from loguru import logger

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

WORKSPACE = Path(__file__).parent
DATA_DIR = WORKSPACE / "temp" / "datasets"


def label_choices(labels: list[str], texts: list[str]) -> str:
    return "\n".join(f"{lab}. {txt}" for lab, txt in zip(labels, texts))


def gsm8k_examples() -> list[dict]:
    path = DATA_DIR / "full_openai_gsm8k_main_test.json"
    rows = json.loads(path.read_text())
    examples = []
    for i, row in enumerate(rows):
        final_answer_match = re.search(r"####\s*(.+)", row["answer"])
        final_answer = final_answer_match.group(1).strip() if final_answer_match else row["answer"].strip()
        num_steps = row["answer"].count("<<")
        examples.append(
            {
                "input": row["question"],
                "output": final_answer,
                "metadata_row_index": i,
                "metadata_task_type": "free_response_math",
                "metadata_reasoning_steps": num_steps,
                "metadata_question_length_chars": len(row["question"]),
                "metadata_full_solution": row["answer"],
            }
        )
    return examples


def mmlu_examples() -> list[dict]:
    path = DATA_DIR / "full_cais_mmlu_all_test.json"
    rows = json.loads(path.read_text())
    examples = []
    for i, row in enumerate(rows):
        choices = row["choices"]
        labels = list(ascii_uppercase[: len(choices)])
        answer_idx = row["answer"]
        examples.append(
            {
                "input": f"{row['question']}\n\n{label_choices(labels, choices)}",
                "output": labels[answer_idx],
                "metadata_row_index": i,
                "metadata_task_type": "classification",
                "metadata_subject": row["subject"],
                "metadata_n_classes": len(choices),
                "metadata_choice_texts": choices,
                "metadata_question_length_chars": len(row["question"]),
            }
        )
    return examples


def arc_challenge_examples() -> list[dict]:
    path = DATA_DIR / "full_allenai_ai2_arc_ARC-Challenge_test.json"
    rows = json.loads(path.read_text())
    examples = []
    for i, row in enumerate(rows):
        labels = row["choices"]["label"]
        texts = row["choices"]["text"]
        if row["answerKey"] not in labels:
            logger.warning(f"ARC row {i} ({row['id']}): answerKey {row['answerKey']!r} not in labels {labels}; skipping")
            continue
        examples.append(
            {
                "input": f"{row['question']}\n\n{label_choices(labels, texts)}",
                "output": row["answerKey"],
                "metadata_row_index": i,
                "metadata_task_type": "classification",
                "metadata_problem_id": row["id"],
                "metadata_n_classes": len(labels),
                "metadata_choice_texts": texts,
                "metadata_question_length_chars": len(row["question"]),
            }
        )
    return examples


def hellaswag_examples() -> list[dict]:
    path = DATA_DIR / "full_Rowan_hellaswag_default_validation.json"
    rows = json.loads(path.read_text())
    examples = []
    for i, row in enumerate(rows):
        endings = row["endings"]
        labels = list(ascii_uppercase[: len(endings)])
        answer_idx = int(row["label"])
        examples.append(
            {
                "input": f"{row['ctx']}\n\n{label_choices(labels, endings)}",
                "output": labels[answer_idx],
                "metadata_row_index": i,
                "metadata_task_type": "classification",
                "metadata_activity_label": row["activity_label"],
                "metadata_n_classes": len(endings),
                "metadata_choice_texts": endings,
                "metadata_question_length_chars": len(row["ctx"]),
            }
        )
    return examples


def commonsense_qa_examples() -> list[dict]:
    path = DATA_DIR / "full_tau_commonsense_qa_default_validation.json"
    rows = json.loads(path.read_text())
    examples = []
    for i, row in enumerate(rows):
        labels = row["choices"]["label"]
        texts = row["choices"]["text"]
        if row["answerKey"] not in labels:
            logger.warning(f"CommonsenseQA row {i} ({row['id']}): answerKey {row['answerKey']!r} not in labels; skipping")
            continue
        examples.append(
            {
                "input": f"{row['question']}\n\n{label_choices(labels, texts)}",
                "output": row["answerKey"],
                "metadata_row_index": i,
                "metadata_task_type": "classification",
                "metadata_problem_id": row["id"],
                "metadata_question_concept": row["question_concept"],
                "metadata_n_classes": len(labels),
                "metadata_choice_texts": texts,
                "metadata_question_length_chars": len(row["question"]),
            }
        )
    return examples


def openbookqa_examples() -> list[dict]:
    path = DATA_DIR / "full_allenai_openbookqa_main_test.json"
    rows = json.loads(path.read_text())
    examples = []
    for i, row in enumerate(rows):
        labels = row["choices"]["label"]
        texts = row["choices"]["text"]
        if row["answerKey"] not in labels:
            logger.warning(f"OpenBookQA row {i} ({row['id']}): answerKey {row['answerKey']!r} not in labels; skipping")
            continue
        examples.append(
            {
                "input": f"{row['question_stem']}\n\n{label_choices(labels, texts)}",
                "output": row["answerKey"],
                "metadata_row_index": i,
                "metadata_task_type": "classification",
                "metadata_problem_id": row["id"],
                "metadata_n_classes": len(labels),
                "metadata_choice_texts": texts,
                "metadata_question_length_chars": len(row["question_stem"]),
            }
        )
    return examples


# Final 3 selected out of 6 candidates: GSM8K, MMLU, ARC-Challenge give
# orthogonal reasoning modes (arithmetic / factual recall / science logic)
# with the documented difficulty spread the artifact plan requires.
# HellaSwag, CommonsenseQA, OpenBookQA were built, previewed, and validated
# but dropped as redundant with ARC-Challenge/CommonsenseQA-style commonsense
# coverage and outside the plan's named triad.
DATASET_BUILDERS = {
    "gsm8k": gsm8k_examples,
    "mmlu": mmlu_examples,
    "arc_challenge": arc_challenge_examples,
}


@logger.catch(reraise=True)
def main() -> None:
    datasets = []
    for name, builder in DATASET_BUILDERS.items():
        logger.info(f"Building examples for {name}")
        examples = builder()
        logger.info(f"{name}: {len(examples)} examples")
        datasets.append({"dataset": name, "examples": examples})

    output = {
        "metadata": {
            "source": "HuggingFace Hub",
            "description": "Six reasoning benchmarks standardized to unified schema for difficulty-stratification research",
            "benchmark_ids": {
                "gsm8k": "openai/gsm8k (config=main, split=test)",
                "mmlu": "cais/mmlu (config=all, split=test)",
                "arc_challenge": "allenai/ai2_arc (config=ARC-Challenge, split=test)",
                "hellaswag": "Rowan/hellaswag (split=validation)",
                "commonsense_qa": "tau/commonsense_qa (split=validation)",
                "openbookqa": "allenai/openbookqa (config=main, split=test)",
            },
        },
        "datasets": datasets,
    }

    out_path = WORKSPACE / "full_data_out.json"
    out_path.write_text(json.dumps(output, indent=2))
    total = sum(len(d["examples"]) for d in datasets)
    logger.info(f"Wrote {total} total examples across {len(datasets)} datasets to {out_path}")


if __name__ == "__main__":
    main()
