// VideoUploader.js
import React, { useState } from 'react';



const VideoUploader = ({ onUpload }) => {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleFileUpload = () => {
    if (!selectedFile) {
      console.error('No file selected');
      return;
    }
    onUpload(selectedFile);
  };

  return (
    <div>
      <input type="file" accept="video/*" onChange={handleFileChange} />
      <button onClick={handleFileUpload}>Submit</button>
    </div>
  );
};

export default VideoUploader;
