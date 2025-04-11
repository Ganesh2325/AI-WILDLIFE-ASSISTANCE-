parks_db = {
    "Kaziranga National Park": ["Indian Rhinoceros", "Elephants", "Swamp Deer"],
    "Jim Corbett National Park": ["Bengal Tiger", "Leopard", "Elephant"],
    "Sundarbans National Park": ["Royal Bengal Tiger", "Fishing Cat", "Saltwater Crocodile"],
    "Gir National Park": ["Asiatic Lion", "Hyena", "Chinkara"],
    # Add more parks here
}

def get_wildlife_for_park(park_name):
    return parks_db.get(park_name.strip(), [])
