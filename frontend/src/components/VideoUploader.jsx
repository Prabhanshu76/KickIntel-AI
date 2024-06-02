import React, { useState } from "react";

const VideoUploader = ({ onUpload }) => {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    if (file) {
      handleFileUpload(file);
    }
  };

  const handleFileUpload = (file) => {
    if (!file) {
      console.error("No file selected");
      return;
    }
    onUpload(file);
  };

  return (
    <div>
      <input type="file" accept="video/*" onChange={handleFileChange} />
    </div>
  );
};

export default VideoUploader;
