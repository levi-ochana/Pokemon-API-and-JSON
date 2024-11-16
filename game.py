import requests
import json
import random
import os
from view_pokemons import fetch_pokemon_list, fetch_pokemon_details, check_pokemon_in_file, save_pokemon_to_file, set_permissions, print_pokemon_details, display_saved_pokemon, check_response_status



# Main function to run the game
def main():
    print("Welcome to the Pokémon game!")
    while True:
        print("\nOptions:")
        print("1. Draw a Pokémon")
        print("2. View all saved Pokémon")
        print("3. Exit")
        
        user_input = input("Choose an option (1/2/3): ").strip()
        
        if user_input == "1":
            print("Game start!")
            pokemon_list = fetch_pokemon_list(limit=5)  # Fetch a list of Pokémon
            if pokemon_list:
                # Fetch details for each Pokémon
                pokemon_details_list = [fetch_pokemon_details(pokemon['url']) for pokemon in pokemon_list if fetch_pokemon_details(pokemon['url'])]

                # Display fetched Pokémon names
                print("Pokémon names retrieved:")
                for pokemon in pokemon_details_list:
                    print(pokemon['name'])  # Display names

                # Choose a random Pokémon
                random_pokemon = random.choice(pokemon_details_list)  
                pokemon_name = random_pokemon['name']

                # Check if the random Pokémon already exists in the file
                set_permissions()
                exists, existing_pokemon = check_pokemon_in_file(pokemon_name)
                if exists:
                    print(f"\n{pokemon_name} already exists in the file.")
                    # Display existing Pokémon details
                    print_pokemon_details(existing_pokemon)
                else:
                    save_pokemon_to_file(random_pokemon)  # Save new Pokémon to the file
                    print(f"\nRandom Pokémon added:")
                    print_pokemon_details(random_pokemon)
            continue
        elif user_input == "2":
            display_saved_pokemon()  # Display all saved Pokémon
        elif user_input == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
