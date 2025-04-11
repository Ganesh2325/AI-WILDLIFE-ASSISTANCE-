from flask import Flask, request, jsonify, render_template
import wikipedia
import random

app = Flask(__name__)

# Basic keyword datasets
wildlife_keywords = ["tiger", "elephant", "leopard", "lion", "bear", "deer", "rhino", "panther", "python", "crocodile"]
parks_keywords = [
    "Jim Corbett National Park", "Kaziranga National Park", "Sundarbans National Park", 
    "Bandipur National Park", "Gir Forest National Park", "Ranthambore National Park", 
    "Periyar National Park", "Manas National Park", "Kanha National Park"
]

# Forest animals in India
forest_animals = [
    "Tiger", "Indian Elephant", "Leopard", "Sloth Bear", "Indian Bison (Gaur)", "Sambar Deer",
    "Chital", "Nilgai", "Barking Deer", "Wild Boar", "Indian Python", "King Cobra", 
    "Great Indian Hornbill", "Indian Peafowl", "Crocodile", "Indian Monitor Lizard", 
    "Indian Star Tortoise", "Langur", "Macaque", "Jackal", "Hyena"
]

def get_wiki_summary(input_text):
    try:
        summary = wikipedia.summary(input_text, sentences=5, auto_suggest=False)
        page = wikipedia.page(input_text, auto_suggest=False)
        images = [img for img in page.images if img.lower().endswith((".jpg", ".jpeg", ".png"))]
        return summary, random.sample(images, min(3, len(images)))
    except:
        return "Sorry, I couldn't find enough detailed information on that topic.", []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    user_input_lower = user_input.lower()

    # Classify the input
    if any(animal.lower() in user_input_lower for animal in wildlife_keywords):
        category = "Local Wildlife"
    elif any(park.lower() in user_input_lower for park in parks_keywords):
        category = "National Park"
    else:
        category = "General Wildlife/Nature"

    # Get description and images
    description, images = get_wiki_summary(user_input)

    # Add extra info if wildlife
    if category == "Local Wildlife":
        extra = f"<br><br><strong>Other animals that live in Indian forests:</strong> " + ", ".join(random.sample(forest_animals, 10))
    elif category == "National Park":
        extra = f"<br><br><strong>This is one of the well-known protected areas in India, rich with biodiversity and home to various wildlife species.</strong>"
    else:
        extra = ""

    # Format images
    image_tags = ""
    for img_url in images:
        image_tags += f'<img src="{img_url}" style="width: 180px; height: 150px; object-fit: cover; margin-right: 10px;">'

    full_response = f"""
    <p><strong>Category:</strong> {category}</p>
    <p>{description}</p>
    {extra}
    <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">{image_tags}</div>
    """

    return jsonify({"reply": full_response})

if __name__ == "__main__":
    app.run(debug=True)
