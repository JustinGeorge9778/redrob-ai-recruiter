import json
import csv
from tqdm import tqdm

from candidate_scorer import score_candidate

DATASET = "data/candidates.jsonl"

results = []

print("Scoring candidates...")

with open(DATASET, "r", encoding="utf-8") as f:

    for line in tqdm(f):

        candidate = json.loads(line)

        score = score_candidate(candidate)

        results.append({
            "candidate_id": candidate["candidate_id"],
            "title": candidate["profile"]["current_title"],
            "score": score
        })

print("Sorting candidates...")

results.sort(
    key=lambda x: x["score"],
    reverse=True
)

TOP_K = 100

top_candidates = results[:TOP_K]

print("\nTOP 20 CANDIDATES\n")

for candidate in top_candidates[:20]:

    print(
        candidate["candidate_id"],
        candidate["title"],
        candidate["score"]
    )

with open(
    "outputs/top100_v1.csv",
    "w",
    newline="",
    encoding="utf-8"
) as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow(
        [
            "candidate_id",
            "rank",
            "score"
        ]
    )

    for rank, candidate in enumerate(
        top_candidates,
        start=1
    ):

        writer.writerow(
            [
                candidate["candidate_id"],
                rank,
                candidate["score"]
            ]
        )

print("\nSaved:")
print("outputs/top100_v1.csv")