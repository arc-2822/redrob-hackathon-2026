
from docx import Document
from pathlib import Path
import json
import csv

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
def contains_any(text, words):
    text = text.lower()

    for word in words:
        if word.lower() in text:
            return True

    return False


def experience_score(profile):

    score = 0

    exp = profile.get("years_of_experience", 0)

    if 5 <= exp <= 9:
        score += 25
    elif 4 <= exp < 5:
        score += 18
    elif 3 <= exp < 4:
        score += 10
    elif 9 < exp <= 12:
        score += 8
    else:
        score += 0
    return score

def title_score(profile):

    score = 0

    title = profile.get("current_title", "").lower()

    preferred = [
        "senior ai engineer",
        "lead ai engineer",
        "staff machine learning engineer",
        "senior machine learning engineer",
        "applied ml engineer",
        "senior applied scientist",
        "applied scientist",
        "senior nlp engineer",
        "search engineer",
        "information retrieval engineer",
        "recommendation systems engineer",
        "ai engineer",
        "ml engineer",
        "machine learning engineer",
        "software engineer",
        "backend engineer",
        "data engineer"
    ]

    avoid = [
        "marketing manager",
        "operations manager",
        "accountant",
        "customer support",
        "sales executive"
    ]

    for t in preferred:
        if t in title:
            score = 20
            break

    for t in avoid:
        if t in title:
            score -= 40
            break

    return score

def skill_score(candidate):

    score = 0

    skills = [
        s["name"].lower()
        for s in candidate.get("skills", [])
    ]

    required = [
        "python",
        "bm25",
        "elasticsearch",
        "opensearch",
        "pinecone",
        "milvus",
        "qdrant",
        "weaviate",
        "faiss",
        "embeddings",
        "sentence-transformers",
        "llamaindex",
        "haystack",
        "pgvector",
        "nlp",
        "mlops",
        "kubeflow",
        "lora",
        "qlora",
        "peft"
    ]

    for skill in required:
        if skill in skills:
            score += 3

    return score

def retrieval_depth_score(career_text):

    score = 0

    retrieval = [
        "retrieval",
        "information retrieval",
        "document retrieval",
        "dense retrieval",
        "hybrid retrieval",
        "semantic retrieval",
        "semantic search",
        "vector search",
        "search engine",
        "search platform",
        "enterprise search",
        "candidate search",
        "job search",
        "query processing",
        "query understanding",
        "search relevance",
        "relevance scoring",
        "vector retrieval",
        "nearest neighbor search",
        "candidate-jd matching",
        "rag"
    ]

    ranking = [
        "ranking",
        "learning-to-rank",
        "reranking",
        "re-ranking",
        "recommendation",
        "recommendation system",
        "recommendation systems"
    ]

    evaluation = [
        "ndcg",
        "mrr",
        "map",
        "recall@k",
        "precision",
        "offline evaluation",
        "online evaluation",
        "a/b",
        "ab test"
    ]

    infrastructure = [
        "faiss",
        "pinecone",
        "milvus",
        "qdrant",
        "weaviate",
        "elasticsearch",
        "opensearch",
        "pgvector"
    ]

    matched_groups = 0

    if contains_any(career_text, retrieval):
        matched_groups += 1

    if contains_any(career_text, ranking):
        matched_groups += 1

    if contains_any(career_text, evaluation):
        matched_groups += 1

    if contains_any(career_text, infrastructure):
        matched_groups += 1

    if matched_groups == 4:
        score += 40
    elif matched_groups == 3:
        score += 25
    elif matched_groups == 2:
        score += 15
    elif matched_groups == 1:
        score += 5

    return score

