import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [inputText, setInputText] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [lastTyped, setLastTyped] = useState(null);

  useEffect(() => {
    const fetchSuggestions = async () => {
      if (inputText.trim()) {
        try {
          // Update the URL to point to your deployed backend on Vercel
          const response = await fetch(`https://<your-vercel-project-name>.vercel.app/api/suggest?input=${inputText}`);
          const data = await response.json();
          setSuggestions(data.suggestions);
        } catch (error) {
          console.error("Error fetching suggestions:", error);
        }
      } else {
        setSuggestions([]);
      }
    };

    fetchSuggestions();
  }, [inputText]);

  const handleChange = (e) => {
    const newText = e.target.value;
    setInputText(newText);
    const lastChar = newText[newText.length - 1]?.toLowerCase();
    setLastTyped(lastChar);
  };

  const handleSuggestionClick = (suggestion) => {
    setInputText((prev) => prev + ' ' + suggestion);
    setSuggestions([]);
  };

  const handleKeyClick = (key) => {
    if (key === 'remove') {
      setInputText((prev) => prev.slice(0, -1)); // Remove the last character
    } else if (key === 'space') {
      setInputText((prev) => prev + ' '); // Add a space
    } else {
      setInputText((prev) => prev + key); // Add the typed character
    }
    setLastTyped(key.toLowerCase());
  };

  const renderKeyboard = () => {
    const rows = [
      ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
      ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
      ['z', 'x', 'c', 'v', 'b', 'n', 'm'],
      ['space', 'remove'] // Replace 'return' with 'remove'
    ];

    return rows.map((row, rowIndex) => (
      <div key={rowIndex} className="keyboard-row">
        {row.map((key, keyIndex) => (
          <div
            key={keyIndex}
            className={`key ${key === lastTyped ? 'active' : ''} ${key === 'space' ? 'space' : ''} ${key === 'remove' ? 'remove' : ''}`}
            onClick={() => handleKeyClick(key)}
          >
            {key === 'space' ? 'Space' : key === 'remove' ? 'Remove' : key}
          </div>
        ))}
      </div>
    ));
  };

  return (
    <div className="App">
      <div className="keyboard-container">
        <header className="App-header">
          <h1>Lexichain</h1>

          {suggestions.length > 0 && (
            <div className="suggestions-list">
              {suggestions.map((suggestion, index) => (
                <div
                  key={index}
                  className="suggestion-item"
                  onClick={() => handleSuggestionClick(suggestion)}
                >
                  {suggestion}
                </div>
              ))}
            </div>
          )}

          <input
            type="text"
            value={inputText}
            onChange={handleChange}
            placeholder="Start typing..."
            className="input-field"
          />

          <div className="virtual-keyboard">
            {renderKeyboard()}
          </div>
        </header>
      </div>
    </div>
  );
}

export default App;
