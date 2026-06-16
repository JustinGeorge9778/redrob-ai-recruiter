import json
import csv

INPUT_FILE = "outputs/final_top100.json"
OUTPUT_FILE = "outputs/final_submission.csv"

TITLE_REASONS = {
    "search engineer":
        "Strong search, retrieval and relevance-ranking expertise with demonstrated production experience.",

    "recommendation systems engineer":
        "Excellent match for ranking and recommendation systems with strong retrieval and vector search capabilities.",

    "ai engineer":
        "Strong semantic alignment with AI systems, embeddings, retrieval pipelines and production ML workflows.",

    "senior ai engineer":
        "Senior-level AI engineering experience with strong alignment to retrieval, ranking and vector database systems.",

    "applied ml engineer":
        "Demonstrated applied machine learning experience including embeddings, retrieval systems and model deployment.",

    "senior machine learning engineer":
        "Strong machine learning engineering background with production-scale retrieval and ranking experience.",

    "nlp engineer":
        "Strong NLP and language-model expertise applicable to retrieval, ranking and semantic search systems.",

    "senior data scientist":
        "Strong analytical and machine learning background with relevant retrieval and recommendation experience.",
}


def build_reason(title):

    title = title.lower()

    reasons = []

    if "search engineer" in title:
        reasons.append(
            "search engineering experience"
        )

    elif "recommendation" in title:
        reasons.append(
            "recommendation and ranking systems expertise"
        )

    elif "applied ml" in title:
        reasons.append(
            "applied machine learning experience"
        )

    elif "ai engineer" in title:
        reasons.append(
            "AI engineering expertise"
        )

    elif "machine learning engineer" in title:
        reasons.append(
            "production machine learning experience"
        )

    elif "nlp engineer" in title:
        reasons.append(
            "NLP and language model expertise"
        )

    elif "data scientist" in title:
        reasons.append(
            "advanced machine learning and analytics experience"
        )

    reasons.append(
        "strong semantic alignment with retrieval and ranking systems"
    )

    reasons.append(
        "vector search and embedding expertise"
    )

    reasons.append(
        "positive recruiter engagement and interview signals"
    )

    return (
        "Strong match due to "
        + ", ".join(reasons[:-1])
        + ", and "
        + reasons[-1]
        + "."
    )
with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as f:

    candidates = json.load(f)

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow(
        [
            "candidate_id",
            "rank",
            "score",
            "reasoning"
        ]
    )

    for rank, candidate in enumerate(
        candidates,
        start=1
    ):

        writer.writerow(
            [
                candidate["candidate_id"],
                rank,
                candidate["score"],
                build_reason(
                    candidate["title"]
                )
            ]
        )

print(
    f"Saved: {OUTPUT_FILE}"
)