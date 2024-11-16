import requests
import json
import os

# Function to check the status of the response
def check_response_status(response):
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error getting data: {response.status_code}")
        return None

# Function to fetch a list of Pokémon
def fetch_pokemon_list(limit=5):
    offset = random.randint(0, 1010 - limit)  # Random starting point
    url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}"
    response = requests.get(url)
    data = check_response_status(response)
    return data.get('results', []) if data else None

# Function to fetch Pokémon details by URL
def fetch_pokemon_details(pokemon_url):
    response = requests.get(pokemon_url)
    data = check_response_status(response)
    if data:
        return {
            "name": data['name'],
            "height": data['height'],
            "weight": data['weight']
        }
    return None

# Updates the file permissions to read and write for all users.
def set_permissions(file_path="pokemon_data.json"):
    if not os.path.exists(file_path):
        open(file_path, 'w').close()  # Creates an empty file if it doesn't exist
    os.chmod(file_path, 0o666)  # Set read and write permissions for all users

# Function to check if a Pokémon exists in the JSON file
def check_pokemon_in_file(pokemon_name, file_path="pokemon_data.json"):
    try:
        with open(file_path, 'r') as file:
            pokemon_data = json.load(file)
            for pokemon in pokemon_data:
                if pokemon['name'] == pokemon_name:
                    return True, pokemon  # Pokémon found
            return False, None  # Pokémon not found
    except FileNotFoundError:
        return False, None  # File not found, treat as if no Pokémon exist

# Function to save Pokémon details to a JSON file
def save_pokemon_to_file(pokemon_details, file_path="pokemon_data.json"):
    try:
        with open(file_path, 'r+') as file:
            pokemon_data = json.load(file)
            pokemon_data.append(pokemon_details)  # Append new Pokémon details
            file.seek(0)  # Move cursor back to the start of the file
            json.dump(pokemon_data, file, indent=2)
    except FileNotFoundError:
        with open(file_path, 'w') as file:
            json.dump([pokemon_details], file, indent=2)  # Create a new file

# Function to print Pokémon details
def print_pokemon_details(pokemon):
    print(f"Name: {pokemon['name']}, Height: {pokemon['height']}, Weight: {pokemon['weight']}")

# Function to display all saved Pokémon
def display_saved_pokemon(file_path="pokemon_data.json"):
    try:
        with open(file_path, 'r') as file:
            pokemon_data = json.load(file)
            print("\nSaved Pokémon:")
            for idx, pokemon in enumerate(pokemon_data, start=1):
                print(f"{idx}. Name: {pokemon['name']}, Height: {pokemon['height']}, Weight: {pokemon['weight']}")
    except FileNotFoundError:
        print("\nNo Pokémon saved yet.")
