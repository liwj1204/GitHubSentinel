class UpdateFetcher:
    def __init__(self, github_api_client, db_client):
        self.github_api_client = github_api_client
        self.db_client = db_client

    def fetch_updates(self, subscriptions):
        for repo_url in subscriptions:
            updates = self.github_api_client.get_repo_updates(repo_url)
            for update in updates:
                self.db_client.store_update(repo_url, str(update))
            print(f"Fetched updates for {repo_url}")
