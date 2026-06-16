import re

RETRIEVAL_TERMS = {
    "retrieval",
    "search",
    "ranking",
    "recommendation",
    "information retrieval",
    "learning to rank",
    "relevance",
    "matching",
    "vector search",
}

VECTOR_DB_TERMS = {
    "faiss",
    "milvus",
    "qdrant",
    "pinecone",
    "weaviate",
    "pgvector",
    "elasticsearch",
    "opensearch",
}

GOOD_TITLES = {
    "search engineer",
    "recommendation systems engineer",
    "ml engineer",
    "machine learning engineer",
    "senior machine learning engineer",
    "ai engineer",
    "senior ai engineer",
    "applied ml engineer",
    "nlp engineer",
    "senior nlp engineer",
    "data scientist",
    "senior data scientist",
    "ai research engineer",
    "senior applied scientist",
}

BAD_TITLES = {
    "accountant",
    "hr manager",
    "sales executive",
    "graphic designer",
    "customer support",
    "civil engineer",
}


def normalize(value, min_v, max_v):
    if max_v == min_v:
        return 0.0

    value = max(min(value, max_v), min_v)

    return (value - min_v) / (max_v - min_v)


def build_candidate_text(candidate):

    profile = candidate.get("profile", {})

    parts = [
        profile.get("headline", ""),
        profile.get("summary", ""),
        profile.get("current_title", ""),
    ]

    for skill in candidate.get("skills", []):
        parts.append(skill.get("name", ""))

    for role in candidate.get("career_history", []):
        parts.append(role.get("title", ""))
        parts.append(role.get("description", ""))

    return " ".join(parts).lower()


def retrieval_score(text):

    score = 0

    for term in RETRIEVAL_TERMS:
        if term in text:
            score += 1

    return score


def vector_db_score(text):

    score = 0

    for term in VECTOR_DB_TERMS:
        if term in text:
            score += 1

    return score


def title_score(title):

    title = title.lower()

    if title in GOOD_TITLES:
        return 1.0

    if title in BAD_TITLES:
        return -1.0

    return 0.0


def experience_score(years):

    if 5 <= years <= 9:
        return 1.0

    if 4 <= years < 5:
        return 0.8

    if 9 < years <= 12:
        return 0.7

    if years >= 3:
        return 0.5

    return 0.2


def consistency_score(title, retrieval, vector_db):

    title = title.lower()

    if title in GOOD_TITLES:
        return 1.0

    if (
        title in BAD_TITLES
        and (retrieval >= 3 or vector_db >= 2)
    ):
        return -1.0

    return 0.0


def behavioral_score(signals):

    github = signals.get(
        "github_activity_score",
        0
    )

    response = signals.get(
        "recruiter_response_rate",
        0
    )

    interview = signals.get(
        "interview_completion_rate",
        0
    )

    score = (
        github * 0.4
        + response * 30
        + interview * 30
    )

    return normalize(score, 0, 100)


def extract_features(candidate):

    profile = candidate.get("profile", {})

    text = build_candidate_text(candidate)

    retrieval = retrieval_score(text)

    vector_db = vector_db_score(text)

    years = profile.get(
        "years_of_experience",
        0
    )

    title = profile.get(
        "current_title",
        ""
    )

    behavior = behavioral_score(
        candidate.get(
            "redrob_signals",
            {}
        )
    )

    return {
        "retrieval_score": retrieval,
        "vector_db_score": vector_db,
        "experience_score": experience_score(years),
        "title_score": title_score(title),
        "consistency_score": consistency_score(
            title,
            retrieval,
            vector_db
        ),
        "behavioral_score": behavior,
    }