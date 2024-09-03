import React, { useState, useEffect } from 'react';
import './App.css';

const BASE_URL = 'http://127.0.0.1:5000';

function App() {
  const [pokemon, setPokemon] = useState(null);
  const [guess, setGuess] = useState('');
  const [hints, setHints] = useState({});
  const [attempts, setAttempts] = useState(0);
  const [message, setMessage] = useState('');
  const [startTime, setStartTime] = useState(null);

  useEffect(() => {
    fetchRandomPokemon();
  }, []);

  const fetchRandomPokemon = async () => {
    const response = await fetch(`${BASE_URL}/api/pokemon`);
    const data = await response.json();
    setPokemon(data);
    setStartTime(new Date());
    setAttempts(0);
    setHints({});
    setGuess('');
    setMessage('');
  };

  const handleGuess = async () => {
    if (!guess) return;

    const response = await fetch(`${BASE_URL}/api/guess`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ guess, pokemon_id: pokemon.id }),
    });
    const data = await response.json();

    setAttempts(attempts + 1);

    if (data.correct) {
      const endTime = new Date();
      const timeTaken = (endTime - startTime) / 1000;
      const minutes = Math.floor(timeTaken / 60);
      const seconds = Math.floor(timeTaken % 60);
      const score = Math.max(0, 100 - (attempts * 10) - (minutes * 2));

      setMessage(`Congratulations! You guessed the Pokémon correctly in ${attempts + 1} attempts.`);
      setMessage((prev) => `${prev} Time taken: ${minutes} minutes and ${seconds} seconds. Your score: ${score}`);
      setGuess('');
    } else {
      setHints(data);
      setGuess('');
      if (attempts + 1 === 8) {
        setMessage("Sorry, you've used all your attempts. Better luck next time!");
      }
    }
  };

  const renderHintBox = (hint, text) => (
    <div className={`hint-box ${hint ? 'yes' : 'no'}`}>
      {text}
    </div>
  );

  const renderSizeBox = (hint) => (
    <div className="hint-box">
      {hint === 'smaller' ? '⬇️' : hint === 'larger' ? '⬆️' : '⏺️'}
    </div>
  );

  return (
    <div className="App">
      <header className="App-header">
        <h1>Guess the Pokémon!</h1>
        {pokemon && (
          <div>
          </div>
        )}
        <input
          type="text"
          value={guess}
          onChange={(e) => setGuess(e.target.value)}
          placeholder="Enter your guess"
        />
        <button onClick={handleGuess}>Submit Guess</button>
        {message && <p>{message}</p>}
        <div className="hints-container">
          {hints.type1 !== undefined && renderHintBox(hints.type1, 'Type 1')}
          {hints.type2 !== undefined && renderHintBox(hints.type2, 'Type 2')}
          {hints.generation !== undefined && renderHintBox(hints.generation, 'Generation')}
          {hints.evolution_stage !== undefined && renderHintBox(hints.evolution_stage, 'Evolution Stage')}
          {hints.size !== undefined && renderSizeBox(hints.size)}
        </div>
      </header>
    </div>
  );
}

export default App;
