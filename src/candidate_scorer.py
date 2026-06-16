import json

JD_KEYWORDS = {
    "embeddings": 10,
    "retrieval": 10,
    "ranking": 10,
    "faiss": 9,
    "qdrant": 9,
    "milvus": 9,
    "pinecone": 9,
    "weaviate": 9,
    "vector": 8,
    "sentence-transformers": 8,
    "bge": 8,
    "e5": 8,
    "llm": 6,
    "fine-tuning": 6,
    "lora": 5,
    "qlora": 5,
    "peft": 5,
    "pytorch": 5,
    "tensorflow": 5,
}

RETRIEVAL_TERMS = {
    "retrieval",
    "search",
    "ranking",
    "recommendation",
    "matching",
    "relevance",
    "vector search"
}

VECTOR_DB_TERMS = {
    "faiss",
    "milvus",
    "qdrant",
    "pinecone",
    "weaviate",
    "opensearch",
    "elasticsearch"
}

GOOD_TITLES = {
    "ml engineer": 20,
    "ai engineer": 20,
    "search engineer": 20,
    "recommendation systems engineer": 20,
    "data scientist": 15,
    "data engineer": 15,
    "backend engineer": 15,
    "analytics engineer": 15,
    "senior ai engineer": 25,
    "applied ml engineer": 20,
    "senior machine learning engineer": 25,
    "senior applied scientist": 20,
    "nlp engineer": 20,
}

BAD_TITLES = {
    "accountant": -20,
    "sales executive": -20,
    "hr manager": -20,
    "graphic designer": -20,
    "customer support": -20,
    "civil engineer": -15,
}

PRODUCTION_TERMS = [
    "production",
    "deployed",
    "real users",
    "scale",
    "latency",
    "online",
    "serving",
]

def score_candidate(candidate):

    score = 0

    profile = candidate.get("profile", {})

    title = profile.get(
        "current_title",
        ""
    ).lower()

    years = profile.get(
        "years_of_experience",
        0
    )

    # JD prefers roughly 5-9 years
    if 5 <= years <= 9:
        score += 20

    elif 4 <= years < 5:
        score += 10

    elif 9 < years <= 12:
        score += 8

    else:
        score -= 5

    text_parts = []

    text_parts.append(
        profile.get("headline", "")
    )

    text_parts.append(
        profile.get("summary", "")
    )

    for skill in candidate.get("skills", []):
        text_parts.append(
            skill.get("name", "")
        )

    for role in candidate.get(
        "career_history",
        []
    ):
        text_parts.append(
            role.get("description", "")
        )

    text = " ".join(text_parts).lower()

    # Core JD keywords
    for keyword, weight in JD_KEYWORDS.items():
        if keyword in text:
            score += weight

    # Retrieval bonus
    for term in RETRIEVAL_TERMS:
        if term in text:
            score += 8

    # Vector DB bonus
    for term in VECTOR_DB_TERMS:
        if term in text:
            score += 10

    # Production experience bonus
    for term in PRODUCTION_TERMS:
        if term in text:
            score += 5

    # Title bonus / penalty
    if title in GOOD_TITLES:
        score += GOOD_TITLES[title]

    if title in BAD_TITLES:
        score += BAD_TITLES[title]

    # Suspicion penalty
    ai_skill_count = 0

    for keyword in JD_KEYWORDS:
        if keyword in text:
            ai_skill_count += 1

    if (
        title in BAD_TITLES
        and ai_skill_count >= 4
    ):
        score -= 30

    # Behavioral signals
    signals = candidate.get(
        "redrob_signals",
        {}
    )

    github = signals.get(
        "github_activity_score",
        -1
    )

    if github > 0:
        score += github * 0.5

    response = signals.get(
        "recruiter_response_rate",
        0
    )

    score += response * 20

    interview = signals.get(
        "interview_completion_rate",
        0
    )

    score += interview * 15

    if signals.get(
        "open_to_work_flag",
        False
    ):
        score += 5

    return round(score, 2)