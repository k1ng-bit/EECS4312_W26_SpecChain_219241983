"""generates structured specs from personas"""

import os
import json
from groq import Groq

MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"        #model

PERSONAS_IN = "personas/personas_auto.json"                 # input persona file
SPEC_OUT = "spec/spec_auto.md"                              # output spec file

os.makedirs("spec", exist_ok=True)

def strip_code_fence(text):                     #remove whitespaces and split 
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if len(lines) >= 2:
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        return "\n".join(lines).strip()
    return text

def main():
    if not os.environ.get("GROQ_API_KEY"):
        raise RuntimeError("GROQ_API_KEY is not set in the environment.")       #error incase no api key present

    with open(PERSONAS_IN, "r", encoding="utf-8") as f:                 # open the input file to read
        personas = json.load(f)

    personas_text = json.dumps(personas, indent=2)

    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    system_prompt = (
        "You are a software requirements engineering assistant. "
        "Write clear, testable requirements. Return plain markdown only."
    )

    user_prompt = f"""
Using the personas below for the MindDoc app, generate exactly 10 functional requirements.

Follow this exact markdown format for each requirement:

# Requirement ID: FR_auto_1
- Description: [The system shall ...]
- Source Persona: [Persona Name]
- Traceability: [Derived from review group A1]
- Acceptance Criteria: [Given ... When ... Then ...]

Rules:
- Exactly 10 requirements.
- Requirement IDs must be FR1 to FR10.
- Each requirement must be testable.
- Avoid vague words like easy, better, user-friendly, fast unless measurable.
- Use persona names exactly as provided.
- Traceability must reference the persona's group.

Personas:
{personas_text}
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

    with open(SPEC_OUT, "w", encoding="utf-8") as f:                #write to spec out 
        f.write(content)

    print(f"Saved {SPEC_OUT}")

if __name__ == "__main__":
    main()