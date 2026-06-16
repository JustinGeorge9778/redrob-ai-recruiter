import json
from collections import Counter

DATASET = "data/candidates.jsonl"

title_counter = Counter()
skill_counter = Counter()
country_counter = Counter()

total_candidates = 0

print("Loading dataset...\n")

with open(DATASET, "r", encoding="utf-8") as f:
    for line in f:
        candidate = json.loads(line)

        total_candidates += 1

        profile = candidate.get("profile", {})

        title_counter[profile.get("current_title", "Unknown")] += 1
        country_counter[profile.get("country", "Unknown")] += 1

        for skill in candidate.get("skills", []):
            skill_counter[skill.get("name", "Unknown")] += 1

print("=" * 50)
print("TOTAL CANDIDATES")
print("=" * 50)
print(total_candidates)

print("\n" + "=" * 50)
print("TOP 20 TITLES")
print("=" * 50)

for title, count in title_counter.most_common(20):
    print(f"{title:<30} {count}")

print("\n" + "=" * 50)
print("TOP 30 SKILLS")
print("=" * 50)

for skill, count in skill_counter.most_common(30):
    print(f"{skill:<30} {count}")

print("\n" + "=" * 50)
print("TOP COUNTRIES")
print("=" * 50)

for country, count in country_counter.most_common(20):
    print(f"{country:<30} {count}")