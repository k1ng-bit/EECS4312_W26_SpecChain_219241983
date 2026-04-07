"""computes metrics: coverage/traceability/ambiguity/testability"""

import os
import re
import json

DATASET_FILE = "data/reviews_clean.jsonl"

PIPELINES = {
    "manual": {
        "personas": "personas/personas_manual.json",
        "spec": "spec/spec_manual.md",
        "tests": "tests/tests_manual.json",
        "groups": "data/review_groups_manual.json",
        "out": "metrics/metrics_manual.json"
    },
    "auto": {
        "personas": "personas/personas_auto.json",
        "spec": "spec/spec_auto.md",
        "tests": "tests/tests_auto.json",
        "groups": "data/review_groups_auto.json",
        "out": "metrics/metrics_auto.json"
    },
    "hybrid": {
        "personas": "personas/personas_hybrid.json",
        "spec": "spec/spec_hybrid.md",
        "tests": "tests/tests_hybrid.json",
        "groups": "data/review_groups_hybrid.json",
        "out": "metrics/metrics_hybrid.json"
    }
}

AMBIGUOUS_WORDS = [
    "fast", "easy", "better", "user-friendly", "simple", "quick", "effective"
]

os.makedirs("metrics", exist_ok=True)

def line_count(path):
    with open(path, "r", encoding="utf-8") as f:
        return sum(1 for _ in f)

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def parse_requirements(spec_path):
    with open(spec_path, "r", encoding="utf-8") as f:
        text = f.read()

    req_ids = re.findall(r"# Requirement ID:\s*(FR\d+)", text)
    persona_refs = re.findall(r"- Source Persona:\s*\[(.*?)\]", text)
    acceptance = re.findall(r"- Acceptance Criteria:\s*\[(.*?)\]", text)

    return {
        "text": text,
        "requirement_ids": req_ids,
        "persona_refs": persona_refs,
        "acceptance": acceptance
    }

def compute_metrics(pipeline_name):
    cfg = PIPELINES[pipeline_name]

    dataset_size = line_count(DATASET_FILE)

    personas_json = load_json(cfg["personas"])
    groups_json = load_json(cfg["groups"])
    tests_json = load_json(cfg["tests"])
    spec_data = parse_requirements(cfg["spec"])

    personas = personas_json.get("personas", [])
    groups = groups_json.get("groups", [])
    tests = tests_json.get("tests", [])

    persona_count = len(personas)
    requirements_count = len(spec_data["requirement_ids"])
    tests_count = len(tests)

    covered_review_ids = set()
    for g in groups:
        for rid in g.get("review_ids", []):
            covered_review_ids.add(rid)

    review_coverage = round(len(covered_review_ids) / dataset_size, 4) if dataset_size else 0.0

    traceability_ratio = 1.0 if requirements_count > 0 and len(spec_data["persona_refs"]) == requirements_count else 0.0

    tested_requirements = {t.get("requirement_id") for t in tests}
    req_set = set(spec_data["requirement_ids"])
    testability_rate = round(len(req_set.intersection(tested_requirements)) / requirements_count, 4) if requirements_count else 0.0

    ambiguous_count = 0
    all_acceptance = " ".join(spec_data["acceptance"]).lower()
    text_lower = spec_data["text"].lower()
    for req_id in spec_data["requirement_ids"]:
        pass

    # simple ambiguity scan, ratio by requirements
    for req_id in spec_data["requirement_ids"]:
        # approximate: count req ambiguous if any ambiguous word appears anywhere in spec
        pattern = rf"# Requirement ID:\s*{req_id}(.*?)(?=# Requirement ID:|$)"
        match = re.search(pattern, spec_data["text"], flags=re.DOTALL)
        if match:
            chunk = match.group(1).lower()
            if any(w in chunk for w in AMBIGUOUS_WORDS):
                ambiguous_count += 1

    ambiguity_ratio = round(ambiguous_count / requirements_count, 4) if requirements_count else 0.0

    # approximate traceability links:
    traceability_links = persona_count + requirements_count

    metrics = {
        "pipeline": pipeline_name,
        "dataset_size": dataset_size,
        "persona_count": persona_count,
        "requirements_count": requirements_count,
        "tests_count": tests_count,
        "traceability_links": traceability_links,
        "review_coverage": review_coverage,
        "traceability_ratio": traceability_ratio,
        "testability_rate": testability_rate,
        "ambiguity_ratio": ambiguity_ratio
    }

    with open(cfg["out"], "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print(f"Saved {cfg['out']}")
    return metrics

def main():
    summary = {}
    for name in ["manual", "auto", "hybrid"]:
        cfg = PIPELINES[name]
        if all(os.path.exists(cfg[k]) for k in ["personas", "spec", "tests", "groups"]):
            summary[name] = compute_metrics(name)

    with open("metrics/metrics_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("Saved metrics/metrics_summary.json")

if __name__ == "__main__":
    main()