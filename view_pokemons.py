import json

# Function to load Pokémon data from the JSON file
def load_pokemon_data(file_path="pokemon_data.json"):
    try:
        with open(file_path, 'r') as file:
            pokemon_data = json.load(file)
            return pokemon_data
    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
        return []
    except json.JSONDecodeError:
        print(f"The file '{file_path}' is not in a valid JSON format.")
        return []

# Function to display all Pokémon
def display_pokemon_data(pokemon_data):
    if pokemon_data:
        print("\nSaved Pokémon:")
        for idx, pokemon in enumerate(pokemon_data, start=1):
            print(f"{idx}. Name: {pokemon['name']}, Height: {pokemon['height']}, Weight: {pokemon['weight']}")
    else:
        print("\nNo Pokémon found in the file.")

# Main function to view Pokémon data
def main():
    print("Viewing saved Pokémon...")
    pokemon_data = load_pokemon_data()  # Load Pokémon data from the JSON file
    display_pokemon_data(pokemon_data)  # Display the loaded data

if __name__ == "__main__":
    main()
