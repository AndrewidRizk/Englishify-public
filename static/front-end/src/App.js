import React, { useState, useEffect } from 'react';
import SearchBar from './components/Search-Bar/SearchBar.js';
import VideoPlayer from './components/Video-Player/VideoPlayer.js';
import Navbar from './components/Nav-bar/Navbar.js';
import Footer from './components/Footer/Footer.js';
import HistoryPanel from './components/HistoryPanel/HistoryPanel';
import WordCombinationPanel from './components/WordCombinationPanel/WordCombinationPanel';
import './App.css';
import Modal from './components/Modal/Modal.js';

const STOP_WORDS = ['of', 'in', 'the', 'and', 'is', 'are', 'for', 'to', 'a', 'an', ' '];

function App() {
  const [videos, setVideos] = useState([]);
  const [history, setHistory] = useState([]);
  const [selectedVideoIndex, setSelectedVideoIndex] = useState(0);
  const [currentCaptionIndex, setCurrentCaptionIndex] = useState(0);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [isSearching, setIsSearching] = useState(false);
  const [combinations, setCombinations] = useState([]);
  const [loadingCombinations, setLoadingCombinations] = useState(false);
  const [showModal, setShowModal] = useState(false); // Modal state


  // Show a sample search suggestion on first load
  useEffect(() => {
    const visitedBefore = localStorage.getItem('visited');
    if (!visitedBefore) {
      const userResponse = window.confirm('Welcome to Englishify! Try searching for "piece of cake" to see an example.');
      if (userResponse) {
        searchVideos('piece of cake');
      }
      localStorage.setItem('visited', true);
    }
  }, []);

    // Show a sample search suggestion on first load
    useEffect(() => {
      const visitedBefore = localStorage.getItem('visited');
      if (!visitedBefore) {
        setShowModal(true);
      }
    }, []);
  
    const handleModalConfirm = () => {
      setShowModal(false);
      localStorage.setItem('visited', 'true');
      searchVideos('piece of cake'); // Search for the suggested phrase
    };
  
    const handleModalClose = () => {
      setShowModal(false);
      localStorage.setItem('visited', 'true');
    };

  // Generate word combinations
  const generateCombinations = (words) => {
    const result = new Set();
    words.forEach((word) => {
      if (!STOP_WORDS.includes(word.toLowerCase())) {
        result.add(word.toLowerCase());
      }
    });
    for (let i = 0; i < words.length; i++) {
      for (let j = i + 1; j <= words.length; j++) {
        const combination = words.slice(i, j).join(' ').trim();
        if (!STOP_WORDS.includes(combination) && combination.length > 1) {
          result.add(combination.toLowerCase());
        }
      }
    }
    return Array.from(result).slice(0, 8);
  };

  const searchVideos = async (query) => {
    setLoading(true);
    setIsSearching(true);
    setVideos([]);
    setSelectedVideoIndex(0);
    setCurrentCaptionIndex(0);
    setQuery(query);

    // Main search request
    const response = await fetch(`http://127.0.0.1:5000/api/search?query=${query}`);
    const data = await response.json();
    const mainSearchHasResults = data.videos.length > 0;

    // Set the main query videos
    setVideos(data.videos);
    setLoading(mainSearchHasResults ? false : true); // Keep loading if no results

    // Only add the main search to history if:
    // 1. It has results.
    // 2. Or it has multiple words (for a single word without results, skip).
    if (mainSearchHasResults || query.trim().split(/\s+/).length > 1) {
      addToHistory(query, data.videos);
    }

    // Generate combinations and fetch them
    const words = query.trim().split(/\s+/);
    let combinationsList = generateCombinations(words);
    combinationsList = combinationsList.filter((item) => item !== query.toLowerCase());

    fetchValidCombinations([query, ...combinationsList], mainSearchHasResults);
  };

  // Add a valid search to history
  const addToHistory = (query, videos) => {
    const totalInstances = videos.reduce((total, video) => total + video.captions.length, 0);
    setHistory((prevHistory) => {
      const exists = prevHistory.find((item) => item.query === query);
      if (!exists) {
        return [...prevHistory, { query, videos, instances: totalInstances }];
      }
      return prevHistory;
    });
  };

  // Fetch combinations and handle fallback scenarios
  const fetchValidCombinations = async (combinationsList, mainSearchHasResults) => {
    setCombinations([]);
    const uniqueCombinations = new Set();
    const validCombinations = [];
    setLoadingCombinations(true);

    for (let i = 0; i < combinationsList.length; i++) {
      const combination = combinationsList[i];
      if (uniqueCombinations.has(combination)) continue;
      uniqueCombinations.add(combination);

      const response = await fetch(`http://127.0.0.1:5000/api/search?query=${combination}`);
      const data = await response.json();

      if (data.videos && data.videos.length > 0) {
        validCombinations.push(combination);
        setCombinations((prevCombinations) => [...prevCombinations, combination]);
      }

      if (!mainSearchHasResults && validCombinations.length === 1) {
        setQuery(validCombinations[0]);
        setVideos(data.videos);
        setLoading(false);
      }
    }
    setLoadingCombinations(false);
    if (!mainSearchHasResults && validCombinations.length === 0) {
      setLoading(false); // Stop loading if no combinations found
    }
  };

  const handleHistorySearch = (query) => {
    setQuery(query);
    searchVideos(query);
  };

  const handleCombinationClick = async (combination) => {
    setLoading(true);
    const response = await fetch(`http://127.0.0.1:5000/api/search?query=${combination}`);
    const data = await response.json();
    setLoading(false);
    setQuery(combination);
    setVideos(data.videos);
  };

  const nextCaption = () => {
    const video = videos[selectedVideoIndex];
    if (video && currentCaptionIndex < video.captions.length - 1) {
      setCurrentCaptionIndex(currentCaptionIndex + 1);
    } else if (selectedVideoIndex < videos.length - 1) {
      setSelectedVideoIndex(selectedVideoIndex + 1);
      setCurrentCaptionIndex(0);
    }
  };

  const prevCaption = () => {
    if (currentCaptionIndex > 0) {
      setCurrentCaptionIndex(currentCaptionIndex - 1);
    } else if (selectedVideoIndex > 0) {
      setSelectedVideoIndex(selectedVideoIndex - 1);
      setCurrentCaptionIndex(videos[selectedVideoIndex - 1].captions.length - 1);
    }
  };

  const currentVideo = videos[selectedVideoIndex];
  const totalInstances = videos.reduce((total, video) => total + video.captions.length, 0);

  return (
    <div className="App">
      <Navbar />
      <Modal
        show={showModal}
        onClose={handleModalClose}
        onConfirm={handleModalConfirm}
        title="Welcome to Englishify"
        message="Try searching for 'piece of cake' to see a fun example!"
      />
      <div className="main-content-container">
        <HistoryPanel history={history} onSearch={handleHistorySearch} />
        <div className={`main-content ${isSearching ? 'shifted-content' : ''}`}>
          <SearchBar onSearch={searchVideos} loading={loading} isSearching={isSearching} query={query} />
          {combinations.length > 0 && (
            <WordCombinationPanel
              combinations={combinations}
              onCombinationClick={handleCombinationClick}
              loading={loadingCombinations}
            />
          )}
          {loading && (
            <div className="loader">
              <div className="lds-ring"><div></div><div></div><div></div><div></div></div>
            </div>
          )}
          {videos.length > 0 && (
            <VideoPlayer
              video={currentVideo}
              query={query}
              onNext={nextCaption}
              onPrev={prevCaption}
              videos={videos}
              selectedVideoIndex={selectedVideoIndex}
              currentCaptionIndex={currentCaptionIndex}
              totalInstances={totalInstances}
            />
          )}
        </div>
      </div>
      <Footer />
    </div>
  );
}

export default App;
