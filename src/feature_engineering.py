import json
from datetime import datetime, timezone
from collections import defaultdict
import pandas as pd

# Bug-related keywords
BUG_KEYWORDS = ["fix", "bug", "issue", "error", "patch"]

def extract_features(commits):
    file_stats = defaultdict(lambda: {
        "commit_count": 0,
        "unique_authors": set(),
        "last_modified": None,
        "bug_fix_count": 0
    })

    now = datetime.now(timezone.utc)

    for commit in commits:
        author = commit.get("author", "unknown")
        date_str = commit.get("date")
        message = commit.get("message", "").lower()
        files = commit.get("files", [])

        try:
            commit_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        except Exception:
            continue

        for file in files:
            # Tag file with repo name if available
            file_key = f"{commit.get('repo', 'unknown')}::{file}"

            stats = file_stats[file_key]
            stats["commit_count"] += 1
            stats["unique_authors"].add(author)

            if stats["last_modified"] is None or commit_date > stats["last_modified"]:
                stats["last_modified"] = commit_date

            if any(keyword in message for keyword in BUG_KEYWORDS):
                stats["bug_fix_count"] += 1

    # Convert to DataFrame
    rows = []
    for file_key, stats in file_stats.items():
        days_since_modified = (now - stats["last_modified"]).days if stats["last_modified"] else None
        rows.append({
            "file": file_key,
            "commit_count": stats["commit_count"],
            "unique_authors": len(stats["unique_authors"]),
            "last_modified_days_ago": days_since_modified,
            "bug_fix_count": stats["bug_fix_count"],
            "is_buggy": 1 if stats["bug_fix_count"] > 0 else 0
        })

    return pd.DataFrame(rows)

def load_commit_data(filepath="data/commit_info.json"):
    with open(filepath, "r") as f:
        return json.load(f)

def save_features(df, path="data/file_features.csv"):
    df.to_csv(path, index=False)
    print(f"✅ Features saved to {path}")
if __name__ == "__main__":
    commits = load_commit_data()
    df = extract_features(commits)
    save_features(df)