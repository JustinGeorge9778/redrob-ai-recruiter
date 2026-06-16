import json

TARGET_IDS = {
    "CAND_0049538",
    "CAND_0061265",
    "CAND_0099806",
    "CAND_0028793",
    "CAND_0018722"
}

with open(
    "data/candidates.jsonl",
    "r",
    encoding="utf-8"
) as f:

    for line in f:

        candidate = json.loads(line)

        if candidate["candidate_id"] in TARGET_IDS:

            profile = candidate["profile"]

            print("\n" + "=" * 80)

            print(
                candidate["candidate_id"]
            )

            print(
                "TITLE:",
                profile["current_title"]
            )

            print(
                "YEARS:",
                profile["years_of_experience"]
            )

            print(
                "COMPANY:",
                profile["current_company"]
            )

            print(
                "\nHEADLINE:"
            )

            print(
                profile["headline"]
            )

            print(
                "\nSKILLS:"
            )

            skills = [
                s["name"]
                for s in candidate["skills"]
            ]

            print(
                skills[:20]
            )

            print(
                "\nBEHAVIOR:"
            )

            signals = candidate[
                "redrob_signals"
            ]

            print(
                {
                    "github":
                    signals.get(
                        "github_activity_score"
                    ),
                    "response":
                    signals.get(
                        "recruiter_response_rate"
                    ),
                    "interview":
                    signals.get(
                        "interview_completion_rate"
                    ),
                    "saved":
                    signals.get(
                        "saved_by_recruiters_30d"
                    )
                }
            )