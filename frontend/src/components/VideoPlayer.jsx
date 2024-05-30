import React from 'react';

const VideoPlayer = () => {
  return (
    <div>
      <h2>Video Player</h2>
      <video width="640" height="360" controls>
        <source src="http://localhost:8000/video" type="video/mp4" />
        Your browser does not support the video tag.
      </video>
    </div>
  );
}

export default VideoPlayer;
