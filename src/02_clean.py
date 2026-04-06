"""cleans raw data & make clean dataset"""

#clean reviews

import json
import re
import os

def clean_text(text):
    text = text.lower()                         # change text to lowercase
    text = re.sub(r'[^a-z\s]', '', text)        # special characters
    text = re.sub(r'\s+', ' ', text).strip()    # whitespaces
    return text

seen = set()
cleaned = []

with open('../data/reviews_raw.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        content = clean_text(data["content"])

        if len(content.split()) < 3:
            continue
        if content in seen:
            continue

        seen.add(content)

        cleaned.append({
            "review_id": data["review_id"],
            "content": content
        })

with open('../data/reviews_clean.jsonl', 'w', encoding='utf-8') as f:        #write cleaned reviews to reviews_clean.jsonl
    for r in cleaned:
        json.dump(r, f)
        f.write("\n")

print(f" \n Updated reviews_clean.jsonl, cleaned dataset size: {len(cleaned)} \n\n")