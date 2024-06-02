// VideoUploader.js
import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';


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
      <Button variant="dark" onClick={handleFileUpload}>Submit</Button>
    </div>
  );
};

export default VideoUploader;