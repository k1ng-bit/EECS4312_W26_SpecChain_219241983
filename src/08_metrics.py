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

    # matches FR1, FR_auto_1, FR_hybrid_1, etc.
    req_pattern = r'([A-Za-z][A-Za-z0-9_]*\d+)'

    chunks = re.split(rf'(?=# Requirement ID:\s*{req_pattern})', text)
    chunks = [c.strip() for c in chunks if c.strip().startswith("# Requirement ID:")]

    requirements = []

    for chunk in chunks:
        req_id_match = re.search(rf"# Requirement ID:\s*{req_pattern}", chunk)
        source_match = re.search(r"- Source Persona:\s*\[?(.*?)\]?\s*$", chunk, flags=re.MULTILINE)
        trace_match = re.search(r"- Traceability:\s*\[?(.*?)\]?\s*$", chunk, flags=re.MULTILINE)
        acc_match = re.search(r"- Acceptance Criteria:\s*\[?(.*?)\]?\s*$", chunk, flags=re.MULTILINE)

        req_id = req_id_match.group(1).strip() if req_id_match else None
        source = source_match.group(1).strip() if source_match else None
        trace = trace_match.group(1).strip() if trace_match else None
        acceptance = acc_match.group(1).strip() if acc_match else ""

        if req_id:
            requirements.append({
                "id": req_id,
                "source_persona": source,
                "traceability": trace,
                "acceptance": acceptance,
                "chunk": chunk
            })

    return requirements

def compute_metrics(pipeline_name):
    cfg = PIPELINES[pipeline_name]

    dataset_size = line_count(DATASET_FILE)

    personas_json = load_json(cfg["personas"])
    groups_json = load_json(cfg["groups"])
    tests_json = load_json(cfg["tests"])
    requirements = parse_requirements(cfg["spec"])

    personas = personas_json.get("personas", [])
    groups = groups_json.get("groups", [])
    tests = tests_json.get("tests", [])

    persona_count = len(personas)
    requirements_count = len(requirements)
    tests_count = len(tests)

    covered_review_ids = set()
    for g in groups:
        for rid in g.get("review_ids", []):
            covered_review_ids.add(rid)

    review_coverage = round(len(covered_review_ids) / dataset_size, 4) if dataset_size else 0.0

    traceable_requirements = 0
    for req in requirements:
        if req["source_persona"] and req["traceability"]:
            traceable_requirements += 1

    traceability_ratio = round(traceable_requirements / requirements_count, 4) if requirements_count else 0.0

    tested_requirements = {t.get("requirement_id") for t in tests}
    req_ids = {r["id"] for r in requirements}
    matched_tested = req_ids.intersection(tested_requirements)
    testability_rate = round(len(matched_tested) / requirements_count, 4) if requirements_count else 0.0

    ambiguous_count = 0
    for req in requirements:
        chunk_lower = req["chunk"].lower()
        if any(word in chunk_lower for word in AMBIGUOUS_WORDS):
            ambiguous_count += 1

    ambiguity_ratio = round(ambiguous_count / requirements_count, 4) if requirements_count else 0.0

    traceability_links = persona_count + traceable_requirements

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