import os
from pathlib import Path

class Config:
    def __init__(self, env_file=".env"):
        self.env_file = Path(env_file)
        self.data = {}
        self.load_env()

    def load_env(self):
        if self.env_file.exists():
            with open(self.env_file, "r") as f:
                for line in f:
                    if "=" in line and not line.strip().startswith("#"):
                        key, value = line.strip().split("=", 1)
                        self.data[key] = value

    def get(self, key, default=None):
        return os.getenv(key, self.data.get(key, default))


class APIFramework:
    def __init__(self, config: Config):
        self.config = config

    def call_api(self, service_name, endpoint):
        key = self.config.get(f"{service_name.upper()}_API_KEY")
        if not key:
            return f"Error: No API key found for {service_name}"
        return f"Calling {service_name} API at '{endpoint}' with key: [HIDDEN] ✅"


if __name__ == "__main__":
    print("🔒 Secure API Framework Example\n")
    config = Config(".env")
    api = APIFramework(config)
    print(api.call_api("openai", "/v1/completions"))
    print(api.call_api("weather", "/v1/current"))
