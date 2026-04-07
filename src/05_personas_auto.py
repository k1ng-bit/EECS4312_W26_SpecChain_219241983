"""automated persona generation pipeline"""

import os
import json
import random
from groq import Groq

MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"

INPUT_FILE = "data/reviews_clean.jsonl"
GROUPS_OUT = "data/review_groups_auto.json"
PERSONAS_OUT = "personas/personas_auto.json"
PROMPT_OUT = "prompts/prompt_auto.json"

os.makedirs("data", exist_ok=True)
os.makedirs("personas", exist_ok=True)
os.makedirs("prompts", exist_ok=True)

def load_reviews(path):
    reviews = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            reviews.append(json.loads(line))
    return reviews

def sample_reviews(reviews, n=500, seed=42):
    random.seed(seed)
    if len(reviews) <= n:
        return reviews
    return random.sample(reviews, n)

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

def call_groq_json(system_prompt, user_prompt):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.2,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    content = completion.choices[0].message.content
    content = strip_code_fence(content)
    return json.loads(content), content

def main():
    if not os.environ.get("GROQ_API_KEY"):
        raise RuntimeError("GROQ_API_KEY is not set in the environment.")

    reviews = load_reviews(INPUT_FILE)
    sampled = sample_reviews(reviews, n=120)

    reviews_text = "\n".join([
        f'review_id: {r["review_id"]} | content: {r["content"]}'
        for r in sampled
    ])

    system_prompt = (
        "You are a software requirements engineering assistant. "
        "Return ONLY valid JSON with no explanation."
    )

    user_prompt = f"""
Using the cleaned user reviews below for the MindDoc app, do two tasks:

1. Create exactly 5 review groups.
2. Create exactly 5 personas, one derived from each review group.

Rules:
- Use only the review IDs given below.
- Each group must have at least 10 review_ids.
- Keep themes meaningful and distinct.
- Personas must be grounded in the grouped reviews.
- Do not invent unsupported claims.
- Return JSON ONLY in this exact schema:

{{
  "groups": [
    {{
      "group_id": "A1",
      "theme": "short theme",
      "review_ids": [1, 2, 3],
      "example_reviews": [
        "short example review text 1",
        "short example review text 2"
      ]
    }}
  ],
  "personas": [
    {{
      "id": "P1",
      "name": "Persona Name",
      "description": "1-2 sentence description",
      "derived_from_group": "G1",
      "goals": ["goal1", "goal2"],
      "pain_points": ["pain1", "pain2"],
      "context": ["context1", "context2"],
      "constraints": ["constraint1", "constraint2"],
      "evidence_reviews": [1, 2]
    }}
  ]
}}

Reviews:
{reviews_text}
""".strip()

    result, raw_response = call_groq_json(system_prompt, user_prompt)

    with open(GROUPS_OUT, "w", encoding="utf-8") as f:
        json.dump({"groups": result["groups"]}, f, indent=2)

    with open(PERSONAS_OUT, "w", encoding="utf-8") as f:
        json.dump({"personas": result["personas"]}, f, indent=2)

    with open(PROMPT_OUT, "w", encoding="utf-8") as f:
        json.dump({
            "model": MODEL_NAME,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "raw_response": raw_response
        }, f, indent=2)

    print("Saved:")
    print(f"- {GROUPS_OUT}")
    print(f"- {PERSONAS_OUT}")
    print(f"- {PROMPT_OUT}")

if __name__ == "__main__":
    main()