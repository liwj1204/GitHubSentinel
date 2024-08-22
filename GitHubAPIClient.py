import requests
import os
from datetime import datetime

class GitHubAPIClient:
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    def get_repo_issues(self, repo_url):
        repo_name = repo_url.split('github.com/')[-1]
        response = requests.get(f'https://api.github.com/repos/{repo_name}/issues', headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return []

    def get_repo_pull_requests(self, repo_url):
        repo_name = repo_url.split('github.com/')[-1]
        response = requests.get(f'https://api.github.com/repos/{repo_name}/pulls', headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return []

    def export_daily_progress(self, repo_url):
        repo_name = repo_url.split('github.com/')[-1].replace('/', '_')
        date_str = datetime.now().strftime("%Y-%m-%d")
        issues = self.get_repo_issues(repo_url)
        pull_requests = self.get_repo_pull_requests(repo_url)

        file_name = f"{repo_name}_{date_str}.md"
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(f"# Daily Progress Report for {repo_name} - {date_str}\n\n")
            
            f.write("## Issues\n")
            if issues:
                for issue in issues:
                    f.write(f"- **{issue['title']}** (#{issue['number']}): {issue['html_url']}\n")
            else:
                f.write("No issues found.\n")
            
            f.write("\n## Pull Requests\n")
            if pull_requests:
                for pr in pull_requests:
                    f.write(f"- **{pr['title']}** (#{pr['number']}): {pr['html_url']}\n")
            else:
                f.write("No pull requests found.\n")

        print(f"Daily progress report saved to {file_name}")
        return file_name