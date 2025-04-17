from flask import Flask, request, jsonify, render_template
import wikipedia
import random

app = Flask(__name__)

# Configure Wikipedia
wikipedia.set_lang("en")
wikipedia.set_rate_limiting(True)

# Common wildlife animals in Indian national parks (with multiple images)
wildlife_data = {
    "tiger": {
        "scientific": "Panthera tigris",
        "status": "Endangered",
        "description": "The Bengal tiger is India's national animal. India hosts about 70% of the world's tiger population in reserves like Ranthambore, Bandhavgarh, and Jim Corbett.",
        "parks": ["Ranthambore National Park", "Bandhavgarh National Park", "Jim Corbett National Park"],
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Tiger_in_Ranthambhore.jpg/800px-Tiger_in_Ranthambhore.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Bengal_tiger_%28Panthera_tigris_tigris%29_female_3.jpg/800px-Bengal_tiger_%28Panthera_tigris_tigris%29_female_3.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Walking_tiger_female.jpg/800px-Walking_tiger_female.jpg"
        ]
    },
    "elephant": {
        "scientific": "Elephas maximus",
        "status": "Endangered",
        "description": "Indian elephants are slightly smaller than African elephants with larger ears. Key habitats include Kaziranga, Periyar, and Nagarhole.",
        "parks": ["Kaziranga National Park", "Periyar National Park", "Nagarhole National Park"],
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Asian_Elephant_at_Corbett_National_Park_%2836573607784%29.jpg/800px-Asian_Elephant_at_Corbett_National_Park_%2836573607784%29.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Elephas_maximus_%28Bandipur%29.jpg/800px-Elephas_maximus_%28Bandipur%29.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Elephant_in_Kaziranga_National_Park.jpg/800px-Elephant_in_Kaziranga_National_Park.jpg"
        ]
    },
    "leopard": {
        "scientific": "Panthera pardus",
        "status": "Vulnerable",
        "description": "Indian leopards are excellent climbers and often drag their prey up trees. Found in many forests across India.",
        "parks": ["Sanjay Gandhi National Park", "Satpura National Park", "Mudumalai National Park"],
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Indian_Leopard_at_Tadoba_Andhari_Tiger_Reserve%2C_Maharashtra.jpg/800px-Indian_Leopard_at_Tadoba_Andhari_Tiger_Reserve%2C_Maharashtra.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Leopard_in_the_Colchester_Zoo.jpg/800px-Leopard_in_the_Colchester_Zoo.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Leopard_in_the_Okavango_%282%29.jpg/800px-Leopard_in_the_Okavango_%282%29.jpg"
        ]
    },
     "lion": {
        "scientific": "Panthera pardus",
        "status": "Vulnerable",
        "description": "Indian leopards are excellent climbers and often drag their prey up trees. Found in many forests across India.",
        "parks": ["Sanjay Gandhi National Park", "Satpura National Park", "Mudumalai National Park"],
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Indian_Leopard_at_Tadoba_Andhari_Tiger_Reserve%2C_Maharashtra.jpg/800px-Indian_Leopard_at_Tadoba_Andhari_Tiger_Reserve%2C_Maharashtra.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Leopard_in_the_Colchester_Zoo.jpg/800px-Leopard_in_the_Colchester_Zoo.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Leopard_in_the_Okavango_%282%29.jpg/800px-Leopard_in_the_Okavango_%282%29.jpg"
        ]
    }
}

