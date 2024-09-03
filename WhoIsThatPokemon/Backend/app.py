from flask import Flask, request, jsonify
import random
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# Sample Pokémon data with additional attributes
pokemon_data = [
    {'id': 1, 'name': 'Bulbasaur', 'type1': 'Grass', 'type2': 'Poison', 'generation': 1, 'evolution_stage': 1, 'size': 0.7},
    {'id': 2, 'name': 'Ivysaur', 'type1': 'Grass', 'type2': 'Poison', 'generation': 1, 'evolution_stage': 2, 'size': 1.0},
    {'id': 3, 'name': 'Venusaur', 'type1': 'Grass', 'type2': 'Poison', 'generation': 1, 'evolution_stage': 3, 'size': 2.0},
    {'id': 4, 'name': 'Charmander', 'type1': 'Fire', 'type2': None, 'generation': 1, 'evolution_stage': 1, 'size': 0.6},
    {'id': 5, 'name': 'Charmeleon', 'type1': 'Fire', 'type2': None, 'generation': 1, 'evolution_stage': 2, 'size': 1.1},
    {'id': 6, 'name': 'Charizard', 'type1': 'Fire', 'type2': 'Flying', 'generation': 1, 'evolution_stage': 3, 'size': 1.7},
    # Add more Pokémon data here
]

@app.route('/api/pokemon', methods=['GET'])
def get_random_pokemon():
    random_pokemon = random.choice(pokemon_data)
    # Exclude the name to avoid giving away the answer
    pokemon_clue = {key: value for key, value in random_pokemon.items() if key != 'name'}
    return jsonify(pokemon_clue)

@app.route('/api/guess', methods=['POST'])
def validate_guess():
    data = request.get_json()
    guess = data.get('guess')
    pokemon_id = data.get('pokemon_id')
    
    guessed_pokemon = next((p for p in pokemon_data if p['name'].lower() == guess.lower()), None)
    target_pokemon = next((p for p in pokemon_data if p['id'] == pokemon_id), None)

    if not guessed_pokemon or not target_pokemon:
        return jsonify({'error': 'Invalid guess or Pokémon ID'}), 400

    hints = {
        'correct': guessed_pokemon['id'] == target_pokemon['id'],
        'type1': guessed_pokemon['type1'] == target_pokemon['type1'],
        'type2': guessed_pokemon['type2'] == target_pokemon['type2'],
        'generation': guessed_pokemon['generation'] == target_pokemon['generation'],
        'evolution_stage': guessed_pokemon['evolution_stage'] == target_pokemon['evolution_stage'],
        'size': ('smaller' if guessed_pokemon['size'] < target_pokemon['size'] else 'larger') if guessed_pokemon['size'] != target_pokemon['size'] else 'equal'
    }

    return jsonify(hints)

if __name__ == '__main__':
    app.run(debug=True)
