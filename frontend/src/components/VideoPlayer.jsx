import React, { useState, useEffect } from "react";
import { uploadVideo, fetchStats } from "./api";
import StatsDisplay from "./StatsDisplay";
import VideoUploader from "./VideoUploader";
import loadingGif from "../assets/sb1.gif";

const VideoPlayer = () => {
  const [videoSrc, setVideoSrc] = useState("");
  const [stats, setStats] = useState({
    team1_passes: 0,
    team2_passes: 0,
    team1_possession_percentage: 0,
    team2_possession_percentage: 0,
  });
  const [isVideoPlaying, setIsVideoPlaying] = useState(false); // Track video playing status

  useEffect(() => {
    if (videoSrc) {
      const interval = setInterval(fetchStatsData, 1000); // Fetch stats every second
      return () => clearInterval(interval); // Cleanup interval on component unmount
    }
  }, [videoSrc]);

  const handleFileUpload = async (file, isDemo = false) => {
    try {
      if (!isDemo) {
        const videoPath = await uploadVideo(file);
        console.log("Path:::" + videoPath);
        setVideoSrc(
          `http://localhost:8000/video-feed?video_path=${encodeURIComponent(
            videoPath
          )}`
        );
      }
    } catch (error) {
      console.error(error);
    }
  };

  const fetchDemoVideo = async (demoNumber) => {
    try {
      setVideoSrc(`http://localhost:8000/video-feed`);
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

  const handleVideoPlay = () => {
    setIsVideoPlaying(true);
  };

  return (
    <div>
      <VideoUploader onUpload={handleFileUpload} onTryDemo={fetchDemoVideo} />
      <div>
        {!isVideoPlaying && !videoSrc ? (
          <div
            style={{
              width: "640px",
              height: "360px",
              position: "relative", // Add position relative for centering
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <img
              src={loadingGif}
              alt="Loading..."
              style={{
                width: "150px",
                height: "150px",
                objectFit: "contain",
              }}
            />
          </div>
        ) : (
          <div style={{ position: "relative" }}>
            {" "}
            {/* Add position relative for centering */}
            <img
              src={videoSrc}
              alt="Out of memory, please click reset or refresh the page."
              style={{
                width: "640px",
                height: "360px",
                display: "block",
                margin: "auto",
              }}
              onLoad={handleVideoPlay} // Trigger when the image (video) loads
            />
            {!isVideoPlaying && (
              <div
                style={{
                  position: "absolute",
                  top: "50%",
                  left: "50%",
                  transform: "translate(-50%, -50%)",
                  color: "white",
                  fontSize: "24px",
                  fontWeight: "bold",
                }}
              >
                Processing...
              </div>
            )}
          </div>
        )}
        <StatsDisplay stats={stats} />
      </div>
    </div>
  );
};

export default VideoPlayer;
