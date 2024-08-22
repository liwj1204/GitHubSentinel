import yaml
import os

class ConfigManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = None

    def load_config(self):
        with open(self.config_file, 'r') as file:
            self.config = yaml.safe_load(file)

        # 从环境变量中获取 GitHub token
        self.config['github_token'] = os.getenv('GITHUB_TOKEN')
        if not self.config['github_token']:
            raise ValueError("GitHub API token is not set. Please set the GITHUB_TOKEN environment variable.")

    def get(self, key, default=None):
        return self.config.get(key, default)
