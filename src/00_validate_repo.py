"""checks required files/folders exist"""
import os

print("Checking repository structure...\n")

REQUIRED_FILES = [
    # data
    "data/reviews_raw.jsonl",
    "data/reviews_clean.jsonl",
    "data/dataset_metadata.json",
    "data/review_groups_manual.json",
    "data/review_groups_hybrid.json",

    # metrics
    "metrics/metrics_manual.json",
    "metrics/metrics_auto.json",
    "metrics/metrics_hybrid.json",

    # src
    "src/00_validate_repo.py",
    "src/01_collect_or_import.py",
    "src/02_clean.py",
    "src/03_manual_coding_template.py",
    "src/04_personas_manual.py",
    "src/05_personas_auto.py",
    "src/06_spec_generate.py",
    "src/07_tests_generate.py",
    "src/08_metrics.py",
    "src/run_all.py",

    # personas
    "personas/personas_manual.json",
    "personas/personas_auto.json",
    "personas/personas_hybrid.json",

    # spec
    "spec/spec_manual.md",
    "spec/spec_auto.md",
    "spec/spec_hybrid.md",

    # tests
    "tests/tests_manual.json",
    "tests/tests_auto.json",
    "tests/tests_hybrid.json",

    # reflection
    "reflection/reflection.md",

    #readme
    "README.md"
]

all_good = True             #if all the files are present then true

for file in REQUIRED_FILES:
    if os.path.exists(file):
        print(f"{file} found")
    else:
        print(f"{file} MISSING")
        all_good = False

print("\nRepository validation complete.")  # If all the files are present.