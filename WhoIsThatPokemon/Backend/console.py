import requests
import time

# Configuration
BASE_URL = "http://127.0.0.1:5000"

# Fetch a random Pokémon
def fetch_random_pokemon():
    response = requests.get(f"{BASE_URL}/api/pokemon")
    return response.json()

# Validate the guess and get hints
def validate_guess(guess, pokemon_id):
    response = requests.post(f"{BASE_URL}/api/guess", json={'guess': guess, 'pokemon_id': pokemon_id})
    return response.json()

def main():
    # Fetch the random Pokémon at the beginning
    pokemon_clue = fetch_random_pokemon()
    pokemon_id = pokemon_clue['id']
    print("Guess the Pokémon!")
    
    start_time = time.time()
    max_attempts = 8
    attempts = 0

    while attempts < max_attempts:
        guess = input("Enter your guess: ")
        attempts += 1
        
        result = validate_guess(guess, pokemon_id)
        
        if result.get('error'):
            print("Error:", result['error'])
            continue
        
        if result['correct']:
            end_time = time.time()
            time_taken = end_time - start_time
            minutes = int(time_taken // 60)
            seconds = int(time_taken % 60)
            score = max(0, 100 - (attempts * 10) - minutes * 2)
            print(f"Congratulations! You guessed the Pokémon correctly in {attempts} attempts.")
            print(f"Time taken: {minutes} minutes and {seconds} seconds.")
            print(f"Your score: {score}")
            break
        else:
            print("Incorrect guess. Here are your hints:")
            print(f"Type1 matches: {'Yes' if result['type1'] else 'No'}")
            print(f"Type2 matches: {'Yes' if result['type2'] else 'No'}")
            print(f"Generation matches: {'Yes' if result['generation'] else 'No'}")
            print(f"Evolution stage matches: {'Yes' if result['evolution_stage'] else 'No'}")
            print(f"Size comparison: {result['size']}")

    if attempts == max_attempts:
        print("Sorry, you've used all your attempts. Better luck next time!")

if __name__ == "__main__":
    main()
