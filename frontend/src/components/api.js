// api.js

const BASE_URL = process.env.REACT_APP_API_URL;

export const uploadVideo = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch(`${BASE_URL}/upload-video`, {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const data = await response.json();
      return data.filename;
    } else {
      throw new Error("Failed to upload video");
    }
  } catch (error) {
    throw new Error(`Error uploading video: ${error.message}`);
  }
};

export const fetchStats = async () => {
  try {
    const response = await fetch(`${BASE_URL}/data`);
    if (response.ok) {
      const data = await response.json();
      return data;
    } else {
      throw new Error("Failed to fetch stats");
    }
  } catch (error) {
    throw new Error(`Error fetching stats: ${error.message}`);
  }
};

export const copyDemoVideo = async (demoNumber) => {
  try {
    const response = await fetch(`${BASE_URL}/demo-video/${demoNumber}`, {
      method: "GET",
    });

    if (response.ok) {
      const data = await response.json();
      return data.message;
    } else {
      throw new Error(`Failed to copy demo video ${demoNumber}`);
    }
  } catch (error) {
    throw new Error(`Error copying demo video ${demoNumber}: ${error.message}`);
  }
};
