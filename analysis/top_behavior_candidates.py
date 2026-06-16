import json

DATASET = "data/candidates.jsonl"

elite = []

for line in open(DATASET, "r", encoding="utf-8"):
    candidate = json.loads(line)

    signals = candidate.get("redrob_signals", {})

    github = signals.get("github_activity_score", -1)
    response = signals.get("recruiter_response_rate", 0)
    interview = signals.get("interview_completion_rate", 0)

    score = (
        github * 0.4 +
        response * 100 * 0.3 +
        interview * 100 * 0.3
    )

    elite.append(
        (
            score,
            candidate["candidate_id"],
            candidate["profile"]["current_title"]
        )
    )

elite.sort(reverse=True)

print("\nTOP 30 BEHAVIORAL CANDIDATES\n")

for row in elite[:30]:
    print(row)