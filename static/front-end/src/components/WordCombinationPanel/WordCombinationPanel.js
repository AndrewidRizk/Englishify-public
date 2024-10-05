import React from 'react';
import './WordCombinationPanel.css';

function WordCombinationPanel({ combinations, onCombinationClick, loading }) {
  return (
    <div className="word-combination-container">
      {combinations.map((combination, index) => (
        <button
          key={index}
          className="word-combination-button"
          onClick={() => onCombinationClick(combination)}
        >
          {combination}
        </button>
      ))}
      {/* Show loading spinner if fetching more combinations */}
      {loading && <div className="loading-spinner"></div>}
    </div>
  );
}

export default WordCombinationPanel;
