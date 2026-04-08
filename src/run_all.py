"""runs the full pipeline end-to-end"""
import os
import sys

def run_step(command, description):             # the run step function to run the file
    print(f"\n - {description} ")
    exit_code = os.system(command)
    if exit_code != 0:
        print(f"\nERROR: {description}")        #if error takes place, print the error message
        print(f"Command: {command}")
        sys.exit(1)

def main():
    print("Starting automated pipeline...\n")

    # Run src/01_collect_or_import.py. It outputs the Raw review data.
    run_step("py src/01_collect_or_import.py", "Collecting or importing raw reviews")

    # Run src/ 02_clean.py . This outputs the cleaned review data.
    run_step("py src/02_clean.py", "Cleaning raw reviews")

    # Making sure the API KEY is set so that the files run successfuly for the auto pipeline
    if not os.environ.get("GROQ_API_KEY"):
        print("ERROR: GROQ_API_KEY is not set in the environment.")         #print error incase api key not set
        print("Set API KEY using $env:GROQ_API_KEY=\"your_key_here\" and rerun run_all.py " ) 
        sys.exit(1)

    # Run 05_personas_auto.py to automatically generate the Personas for the automated pipeline
    run_step("py src/05_personas_auto.py", "Generating automated review groups and personas")

    # Run 06_spec_generate.py to automatically generate the spec documentation for the automated pipleline
    run_step("py src/06_spec_generate.py", "Generating automated specification")

    # Run 07_tests_generate.py to automatically generate the tests for teh automated pipeling
    run_step("py src/07_tests_generate.py", "Generating automated tests")

    # Run the metrics.py script to generate the metrics for auto pipleling and update summary
    run_step("py src/08_metrics.py", "Computing all metrics")

    print("\nAutomated pipeline generation complete.")          #message when generated successfuly

if __name__ == "__main__":
    main()