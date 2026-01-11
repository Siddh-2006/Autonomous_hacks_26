import requests
from datetime import datetime, timedelta

def fetch_github_metrics(org_name="couchbase"):
    """
    Fetches engineering metrics from GitHub API.
    Metrics:
    - total_commits_last_30d
    - total_commits_prev_30d
    - active_contributors (count of unique authors in last 30d)
    - new_repos_90d (count of repos created in last 90d)
    """
    base_url = f"https://api.github.com/orgs/{org_name}/repos?type=public&sort=updated&per_page=30"
    
    # We use unauthenticated requests for public data. 
    # Rate limit is 60/hr. If hit, we return safe defaults.
    # UPGRADE: Check for GITHUB_TOKEN in env for higher rate limits (5000/hr).
    import os
    token = os.getenv("GITHUB_TOKEN")
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
        print("[INFO] Using GitHub Token for increased rate limits.")

    
    metrics = {
        "total_commits_last_30d": 0,
        "total_commits_prev_30d": 0,
        "active_contributors": 0,
        "new_repos_90d": 0,
        "release_cadence": "Unknown",
        "core_repos": [],
        # --- CPO METRICS ---
        "open_issues": 0,
        "closed_issues_30d": 0,
        "avg_resolution_time_hours": 0.0,
        "total_stars": 0,
        "total_forks": 0
    }
    
    try:
        # 1. Fetch Repos (Top 30 recently updated)
        resp = requests.get(base_url, headers=headers, timeout=10)
        if resp.status_code != 200:
            print(f"[WARNING] GitHub API Error: {resp.status_code}")
            return metrics
            
        repos = resp.json()
        
        # Date ranges
        now = datetime.utcnow()
        thirty_days_ago = now - timedelta(days=30)
        sixty_days_ago = now - timedelta(days=60)
        ninety_days_ago = now - timedelta(days=90)
        
        unique_authors = set()
        resolution_times = []
        
        # 2. Analyze individual repos (limit to top 5 to save rate limit)
        for repo in repos[:5]:
            repo_name = repo['name']
            created_at = datetime.strptime(repo['created_at'], "%Y-%m-%dT%H:%M:%SZ")
            
            # CPO: Adoption Signals
            metrics["total_stars"] += repo.get('stargazers_count', 0)
            metrics["total_forks"] += repo.get('forks_count', 0)
            metrics["open_issues"] += repo.get('open_issues_count', 0)

            # Innovation Signal: New Repos
            if created_at > ninety_days_ago:
                metrics["new_repos_90d"] += 1
            
            # Fetch Commits & Issues (Parallel-ish logic)
            # A. COMMITS
            commits_url = f"https://api.github.com/repos/{org_name}/{repo_name}/commits?since={sixty_days_ago.isoformat()}"
            commits_resp = requests.get(commits_url, headers=headers, timeout=5)
            
            if commits_resp.status_code == 200:
                commits = commits_resp.json()
                for c in commits:
                    commit_date_str = c['commit']['author']['date']
                    commit_date = datetime.strptime(commit_date_str, "%Y-%m-%dT%H:%M:%SZ")
                    
                    if commit_date > thirty_days_ago:
                        metrics["total_commits_last_30d"] += 1
                        metrics["core_repos"].append(repo_name)
                        author = c['commit']['author']['email']
                        unique_authors.add(author)
                    elif commit_date > sixty_days_ago:
                        metrics["total_commits_prev_30d"] += 1

            # B. ISSUES (CPO Logic)
            # Fetch closed issues to measure resolution speed
            issues_url = f"https://api.github.com/repos/{org_name}/{repo_name}/issues?state=closed&since={thirty_days_ago.isoformat()}&per_page=20"
            issues_resp = requests.get(issues_url, headers=headers, timeout=5)
            
            if issues_resp.status_code == 200:
                issues = issues_resp.json()
                for issue in issues:
                    if 'pull_request' in issue: continue # Skip PRs, we want user issues
                    
                    metrics["closed_issues_30d"] += 1
                    created = datetime.strptime(issue['created_at'], "%Y-%m-%dT%H:%M:%SZ")
                    closed = datetime.strptime(issue['closed_at'], "%Y-%m-%dT%H:%M:%SZ")
                    resolution_hours = (closed - created).total_seconds() / 3600
                    resolution_times.append(resolution_hours)

        metrics["active_contributors"] = len(unique_authors)
        metrics["core_repos"] = list(set(metrics["core_repos"]))
        
        # Calculate Resolution Time
        if resolution_times:
            metrics["avg_resolution_time_hours"] = sum(resolution_times) / len(resolution_times)

        # Heuristic for Release Cadence
        if metrics["total_commits_last_30d"] > 50:
            metrics["release_cadence"] = "High"
        elif metrics["total_commits_last_30d"] > 10:
            metrics["release_cadence"] = "Moderate"
        else:
            metrics["release_cadence"] = "Low"
            
    except Exception as e:
        print(f"[ERROR] GitHub Scrape Failed: {e}")
        
    return metrics
