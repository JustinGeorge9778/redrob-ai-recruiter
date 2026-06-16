import json

DATASET = "data/candidates.jsonl"

SUSPICIOUS = []

AI_SKILLS = {
    "llm",
    "pytorch",
    "tensorflow",
    "retrieval",
    "embedding",
    "embeddings",
    "vector",
    "faiss",
    "milvus",
    "qdrant",
    "weaviate",
    "pinecone",
    "nlp",
    "machine learning",
    "deep learning",
    "rag",
    "fine-tuning",
}

NON_AI_TITLES = {
    "accountant",
    "hr manager",
    "sales executive",
    "graphic designer",
    "civil engineer",
    "operations manager",
    "customer support",
}

for line in open(DATASET, "r", encoding="utf-8"):
    candidate = json.loads(line)

    title = (
        candidate.get("profile", {})
        .get("current_title", "")
        .lower()
    )

    skills = [
        s.get("name", "").lower()
        for s in candidate.get("skills", [])
    ]

    ai_skill_count = 0

    for skill in skills:
        for keyword in AI_SKILLS:
            if keyword in skill:
                ai_skill_count += 1

    if title in NON_AI_TITLES and ai_skill_count >= 4:
        SUSPICIOUS.append(
            (
                candidate["candidate_id"],
                title,
                ai_skill_count
            )
        )

print("\nSUSPICIOUS PROFILES")
print(len(SUSPICIOUS))

print("\nFIRST 20")

for item in SUSPICIOUS[:20]:
    print(item)