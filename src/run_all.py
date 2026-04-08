"""runs the full pipeline end-to-end"""
import os
import sys

def run_step(command, description):
    print(f"\n=== {description} ===")
    exit_code = os.system(command)
    if exit_code != 0:
        print(f"\nERROR: Step failed -> {description}")
        print(f"Command: {command}")
        sys.exit(1)

def main():
    print("Starting automated pipeline...\n")

    # Step 1: Collect or import raw reviews
    # Produces: data/reviews_raw.jsonl
    # If your raw dataset already exists, this step can still be rerun.
    run_step("py src/01_collect_or_import.py", "Step 1 - Collect or import raw reviews")

    # Step 2: Clean raw reviews
    # Produces: data/reviews_clean.jsonl and supports dataset metadata
    run_step("py src/02_clean.py", "Step 2 - Clean raw reviews")

    # Step 3: Generate automated review groups and personas
    # Produces:
    # - data/review_groups_auto.json
    # - personas/personas_auto.json
    # - prompts/prompt_auto.json
    run_step("py src/05_personas_auto.py", "Step 3 - Generate automated review groups and personas")

    # Step 4: Generate automated specification
    # Produces: spec/spec_auto.md
    run_step("py src/06_spec_generate.py", "Step 4 - Generate automated specification")

    # Step 5: Generate automated validation tests
    # Produces: tests/tests_auto.json
    run_step("py src/07_tests_generate.py", "Step 5 - Generate automated tests")

    # Step 6: Compute metrics
    # Produces:
    # - metrics/metrics_manual.json
    # - metrics/metrics_auto.json
    # - metrics/metrics_hybrid.json
    # - metrics/metrics_summary.json
    run_step("py src/08_metrics.py", "Step 6 - Compute metrics")

    print("\nAutomated pipeline completed successfully.")

if __name__ == "__main__":
    main()