# Comprehensive list of Indian national parks with data
indian_national_parks = {
    "Jim Corbett National Park": {
        "location": "Uttarakhand",
        "established": 1936,
        "area": "520.8 km²",
        "best_time": "November to June",
        "highlights": ["Tiger sightings", "Elephant safari", "Diverse birdlife"],
        "animals": ["Bengal tiger", "Asian elephant", "Leopard", "Sloth bear"],
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Corbett_Tiger_Reserve.jpg/800px-Corbett_Tiger_Reserve.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Jim_Corbett_National_Park.jpg/800px-Jim_Corbett_National_Park.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Corbett_Landscape.jpg/800px-Corbett_Landscape.jpg"
        ]
    },
    "Kaziranga National Park": {
        "location": "Assam",
        "established": 1974,
        "area": "430 km²",
        "best_time": "November to April",
        "highlights": ["One-horned rhinos", "Elephant grass wetlands", "Bird watching"],
        "animals": ["Indian rhinoceros", "Asian elephant", "Royal Bengal tiger", "Wild water buffalo"],
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/One_horned_rhino.jpg/800px-One_horned_rhino.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Kaziranga_landscape.jpg/800px-Kaziranga_landscape.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Kaziranga_National_Park_03.jpg/800px-Kaziranga_National_Park_03.jpg"
        ]
    },
    "Sundarbans National Park": {
        "location": "West Bengal",
        "established": 1984,
        "area": "1,330.10 km²",
        "best_time": "September to March",
        "highlights": ["Royal Bengal tigers", "Mangrove forests", "River cruises"],
        "animals": ["Bengal tiger", "Saltwater crocodile", "Indian python", "Ganges river dolphin"],
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Sundarban_Tiger.jpg/800px-Sundarban_Tiger.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Sundarban.jpg/800px-Sundarban.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Sundarbans_Beauty.jpg/800px-Sundarbans_Beauty.jpg"
        ]
    },
    "Ranthambore National Park": {
        "location": "Rajasthan",
        "established": 1980,
        "area": "392 km²",
        "best_time": "October to June",
        "highlights": ["Tiger spotting", "Ranthambore Fort", "Scenic lakes"],
        "animals": ["Bengal tiger", "Indian leopard", "Sloth bear", "Sambar deer"],
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Tiger_in_Ranthambhore.jpg/800px-Tiger_in_Ranthambhore.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Ranthambore_Fort.jpg/800px-Ranthambore_Fort.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Ranthambore_National_Park.jpg/800px-Ranthambore_National_Park.jpg"
        ]
    },
    "Bandhavgarh National Park": {
        "location": "Madhya Pradesh",
        "established": 1968,
        "area": "448.85 km²",
        "best_time": "October to June",
        "highlights": ["High tiger density", "Ancient Bandhavgarh Fort", "Varied topography"],
        "animals": ["Bengal tiger", "Indian leopard", "Gaur", "Sloth bear"],
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Bandhavgarh_Fort.JPG/800px-Bandhavgarh_Fort.JPG",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Bandhavgarh_National_Park.jpg/800px-Bandhavgarh_National_Park.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Bandhavgarh_Tiger_Reserve.jpg/800px-Bandhavgarh_Tiger_Reserve.jpg"
        ]
    },
    "Kanha National Park": {
        "location": "Madhya Pradesh",
        "established": 1955,
        "area": "940 km²",
        "best_time": "October to June",
        "highlights": ["Inspiration for Jungle Book", "Barasingha conservation", "Diverse ecosystems"],
        "animals": ["Bengal tiger", "Barasingha", "Indian wild dog", "Leopard"],
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Kanha_National_Park.jpg/800px-Kanha_National_Park.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Hardground_Barasingha_at_Kanha_National_Park.jpg/800px-Hardground_Barasingha_at_Kanha_National_Park.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Kanha_Tiger_Reserve.jpg/800px-Kanha_Tiger_Reserve.jpg"
        ]
    },
    "Periyar National Park": {
        "location": "Kerala",
        "established": 1982,
        "area": "350 km²",
        "best_time": "September to April",
        "highlights": ["Periyar Lake", "Boat safaris", "Elephant herds"],
        "animals": ["Asian elephant", "Bengal tiger", "Indian bison", "Sambar deer"],
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Periyar_Lake.jpg/800px-Periyar_Lake.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Periyar_National_Park.jpg/800px-Periyar_National_Park.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Periyar_Wildlife_Sanctuary.jpg/800px-Periyar_Wildlife_Sanctuary.jpg"
        ]
    },
    "Gir National Park": {
        "location": "Gujarat",
        "established": 1965,
        "area": "1,412 km²",
        "best_time": "December to March",
        "highlights": ["Asiatic lions", "Diverse bird species", "Scenic landscapes"],
        "animals": ["Asiatic lion", "Indian leopard", "Sloth bear", "Striped hyena"],
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Asiatic_Lion_in_Gir_Forest.jpg/800px-Asiatic_Lion_in_Gir_Forest.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Gir_Forest_National_Park.jpg/800px-Gir_Forest_National_Park.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Gir_National_Park_Landscape.jpg/800px-Gir_National_Park_Landscape.jpg"
        ]
    },
    "Bandipur National Park": {
        "location": "Karnataka",
        "established": 1974,
        "area": "874.2 km²",
        "best_time": "October to May",
        "highlights": ["Part of Nilgiri Biosphere", "Elephant corridor", "Tiger reserve"],
        "animals": ["Bengal tiger", "Indian elephant", "Gaur", "Dhole"],
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Bandipur_Tiger_Reserve.jpg/800px-Bandipur_Tiger_Reserve.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Bandipur_National_Park.jpg/800px-Bandipur_National_Park.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Elephants_in_Bandipur.jpg/800px-Elephants_in_Bandipur.jpg"
        ]
    },
    "Nagarhole National Park": {
        "location": "Karnataka",
        "established": 1988,
        "area": "643.39 km²",
        "best_time": "October to May",
        "highlights": ["Kabini river", "Dense forests", "Rich wildlife"],
        "animals": ["Bengal tiger", "Indian leopard", "Asian elephant", "Dhole"],
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Nagarhole_National_Park.jpg/800px-Nagarhole_National_Park.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Nagarhole_Landscape.jpg/800px-Nagarhole_Landscape.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Nagarhole_Wildlife.jpg/800px-Nagarhole_Wildlife.jpg"
        ]
    },
    "Tadoba Andhari Tiger Reserve": {
        "location": "Maharashtra",
        "established": 1995,
        "area": "625.4 km²",
        "best_time": "October to June",
        "highlights": ["High tiger density", "Ancient Tadoba Lake", "Diverse flora"],
        "animals": ["Bengal tiger", "Indian leopard", "Sloth bear", "Gaur"],
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Tadoba_Andhari_Tiger_Reserve.jpg/800px-Tadoba_Andhari_Tiger_Reserve.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Tadoba_Lake.jpg/800px-Tadoba_Lake.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Indian_Leopard_at_Tadoba_Andhari_Tiger_Reserve%2C_Maharashtra.jpg/800px-Indian_Leopard_at_Tadoba_Andhari_Tiger_Reserve%2C_Maharashtra.jpg"
        ]
    },
    "Pench National Park": {
        "location": "Madhya Pradesh",
        "established": 1975,
        "area": "292.85 km²",
        "best_time": "October to June",
        "highlights": ["Setting for Jungle Book", "Pench river", "Rich biodiversity"],
        "animals": ["Bengal tiger", "Indian leopard", "Gaur", "Wild dog"],
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Pench_National_Park.jpg/800px-Pench_National_Park.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Pench_Tiger_Reserve.jpg/800px-Pench_Tiger_Reserve.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Pench_Landscape.jpg/800px-Pench_Landscape.jpg"
        ]
    },
    "Satpura National Park": {
        "location": "Madhya Pradesh",
        "established": 1981,
        "area": "524 km²",
        "best_time": "October to April",
        "highlights": ["Diverse terrain", "Walking safaris", "Rare species"],
        "animals": ["Bengal tiger", "Indian leopard", "Sloth bear", "Indian giant squirrel"],
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Satpura_National_Park.jpg/800px-Satpura_National_Park.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Satpura_Tiger_Reserve.jpg/800px-Satpura_Tiger_Reserve.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Satpura_Landscape.jpg/800px-Satpura_Landscape.jpg"
        ]
    }
}

