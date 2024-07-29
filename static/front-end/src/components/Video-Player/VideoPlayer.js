import React from 'react';
import './VideoPlayer.css';

function highlightWords(text, words) {
  const regex = new RegExp(`(${words.join('|')})`, 'gi');
  return text.split(regex).map((part, index) =>
    words.includes(part.toLowerCase()) ? <mark key={index}>{part}</mark> : part
  );
}

function VideoPlayer({ video, caption, query, onNext, onPrev, videos, selectedVideoIndex, currentCaptionIndex }) {
  const startTime = caption ? caption.start_time : 0;

  return (
    <div className="video-player">
      <h2>{video.title}</h2>
      <iframe
        src={`https://www.youtube.com/embed/${video.video_id}?start=${startTime}`}
        frameBorder="0"
        allowFullScreen
        key={`${video.video_id}-${startTime}`} // key prop forces re-render on time change
        style={{width:"800px", height:"450px"}}
      ></iframe>
      {caption && (
        <div className="caption">
          {highlightWords(caption.text, query.split(' '))}
        </div>
      )}
      <div className="navigation">
        <button onClick={onPrev} disabled={selectedVideoIndex === 0 && currentCaptionIndex === 0}>Previous</button>
        <button onClick={onNext} disabled={selectedVideoIndex === videos.length - 1 && currentCaptionIndex === video.captions.length - 1}>Next</button>
      </div>
    </div>
  );
}

export default VideoPlayer;
