class UpdateFetcher:
    def __init__(self, github_api_client, db_client):
        self.github_api_client = github_api_client
        self.db_client = db_client

    def fetch_updates(self, subscriptions):
        for repo_url in subscriptions:
            issues = self.github_api_client.get_repo_issues(repo_url)
            pull_requests = self.github_api_client.get_repo_pull_requests(repo_url)

            # 处理和存储更新信息
            if issues:
                for issue in issues:
                    self.db_client.store_update(repo_url, f"Issue: {issue['title']} - {issue['html_url']}")

            if pull_requests:
                for pr in pull_requests:
                    self.db_client.store_update(repo_url, f"Pull Request: {pr['title']} - {pr['html_url']}")

            print(f"Fetched updates for {repo_url}")