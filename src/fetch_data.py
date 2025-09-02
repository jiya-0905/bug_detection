import requests
import time
import os

BASE_URL = "https://api.github.com"

# Optional: Use a GitHub token to boost rate limits
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # You can set this in your environment

headers = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "JiyaBugPredictor"
}

if GITHUB_TOKEN:
    headers["Authorization"] = f"token {GITHUB_TOKEN}"

def get_commits(owner, repo, max_pages=5, per_page=100):
    all_commits = []
    for page in range(1, max_pages + 1):
        url = f"{BASE_URL}/repos/{owner}/{repo}/commits?page={page}&per_page={per_page}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:

            commits = response.json()
            if not commits:
                break
            all_commits.extend(commits)
            time.sleep(1)
        else:
            print(f"Error fetching commits: {response.status_code}")
            break
    return all_commits

def extract_commit_info(commits, owner, repo):
    commit_data = []
    for commit in commits:
        sha = commit.get("sha")
        url = f"{BASE_URL}/repos/{owner}/{repo}/commits/{sha}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            commit_details = response.json()
            files_changed = [f["filename"] for f in commit_details.get("files", [])]
            info = {
                "sha": sha,
                "author": commit_details.get("commit", {}).get("author", {}).get("name"),
                "date": commit_details.get("commit", {}).get("author", {}).get("date"),
                "message": commit_details.get("commit", {}).get("message"),
                "files": files_changed
            }
            commit_data.append(info)
            time.sleep(0.5)
        else:
            print(f"Error fetching commit details for {sha}: {response.status_code}")
            continue
    return commit_data

# Example usage
if __name__ == "__main__":
    owner = "pallets"
    repo = "flask"
    commits = get_commits(owner, repo)
    commit_info = extract_commit_info(commits, owner, repo)
    import json

# Save commit_info to JSON
    print(f"Fetched {len(commit_info)} commits with file-level data.")
    with open("data/commit_info.json", "w") as f:
        json.dump(commit_info, f, indent=2)
    print("✅ Commit data saved to data/commit_info.json")
