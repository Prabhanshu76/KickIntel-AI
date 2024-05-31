// api.js
export const uploadVideo = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
  
    try {
      const response = await fetch('http://localhost:8000/upload-video', {
        method: 'POST',
        body: formData,
      });
  
      if (response.ok) {
        const data = await response.json();
        return data.video_path;
      } else {
        throw new Error('Failed to upload video');
      }
    } catch (error) {
      throw new Error('Error uploading video:', error);
    }
  };
  
  export const fetchStats = async () => {
    try {
      const response = await fetch('http://localhost:8000/data');
      if (response.ok) {
        const data = await response.json();
        return data;
      } else {
        throw new Error('Failed to fetch stats');
      }
    } catch (error) {
      throw new Error('Error fetching stats:', error);
    }
  };
  