from env import EnvConfig

class APIFramework:
    def __init__(self, config: EnvConfig):
        self.config = config

    def call_api(self, service_name, endpoint):
        key = self.config.get(f"{service_name.upper()}_API_KEY")
        if not key:
            return f"Error: No API key found for {service_name}"
        return f"Calling {service_name} API at '{endpoint}' with key: [HIDDEN] ✅"


if __name__ == "__main__":
    print("🔒 Secure API Framework Example\n")
    config = EnvConfig(".env")
    config.ensure_env_exists()
    api = APIFramework(config)
    print(api.call_api("openai", "/v1/completions"))
    print(api.call_api("weather", "/v1/current"))
