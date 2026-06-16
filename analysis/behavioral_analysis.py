import json
import statistics

DATASET = "data/candidates.jsonl"

github_scores = []
response_rates = []
interview_rates = []
saved_counts = []

for line in open(DATASET, "r", encoding="utf-8"):
    candidate = json.loads(line)

    signals = candidate.get("redrob_signals", {})

    github = signals.get("github_activity_score", -1)
    response = signals.get("recruiter_response_rate", -1)
    interview = signals.get("interview_completion_rate", -1)
    saved = signals.get("saved_by_recruiters_30d", -1)

    if github >= 0:
        github_scores.append(github)

    if response >= 0:
        response_rates.append(response)

    if interview >= 0:
        interview_rates.append(interview)

    if saved >= 0:
        saved_counts.append(saved)

print("\nGITHUB ACTIVITY")
print("Average:", round(statistics.mean(github_scores), 2))
print("Max:", max(github_scores))

print("\nRECRUITER RESPONSE RATE")
print("Average:", round(statistics.mean(response_rates), 2))
print("Max:", max(response_rates))

print("\nINTERVIEW COMPLETION RATE")
print("Average:", round(statistics.mean(interview_rates), 2))
print("Max:", max(interview_rates))

print("\nSAVED BY RECRUITERS")
print("Average:", round(statistics.mean(saved_counts), 2))
print("Max:", max(saved_counts))