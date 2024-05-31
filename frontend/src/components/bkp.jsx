import React, { useState, useEffect } from 'react';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

const VideoPlayer = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [videoSrc, setVideoSrc] = useState('');
  const [stats, setStats] = useState({
    team1_passes: 0,
    team2_passes: 0,
    team1_possession_percentage: 0,
    team2_possession_percentage: 0,
  });

  useEffect(() => {
    if (videoSrc) {
      const interval = setInterval(fetchStats, 1000); // Fetch stats every second
      return () => clearInterval(interval); // Cleanup interval on component unmount
    }
  }, [videoSrc]);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleFileUpload = async () => {
    if (!selectedFile) {
      console.error('No file selected');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://localhost:8000/upload-video', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        const videoPath = encodeURIComponent(data.video_path);
        setVideoSrc(`http://localhost:8000/video-feed?video_path=${videoPath}`);
      } else {
        console.error('Failed to upload video');
      }
    } catch (error) {
      console.error('Error uploading video:', error);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await fetch('http://localhost:8000/data');
      if (response.ok) {
        const data = await response.json();
        setStats(data);
      } else {
        console.error('Failed to fetch stats');
      }
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  // Calculate the percentage for team 2
  const team2_possession_percentage = 100 - stats.team1_possession_percentage;

  return (
    <div>
      <h2>Video Player</h2>
      <input type="file" accept="video/*" onChange={handleFileChange} />
      <button onClick={handleFileUpload}>Submit</button>
      {videoSrc && (
        <div>
          <img
            src={videoSrc}
            alt="Real-time video stream"
            style={{ width: '640px', height: '360px', display: 'block', margin: 'auto' }}
          />
          <div>
            <h3>Real-time Stats</h3>
            <p>Team 1 Passes: {stats.team1_passes}</p>
            <p>Team 2 Passes: {stats.team2_passes}</p>
            <div style={{ display: 'flex', justifyContent: 'space-around', marginTop: '20px' }}>
              <div style={{ width: '100px', height: '100px' }}>
                <CircularProgressbar
                  value={stats.team1_possession_percentage}
                  text={`${Math.round(stats.team1_possession_percentage)}%`}
                  styles={buildStyles({
                    textSize: '16px',
                    pathColor: `rgba(62, 152, 199, ${stats.team1_possession_percentage / 100})`,
                    textColor: '#f88',
                    trailColor: '#d6d6d6',
                    backgroundColor: '#3e98c7',
                  })}
                />
                <p style={{ textAlign: 'center' }}>Team 1 Possession</p>
              </div>
              <div style={{ width: '100px', height: '100px' }}>
                <CircularProgressbar
                  value={team2_possession_percentage}
                  text={`${Math.round(team2_possession_percentage)}%`}
                  styles={buildStyles({
                    textSize: '16px',
                    pathColor: `rgba(62, 152, 199, ${team2_possession_percentage / 100})`,
                    textColor: '#f88',
                    trailColor: '#d6d6d6',
                    backgroundColor: '#3e98c7',
                  })}
                />
                <p style={{ textAlign: 'center' }}>Team 2 Possession</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default VideoPlayer;