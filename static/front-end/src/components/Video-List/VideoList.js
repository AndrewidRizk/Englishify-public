import React from 'react';
import './VideoList.css';

function VideoList({ videos, onVideoSelect }) {
  return (
    <div className="video-list">
      {videos.map((video) => (
        <div key={video.video_id} onClick={() => onVideoSelect(video)} className="video-item">
          {video.title}
        </div>
      ))}
    </div>
  );
}

export default VideoList;
