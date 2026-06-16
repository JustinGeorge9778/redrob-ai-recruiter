import json
import csv

INPUT_RANKING = "outputs/final_top100.json"
CANDIDATES_FILE = "data/candidates.jsonl"
OUTPUT_FILE = "outputs/final_submission.csv"

candidate_lookup = {}

print("Loading candidates...")

with open(CANDIDATES_FILE, "r", encoding="utf-8") as f:
    for line in f:
        c = json.loads(line)
        candidate_lookup[c["candidate_id"]] = c

print("Loading ranking...")

with open(INPUT_RANKING, "r", encoding="utf-8") as f:
    ranked = json.load(f)


IMPORTANT_SKILLS = {
    "embeddings",
    "vector search",
    "retrieval",
    "ranking",
    "recommendation systems",
    "learning to rank",
    "information retrieval",
    "faiss",
    "qdrant",
    "milvus",
    "pinecone",
    "weaviate",
    "elasticsearch",
    "opensearch",
    "sentence transformers",
    "rag",
    "llms",
    "langchain",
    "haystack",
    "bge",
    "e5",
    "lora",
    "qlora",
    "peft",
}


def build_reason(candidate):

    profile = candidate.get(
        "profile",
        {}
    )

    title = profile.get(
        "current_title",
        "Unknown"
    )

    years = profile.get(
        "years_of_experience",
        0
    )

    priority = []
    other = []

    for skill in candidate.get(
        "skills",
        []
    ):

        name = skill.get(
            "name",
            ""
        )

        if (
            name.lower()
            in IMPORTANT_SKILLS
        ):
            priority.append(name)

        else:
            other.append(name)

    top_skills = priority[:3]

    if len(top_skills) < 3:

        top_skills.extend(
            other[
                : 3 - len(top_skills)
            ]
        )

    signals = candidate.get(
        "redrob_signals",
        {}
    )

    response = signals.get(
        "recruiter_response_rate",
        0
    )

    interview = signals.get(
        "interview_completion_rate",
        0
    )

    return (
        f"{title} with {years} years of experience. "
        f"Demonstrates expertise in {', '.join(top_skills)}. "
        f"Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. "
        f"Recruiter response rate {response:.2f} and interview completion rate {interview:.2f} indicate strong hiring readiness."
    )
    return (
        f"{title} with {years} years of experience. "
        f"Key skills include {', '.join(skills)}. "
        f"Strong alignment with the JD's retrieval, ranking and AI requirements. "
        f"Recruiter response rate: {response:.2f}; "
        f"interview completion rate: {interview:.2f}."
    )


rows = []

for rank, row in enumerate(
    ranked,
    start=1
):

    cid = row["candidate_id"]

    candidate = candidate_lookup[cid]

    rows.append(
        [
            cid,
            rank,
            row["score"],
            build_reason(candidate)
        ]
    )

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow(
        [
            "candidate_id",
            "rank",
            "score",
            "reasoning"
        ]
    )

    writer.writerows(rows)

print(
    f"Saved: {OUTPUT_FILE}"
)