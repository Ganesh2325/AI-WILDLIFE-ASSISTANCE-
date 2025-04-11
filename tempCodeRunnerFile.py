from flask import Flask, request, jsonify, render_template
import wikipedia
import random
import re

app = Flask(__name__)

# Sample list (expand this list)
national_parks = {
    "Jim Corbett National Park": "Uttarakhand",
    "Kaziranga National Park": "Assam",
    "Gir Forest National Park": "Gujarat",
    "Sundarbans National Park": "West Bengal",
    "Bandipur National Park": "Karnataka"
}

animal_facts = {
    "tiger": [
        "Tigers have striped skin, not just striped fur.",
        "A tiger's roar can be heard as far as 3 kilometers away.",
        "Tigers are excellent swimmers and enjoy bathing."
    ],
    "elephant": [
        "Elephants are the only animals that can't jump.",
        "Their trunks have more than 40,000 muscles!",
        "Elephants can recognize themselves in a mirror."
    ]
}

def identify_type(query):
    for park in national_parks:
        if park.lower() in query.lower():
            return "park", park
    for animal in animal_facts:
        if animal.lower() in query.lower():
            return "animal", animal
    return "unknown", query

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json["message"]
    input_type, name = identify_type(user_msg)

    try:
        summary = wikipedia.summary(name, sentences=2)
        images = wikipedia.page(name).images
        image_list = [img for img in images if img.lower().endswith(('.jpg', '.jpeg', '.png'))]
        random.shuffle(image_list)
        image_tags = "".join([f'<img src="{img}" alt="{name}" />' for img in image_list[:3]])
    except:
        summary = "Sorry, I couldn't fetch data for that."
        image_tags = ""

    if input_type == "park":
        description = f"<b>{name}</b> is a <span style='color:green;'>National Park</span> located in {national_parks[name]}."
        map_iframe = f"""<iframe width="100%" height="300" frameborder="0" style="border:0"
            src="https://www.google.com/maps?q={name.replace(' ', '+')}&output=embed" allowfullscreen></iframe>"""
        reply = f"{description}<br><br>{summary}<br>{map_iframe}<br>{image_tags}"

    elif input_type == "animal":
        fact = random.choice(animal_facts.get(name.lower(), ["No facts found."]))
        description = f"<b>{name.title()}</b> is a <span style='color:brown;'>Local Wildlife</span> species."
        reply = f"{description}<br><br>{summary}<br><i>Did you know?</i> 🧠 {fact}<br>{image_tags}"

    else:
        reply = f"I'm not sure if it's a park or an animal. Here's what I found:<br>{summary}<br>{image_tags}"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
