import json
import pickle
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

from feature_extractor import extract_features

# -----------------------------
# CONFIG
# -----------------------------

TOP_K_RETRIEVAL = 10000
TOP_K_FINAL = 100

JD_TEXT = """
Senior AI Engineer

Required Skills:
Embeddings
Retrieval Systems
Search Systems
Ranking Systems
Recommendation Systems
Learning To Rank
Vector Databases
FAISS
Qdrant
Milvus
Pinecone
Weaviate
Sentence Transformers
LLMs
RAG
Production ML Systems
Python
"""

# -----------------------------
# LOAD MODEL
# -----------------------------

print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# -----------------------------
# LOAD FAISS
# -----------------------------

print("Loading FAISS index...")

index = faiss.read_index(
    "models/candidate_faiss.index"
)

print("Loading candidate ids...")

with open(
    "models/candidate_ids.pkl",
    "rb"
) as f:
    candidate_ids = pickle.load(f)

# -----------------------------
# RETRIEVE TOP 5000
# -----------------------------

print("Encoding JD...")

query_embedding = model.encode(
    [JD_TEXT],
    convert_to_numpy=True
).astype("float32")

faiss.normalize_L2(
    query_embedding
)

scores, indices = index.search(
    query_embedding,
    TOP_K_RETRIEVAL
)

semantic_scores = {}

for score, idx in zip(
    scores[0],
    indices[0]
):
    semantic_scores[
        candidate_ids[idx]
    ] = float(score)

candidate_pool = set(
    semantic_scores.keys()
)

print(
    f"Retrieved {len(candidate_pool)} candidates"
)

# -----------------------------
# LOAD CANDIDATES
# -----------------------------

print("Loading candidate data...")

ranked = []

with open(
    "data/candidates.jsonl",
    "r",
    encoding="utf-8"
) as f:

    for line in f:

        candidate = json.loads(line)

        candidate_id = candidate[
            "candidate_id"
        ]

        if candidate_id not in candidate_pool:
            continue

        features = extract_features(
            candidate
        )

        semantic = semantic_scores[
            candidate_id
        ]

        semantic_score = semantic

        behavioral_score = features[
            "behavioral_score"
        ]

        experience_score = features[
            "experience_score"
        ]

        retrieval_score = min(
            features["retrieval_score"] / 8,
            1.0
        )

        vector_score = min(
            features["vector_db_score"] / 8,
            1.0
        )

        title_score = (
            features["title_score"] + 1
        ) / 2

        consistency_score = (
            features["consistency_score"] + 1
        ) / 2

        final_score = (
            semantic_score * 0.45
            + behavioral_score * 0.25
            + experience_score * 0.10
            + retrieval_score * 0.10
            + vector_score * 0.05
            + consistency_score * 0.05
        )

        ranked.append(
            {
                "candidate_id":
                candidate_id,

                "title":
                candidate["profile"][
                    "current_title"
                ],

                "score":
                round(
                    final_score,
                    6
                )
            }
        )

# -----------------------------
# SORT
# -----------------------------

ranked.sort(
    key=lambda x: x["score"],
    reverse=True
)

top100 = ranked[:TOP_K_FINAL]

print("\nTOP 20 FINAL\n")

for row in top100[:20]:

    print(
        row["candidate_id"],
        row["title"],
        row["score"]
    )

# -----------------------------
# SAVE
# -----------------------------

with open(
    "outputs/final_top100.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        top100,
        f,
        indent=2
    )

print(
    "\nSaved outputs/final_top100.json"
)