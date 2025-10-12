import os
from pathlib import Path

class EnvConfig:
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

    def set(self, key, value):
        self.data[key] = value
        self.save_env()

    def save_env(self):
        with open(self.env_file, "w") as f:
            for key, value in self.data.items():
                f.write(f"{key}={value}\n")

    def ensure_env_exists(self):
        if not self.env_file.exists():
            with open(self.env_file, "w") as f:
                f.write("# Example .env file\nOPENAI_API_KEY=\nWEATHER_API_KEY=\n")


"""
🧠 Personal AI Assistant — Flask Web Interface
-------------------------------------------------
A browser-based AI-powered personal assistant designed to automate daily tasks through
speech recognition, natural language processing, and web integration.

🚀 Overview:
This project merges backend intelligence (Flask + OpenAI API) with a modern,
interactive frontend (HTML, CSS, JavaScript, Web Speech API). The assistant can
accept both voice and text commands, respond via speech synthesis, and perform
various automated actions — all within the browser interface.

🧩 Tech Stack & Packages:
- Flask → Web server and API routing
- speech_recognition → Voice input capture and transcription
- pyttsx3 → Text-to-speech engine for spoken responses
- openai → AI-powered natural language understanding
- Web Speech API (JS) → Real-time voice capture and playback
- HTML/CSS/JS → Frontend user interface and interactivity

💡 Key Concepts Implemented:
- RESTful API development with Flask
- Real-time client–server communication using Fetch API
- Secure API key handling and modular architecture
- Voice-to-text and text-to-speech pipeline
- Asynchronous JavaScript for smooth, non-blocking operations
- Error handling and response management

🎯 Purpose:
To demonstrate a complete AI + Web integration workflow capable of
automating personal tasks such as opening websites, answering queries,
and providing real-time conversational assistance — deployed securely
on a personal Flask server.
"""

from flask import Flask, render_template, request, jsonify
import webbrowser
import speech_recognition as sr
import pyttsx3
from openai import OpenAI
import threading
import time

# ----------------- Initialization ----------------- #

app = Flask(__name__)
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Configure your AI Client (DeepSeek / OpenAI compatible endpoint)
client = OpenAI(
    api_key="your_api_key_here",
    base_url="https://api.deepseek.com"
)

# ----------------- Utility Functions ----------------- #

def speak(text: str):
    """Convert text into speech output using pyttsx3."""
    print(f"[Assistant]: {text}")
    engine.say(text)
    engine.runAndWait()

def ai_response(prompt: str) -> str:
    """Send user input to the AI model and return the assistant's reply."""
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful personal assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error communicating with AI: {e}"

def execute_command(command: str) -> str:
    """Recognize and execute predefined voice or text commands."""
    command = command.lower()

    if "google" in command:
        speak("Opening Google...")
        webbrowser.open("https://www.google.com")
        return "Opened Google successfully."

    elif "youtube" in command:
        speak("Opening YouTube...")
        webbrowser.open("https://www.youtube.com")
        return "Opened YouTube successfully."

    elif "linkedin" in command:
        speak("Opening LinkedIn...")
        webbrowser.open("https://www.linkedin.com")
        return "Opened LinkedIn successfully."

    elif "discord" in command:
        speak("Opening Discord...")
        webbrowser.open("https://discord.com/app")
        return "Opened Discord successfully."

    else:
        ai_reply = ai_response(command)
        speak(ai_reply)
        return ai_reply


# ----------------- Voice Input Handler ----------------- #

def listen_for_voice():
    """Continuously listens for the wake word and processes voice commands."""
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("\n🎙️ Listening for wake word 'Personal Assistant'...")
                audio = recognizer.listen(source, timeout=7, phrase_time_limit=5)

            word = recognizer.recognize_google(audio)
            print("Heard:", word)

            if "personal assistant" in word.lower():
                speak("Yes, I'm listening...")
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    print("Listening for your command...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

                command = recognizer.recognize_google(audio)
                print("Command:", command)
                execute_command(command)

        except Exception as e:
            print("Voice recognition error:", e)
            continue


# ----------------- Flask Routes ----------------- #

@app.route("/")
def home():
    """Render the main web interface."""
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    """Handle commands coming from the web interface."""
    user_input = request.json.get("command", "")
    if not user_input:
        return jsonify({"response": "No command received."})

    print(f"🧾 Command from Web: {user_input}")
    reply = execute_command(user_input)
    return jsonify({"response": reply})


# ----------------- Entry Point ----------------- #

if __name__ == "__main__":
    # Optional: Run voice listener in background thread
    threading.Thread(target=listen_for_voice, daemon=True).start()

    print("\n🌐 Personal Assistant running at http://127.0.0.1:5000")
    print("🔹 Voice mode active (say 'Personal Assistant' to wake).")
    print("🔹 Web mode active (open browser interface).")
    speak("Personal Assistant is now online and ready.")
    app.run(debug=True)
