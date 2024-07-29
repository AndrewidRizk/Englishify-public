import React, { useState } from 'react';
import SearchBar from './components/Search-Bar/SearchBar.js';
import VideoPlayer from './components/Video-Player/VideoPlayer.js';
import Navbar from './components/Nav-bar/Navbar.js';

function App() {
  const [videos, setVideos] = useState([]);
  const [selectedVideoIndex, setSelectedVideoIndex] = useState(0);
  const [currentCaptionIndex, setCurrentCaptionIndex] = useState(0);
  const [query, setQuery] = useState('');

  const searchVideos = async (query) => {
    setVideos([]); // Clear previous results
    setSelectedVideoIndex(0);
    setCurrentCaptionIndex(0);
    setQuery(query);

    const response = await fetch(`http://127.0.0.1:5000/api/search?query=${query}`);
    const data = await response.json();
    setVideos(data.videos);
    if (data.videos.length > 0) {
      setSelectedVideoIndex(0);
      setCurrentCaptionIndex(0);
    }
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
  const currentCaption = currentVideo ? currentVideo.captions[currentCaptionIndex] : null;

  return (
    <div className="App">
      <Navbar />
      <div className="main-content">
        <SearchBar onSearch={searchVideos} />
        {currentVideo && (
          <VideoPlayer
            video={currentVideo}
            caption={currentCaption}
            query={query}
            onNext={nextCaption}
            onPrev={prevCaption}
            videos={videos}
            selectedVideoIndex={selectedVideoIndex}
            currentCaptionIndex={currentCaptionIndex}
          />
        )}
      </div>
    </div>
  );
}

export default App;
