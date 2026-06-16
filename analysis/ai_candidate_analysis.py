import json
from collections import Counter

DATASET = "data/candidates.jsonl"

AI_KEYWORDS = [
    "machine learning",
    "deep learning",
    "llm",
    "rag",
    "nlp",
    "transformer",
    "embeddings",
    "retrieval",
    "vector",
    "faiss",
    "pinecone",
    "weaviate",
    "qdrant",
    "milvus",
    "langchain",
    "langgraph",
    "fine-tuning",
    "lora",
    "qlora",
    "pytorch",
    "tensorflow",
    "bert",
]

ai_candidates = 0
title_counter = Counter()

with open(DATASET, "r", encoding="utf-8") as f:
    for line in f:
        candidate = json.loads(line)

        text_parts = []

        profile = candidate.get("profile", {})
        text_parts.append(profile.get("headline", ""))
        text_parts.append(profile.get("summary", ""))

        for skill in candidate.get("skills", []):
            text_parts.append(skill.get("name", ""))

        for job in candidate.get("career_history", []):
            text_parts.append(job.get("description", ""))

        full_text = " ".join(text_parts).lower()

        if any(keyword in full_text for keyword in AI_KEYWORDS):
            ai_candidates += 1
            title_counter[profile.get("current_title", "Unknown")] += 1

print("\nAI RELATED CANDIDATES")
print(ai_candidates)

print("\nTOP AI TITLES")
for title, count in title_counter.most_common(20):
    print(f"{title:<30} {count}")