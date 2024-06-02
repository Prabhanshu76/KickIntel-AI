import React, { useState } from "react";
import { FaSyncAlt } from "react-icons/fa";
import { copyDemoVideo } from "./api";

const VideoUploader = ({ onUpload, onTryDemo }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [buttonsDisabled, setButtonsDisabled] = useState(false);

  const handleFileUpload = (file) => {
    if (!file) {
      console.error("No file selected");
      return;
    }
    console.log("Uploading file:", file);
    onUpload(file);
  };

  const handleReset = () => {
    setSelectedFile(null);
    window.location.reload(); // Refresh the webpage
  };

  const disableButtons = () => {
    setButtonsDisabled(true);
  };

  const tryDemoVideo = async (demoNumber) => {
    try {
      disableButtons(); // Disable buttons while fetching/copying demo video
      const message = await copyDemoVideo(demoNumber);
      onTryDemo(message);
      console.log(message);
    } catch (error) {
      console.error("Error trying demo video:", error);
    }
  };

  const buttonStyle = {
    display: "inline-block",
    padding: "10px 20px",
    marginBottom: "5%",
    fontSize: "16px",
    fontWeight: "bold",
    color: "white",
    backgroundColor: buttonsDisabled ? "#0056b3" : "#007BFF", // Change color based on buttonsDisabled state
    border: "none",
    borderRadius: "5px",
    cursor: buttonsDisabled ? "not-allowed" : "pointer", // Change cursor based on buttonsDisabled state
    transition: "background-color 0.3s",
  };

  const resetButtonStyle = {
    ...buttonStyle,
    cursor: "pointer", // Reset button always has pointer cursor
    backgroundColor: "#007BFF", // Reset button always has its original color
  };

  const buttonHoverEffect = (e, style) => {
    if (!buttonsDisabled) {
      // Apply hover effect only if buttons are not disabled
      e.currentTarget.style.backgroundColor = style.backgroundColor;
    }
  };

  return (
    <div style={{ display: "flex", alignItems: "center", width: "100%" }}>
      <input
        type="file"
        accept="video/*"
        id="file"
        onChange={(e) => {
          const file = e.target.files[0];
          setSelectedFile(file);
          if (file) {
            handleFileUpload(file);
          }
        }}
        style={{ display: "none" }}
      />
      <label
        htmlFor="file"
        style={{ ...buttonStyle, marginBottom: "10px" }}
        onMouseOver={(e) =>
          buttonHoverEffect(e, { backgroundColor: "#0056b3" })
        }
        onMouseOut={(e) => buttonHoverEffect(e, { backgroundColor: "#007BFF" })}
        onMouseDown={(e) =>
          buttonHoverEffect(e, { backgroundColor: "#004085" })
        }
        onMouseUp={(e) => buttonHoverEffect(e, { backgroundColor: "#0056b3" })}
        onClick={disableButtons} // Disable buttons on click
      >
        Upload Video
      </label>
      <button
        style={{
          ...resetButtonStyle,
          marginBottom: "10px",
          marginLeft: "2%",
          borderRadius: "1px",
        }}
        onClick={handleReset}
        onMouseOver={(e) =>
          buttonHoverEffect(e, { backgroundColor: "#0056b3" })
        }
        onMouseOut={(e) => buttonHoverEffect(e, { backgroundColor: "#007BFF" })}
        onMouseDown={(e) =>
          buttonHoverEffect(e, { backgroundColor: "#004085" })
        }
        onMouseUp={(e) => buttonHoverEffect(e, { backgroundColor: "#0056b3" })}
      >
        <FaSyncAlt />
      </button>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          marginLeft: "auto",
          alignItems: "center",
        }}
      >
        <button
          style={buttonStyle}
          onMouseOver={(e) =>
            buttonHoverEffect(e, { backgroundColor: "#0056b3" })
          }
          onMouseOut={(e) =>
            buttonHoverEffect(e, { backgroundColor: "#007BFF" })
          }
          onMouseDown={(e) =>
            buttonHoverEffect(e, { backgroundColor: "#004085" })
          }
          onMouseUp={(e) =>
            buttonHoverEffect(e, { backgroundColor: "#0056b3" })
          }
          onClick={() => tryDemoVideo(1)} // Call onTryDemo with demo number 1
          disabled={buttonsDisabled} // Disable the button based on buttonsDisabled state
        >
          Try demo 1
        </button>
        <button
          style={buttonStyle}
          onMouseOver={(e) =>
            buttonHoverEffect(e, { backgroundColor: "#0056b3" })
          }
          onMouseOut={(e) =>
            buttonHoverEffect(e, { backgroundColor: "#007BFF" })
          }
          onMouseDown={(e) =>
            buttonHoverEffect(e, { backgroundColor: "#004085" })
          }
          onMouseUp={(e) =>
            buttonHoverEffect(e, { backgroundColor: "#0056b3" })
          }
          onClick={() => tryDemoVideo(2)} // Call onTryDemo with demo number 2
          disabled={buttonsDisabled} // Disable the button based on buttonsDisabled state
        >
          Try demo 2
        </button>
      </div>
    </div>
  );
};

export default VideoUploader;
