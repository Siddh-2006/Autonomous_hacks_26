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
    
    metrics = {
        "total_commits_last_30d": 0,
        "total_commits_prev_30d": 0,
        "active_contributors": 0,
        "new_repos_90d": 0,
        "release_cadence": "Unknown",
        "core_repos": []
    }
    
    try:
        # 1. Fetch Repos (Top 30 recently updated)
        resp = requests.get(base_url, timeout=10)
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
        
        # 2. Analyze individual repos (limit to top 5 to save rate limit)
        for repo in repos[:5]:
            repo_name = repo['name']
            created_at = datetime.strptime(repo['created_at'], "%Y-%m-%dT%H:%M:%SZ")
            
            # Innovation Signal: New Repos
            if created_at > ninety_days_ago:
                metrics["new_repos_90d"] += 1
            
            # Fetch Commits
            commits_url = f"https://api.github.com/repos/{org_name}/{repo_name}/commits?since={sixty_days_ago.isoformat()}"
            commits_resp = requests.get(commits_url, timeout=5)
            
            if commits_resp.status_code == 200:
                commits = commits_resp.json()
                
                # Filter & Count
                for c in commits:
                    commit_date_str = c['commit']['author']['date']
                    commit_date = datetime.strptime(commit_date_str, "%Y-%m-%dT%H:%M:%SZ")
                    
                    if commit_date > thirty_days_ago:
                        metrics["total_commits_last_30d"] += 1
                        metrics["core_repos"].append(repo_name)
                        # Author tracking
                        author = c['commit']['author']['email']
                        unique_authors.add(author)
                    elif commit_date > sixty_days_ago:
                        metrics["total_commits_prev_30d"] += 1

        metrics["active_contributors"] = len(unique_authors)
        metrics["core_repos"] = list(set(metrics["core_repos"]))
        
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
