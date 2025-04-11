from flask import Flask, render_template, request, jsonify
import wikipedia

app = Flask(__name__)

# Keywords to classify user input
wildlife_keywords = ['tiger', 'elephant', 'leopard', 'deer', 'bird', 'snake', 'wildlife', 'panther', 'bear', 'fox', 'crocodile']
park_keywords = ['national park', 'sanctuary', 'reserve', 'forest', 'wildlife sanctuary', 'biosphere reserve']

def classify_input(user_input):
    input_lower = user_input.lower()
    if any(keyword in input_lower for keyword in park_keywords):
        return 'park'
    elif any(keyword in input_lower for keyword in wildlife_keywords):
        return 'wildlife'
    return 'general'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    classification = classify_input(user_input)

    try:
        summary = wikipedia.summary(user_input, sentences=5)
        if classification == 'park':
            response = f"<strong>🏞️ National Park Info:</strong><br><p>{summary}</p>"
        elif classification == 'wildlife':
            response = f"<strong>🦁 Wildlife Info:</strong><br><p>{summary}</p>"
        else:
            response = f"<strong>🌿 General Info:</strong><br><p>{summary}</p>"
    except wikipedia.exceptions.DisambiguationError as e:
        response = f"<strong>⚠️ Ambiguous Query:</strong> Try one of these: {', '.join(e.options[:5])}"
    except wikipedia.exceptions.PageError:
        response = "❌ Sorry, I couldn't find any information about that."
    except Exception as e:
        response = f"⚠️ Something went wrong: {str(e)}"

    return jsonify({'reply': response})

if __name__ == '__main__':
    app.run(debug=True)
