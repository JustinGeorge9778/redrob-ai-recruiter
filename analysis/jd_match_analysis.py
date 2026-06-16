import json
from collections import Counter

DATASET = "data/candidates.jsonl"

JD_SKILLS = [
    "embeddings",
    "retrieval",
    "ranking",
    "faiss",
    "pinecone",
    "qdrant",
    "weaviate",
    "milvus",
    "vector",
    "sentence-transformers",
    "bge",
    "e5",
    "llm",
    "fine-tuning",
    "lora",
    "qlora",
    "peft",
    "pytorch",
    "tensorflow",
]

matches = 0
title_counter = Counter()

for line in open(DATASET, "r", encoding="utf-8"):
    candidate = json.loads(line)

    text_parts = []

    profile = candidate.get("profile", {})
    text_parts.append(profile.get("headline", ""))
    text_parts.append(profile.get("summary", ""))

    for skill in candidate.get("skills", []):
        text_parts.append(skill.get("name", ""))

    for role in candidate.get("career_history", []):
        text_parts.append(role.get("description", ""))

    full_text = " ".join(text_parts).lower()

    score = 0

    for skill in JD_SKILLS:
        if skill in full_text:
            score += 1

    if score >= 3:
        matches += 1
        title_counter[
            profile.get("current_title", "Unknown")
        ] += 1

print("\nLIKELY JD MATCHES")
print(matches)

print("\nTOP TITLES")
for title, count in title_counter.most_common(25):
    print(f"{title:<30} {count}")