import json
import os

class SubscriptionManager:
    def __init__(self, json_file):
        self.json_file = json_file
        self.subscriptions = self.load_subscriptions()

    def load_subscriptions(self):
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        return []

    def save_subscriptions(self):
        with open(self.json_file, 'w', encoding='utf-8') as file:
            json.dump(self.subscriptions, file, indent=4)

    def add_subscription(self, repo_url):
        if repo_url not in self.subscriptions:
            self.subscriptions.append(repo_url)
            self.save_subscriptions()
            print(f"Subscribed to {repo_url}")
        else:
            print(f"Already subscribed to {repo_url}")

    def remove_subscription(self, repo_url):
        if repo_url in self.subscriptions:
            self.subscriptions.remove(repo_url)
            self.save_subscriptions()
            print(f"Unsubscribed from {repo_url}")
        else:
            print(f"Not subscribed to {repo_url}")

    def list_subscriptions(self):
        return self.subscriptions