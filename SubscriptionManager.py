class SubscriptionManager:
    def __init__(self, db_client):
        self.db_client = db_client
        self.subscriptions = []

    def add_subscription(self, repo_url):
        self.subscriptions.append(repo_url)
        print(f"Subscribed to {repo_url}")

    def remove_subscription(self, repo_url):
        self.subscriptions = [url for url in self.subscriptions if url != repo_url]
        print(f"Unsubscribed from {repo_url}")

    def list_subscriptions(self):
        return self.subscriptions
