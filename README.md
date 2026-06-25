# AI Recruiter System

## Redrob AI Recruiter Challenge Submission

This project is a hybrid AI-powered recruiting system designed to identify, evaluate, and rank the most relevant candidates for highly specialized roles at scale.

Unlike traditional ATS systems that rely heavily on keyword matching, the system combines semantic understanding, behavioral intelligence, experience validation, and explainable ranking to surface the strongest candidates from a pool of 100,000 profiles.

---

# Problem Statement

The challenge requires building an AI recruiter capable of:

* Deep Job Understanding
* Contextual Candidate Matching
* Behavioral Signal Integration
* Intelligent Candidate Ranking
* Explainable Recommendations

The goal is not simply filtering resumes but producing a highly relevant ranked shortlist that mirrors expert recruiter decision-making.

---

# Solution Overview

The system uses a multi-stage retrieval and ranking architecture.

```text
Job Description
       │
       ▼
Semantic Embedding Generation
(Sentence Transformers)
       │
       ▼
FAISS Vector Retrieval
(100,000 Candidates)
       │
       ▼
Top Candidate Pool
       │
       ▼
Feature Extraction
       │
       ├── Semantic Relevance
       ├── Experience Alignment
       ├── Skill Alignment
       ├── Retrieval Expertise
       ├── Ranking Expertise
       ├── Behavioral Signals
       └── Profile Consistency
       │
       ▼
Cross-Encoder Re-ranking
       │
       ▼
Hybrid Ensemble Ranking
       │
       ▼
Top 100 Ranked Candidates
       │
       ▼
Explainable Recommendations
```

---

# Key Innovations

## Semantic Candidate Understanding

Traditional ATS systems search for exact keywords.

This system converts both the Job Description and candidate profiles into dense vector representations using Sentence Transformers.

This allows identification of:

* Similar concepts
* Related expertise
* Transferable experience

even when exact keywords do not match.

---

## Large Scale Candidate Retrieval

A FAISS vector index enables fast similarity search across 100,000 candidate profiles.

Benefits:

* Millisecond retrieval
* Semantic search
* Scalable architecture

---

## Hybrid Ranking Engine

Final ranking is based on multiple signals rather than a single similarity score.

### Semantic Signals

* Embeddings
* Retrieval expertise
* Ranking expertise
* Vector database experience
* LLM ecosystem experience

### Experience Signals

* Current role relevance
* Career progression
* Years of experience

### Behavioral Signals

* GitHub activity
* Recruiter response rate
* Interview completion rate
* Open-to-work status
* Recruiter saves

### Quality Signals

* Profile consistency
* Experience-skill alignment
* Keyword stuffing detection
* Honeypot detection

---

## Explainable AI

Every recommendation includes a human-readable explanation.

Example:

> Recommendation Systems Engineer with 6.6 years of experience. Demonstrates expertise in Qdrant, Learning to Rank and LangChain. Strong match for production retrieval and ranking systems. Recruiter response rate 0.94 and interview completion rate 0.57 indicate strong hiring readiness.

---

# Competition Features

* Semantic Candidate Retrieval using Sentence Transformers
* FAISS Vector Search over 100,000 profiles
* Multi-Dimensional Candidate Scoring
* Cross-Encoder Re-ranking
* Behavioral Signal Analysis
* Experience Quality Assessment
* Honeypot Candidate Detection
* Explainable AI Recommendations
* Human-Readable Candidate Reasoning

---

# Challenges Addressed

* Keyword Stuffing
* Fake Expertise Signals
* Role Mismatch Detection
* Large Scale Candidate Retrieval
* Recruiter Explainability
* Candidate Quality Validation

---

# Technical Stack

## Retrieval

* Sentence Transformers
* all-MiniLM-L6-v2
* FAISS

## Processing

* Python
* NumPy
* Pandas

## Ranking

* Enhanced Candidate Scorer
* Cross-Encoder Re-ranker
* Ensemble Ranking Engine

## Visualization

* HTML
* CSS
* JavaScript

---

# Methodology

## Stage 1 — Job Description Understanding

Analyzed:

* Required skills
* Preferred skills
* Experience expectations
* Culture indicators
* Domain-specific requirements

## Stage 2 — Semantic Retrieval

Generated embeddings for candidate profiles.

Built a FAISS vector index.

Retrieved top semantic matches for the target role.

## Stage 3 — Feature Engineering

Extracted:

* Semantic similarity
* Retrieval expertise
* Ranking expertise
* Vector database expertise
* Experience relevance
* Behavioral indicators
* Profile quality signals

## Stage 4 — Cross-Encoder Re-ranking

Applied deep semantic comparison between:

* Job Description
* Candidate Profile

to improve relevance ordering.

## Stage 5 — Ensemble Ranking

Combined:

* Initial Retrieval Score
* Cross-Encoder Score
* Skill Match Score
* Behavioral Signals
* Experience Quality

into a final ranking score.

## Stage 6 — Explainable Output

Generated:

* Ranked candidate list
* Individual reasoning
* Human-readable recommendations

---

# Repository Structure

```text
redrob-ai-recruiter/

├── ai_recruiter.py
├── ultimate_ranker.py
├── enhanced_scorer.py
├── cross_encoder_rerank.py
├── ensemble_ranker.py
├── jd_parser.py
├── run_ultimate.py
├── validate_submission.py

├── outputs/
│   └── final_submission.csv

├── README.md
├── requirements.txt
├── submission_metadata.yaml
├── index.html
├── style.css
└── script.js
```

---

# Running the Project

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Execute Ranking Pipeline

```bash
python run_ultimate.py --jd job_description.txt
```

## Validate Submission

```bash
python validate_submission.py outputs/final_submission.csv
```

## Generated Output

```text
outputs/final_submission.csv
```

Contains:

* Candidate ID
* Rank
* Final Score
* Explainable Reasoning

---
# Pre-computation

The ranking system uses pre-computed candidate embeddings and a FAISS index to enable efficient semantic retrieval.

These artifacts are generated once before ranking and are reused during inference.

To regenerate the artifacts from the original challenge dataset:

```bash
python src/embed_candidates.py
python src/build_faiss_index.py
```

The online ranking step does **not** rebuild embeddings or indexes.

To generate the final submission:

```bash
python run_ultimate.py --jd job_description.txt
```

The ranking pipeline loads the pre-computed artifacts and produces the final ranked CSV within the competition's CPU-only execution constraints.


# Results

The system successfully:

* Processes 100,000 candidates
* Performs semantic retrieval using embeddings
* Applies cross-encoder re-ranking
* Integrates behavioral signals
* Produces explainable recommendations
* Generates a ranked Top-100 shortlist

---

# Dataset

The dataset was provided as part of the Redrob AI Recruiter Challenge.

Due to repository size constraints, the dataset is not included.

---

# Author

Justin George

B.Tech Computer Science Engineering (Artificial Intelligence)

Mar Baselios Christian College of Engineering and Technology

Redrob AI Recruiter Challenge Submission 2026
