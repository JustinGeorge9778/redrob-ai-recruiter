import faiss
import pickle
import numpy as np

from sentence_transformers import SentenceTransformer

JD_TEXT = """
Senior AI Engineer

Embeddings
Retrieval
Ranking Systems
Vector Databases
Python
Evaluation Frameworks
Hybrid Search
FAISS
Qdrant
Milvus
Pinecone
Weaviate
Production ML Systems
LLM Re-ranking
"""

print("Loading model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Loading index...")

index = faiss.read_index(
    "models/candidate_faiss.index"
)

print("Loading candidate ids...")

with open(
    "models/candidate_ids.pkl",
    "rb"
) as f:
    candidate_ids = pickle.load(f)

print("Encoding JD...")

query_embedding = model.encode(
    [JD_TEXT],
    convert_to_numpy=True
).astype("float32")

faiss.normalize_L2(query_embedding)

TOP_K = 5000

scores, indices = index.search(
    query_embedding,
    TOP_K
)

print("\nTOP 20 SEMANTIC MATCHES\n")

for rank in range(20):

    idx = indices[0][rank]

    print(
        rank + 1,
        candidate_ids[idx],
        round(float(scores[0][rank]), 4)
    )

with open(
    "outputs/top5000_candidates.txt",
    "w",
    encoding="utf-8"
) as f:

    for idx in indices[0]:

        f.write(
            candidate_ids[idx] + "\n"
        )

print("\nSaved:")
print("outputs/top5000_candidates.txt")