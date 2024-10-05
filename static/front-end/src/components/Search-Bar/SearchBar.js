import React, { useState, useEffect, useRef } from 'react';
import './SearchBar.css';

// Define stopwords outside the component to avoid re-creation on each render
const STOP_WORDS = [
  "of", "in", "is", "are", "for", "not", "i", "to", "the", "a", "an", "on", "and", "as", "but", "by", 
  "with", "was", "were", "it", "that", "at", "this", "which", "from"
];

function SearchBar({ onSearch, loading, isSearching }) {
  const [query, setQuery] = useState('');
  const inputRef = useRef();

  // Set focus on the input field when the component loads
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  const handleSearch = () => {
    const words = query.trim().split(/\s+/);

    // Check if the query is empty or a single word that is a stopword
    if (words.length === 1 && STOP_WORDS.includes(words[0].toLowerCase())) {
      alert(`"${words[0]}" is a very common word and cannot be searched alone. Please add more words or use a more specific term.`);
      return;
    }

    // If the query is empty, show a specific alert
    if (!query.trim()) {
      alert("Please enter a word or phrase to search.");
      return;
    }

    // Proceed with search if input is valid and loading is not active
    if (!loading) onSearch(query);
  };

  return (
    <div className={`search-bar-container ${isSearching ? 'search-bar-container-shifted' : ''}`}>
      {/* Logo/Title above the search bar */}
      <h1 className={`site-title ${isSearching ? 'site-title-small' : ''}`}>Englishify</h1>
      
      {/* Search Bar */}
      <div className={`search-bar ${isSearching ? 'search-bar-animate' : ''}`}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search for a word or phrase"
          required
          ref={inputRef} // Set ref to the input for auto-focus
        />
        <button onClick={handleSearch} disabled={loading}>
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>
    </div>
  );
}

export default SearchBar;
