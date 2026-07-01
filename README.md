# Intelligent Candidate Discovery & Ranking System

**Redrob Hackathon 2026**

---

# Project Overview

This project was developed for the **Redrob Intelligent Candidate Discovery & Ranking Challenge**.

The goal was to identify and rank the **Top 100 candidates** from a dataset of **over 100,000 candidate profiles** for the **"Senior AI Engineer"** role.

Instead of relying only on keyword matching, this solution combines semantic similarity, behavioural hiring signals, profile information, technical skills, and career history to identify candidates who best match the job requirements.

The final output is an explainable ranked shortlist where every recommended candidate includes a score along with reasoning explaining why they were selected.

---

# Solution Approach

The ranking engine follows a hybrid multi-stage scoring pipeline.

## 1. Semantic Job Matching (TF-IDF)

The complete Job Description is converted into a TF-IDF representation.

Each candidate's career history and professional summary are also converted into TF-IDF vectors.

Cosine Similarity is then used to measure semantic similarity between the Job Description and every candidate profile.

This enables the system to capture contextual relevance beyond simple keyword matching.

---

## 2. Experience Scoring

Candidates whose years of experience closely match the preferred range described in the Job Description receive higher scores.

Profiles with significantly lower or higher experience receive lower scores.

---

## 3. Title Scoring

Current job titles are evaluated against AI, Machine Learning, NLP, Search, Recommendation, and Retrieval-related engineering roles.

Examples include:

- Senior AI Engineer
- Machine Learning Engineer
- NLP Engineer
- Applied Scientist
- Recommendation Systems Engineer
- Search Engineer

Unrelated roles receive penalties.

---

## 4. Skill Scoring

Relevant technical skills contribute positively to the final score.

Skills considered include:

- Python
- Information Retrieval
- BM25
- Elasticsearch
- OpenSearch
- FAISS
- Pinecone
- Milvus
- Qdrant
- Weaviate
- Recommendation Systems
- Learning to Rank
- Semantic Search
- Vector Search
- Embeddings
- LangChain
- LlamaIndex
- RAG
- LoRA
- QLoRA
- PEFT
- Kubeflow
- MLflow

---

## 5. Behavioural Signal Analysis

Behavioural hiring signals help estimate candidate availability and hiring readiness.

Signals considered include:

- Open to Work
- Recruiter Response Rate
- GitHub Activity
- Interview Completion Rate
- Notice Period

These signals are combined with profile information to improve ranking quality.

---

## 6. Career History Analysis

Instead of relying only on listed skills, the system analyses career history to identify practical production experience in:

- Retrieval Systems
- Recommendation Systems
- Ranking Systems
- Semantic Search
- Vector Search Infrastructure
- Production AI Deployments
- Evaluation Pipelines

This helps identify candidates with real-world experience beyond keyword matching.

---

## 7. Retrieval Depth Score

Candidates demonstrating stronger experience across retrieval, ranking, recommendation systems, evaluation metrics, and vector databases receive additional credit.

This component closely aligns the ranking process with the expectations described in the Job Description.

---

## 8. Profile Consistency Check

Reported years of experience are compared with accumulated career history.

Large inconsistencies between profile information and work history receive penalties.

---

# Final Ranking

Each candidate receives a final score by combining:

- TF-IDF Semantic Similarity
- Experience Score
- Title Score
- Skill Score
- Behavioural Signal Score
- Retrieval Depth Score
- Career History Analysis
- Profile Consistency Check

Candidates are then sorted by their final score, and the **Top 100** candidates are selected.

---

# Explainable Ranking

For every shortlisted candidate, the system generates human-readable reasoning including:

- Years of Experience
- Core Technical Skills
- Behavioural Signals
- Retrieval & Ranking Experience
- Production Search Experience
- Location Information (when applicable)

This allows recruiters to understand why a candidate was recommended rather than only seeing a score.

---

# Output

The system generates:

- `submission.csv`

Each row contains:

- Candidate ID
- Rank
- Final Score
- Human-readable Reasoning

---

# Technologies Used

- Python
- scikit-learn
- TF-IDF Vectorization
- Cosine Similarity
- CSV
- JSON

---

# Project Structure

```text
.
├── rank.py
├── submission.csv
├── validate_submission.py
├── candidate_schema.json
├── sample_candidates.json
├── submission_metadata_template.yaml
├── README.md
├── inspect_top10.py
├── job_description.docx
├── redrob_signals_doc.docx
├── submission_spec.docx
└── candidates.jsonl

```

# Dataset

The `candidates.jsonl` dataset is provided by the hackathon organizers and is not included in this GitHub repository due to GitHub's file size limitations.
---

# Running the Project

Generate the ranked submission:

```bash
python rank.py
```

Validate the generated submission:

```bash
python validate_submission.py submission.csv
```

---

# Design Philosophy

Recruiters often review hundreds of profiles for a single role, and simple keyword matching can overlook strong candidates whose experience is described differently from the job description.

This project combines semantic similarity with heuristic scoring to evaluate candidates using multiple signals, including career history, technical skills, behavioural indicators, and retrieval-specific experience.

Rather than depending on a single ranking signal, the system uses multiple independent scoring components to produce an explainable ranking that better reflects overall candidate-job fit.

---

# Validation

The generated `submission.csv` was validated using the official `validate_submission.py` script provided with the challenge dataset.

The output satisfies the required submission format and contains:

- Candidate ID
- Rank
- Score
- Human-readable Reasoning

---

