const candidates = [
  {
    "candidate_id": "CAND_0061265",
    "rank": 1,
    "score": 0.779124,
    "reasoning": "Recommendation Systems Engineer with 6.6 years of experience. Demonstrates expertise in Qdrant, LangChain, Learning to Rank. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.94 and interview completion rate 0.57 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0079387",
    "rank": 2,
    "score": 0.775131,
    "reasoning": "AI Engineer with 6.9 years of experience. Demonstrates expertise in Recommendation Systems, Sentence Transformers, Vector Search. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.81 and interview completion rate 0.90 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0018722",
    "rank": 3,
    "score": 0.773482,
    "reasoning": "Recommendation Systems Engineer with 6.6 years of experience. Demonstrates expertise in Weaviate, Recommendation Systems, LLMs. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.79 and interview completion rate 0.91 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0071974",
    "rank": 4,
    "score": 0.773174,
    "reasoning": "Senior AI Engineer with 7.8 years of experience. Demonstrates expertise in LoRA, Learning to Rank, Weaviate. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.76 and interview completion rate 0.85 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0002025",
    "rank": 5,
    "score": 0.762659,
    "reasoning": "Senior AI Engineer with 5.9 years of experience. Demonstrates expertise in FAISS, OpenSearch, Haystack. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.80 and interview completion rate 0.81 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0062247",
    "rank": 6,
    "score": 0.758914,
    "reasoning": "AI Engineer with 7.3 years of experience. Demonstrates expertise in Pinecone, Vector Search, Qdrant. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.78 and interview completion rate 0.84 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0093912",
    "rank": 7,
    "score": 0.756102,
    "reasoning": "Senior Data Scientist with 5.3 years of experience. Demonstrates expertise in Milvus, Embeddings, Recommendation Systems. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.66 and interview completion rate 0.96 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0018499",
    "rank": 8,
    "score": 0.75405,
    "reasoning": "Senior Machine Learning Engineer with 7.2 years of experience. Demonstrates expertise in Weaviate, Recommendation Systems, Pinecone. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.61 and interview completion rate 0.80 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0041669",
    "rank": 9,
    "score": 0.750259,
    "reasoning": "Recommendation Systems Engineer with 8.0 years of experience. Demonstrates expertise in FAISS, Milvus, PEFT. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.77 and interview completion rate 0.93 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0028793",
    "rank": 10,
    "score": 0.74976,
    "reasoning": "Search Engineer with 7.2 years of experience. Demonstrates expertise in Embeddings, Haystack, LoRA. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.57 and interview completion rate 0.70 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0065195",
    "rank": 11,
    "score": 0.747963,
    "reasoning": "Search Engineer with 5.1 years of experience. Demonstrates expertise in LLMs, QLoRA, Elasticsearch. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.80 and interview completion rate 0.91 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0074735",
    "rank": 12,
    "score": 0.746273,
    "reasoning": "Applied ML Engineer with 5.5 years of experience. Demonstrates expertise in RAG, Weaviate, Information Retrieval. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.77 and interview completion rate 0.78 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0049538",
    "rank": 13,
    "score": 0.746176,
    "reasoning": "Applied ML Engineer with 5.8 years of experience. Demonstrates expertise in Learning to Rank, OpenSearch, Vector Search. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.72 and interview completion rate 0.67 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0099806",
    "rank": 14,
    "score": 0.739081,
    "reasoning": "AI Engineer with 4.6 years of experience. Demonstrates expertise in LoRA, RAG, FAISS. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.76 and interview completion rate 0.85 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0094056",
    "rank": 15,
    "score": 0.7388,
    "reasoning": "NLP Engineer with 5.9 years of experience. Demonstrates expertise in Pinecone, Milvus, PEFT. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.82 and interview completion rate 0.89 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0083307",
    "rank": 16,
    "score": 0.736624,
    "reasoning": "Search Engineer with 7.8 years of experience. Demonstrates expertise in Embeddings, QLoRA, PEFT. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.70 and interview completion rate 0.83 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0039383",
    "rank": 17,
    "score": 0.736588,
    "reasoning": "Applied ML Engineer with 7.1 years of experience. Demonstrates expertise in FAISS, Recommendation Systems, QLoRA. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.61 and interview completion rate 0.97 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0047721",
    "rank": 18,
    "score": 0.735131,
    "reasoning": "Senior Data Scientist with 7.0 years of experience. Demonstrates expertise in Learning to Rank, Milvus, RAG. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.49 and interview completion rate 0.74 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0005649",
    "rank": 19,
    "score": 0.73429,
    "reasoning": "Senior Data Scientist with 7.4 years of experience. Demonstrates expertise in Haystack, Recommendation Systems, QLoRA. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.57 and interview completion rate 0.88 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0042029",
    "rank": 20,
    "score": 0.731951,
    "reasoning": "Senior Data Scientist with 6.5 years of experience. Demonstrates expertise in RAG, Haystack, Elasticsearch. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.67 and interview completion rate 0.74 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0069905",
    "rank": 21,
    "score": 0.731826,
    "reasoning": "Applied ML Engineer with 6.6 years of experience. Demonstrates expertise in LoRA, Recommendation Systems, Sentence Transformers. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.78 and interview completion rate 0.93 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0014440",
    "rank": 22,
    "score": 0.731643,
    "reasoning": "Recommendation Systems Engineer with 6.4 years of experience. Demonstrates expertise in Elasticsearch, Milvus, FAISS. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.64 and interview completion rate 0.84 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0054123",
    "rank": 23,
    "score": 0.730265,
    "reasoning": "Applied ML Engineer with 4.7 years of experience. Demonstrates expertise in LangChain, Weaviate, Qdrant. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.87 and interview completion rate 0.71 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0020708",
    "rank": 24,
    "score": 0.729884,
    "reasoning": "Search Engineer with 4.2 years of experience. Demonstrates expertise in Learning to Rank, Elasticsearch, LangChain. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.84 and interview completion rate 0.88 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0064326",
    "rank": 25,
    "score": 0.728254,
    "reasoning": "Search Engineer with 7.6 years of experience. Demonstrates expertise in Milvus, Weaviate, RAG. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.94 and interview completion rate 0.90 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0017960",
    "rank": 26,
    "score": 0.728202,
    "reasoning": "Recommendation Systems Engineer with 7.7 years of experience. Demonstrates expertise in QLoRA, Haystack, Qdrant. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.72 and interview completion rate 0.64 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0052328",
    "rank": 27,
    "score": 0.724251,
    "reasoning": "Recommendation Systems Engineer with 6.5 years of experience. Demonstrates expertise in LoRA, OpenSearch, QLoRA. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.79 and interview completion rate 0.95 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0044855",
    "rank": 28,
    "score": 0.722806,
    "reasoning": "Senior Data Scientist with 6.6 years of experience. Demonstrates expertise in Learning to Rank, OpenSearch, Information Retrieval. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.57 and interview completion rate 0.90 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0046064",
    "rank": 29,
    "score": 0.720755,
    "reasoning": "Senior NLP Engineer with 8.9 years of experience. Demonstrates expertise in Pinecone, Haystack, OpenSearch. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.78 and interview completion rate 0.80 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0011687",
    "rank": 30,
    "score": 0.720099,
    "reasoning": "Senior NLP Engineer with 7.8 years of experience. Demonstrates expertise in OpenSearch, FAISS, PEFT. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.89 and interview completion rate 0.77 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0020877",
    "rank": 31,
    "score": 0.719954,
    "reasoning": "Applied ML Engineer with 5.1 years of experience. Demonstrates expertise in QLoRA, Elasticsearch, OpenSearch. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.66 and interview completion rate 0.75 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0098846",
    "rank": 32,
    "score": 0.71934,
    "reasoning": "AI Engineer with 7.6 years of experience. Demonstrates expertise in PEFT, QLoRA, Qdrant. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.62 and interview completion rate 0.80 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0053591",
    "rank": 33,
    "score": 0.717896,
    "reasoning": "AI Engineer with 5.3 years of experience. Demonstrates expertise in LangChain, Embeddings, Milvus. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.81 and interview completion rate 0.97 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0030031",
    "rank": 34,
    "score": 0.717736,
    "reasoning": "AI Engineer with 5.7 years of experience. Demonstrates expertise in Information Retrieval, RAG, LoRA. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.94 and interview completion rate 0.81 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0051615",
    "rank": 35,
    "score": 0.717643,
    "reasoning": "Search Engineer with 4.6 years of experience. Demonstrates expertise in RAG, Milvus, Sentence Transformers. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.88 and interview completion rate 0.89 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0066999",
    "rank": 36,
    "score": 0.717108,
    "reasoning": "Recommendation Systems Engineer with 5.9 years of experience. Demonstrates expertise in OpenSearch, FAISS, LLMs. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.63 and interview completion rate 0.61 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0044883",
    "rank": 37,
    "score": 0.713452,
    "reasoning": "AI Engineer with 6.3 years of experience. Demonstrates expertise in Embeddings, QLoRA, CNN. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.84 and interview completion rate 0.77 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0050876",
    "rank": 38,
    "score": 0.713203,
    "reasoning": "Applied ML Engineer with 6.0 years of experience. Demonstrates expertise in Qdrant, FAISS, OpenSearch. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.67 and interview completion rate 0.97 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0007009",
    "rank": 39,
    "score": 0.710741,
    "reasoning": "Recommendation Systems Engineer with 7.9 years of experience. Demonstrates expertise in Weaviate, Embeddings, Learning to Rank. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.62 and interview completion rate 0.87 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0039754",
    "rank": 40,
    "score": 0.709109,
    "reasoning": "Senior Applied Scientist with 16.2 years of experience. Demonstrates expertise in Qdrant, OpenSearch, LLMs. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.81 and interview completion rate 0.98 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0061339",
    "rank": 41,
    "score": 0.708379,
    "reasoning": "Search Engineer with 4.2 years of experience. Demonstrates expertise in Information Retrieval, Milvus, Vector Search. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.90 and interview completion rate 0.65 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0044222",
    "rank": 42,
    "score": 0.707708,
    "reasoning": "AI Engineer with 7.7 years of experience. Demonstrates expertise in Vector Search, OpenSearch, Qdrant. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.60 and interview completion rate 0.89 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0076163",
    "rank": 43,
    "score": 0.706919,
    "reasoning": "NLP Engineer with 6.9 years of experience. Demonstrates expertise in Weaviate, LangChain, Sentence Transformers. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.84 and interview completion rate 0.72 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0006418",
    "rank": 44,
    "score": 0.706351,
    "reasoning": "Machine Learning Engineer with 5.7 years of experience. Demonstrates expertise in Embeddings, Weaviate, Elasticsearch. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.92 and interview completion rate 0.89 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0018549",
    "rank": 45,
    "score": 0.704968,
    "reasoning": "Recommendation Systems Engineer with 6.8 years of experience. Demonstrates expertise in Weaviate, Elasticsearch, LangChain. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.73 and interview completion rate 0.67 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0006567",
    "rank": 46,
    "score": 0.703376,
    "reasoning": "Senior AI Engineer with 7.9 years of experience. Demonstrates expertise in Haystack, Recommendation Systems, Speech Recognition. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.79 and interview completion rate 0.93 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0078042",
    "rank": 47,
    "score": 0.70304,
    "reasoning": "Applied ML Engineer with 4.7 years of experience. Demonstrates expertise in OpenSearch, Sentence Transformers, Pinecone. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.91 and interview completion rate 0.92 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0079064",
    "rank": 48,
    "score": 0.701715,
    "reasoning": "Senior Data Scientist with 5.2 years of experience. Demonstrates expertise in OpenSearch, Pinecone, QLoRA. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.91 and interview completion rate 0.93 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0070398",
    "rank": 49,
    "score": 0.701178,
    "reasoning": "Machine Learning Engineer with 7.2 years of experience. Demonstrates expertise in RAG, FAISS, Embeddings. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.60 and interview completion rate 0.64 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0088025",
    "rank": 50,
    "score": 0.701094,
    "reasoning": "Staff Machine Learning Engineer with 8.6 years of experience. Demonstrates expertise in Pinecone, QLoRA, LLMs. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.83 and interview completion rate 0.95 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0011162",
    "rank": 51,
    "score": 0.700776,
    "reasoning": "Recommendation Systems Engineer with 5.8 years of experience. Demonstrates expertise in FAISS, Vector Search, LangChain. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.75 and interview completion rate 0.66 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0035879",
    "rank": 52,
    "score": 0.699386,
    "reasoning": "AI Research Engineer with 4.5 years of experience. Demonstrates expertise in Pinecone, Elasticsearch, CI/CD. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.82 and interview completion rate 0.65 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0043228",
    "rank": 53,
    "score": 0.699285,
    "reasoning": "Applied ML Engineer with 6.8 years of experience. Demonstrates expertise in Haystack, Vector Search, Sentence Transformers. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.41 and interview completion rate 0.94 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0081686",
    "rank": 54,
    "score": 0.698512,
    "reasoning": "Search Engineer with 6.0 years of experience. Demonstrates expertise in Embeddings, FAISS, Milvus. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.91 and interview completion rate 0.86 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0081852",
    "rank": 55,
    "score": 0.698486,
    "reasoning": "Senior Data Scientist with 5.9 years of experience. Demonstrates expertise in Milvus, Weaviate, Haystack. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.44 and interview completion rate 0.77 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0055992",
    "rank": 56,
    "score": 0.698409,
    "reasoning": "AI Engineer with 16.9 years of experience. Demonstrates expertise in Information Retrieval, FAISS, RAG. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.72 and interview completion rate 0.91 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0075249",
    "rank": 57,
    "score": 0.697708,
    "reasoning": "Applied ML Engineer with 6.2 years of experience. Demonstrates expertise in Sentence Transformers, Milvus, Pinecone. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.82 and interview completion rate 0.63 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0036437",
    "rank": 58,
    "score": 0.696006,
    "reasoning": "Search Engineer with 4.8 years of experience. Demonstrates expertise in OpenSearch, Elasticsearch, Sentence Transformers. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.87 and interview completion rate 0.90 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0077337",
    "rank": 59,
    "score": 0.695925,
    "reasoning": "Staff Machine Learning Engineer with 7.0 years of experience. Demonstrates expertise in QLoRA, Pinecone, Information Retrieval. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.95 and interview completion rate 0.73 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0042506",
    "rank": 60,
    "score": 0.693696,
    "reasoning": "Search Engineer with 4.2 years of experience. Demonstrates expertise in PEFT, Information Retrieval, Milvus. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.48 and interview completion rate 0.82 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0041610",
    "rank": 61,
    "score": 0.693593,
    "reasoning": "Recommendation Systems Engineer with 6.7 years of experience. Demonstrates expertise in LoRA, Elasticsearch, OpenSearch. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.52 and interview completion rate 0.80 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0052682",
    "rank": 62,
    "score": 0.692034,
    "reasoning": "NLP Engineer with 6.6 years of experience. Demonstrates expertise in QLoRA, FAISS, LLMs. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.88 and interview completion rate 0.88 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0082489",
    "rank": 63,
    "score": 0.690637,
    "reasoning": "ML Engineer with 5.3 years of experience. Demonstrates expertise in Haystack, Weaviate, PEFT. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.71 and interview completion rate 0.91 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0091534",
    "rank": 64,
    "score": 0.690586,
    "reasoning": "AI Engineer with 16.6 years of experience. Demonstrates expertise in Qdrant, Sentence Transformers, RAG. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.84 and interview completion rate 0.81 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0000031",
    "rank": 65,
    "score": 0.690143,
    "reasoning": "Recommendation Systems Engineer with 6.0 years of experience. Demonstrates expertise in FAISS, Pinecone, Embeddings. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.91 and interview completion rate 0.60 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0005538",
    "rank": 66,
    "score": 0.689862,
    "reasoning": "Senior AI Engineer with 5.9 years of experience. Demonstrates expertise in QLoRA, LoRA, Haystack. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.81 and interview completion rate 0.76 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0036184",
    "rank": 67,
    "score": 0.688779,
    "reasoning": "Recommendation Systems Engineer with 6.0 years of experience. Demonstrates expertise in QLoRA, FAISS, LangChain. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.90 and interview completion rate 0.62 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0084819",
    "rank": 68,
    "score": 0.688092,
    "reasoning": "Search Engineer with 4.5 years of experience. Demonstrates expertise in OpenSearch, Recommendation Systems, Weaviate. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.74 and interview completion rate 0.82 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0051630",
    "rank": 69,
    "score": 0.687359,
    "reasoning": "Machine Learning Engineer with 6.0 years of experience. Demonstrates expertise in Elasticsearch, Embeddings, Recommendation Systems. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.51 and interview completion rate 0.72 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0058146",
    "rank": 70,
    "score": 0.687295,
    "reasoning": "AI Research Engineer with 5.1 years of experience. Demonstrates expertise in Information Retrieval, LLMs, Recommendation Systems. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.79 and interview completion rate 0.95 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0092706",
    "rank": 71,
    "score": 0.686596,
    "reasoning": "AI Research Engineer with 5.8 years of experience. Demonstrates expertise in Sentence Transformers, Weights & Biases, Speech Recognition. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.78 and interview completion rate 0.76 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0081846",
    "rank": 72,
    "score": 0.686487,
    "reasoning": "Lead AI Engineer with 6.7 years of experience. Demonstrates expertise in Information Retrieval, Learning to Rank, Elasticsearch. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.73 and interview completion rate 0.94 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0030827",
    "rank": 73,
    "score": 0.685694,
    "reasoning": "Senior Data Scientist with 5.4 years of experience. Demonstrates expertise in Recommendation Systems, FAISS, Qdrant. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.52 and interview completion rate 0.61 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0030953",
    "rank": 74,
    "score": 0.685478,
    "reasoning": "Search Engineer with 7.8 years of experience. Demonstrates expertise in Learning to Rank, Qdrant, Weaviate. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.63 and interview completion rate 0.62 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0044890",
    "rank": 75,
    "score": 0.6849,
    "reasoning": "AI Research Engineer with 5.0 years of experience. Demonstrates expertise in FAISS, LLMs, Haystack. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.79 and interview completion rate 0.68 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0029367",
    "rank": 76,
    "score": 0.684548,
    "reasoning": "Senior Data Scientist with 5.7 years of experience. Demonstrates expertise in Haystack, QLoRA, FAISS. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.77 and interview completion rate 0.58 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0074225",
    "rank": 77,
    "score": 0.683889,
    "reasoning": "Machine Learning Engineer with 4.3 years of experience. Demonstrates expertise in Recommendation Systems, Elasticsearch, Milvus. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.91 and interview completion rate 0.80 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0075574",
    "rank": 78,
    "score": 0.683221,
    "reasoning": "Machine Learning Engineer with 5.7 years of experience. Demonstrates expertise in Weaviate, Recommendation Systems, OpenSearch. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.58 and interview completion rate 0.96 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0061175",
    "rank": 79,
    "score": 0.682054,
    "reasoning": "AI Research Engineer with 6.7 years of experience. Demonstrates expertise in Milvus, Recommendation Systems, Vector Search. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.48 and interview completion rate 0.66 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0008425",
    "rank": 80,
    "score": 0.681128,
    "reasoning": "Senior NLP Engineer with 7.8 years of experience. Demonstrates expertise in Learning to Rank, Qdrant, Sentence Transformers. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.66 and interview completion rate 0.77 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0096172",
    "rank": 81,
    "score": 0.681001,
    "reasoning": "NLP Engineer with 5.2 years of experience. Demonstrates expertise in OpenSearch, Haystack, Elasticsearch. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.47 and interview completion rate 0.70 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0000981",
    "rank": 82,
    "score": 0.678947,
    "reasoning": "ML Engineer with 6.4 years of experience. Demonstrates expertise in Pinecone, OpenSearch, Semantic Search. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.55 and interview completion rate 0.92 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0090155",
    "rank": 83,
    "score": 0.678625,
    "reasoning": "ML Engineer with 5.8 years of experience. Demonstrates expertise in Milvus, Qdrant, Pinecone. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.64 and interview completion rate 0.88 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0075439",
    "rank": 84,
    "score": 0.678449,
    "reasoning": "Machine Learning Engineer with 4.3 years of experience. Demonstrates expertise in Learning to Rank, LoRA, Elasticsearch. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.56 and interview completion rate 0.83 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0040887",
    "rank": 85,
    "score": 0.678302,
    "reasoning": "Machine Learning Engineer with 4.7 years of experience. Demonstrates expertise in FAISS, LoRA, LangChain. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.84 and interview completion rate 0.80 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0051292",
    "rank": 86,
    "score": 0.678297,
    "reasoning": "Applied ML Engineer with 5.2 years of experience. Demonstrates expertise in FAISS, LLMs, Vector Search. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.52 and interview completion rate 0.56 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0057701",
    "rank": 87,
    "score": 0.678231,
    "reasoning": "Recommendation Systems Engineer with 4.1 years of experience. Demonstrates expertise in OpenSearch, Qdrant, PEFT. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.56 and interview completion rate 0.61 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0024620",
    "rank": 88,
    "score": 0.677877,
    "reasoning": "AI Engineer with 5.9 years of experience. Demonstrates expertise in Information Retrieval, PEFT, Recommendation Systems. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.41 and interview completion rate 0.98 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0053695",
    "rank": 89,
    "score": 0.677769,
    "reasoning": "Recommendation Systems Engineer with 5.8 years of experience. Demonstrates expertise in Pinecone, LangChain, Recommendation Systems. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.60 and interview completion rate 0.55 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0008295",
    "rank": 90,
    "score": 0.676973,
    "reasoning": "AI Research Engineer with 6.5 years of experience. Demonstrates expertise in PEFT, Weaviate, QLoRA. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.89 and interview completion rate 0.90 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0026532",
    "rank": 91,
    "score": 0.676927,
    "reasoning": "Recommendation Systems Engineer with 4.8 years of experience. Demonstrates expertise in LoRA, PEFT, Embeddings. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.52 and interview completion rate 0.72 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0096142",
    "rank": 92,
    "score": 0.676663,
    "reasoning": "Applied ML Engineer with 5.0 years of experience. Demonstrates expertise in LoRA, Weaviate, Pinecone. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.84 and interview completion rate 0.55 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0015528",
    "rank": 93,
    "score": 0.676477,
    "reasoning": "Applied ML Engineer with 7.4 years of experience. Demonstrates expertise in Weaviate, LangChain, Information Retrieval. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.53 and interview completion rate 0.72 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0007411",
    "rank": 94,
    "score": 0.675237,
    "reasoning": "Senior Machine Learning Engineer with 8.0 years of experience. Demonstrates expertise in OpenSearch, Vector Search, Information Retrieval. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.12 and interview completion rate 0.80 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0012957",
    "rank": 95,
    "score": 0.674725,
    "reasoning": "Search Engineer with 4.9 years of experience. Demonstrates expertise in RAG, PEFT, LangChain. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.67 and interview completion rate 0.94 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0081053",
    "rank": 96,
    "score": 0.674111,
    "reasoning": "NLP Engineer with 5.4 years of experience. Demonstrates expertise in LoRA, QLoRA, Qdrant. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.83 and interview completion rate 0.79 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0086022",
    "rank": 97,
    "score": 0.673203,
    "reasoning": "Senior Applied Scientist with 5.3 years of experience. Demonstrates expertise in Vector Search, Recommendation Systems, Elasticsearch. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.55 and interview completion rate 0.68 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0030468",
    "rank": 98,
    "score": 0.673068,
    "reasoning": "Senior Applied Scientist with 5.4 years of experience. Demonstrates expertise in OpenSearch, Milvus, Recommendation Systems. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.78 and interview completion rate 0.82 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0010603",
    "rank": 99,
    "score": 0.672822,
    "reasoning": "ML Engineer with 5.3 years of experience. Demonstrates expertise in Information Retrieval, OpenSearch, PEFT. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.94 and interview completion rate 0.64 indicate strong hiring readiness."
  },
  {
    "candidate_id": "CAND_0046525",
    "rank": 100,
    "score": 0.671492,
    "reasoning": "Senior Machine Learning Engineer with 6.1 years of experience. Demonstrates expertise in Elasticsearch, LangChain, Information Retrieval. Strong match for the JD's focus on embeddings, retrieval, ranking and vector search systems. Recruiter response rate 0.88 and interview completion rate 0.81 indicate strong hiring readiness."
  }
];