from flask import Flask, render_template, request, jsonify
from jarvis_core import processCommand  # your existing Jarvis logic

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    command = data.get('command')
    
    print("Received command:", command)
    
    try:
        response = processCommand(command)
        print("Response:", response)
        return jsonify({'response': response})
    except Exception as e:
        print("Error in processCommand:", e)
        return jsonify({'response': f"Error: {e}"})

if __name__ == '__main__':
    app.run(debug=True)
