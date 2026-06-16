import json
import pickle
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

DATASET = "data/candidates.jsonl"

print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

candidate_ids = []
candidate_texts = []

print("Reading candidates...")

with open(
    DATASET,
    "r",
    encoding="utf-8"
) as f:

    for line in tqdm(f):

        candidate = json.loads(line)

        profile = candidate.get(
            "profile",
            {}
        )

        text_parts = []

        text_parts.append(
            profile.get(
                "current_title",
                ""
            )
        )

        text_parts.append(
            profile.get(
                "headline",
                ""
            )
        )

        text_parts.append(
            profile.get(
                "summary",
                ""
            )
        )

        for skill in candidate.get(
            "skills",
            []
        ):
            text_parts.append(
                skill.get(
                    "name",
                    ""
                )
            )

        for job in candidate.get(
            "career_history",
            []
        ):
            text_parts.append(
                job.get(
                    "title",
                    ""
                )
            )

            text_parts.append(
                job.get(
                    "description",
                    ""
                )
            )

        full_text = " ".join(text_parts)

        candidate_ids.append(
            candidate["candidate_id"]
        )

        candidate_texts.append(
            full_text
        )

print("\nGenerating embeddings...")

embeddings = model.encode(
    candidate_texts,
    batch_size=128,
    show_progress_bar=True,
    convert_to_numpy=True
)

print("Embeddings shape:", embeddings.shape)

np.save(
    "models/candidate_embeddings.npy",
    embeddings
)

with open(
    "models/candidate_ids.pkl",
    "wb"
) as f:

    pickle.dump(
        candidate_ids,
        f
    )

print("\nSaved:")
print("models/candidate_embeddings.npy")
print("models/candidate_ids.pkl")