
import json
import os

CONFIG_FILE = "config.json"

DEFAULT_PREFERENCES = {
    "decimal_places": 2,
    "default_input_unit": "mm",
    "default_output_unit": "mil",
}

class ConfigManager:
    def __init__(self):
        self.preferences = DEFAULT_PREFERENCES.copy()
        self.load()

    def load(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Update defaults with loaded data to ensure new keys are present
                    self.preferences.update(data)
            except (json.JSONDecodeError, OSError):
                pass 

    def save(self):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.preferences, f, indent=4)
        except OSError:
            pass

    def get(self, key, default=None):
        return self.preferences.get(key, default)

    def set(self, key, value):
        self.preferences[key] = value
        self.save()