def score_candidate(candidate):

    score = 0

    profile = candidate["profile"]
    signals = candidate["redrob_signals"]

    # Basic profile scoring
    score += experience_score(profile)
    score += title_score(profile)
    score += skill_score(candidate)

   
    # Behavioural signals

    if signals.get("open_to_work_flag"):
        score += 10
    else:
        score -= 5

    response = signals.get("recruiter_response_rate", 0)

    if response >= 0.7:
        score += 10
    elif response >= 0.4:
        score += 5
    elif response < 0.2:
        score -= 8

    github = signals.get("github_activity_score", 0)

    if github >= 50:
        score += 10
    elif github >= 20:
        score += 5
    elif github < 10:
        score -= 5

    completion = signals.get("interview_completion_rate", 0)

    if completion >= 0.8:
        score += 10
    elif completion >= 0.5:
        score += 5

    notice = signals.get("notice_period_days", 180)

    if notice <= 30:
        score += 10
    elif notice <= 60:
        score += 5
    elif notice > 90:
        score -= 5

    # Build career history text
    career_text = ""

    for job in candidate.get("career_history", []):
        career_text += " "
        career_text += job.get("title", "").lower()
        career_text += " "
        career_text += job.get("description", "").lower()

   
    # Retrieval / Ranking depth
    
    score += retrieval_depth_score(career_text)

    
    # High-value JD terms
   
    high_value_terms = [
        "learning-to-rank",
        "candidate-jd matching",
        "hybrid retrieval",
        "recommendation system",
        "recommendation systems",
        "semantic search",
        "rag",
        "ndcg",
        "mrr",
        "offline evaluation",
        "online evaluation",
        "behavioral signals"
    ]

    medium_value_terms = [
        "bm25",
        "faiss",
        "pinecone",
        "milvus",
        "qdrant",
        "weaviate",
        "opensearch",
        "pgvector",
        "vector search",
        "dense retrieval",
        "embeddings",
        "embedding",
        "sentence-transformers",
        "bge",
        "reranking",
        "re-ranking"
    ]

    general_terms = [
        "search",
        "ranking",
        "retrieval",
        "recommendation",
        "llm",
        "llama",
        "lora",
        "qlora",
        "mlflow",
        "kubeflow",
        "bentoml",
        "feature engineering",
        "ab testing",
        "a/b"
    ]

    production_terms = [
        "production",
        "deployed",
        "shipped",
        "live",
        "real users",
        "millions",
        "scale",
        "latency",
        "p95",
        "ab test",
        "a/b test",
        "offline evaluation",
        "online evaluation",
        "recruiter feedback",
        "monitoring",
        "feature store",
        "experiment tracking"
    ]

    # Keyword scoring
 
    for term in high_value_terms:
        if term in career_text:
            score += 6

    for term in medium_value_terms:
        if term in career_text:
            score += 3

    for term in general_terms:
        if term in career_text:
            score += 1

    for term in production_terms:
        if term in career_text:
            score += 4

    
    # Profile consistency
   
    total_months = 0

    for job in candidate.get("career_history", []):
        total_months += job.get("duration_months", 0)

    profile_years = profile.get("years_of_experience", 0)
    career_years = total_months / 12

    if abs(profile_years - career_years) > 2:
        score -= 20

    return score

# Read the job description
doc = Document("India_runs_data_and_ai_challenge/job_description.docx")
job_description = ""

for para in doc.paragraphs:
    job_description += para.text + "\n"

job_description = job_description.lower()

all_candidates = []
career_texts = []

with open(
    "India_runs_data_and_ai_challenge/candidates.jsonl",
    "r",
    encoding="utf-8"
) as f:

    for line in f:

        candidate = json.loads(line)

        all_candidates.append(candidate)

        career_text = ""

        for job in candidate.get("career_history", []):

            career_text += " "
            career_text += job.get("title", "")
            career_text += " "
            career_text += job.get("description", "")

        career_text += " "
        career_text += candidate["profile"].get("summary", "")

        career_texts.append(career_text)

vectorizer = TfidfVectorizer(
    max_features=3000,
    ngram_range=(1, 1),
    stop_words="english"
    
)

# Use the ACTUAL job description you already loaded
corpus = career_texts + [job_description]

tfidf_matrix = vectorizer.fit_transform(corpus)

jd_vector = tfidf_matrix[-1]
candidate_vectors = tfidf_matrix[:-1]

semantic_scores = cosine_similarity(
    candidate_vectors,
    jd_vector
).flatten()

top_candidates = []

for candidate, semantic_score in zip(all_candidates, semantic_scores):

    score = score_candidate(candidate)

    # Blend semantic similarity with heuristic score
    score += semantic_score * 80
    score = round(score, 2)

    top_candidates.append(
        (
            score,
            candidate
        )
    )

top_candidates.sort(
    key=lambda x: (-x[0], x[1]["candidate_id"])
)


top100 = top_candidates[:100]

output_file = Path(__file__).parent / "submission.csv"