# Biodiversity hotspots in India with multiple images
biodiversity_hotspots = {
    "Western Ghats": {
        "description": "One of the world's eight hottest hotspots of biological diversity with many endemic species.",
        "parks": ["Periyar National Park", "Silent Valley National Park", "Eravikulam National Park"],
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Western_Ghats_Mountains.jpg/800px-Western_Ghats_Mountains.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Western_Ghats_1.jpg/800px-Western_Ghats_1.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Western_Ghats_2.jpg/800px-Western_Ghats_2.jpg"
        ]
    },
    "Eastern Himalayas": {
        "description": "Contains a diverse range of flora and fauna, with many species found nowhere else on Earth.",
        "parks": ["Khangchendzonga National Park", "Namdapha National Park", "Singalila National Park"],
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Kanchenjunga_from_Chowri_Khang.jpg/800px-Kanchenjunga_from_Chowri_Khang.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Eastern_Himalayas_landscape.jpg/800px-Eastern_Himalayas_landscape.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Eastern_Himalayas_forest.jpg/800px-Eastern_Himalayas_forest.jpg"
        ]
    }
}

def get_wikipedia_summary(query):
    """Get summary from Wikipedia"""
    try:
        return wikipedia.summary(query, sentences=5)
    except:
        return None

def generate_images_html(images, count=3):
    """Generate HTML for multiple images in a grid"""
    selected_images = random.sample(images, min(count, len(images)))
    return "".join([
        f'<img src="{img}" class="rounded-lg shadow-md w-full h-48 object-cover">'
        for img in selected_images
    ])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"].strip().lower()
    
    # Help and general queries
    if any(keyword in user_input for keyword in ["help", "what can you do"]):
        return jsonify({
            "reply": """
            <div class="bg-blue-100 border-l-4 border-blue-500 p-4 rounded">
                <h3 class="font-bold text-lg">I can help you with:</h3>
                <ul class="list-disc list-inside mt-2">
                    <li>Information about any national park in India</li>
                    <li>Details about wildlife animals and their conservation status</li>
                    <li>Best time to visit specific parks</li>
                    <li>India's biodiversity hotspots</li>
                    <li>Suggestions for popular parks to visit</li>
                </ul>
                <p class="mt-2">Try asking: "Tell me about Jim Corbett" or "Show elephants in India"</p>
            </div>
            """
        })
    
    # Wildlife animal queries
    for animal, data in wildlife_data.items():
        if animal in user_input:
            images_html = f"""
            <div class="grid grid-cols-1 md:grid-cols-3 gap-2 mt-3">
                {generate_images_html(data["images"])}
            </div>
            """
            
            parks_list = "".join([f"<li>{park}</li>" for park in data["parks"]])
            
            return jsonify({
                "reply": f"""
                <div class="bg-amber-100 border-l-4 border-amber-500 p-4 rounded">
                    <h3 class="text-xl font-bold">{animal.capitalize()} <span class="text-sm bg-red-200 px-2 py-1 rounded">{data["status"]}</span></h3>
                    {images_html}
                    <div class="mt-2">
                        <p><strong>Scientific Name:</strong> {data["scientific"]}</p>
                        <p class="mt-2">{data["description"]}</p>
                        <p class="mt-2 font-semibold">Found in these parks:</p>
                        <ul class="list-disc list-inside">
                            {parks_list}
                        </ul>
                    </div>
                </div>
                """
            })
    
    # National park queries - first check our comprehensive database
    for park_name, park_data in indian_national_parks.items():
        if park_name.lower() in user_input:
            description = get_wikipedia_summary(park_name) or f"A beautiful national park in {park_data['location']} known for its wildlife."
            
            images_html = f"""
            <div class="grid grid-cols-1 md:grid-cols-3 gap-2 mt-3">
                {generate_images_html(park_data["images"])}
            </div>
            """
            
            animals_list = "".join([f"<li>{animal}</li>" for animal in park_data["animals"]])
            highlights_list = "".join([f"<li>{hl}</li>" for hl in park_data["highlights"]])
            
            return jsonify({
                "reply": f"""
                <div class="bg-green-100 border-l-4 border-green-500 p-4 rounded">
                    <h3 class="text-xl font-bold">{park_name}</h3>
                    {images_html}
                    <div class="mt-2">
                        <p><strong>Location:</strong> {park_data["location"]}</p>
                        <p><strong>Established:</strong> {park_data["established"]}</p>
                        <p><strong>Area:</strong> {park_data["area"]}</p>
                        <p><strong>Best Time to Visit:</strong> {park_data["best_time"]}</p>
                        <p class="mt-2">{description}</p>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-3">
                            <div>
                                <p class="font-semibold">Key Wildlife:</p>
                                <ul class="list-disc list-inside">
                                    {animals_list}
                                </ul>
                            </div>
                            <div>
                                <p class="font-semibold">Highlights:</p>
                                <ul class="list-disc list-inside">
                                    {highlights_list}
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
                """
            })
    
    # Biodiversity hotspots
    for hotspot, data in biodiversity_hotspots.items():
        if hotspot.lower() in user_input:
            images_html = f"""
            <div class="grid grid-cols-1 md:grid-cols-3 gap-2 mt-3">
                {generate_images_html(data["images"])}
            </div>
            """
            
            parks_list = "".join([f"<li>{park}</li>" for park in data["parks"]])
            
            return jsonify({
                "reply": f"""
                <div class="bg-purple-100 border-l-4 border-purple-500 p-4 rounded">
                    <h3 class="text-xl font-bold">{hotspot} Biodiversity Hotspot</h3>
                    {images_html}
                    <div class="mt-2">
                        <p>{data["description"]}</p>
                        <p class="mt-2 font-semibold">Notable National Parks:</p>
                        <ul class="list-disc list-inside">
                            {parks_list}
                        </ul>
                    </div>
                </div>
                """
            })
    
    # Best time to visit queries
    if "best time" in user_input or "when to visit" in user_input:
        park_found = None
        for park_name in indian_national_parks:
            if park_name.lower() in user_input:
                park_found = park_name
                break
        
        if park_found:
            park_data = indian_national_parks[park_found]
            return jsonify({
                "reply": f"""
                <div class="bg-blue-100 border-l-4 border-blue-500 p-4 rounded">
                    <h3 class="text-xl font-bold">Best Time to Visit {park_found}</h3>
                    <p class="mt-2">The ideal time to visit {park_found} in {park_data["location"]} is <strong>{park_data["best_time"]}</strong>.</p>
                    <p class="mt-2">During this period, you can expect:</p>
                    <ul class="list-disc list-inside">
                        {"".join([f"<li>{hl}</li>" for hl in park_data["highlights"]])}
                    </ul>
                </div>
                """
            })
        else:
            return jsonify({
                "reply": """
                <div class="bg-yellow-100 border-l-4 border-yellow-500 p-4 rounded">
                    <p>I can tell you the best time to visit specific national parks.</p>
                    <p class="mt-2">Try asking about:</p>
                    <ul class="list-disc list-inside">
                        <li>Best time to visit Jim Corbett</li>
                        <li>When should I go to Kaziranga</li>
                        <li>Best season for Ranthambore</li>
                    </ul>
                </div>
                """
            })
    
    # Park suggestions
    if any(keyword in user_input for keyword in ["suggest", "recommend", "popular parks", "list parks"]):
        parks_list = "".join([f"""
            <li class="mb-2">
                <strong>{park}</strong> - {data["location"]} (Best time: {data["best_time"]})
            </li>
        """ for park, data in indian_national_parks.items()])
        
        return jsonify({
            "reply": f"""
            <div class="bg-indigo-100 border-l-4 border-indigo-500 p-4 rounded">
                <h3 class="text-xl font-bold">National Parks in India</h3>
                <ul class="list-disc list-inside mt-2">
                    {parks_list}
                </ul>
                <p class="mt-2">Ask me about any of these for more details!</p>
            </div>
            """
        })
    
    # Try generic Wikipedia search as fallback for any national park not in our database
    if "national park" in user_input or any(park_keyword in user_input for park_keyword in ["park", "wildlife", "sanctuary"]):
        try:
            # Try to get the exact page first
            page = wikipedia.page(user_input)
            
            # If we get a disambiguation page, look for options containing "National Park"
            if "(disambiguation)" in page.title:
                options = wikipedia.search(user_input)
                park_options = [opt for opt in options if "National Park" in opt]
                if park_options:
                    page = wikipedia.page(park_options[0])
            
            # Generate response with images
            image_html = ""
            if page.images:
                image_urls = [img for img in page.images if img.lower().endswith(('.jpg', '.jpeg', '.png'))]
                if image_urls:
                    selected_images = random.sample(image_urls, min(3, len(image_urls)))
                    images_html = "".join([
                        f'<img src="{img}" class="rounded-lg shadow-md w-full h-48 object-cover">'
                        for img in selected_images
                    ])
                    image_html = f"""
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-2 mt-3">
                        {images_html}
                    </div>
                    """
            
            # Get the full summary
            summary = wikipedia.summary(page.title, sentences=10)
            
            # Try to extract key information if available
            info_box = ""
            try:
                page_info = page.html()
                if "infobox" in page_info.lower():
                    info_box = """
                    <div class="mt-3 p-3 bg-gray-100 rounded-lg">
                        <p class="font-semibold">Quick Facts:</p>
                        <p>More detailed information available on Wikipedia</p>
                    </div>
                    """
            except:
                pass
            
            return jsonify({
                "reply": f"""
                <div class="bg-green-100 border-l-4 border-green-500 p-4 rounded">
                    <h3 class="text-xl font-bold">{page.title}</h3>
                    {image_html}
                    <div class="mt-2">{summary}</div>
                    {info_box}
                    <div class="mt-3">
                        <a href="{page.url}" target="_blank" class="text-blue-600 hover:underline">Read more on Wikipedia</a>
                    </div>
                </div>
                """
            })
        except wikipedia.PageError:
            pass
        except:
            pass
    
    # Animal sightings probability
    if any(keyword in user_input for keyword in ["see tiger", "spot leopard", "elephant sightings", "chances of seeing"]):
        for animal in wildlife_data:
            if animal in user_input:
                parks_with_animal = wildlife_data[animal]["parks"]
                best_parks = random.sample(parks_with_animal, min(2, len(parks_with_animal)))
                best_parks_list = "".join([f"<li>{park} (High probability)</li>" for park in best_parks])
                
                return jsonify({
                    "reply": f"""
                    <div class="bg-blue-100 border-l-4 border-blue-500 p-4 rounded">
                        <h3 class="text-xl font-bold">{animal.capitalize()} Sightings</h3>
                        <p class="mt-2">The best national parks to see {animal}s in India are:</p>
                        <ul class="list-disc list-inside mt-2">
                            {best_parks_list}
                        </ul>
                        <p class="mt-2">For the best experience, visit during early morning or late afternoon safaris.</p>
                        <p class="mt-2">Ask me about any of these parks for more details!</p>
                    </div>
                    """
                })
    
    # Conservation status queries
    if any(keyword in user_input for keyword in ["conservation", "endangered", "protected", "threatened"]):
        animals_list = []
        for animal, data in wildlife_data.items():
            animals_list.append(f"""
                <div class="flex items-center justify-between py-2 border-b">
                    <span class="font-medium">{animal.capitalize()}</span>
                    <span class="px-3 py-1 rounded-full text-xs { 'bg-red-200 text-red-800' if data['status'] == 'Endangered' else 'bg-orange-200 text-orange-800' if data['status'] == 'Vulnerable' else 'bg-yellow-200 text-yellow-800' }">
                        {data['status']}
                    </span>
                </div>
            """)
        
        return jsonify({
            "reply": f"""
            <div class="bg-purple-100 border-l-4 border-purple-500 p-4 rounded">
                <h3 class="text-xl font-bold">Conservation Status of Indian Wildlife</h3>
                <div class="mt-3">
                    {"".join(animals_list)}
                </div>
                <p class="mt-3">Ask about any animal to learn more about its conservation efforts.</p>
            </div>
            """
        })
    
    # Park comparison
    if any(keyword in user_input for keyword in ["compare", "vs", "difference between"]):
        parks_to_compare = []
        for park_name in indian_national_parks:
            if park_name.lower() in user_input:
                parks_to_compare.append(park_name)
                if len(parks_to_compare) == 2:
                    break
        
        if len(parks_to_compare) == 2:
            park1 = indian_national_parks[parks_to_compare[0]]
            park2 = indian_national_parks[parks_to_compare[1]]
            
            comparison_html = f"""
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-3">
                <div class="bg-green-50 p-3 rounded-lg">
                    <h4 class="font-bold text-lg">{parks_to_compare[0]}</h4>
                    <p><strong>Location:</strong> {park1['location']}</p>
                    <p><strong>Area:</strong> {park1['area']}</p>
                    <p><strong>Best Time:</strong> {park1['best_time']}</p>
                    <p class="mt-2"><strong>Key Animals:</strong></p>
                    <ul class="list-disc list-inside">
                        {"".join([f"<li>{animal}</li>" for animal in park1['animals'][:3]])}
                    </ul>
                </div>
                <div class="bg-green-50 p-3 rounded-lg">
                    <h4 class="font-bold text-lg">{parks_to_compare[1]}</h4>
                    <p><strong>Location:</strong> {park2['location']}</p>
                    <p><strong>Area:</strong> {park2['area']}</p>
                    <p><strong>Best Time:</strong> {park2['best_time']}</p>
                    <p class="mt-2"><strong>Key Animals:</strong></p>
                    <ul class="list-disc list-inside">
                        {"".join([f"<li>{animal}</li>" for animal in park2['animals'][:3]])}
                    </ul>
                </div>
            </div>
            <div class="mt-3 p-3 bg-blue-50 rounded-lg">
                <p class="font-semibold">Summary:</p>
                <p class="mt-1">{parks_to_compare[0]} is better for {random.choice(park1['highlights'])}, while {parks_to_compare[1]} is known for {random.choice(park2['highlights'])}.</p>
                <p class="mt-1">Both parks offer unique wildlife experiences in different regions of India.</p>
            </div>
            """
            
            return jsonify({
                "reply": f"""
                <div class="bg-indigo-100 border-l-4 border-indigo-500 p-4 rounded">
                    <h3 class="text-xl font-bold">Comparing {parks_to_compare[0]} and {parks_to_compare[1]}</h3>
                    {comparison_html}
                </div>
                """
            })
        else:
            return jsonify({
                "reply": """
                <div class="bg-yellow-100 border-l-4 border-yellow-500 p-4 rounded">
                    <p>I can compare two national parks for you. Try asking:</p>
                    <ul class="list-disc list-inside mt-2">
                        <li>Compare Jim Corbett and Ranthambore</li>
                        <li>Difference between Kaziranga and Sundarbans</li>
                    </ul>
                </div>
                """
            })
    
    # Park by state/region
    if "parks in" in user_input:
        state = user_input.replace("parks in", "").strip()
        parks_in_state = []
        
        for park_name, park_data in indian_national_parks.items():
            if state.lower() in park_data["location"].lower():
                parks_in_state.append(park_name)
        
        if parks_in_state:
            parks_list = "".join([f"""
                <li class="mb-2">
                    <strong>{park}</strong> - Best time: {indian_national_parks[park]['best_time']}
                </li>
            """ for park in parks_in_state])
            
            return jsonify({
                "reply": f"""
                <div class="bg-green-100 border-l-4 border-green-500 p-4 rounded">
                    <h3 class="text-xl font-bold">National Parks in {state.title()}</h3>
                    <ul class="list-disc list-inside mt-2">
                        {parks_list}
                    </ul>
                    <p class="mt-2">Ask about any park for more details!</p>
                </div>
                """
            })
        else:
            return jsonify({
                "reply": f"""
                <div class="bg-yellow-100 border-l-4 border-yellow-500 p-4 rounded">
                    <p>I couldn't find national parks specifically in {state}. Here are some popular parks in India:</p>
                    <ul class="list-disc list-inside mt-2">
                        <li>Jim Corbett National Park (Uttarakhand)</li>
                        <li>Kaziranga National Park (Assam)</li>
                        <li>Ranthambore National Park (Rajasthan)</li>
                    </ul>
                </div>
                """
            })
    
    # Unknown query response
    return jsonify({
        "reply": """
        <div class="bg-red-100 border-l-4 border-red-500 p-4 rounded">
            <p>I couldn't understand your query. Here's what I can help with:</p>
            <ul class="list-disc list-inside mt-2">
                <li>Information about any national park in India</li>
                <li>Wildlife animals and their conservation status</li>
                <li>Best time to visit parks</li>
                <li>Biodiversity hotspots</li>
                <li>Compare different national parks</li>
                <li>Find parks in specific states</li>
            </ul>
            <p class="mt-2">Try asking:</p>
            <ul class="list-disc list-inside">
                <li>"Tell me about Jim Corbett National Park"</li>
                <li>"Show elephants in India"</li>
                <li>"Compare Ranthambore and Bandhavgarh"</li>
                <li>"Parks in Karnataka"</li>
            </ul>
        </div>
        """
    })

if __name__ == "__main__":
    app.run(debug=True)