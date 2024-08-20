import requests

class GitHubAPIClient:
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    def get_repo_updates(self, repo_url):
        repo_name = repo_url.split('github.com/')[-1]
        response = requests.get(f'https://api.github.com/repos/{repo_name}/events', headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return []