with open(
    output_file,
    "w",
    newline="",
    encoding="utf-8"
) as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "candidate_id",
        "rank",
        "score",
        "reasoning"
    ])

    for rank, item in enumerate(top100, start=1):

        score = item[0]
        candidate = item[1]

        profile = candidate["profile"]
        signals = candidate["redrob_signals"]

        candidate_id = candidate["candidate_id"]

        title = profile.get("current_title", "")

        reason = []

        # Experience
        reason.append(
    f"{title} with {profile.get('years_of_experience',0):.1f} years of experience"
)

        # Top skills
        skills = candidate.get("skills", [])

        important_skills = [
            "python",
            "retrieval",
            "information retrieval",
            "recommendation systems",
            "learning to rank",
            "bm25",
            "elasticsearch",
            "opensearch",
            "faiss",
            "pinecone",
            "milvus",
            "qdrant",
            "weaviate",
            "llamaindex",
            "langchain",
            "rag",
            "vector search",
            "embeddings",
            "nlp",
            "transformers",
            "lora",
            "qlora",
            "peft",
            "mlops",
            "kubeflow",
            "pytorch",
            "tensorflow"
        ]

        selected_skills = []

        # Prefer skills that are highly relevant to the JD
        for keyword in important_skills:
            for skill in skills:
                skill_name = skill["name"]

                if (
                    keyword.lower()
                    in skill_name.lower()
                    and skill_name not in selected_skills
                ):
                    selected_skills.append(skill_name)

                if len(selected_skills) == 3:
                    break

            if len(selected_skills) == 3:
                break

        # If fewer than 3 important skills were found,
        # fill with remaining skills
        if len(selected_skills) < 3:
            for skill in skills:
                skill_name = skill["name"]

                if skill_name not in selected_skills:
                    selected_skills.append(skill_name)

                if len(selected_skills) == 3:
                    break

        if selected_skills:
            reason.append(
                "Core skills: " + ", ".join(selected_skills)
            )
        # Behaviour signals
        if signals.get("open_to_work_flag"):
            reason.append("Open to work")

        if signals.get("github_activity_score", 0) >= 50:
            reason.append("Active GitHub")

        if signals.get("notice_period_days", 180) <= 30:
            reason.append("30-day notice period")

# Explain WHY they fit the JD
        career_text = ""

        parts = []

        for job in candidate.get("career_history", []):

            parts.append(
                job.get("title", "")
            )

            parts.append(
                job.get("description", "")
            )

        summary = candidate["profile"].get("summary", "")

        if len(summary) > 30:
            parts.append(summary)

        career_text = " ".join(parts)

        career_texts.append(career_text.lower())
        matches = []

        if contains_any(career_text, [
            "retrieval",
            "hybrid retrieval",
            "dense retrieval",
            "semantic search"
        ]):
            matches.append("retrieval systems")

        if contains_any(career_text, [
            "ranking",
            "learning-to-rank",
            "recommendation"
        ]):
            matches.append("ranking/recommendation systems")

        if contains_any(career_text, [
            "ndcg",
            "mrr",
            "offline evaluation",
            "online evaluation"
        ]):
            matches.append("ranking evaluation")

        if contains_any(career_text, [
            "faiss",
            "pinecone",
            "milvus",
            "qdrant",
            "weaviate",
            "elasticsearch"
        ]):
            matches.append("vector search infrastructure")

        if matches:

            if len(matches) >= 4:
                reason.append(
                "Strong evidence of production-scale work across "
                + ", ".join(matches)
            )

            elif len(matches) == 3:
                reason.append(
                "Career history demonstrates solid experience with "
                + ", ".join(matches)
            )

            elif len(matches) == 2:
                reason.append(
                "Relevant experience in "
                + " and ".join(matches)
            )

            else:
                reason.append(
                "Career history includes "
                    + matches[0]
            )

                # Location mention
        location = profile.get("location", "")
        location_lower = location.lower()

        if "pune" in location_lower or "noida" in location_lower:
            reason.append(
                f"Based in {location} — matches JD's preferred hub"
            )

        elif any(c in location_lower for c in ["hyderabad", "mumbai", "delhi"]):
            reason.append(
                f"Based in {location} — one of the JD's welcomed cities"
            )

        elif profile.get("country", "").lower() != "india":
            reason.append(
                f"Based in {location} — outside India, no visa sponsorship per JD"
            )

        # Recency caveat
        last_active = signals.get("last_active_date", "")

        try:
            from datetime import datetime

            days_inactive = (
                datetime(2026, 5, 27)
                - datetime.strptime(last_active, "%Y-%m-%d")
            ).days

            if days_inactive > 180:
                reason.append(
                    f"Caveat: inactive for {days_inactive} days — confirm still in market"
                )

            elif days_inactive > 90:
                reason.append(
                    f"Note: last active {days_inactive} days ago — worth confirming availability"
                )

        except (ValueError, TypeError):
            pass

        # Honest weakness note for lower ranks
        if rank > 50 and len(matches) <= 1:
            reason.append(
                "Weaker direct evidence of retrieval/ranking ownership — verify fit before prioritising"
            )

        elif rank > 75 and len(matches) <= 2:
            reason.append(
                "Partial stack overlap with JD — worth a closer look before prioritising over higher-ranked candidates"
            )

        reasoning = ". ".join(reason)

        writer.writerow([
            candidate_id,
            rank,
            score,
            reasoning
        ])
print("submission.csv created successfully")

print("\nTOP 10\n")

for score, candidate in top100[:10]:
    print(
        candidate["candidate_id"],
        score,
        candidate["profile"]["current_title"],
        candidate["profile"]["years_of_experience"]
    )