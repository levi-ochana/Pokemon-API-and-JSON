import json
import random
import requests
import os



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
            # If the file is empty, return False immediately
            if file.read(1) == '':
                return False, None  # Empty file, no Pokémon found
            file.seek(0)  # Reset the cursor to the beginning of the file
            pokemon_data = json.load(file)
            for pokemon in pokemon_data:
                if pokemon['name'] == pokemon_name:
                    return True, pokemon  # Pokémon found
            return False, None  # Pokémon not found
    except FileNotFoundError:
        return False, None  # File not found, treat as if no Pokémon exist
    except json.JSONDecodeError:
        # If the file is not valid JSON, return False
        print(f"Error: The file {file_path} is not a valid JSON.")
        return False, None

# Function to save Pokémon details to a JSON file
def save_pokemon_to_file(pokemon):
    file_path = 'saved_pokemons.json'
    
    # If the file doesn't exist, initialize it
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump([], file)  # Initialize the file with an empty list

    # Read existing data from the file
    with open(file_path, 'r') as file:
        try:
            pokemon_data = json.load(file)
        except json.JSONDecodeError:
            pokemon_data = []

    # Add the new Pokémon to the list
    pokemon_data.append(pokemon)

    # Save the updated data
    with open(file_path, 'w') as file:
        json.dump(pokemon_data, file, indent=4)
        
# Function to print Pokémon details
def print_pokemon_details(pokemon):
    print(f"Name: {pokemon['name']}, Height: {pokemon['height']}, Weight: {pokemon['weight']}")

# Function to display all saved Pokémon
def display_saved_pokemon():
    file_path = 'saved_pokemons.json'

    # Check if the file exists
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        print("No saved Pokémon.")
        return

    # Read the Pokémon data from the file
    with open(file_path, 'r') as file:
        try:
            pokemon_data = json.load(file)
            if len(pokemon_data) == 0:
                print("No saved Pokémon.")
            else:
                print("Saved Pokémon:")
                for pokemon in pokemon_data:
                    print(pokemon['name'])
        except json.JSONDecodeError:
            print("Error reading saved Pokémon data.")
