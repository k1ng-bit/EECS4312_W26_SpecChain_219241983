"""imports or reads your raw dataset; if you scraped, include scraper here"""

from google_play_scraper import reviews_all
import json

# the app id for MindDoc: Mental Health Support
app_id = "de.moodpath.android"

# fetching all the reviews
reviews = reviews_all(
    app_id,
    lang='en',
    country='us',       #taking reviews from US
    sleep_milliseconds=0
)

reviews = reviews[:3500] #taking 3500 reviews

print("Number of Reviews taken: " , len(reviews))
print(reviews[0])       #printing the first review

with open("data/reviews_raw.jsonl", "w", encoding="utf-8") as f:     #writing the raw reviews into reviews_raw.jsonl file
    for i, review in enumerate(reviews):
        json.dump({
            "review_id": i,
            "content": review["content"],
            "score": review["score"]
        }, f)
        f.write("\n")

print("\n Updated reviews_raw.jsonl, Data saved ! \n\n")