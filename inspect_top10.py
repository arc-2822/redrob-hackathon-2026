import json

top_ids = {
    "CAND_0079387",
    "CAND_0081846",
    "CAND_0055905",
    "CAND_0046064",
    "CAND_0075249",
    "CAND_0077337",
    "CAND_0071974",
    "CAND_0044883",
    "CAND_0002025",
    "CAND_0088025"
}

with open(
    "India_runs_data_and_ai_challenge/candidates.jsonl",
    "r",
    encoding="utf-8"
) as f:

    for line in f:

        candidate = json.loads(line)

        if candidate["candidate_id"] in top_ids:

            print("=" * 70)
            print(candidate["candidate_id"])
            print(candidate["profile"]["current_title"])
            print(candidate["profile"]["years_of_experience"])

            print("\nSUMMARY:")
            print(candidate["profile"]["summary"])

            print("\nCAREER:")

            for job in candidate["career_history"]:
                print("-", job["title"])
                print(job["description"].encode("ascii", "ignore").decode())

            print("\nBEHAVIOR:")
            print(candidate["redrob_signals"])