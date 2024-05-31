// VideoPlayer.js
import React, { useState, useEffect } from 'react';
import { uploadVideo, fetchStats } from './api';
import StatsDisplay from './StatsDisplay';
import VideoUploader from './VideoUploader';

const VideoPlayer = () => {
  const [videoSrc, setVideoSrc] = useState('');
  const [stats, setStats] = useState({
    team1_passes: 0,
    team2_passes: 0,
    team1_possession_percentage: 0,
    team2_possession_percentage: 0,
  });

  useEffect(() => {
    if (videoSrc) {
      const interval = setInterval(fetchStatsData, 1000); // Fetch stats every second
      return () => clearInterval(interval); // Cleanup interval on component unmount
    }
  }, [videoSrc]);

  const handleFileUpload = async (file) => {
    try {
      const videoPath = await uploadVideo(file);
      setVideoSrc(`http://localhost:8000/video-feed?video_path=${encodeURIComponent(videoPath)}`);
    } catch (error) {
      console.error(error);
    }
  };

  const fetchStatsData = async () => {
    try {
      const statsData = await fetchStats();
      setStats(statsData);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h2>Video Player</h2>
      <VideoUploader onUpload={handleFileUpload} />
      {videoSrc && (
        <div>
          <img
            src={videoSrc}
            alt="Real-time video stream"
            style={{ width: '640px', height: '360px', display: 'block', margin: 'auto' }}
          />
          <StatsDisplay stats={stats} />
        </div>
      )}
    </div>
  );
};

export default VideoPlayer;
