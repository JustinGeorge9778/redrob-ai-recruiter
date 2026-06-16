import faiss
import numpy as np

print("Loading embeddings...")

embeddings = np.load(
    "models/candidate_embeddings.npy"
).astype("float32")

print("Shape:", embeddings.shape)

faiss.normalize_L2(embeddings)

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

index.add(embeddings)

faiss.write_index(
    index,
    "models/candidate_faiss.index"
)

print("\nSaved:")
print("models/candidate_faiss.index")