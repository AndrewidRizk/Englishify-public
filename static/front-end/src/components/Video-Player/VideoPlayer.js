import React, { useEffect } from 'react';
import './VideoPlayer.css';
import { FaChevronLeft, FaChevronRight } from "react-icons/fa"; // Import arrow icons

function highlightWords(text, words) {
  const regex = new RegExp(`(${words.join('|')})`, 'gi');
  return text.split(regex).map((part, index) =>
    words.includes(part.toLowerCase()) ? <mark key={index}>{part}</mark> : part
  );
}

function VideoPlayer({ video, query, onNext, onPrev, videos, selectedVideoIndex, currentCaptionIndex, totalInstances }) {
  // Calculate the current global position across all captions
  const currentInstance = videos
    .slice(0, selectedVideoIndex)
    .reduce((acc, video) => acc + video.captions.length, 0) + currentCaptionIndex + 1;

  const startTime = video.captions[currentCaptionIndex]?.start_time || 0;
  const videoUrl = `https://www.youtube.com/watch?v=${video.video_id}&t=${Math.floor(startTime)}s`;

  const copyLink = () => {
    navigator.clipboard.writeText(videoUrl);
    alert('Link copied to clipboard!');
  };

  return (
    <div className="video-player-container">
      {/* Video Controls */}
      <div className="video-info">
        <button onClick={copyLink} className="copy-link-btn">Copy Link</button>
        <div className="instance-counter">
          Instance {currentInstance} of {totalInstances}
        </div>
      </div>

      {/* Video Player */}
      <iframe
        src={`https://www.youtube.com/embed/${video.video_id}?start=${startTime}`}
        frameBorder="0"
        allowFullScreen
        key={`${video.video_id}-${startTime}`}  // key prop forces re-render on time change
        className="video-frame"
      ></iframe>

      {/* Caption Display */}
      {video.captions && (
        <div className="caption-container">
          <div className="caption">
            {highlightWords(video.captions[currentCaptionIndex].text, query.split(' '))}
          </div>
        </div>
      )}

      {/* Navigation Buttons in a New Row */}
      <div className="navigation">
        <button onClick={onPrev} disabled={selectedVideoIndex === 0 && currentCaptionIndex === 0} className="nav-btn-left">
          <FaChevronLeft /> {/* Left arrow icon */}
        </button>
        <button onClick={onNext} disabled={selectedVideoIndex === videos.length - 1 && currentCaptionIndex === video.captions.length - 1} className="nav-btn-right">
          <FaChevronRight /> {/* Right arrow icon */}
        </button>
      </div>
    </div>
  );
}

export default VideoPlayer;
