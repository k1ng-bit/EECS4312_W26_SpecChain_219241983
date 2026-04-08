"""checks required files/folders exist"""

import os

REQUIRED_FOLDERS = [
    "data",
    "personas",
    "spec",
    "tests",
    "metrics",
    "src",
    "prompts",
    "reflection"
]

REQUIRED_FILES = [
    # data
    "data/reviews_raw.jsonl",
    "data/reviews_clean.jsonl",
    "data/dataset_metadata.json",
    "data/review_groups_manual.json",
    "data/review_groups_auto.json",
    "data/review_groups_hybrid.json",

    # personas
    "personas/personas_manual.json",
    "personas/personas_auto.json",
    "personas/personas_hybrid.json",

    # specs
    "spec/spec_manual.md",
    "spec/spec_auto.md",
    "spec/spec_hybrid.md",

    # tests
    "tests/tests_manual.json",
    "tests/tests_auto.json",
    "tests/tests_hybrid.json",

    # metrics
    "metrics/metrics_manual.json",
    "metrics/metrics_auto.json",
    "metrics/metrics_hybrid.json",
    "metrics/metrics_summary.json",

    # prompts
    "prompts/prompt_auto.json",

    # src
    "src/00_validate_repo.py",
    "src/01_collect_or_import.py",
    "src/02_clean.py",
    "src/03_manual_coding_template.py",
    "src/05_personas_auto.py",
    "src/06_spec_generate.py",
    "src/07_tests_generate.py",
    "src/08_metrics.py",
    "src/run_all.py"
]

def main():
    print("Checking repository structure...\n")

    all_good = True

    for folder in REQUIRED_FOLDERS:
        if os.path.isdir(folder):
            print(f"{folder}/ found")
        else:
            print(f"{folder}/ MISSING")
            all_good = False

    print()

    for file_path in REQUIRED_FILES:
        if os.path.exists(file_path):
            print(f"{file_path} found")
        else:
            print(f"{file_path} MISSING")
            all_good = False

    print("\nRepository validation complete.")

    if all_good:
        print("All required folders and files are present.")
    else:
        print("Some required folders or files are missing.")

if __name__ == "__main__":
    main()