import yaml

class ConfigManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = None

    def load_config(self):
        with open(self.config_file, 'r') as file:
            self.config = yaml.safe_load(file)

    def get(self, key, default=None):
        return self.config.get(key, default)
