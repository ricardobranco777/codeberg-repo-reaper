import concurrent.futures
import requests

# ---------------- CONFIGURATION ----------------
TOKEN = "YOUR_CODEBERG_TOKEN"
USERNAME = "YOUR_USERNAME"
BASE_URL = "https://codeberg.org/api/v1"

# Safety and Concurrency Settings
DRY_RUN = True      # Set to False to perform actual deletions!
MAX_WORKERS = 10    # Number of parallel deletion threads
WHITELIST = ["keep-this-repo", "important-project"]  # Repos to preserve
# -----------------------------------------------

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/json"
}

def fetch_all_repositories():
    """Paginate through all pages until all user repositories are retrieved."""
    all_repos = []
    page = 1
    limit = 50  # Standard page size limit for Forgejo/Gitea API

    print("Fetching all repositories across all pages...")
    while True:
        url = f"{BASE_URL}/user/repos?page={page}&limit={limit}"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"❌ Error fetching page {page}: {response.status_code}")
            break
            
        data = response.json()
        if not data:
            break  # Reached the end of pagination
            
        all_repos.extend(data)
        print(f"  -> Fetched page {page} ({len(data)} repositories found)")
        page += 1

    return all_repos

def delete_repository(repo_name):
    """Worker function executed across multiple threads."""
    if repo_name in WHITELIST:
        print(f"🛡️  [SKIPPED] Whitelisted: {repo_name}")
        return

    if DRY_RUN:
        print(f"🔍 [DRY RUN] Would delete: {repo_name}")
        return

    url = f"{BASE_URL}/repos/{USERNAME}/{repo_name}"
    res = requests.delete(url, headers=headers)
    
    if res.status_code == 204:
        print(f"✅ [DELETED] {repo_name}")
    else:
        print(f"❌ [FAILED] {repo_name} - Status HTTP {res.status_code}")

def main():
    repos = fetch_all_repositories()
    total_count = len(repos)
    print(f"\nFound {total_count} total repositories.")

    if total_count == 0:
        print("No repositories to process.")
        return

    if DRY_RUN:
        print("\n⚠️  DRY RUN MODE IS ACTIVE. No repositories will actually be deleted.")
        print("Set `DRY_RUN = False` in the script when you are ready.\n")

    # Extract repo names and execute deletions in parallel threads
    repo_names = [repo["name"] for repo in repos]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(delete_repository, repo_names)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
