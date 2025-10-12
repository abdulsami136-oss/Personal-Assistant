# jarvis_core.py
from openai import OpenAI

def aiProcess(command):
    client = OpenAI(
        api_key="sk-8e13b4f672aa4e6b89a77d04dc1797ae",
        base_url="https://api.deepseek.com"
    )

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": command}
        ]
    )

    return response.choices[0].message.content


def processCommand(command):
    command = command.lower()

    if "google" in command:
        return "Opening Google...", "https://www.google.com"
    elif "linkedin" in command:
        return "Opening LinkedIn...", "https://www.linkedin.com"
    elif "youtube" in command:
        return "Opening YouTube...", "https://www.youtube.com"
    elif "discord" in command:
        return "Opening Discord...", "https://discord.com/app"
    else:
        output = aiProcess(command)
        return output, None

