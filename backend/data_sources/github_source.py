import requests
from datetime import datetime, timedelta
from dateutil.parser import parse
from config import Config

class GitHubSource:
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {Config.GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.org = Config.GITHUB_ORG
        self.repos = Config.CORE_REPOS

    def fetch_repo_stats(self):
        """
        Aggregates stats across all core repositories.
        """
        aggregated_stats = {
            "total_commits_current": 0,
            "total_commits_prev": 0,
            "contributors": set(),
            "releases": [],
            "repo_activity": {}
        }

        # Time ranges
        now = datetime.utcnow()
        current_period_start = now - timedelta(days=Config.HISTORY_DAYS)
        previous_period_start = current_period_start - timedelta(days=Config.HISTORY_DAYS)

        for repo in self.repos:
            try:
                # 1. Fetch Commits (Current Period)
                # Note: GitHub API pagination is required for accurate counts, 
                # but for MVP we might hit limits. Using per_page=100 and counting pages is safe.
                # Optimized: Use search/commits for count? Or simple list.
                # Let's use simple list with 'since' and 'until'
                
                # Current period
                commits_curr = self._get_commit_count(repo, current_period_start, now)
                # Previous period
                commits_prev = self._get_commit_count(repo, previous_period_start, current_period_start)
                
                aggregated_stats["total_commits_current"] += commits_curr
                aggregated_stats["total_commits_prev"] += commits_prev
                aggregated_stats["repo_activity"][repo] = commits_curr

                # 2. Fetch Contributors
                # We can deduce active contributors from the commits logic or hit /contributors
                # Getting contributors from the last 90 days specifically is better done via commits.
                contributors = self._get_active_contributors(repo, current_period_start)
                aggregated_stats["contributors"].update(contributors)

                # 3. Fetch Releases
                releases = self._get_recent_releases(repo, current_period_start)
                aggregated_stats["releases"].extend(releases)

            except Exception as e:
                print(f"Error fetching data for {repo}: {e}")

        return {
            "commit_velocity_current": aggregated_stats["total_commits_current"],
            "commit_velocity_prev": aggregated_stats["total_commits_prev"],
            "active_contributors_count": len(aggregated_stats["contributors"]),
            "recent_releases_count": len(aggregated_stats["releases"]),
            "repo_breakdown": aggregated_stats["repo_activity"]
        }

    def _get_commit_count(self, repo, since, until):
        # Using list commits endpoint
        url = f"{self.base_url}/repos/{self.org}/{repo}/commits"
        params = {
            "since": since.isoformat(),
            "until": until.isoformat(),
            "per_page": 1, 
        }
        # To get count without iterating pages, we can use Link header in a specialized way 
        # but standardized way is iterating or valid search. 
        # For simplicity in MVP without hitting heavy rate limits: use simple pagination count (max 100 per page)
        # Or requests 'HEAD'?
        # Let's just fetch simplified list.
        
        # ACTUALLY, strict requirement: /repos/{repo}/commits
        # We'll just fetch pages.
        count = 0
        page = 1
        while True:
            params["per_page"] = 100
            params["page"] = page
            resp = requests.get(url, headers=self.headers, params=params)
            if resp.status_code != 200:
                break
            data = resp.json()
            if not data:
                break
            count += len(data)
            if len(data) < 100:
                break
            page += 1
        return count

    def _get_active_contributors(self, repo, since):
        contributors = set()
        url = f"{self.base_url}/repos/{self.org}/{repo}/commits"
        params = {
            "since": since.isoformat(),
            "per_page": 100 # Last 100 commits is a good proxy for "recent active" contributors
        }
        resp = requests.get(url, headers=self.headers, params=params)
        if resp.status_code == 200:
            for commit in resp.json():
                if commit.get("author") and commit["author"].get("login"):
                    contributors.add(commit["author"]["login"])
                elif commit.get("commit") and commit["commit"].get("author"):
                    # Fallback to git email/name if github user not mapped
                    contributors.add(commit["commit"]["author"]["email"])
        return contributors

    def _get_recent_releases(self, repo, since):
        releases = []
        url = f"{self.base_url}/repos/{self.org}/{repo}/releases"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200:
            for release in resp.json():
                published_at = parse(release["published_at"]).replace(tzinfo=None)
                if published_at > since:
                    releases.append(published_at)
        return releases
