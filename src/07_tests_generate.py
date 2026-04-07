"""generates tests from specs"""

import os
import re
import json
from groq import Groq

MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"

SPEC_IN = "spec/spec_auto.md"
TESTS_OUT = "tests/tests_auto.json"

os.makedirs("tests", exist_ok=True)

def strip_code_fence(text):
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if len(lines) >= 2:
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        return "\n".join(lines).strip()
    return text

def extract_requirement_ids(spec_text):
    return re.findall(r"# Requirement ID:\s*(FR\d+)", spec_text)

def main():
    if not os.environ.get("GROQ_API_KEY"):
        raise RuntimeError("GROQ_API_KEY is not set in the environment.")

    with open(SPEC_IN, "r", encoding="utf-8") as f:
        spec_text = f.read()

    req_ids = extract_requirement_ids(spec_text)
    if not req_ids:
        raise RuntimeError("No requirement IDs found in spec_auto.md")

    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    system_prompt = (
        "You are a software testing assistant. Return ONLY valid JSON."
    )

    user_prompt = f"""
Generate exactly one test scenario for each requirement in the specification below.

Return JSON ONLY in this exact schema:
{{
  "tests": [
    {{
      "test_id": "T_auto_1",
      "requirement_id": "FR1",
      "scenario": "short scenario name",
      "steps": ["step 1", "step 2"],
      "expected_result": "expected result"
    }}
  ]
}}

Rules:
- Create exactly {len(req_ids)} tests.
- Cover every requirement exactly once.
- requirement_id must be one of: {req_ids}
- Use unique test IDs in the format T_auto_1, T_auto_2, ...
- Steps must be clear and executable.

Specification:
{spec_text}
""".strip()

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.2,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    content = strip_code_fence(completion.choices[0].message.content)
    tests_json = json.loads(content)

    with open(TESTS_OUT, "w", encoding="utf-8") as f:
        json.dump(tests_json, f, indent=2)

    print(f"Saved {TESTS_OUT}")

if __name__ == "__main__":
    main()