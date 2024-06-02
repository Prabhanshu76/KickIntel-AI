import React from 'react';
import VideoPlayer from './components/VideoPlayer';
import CardOne from './components/CardOne';

const App = () => {
  return (
    <div style={{ textAlign: 'center', marginTop: '50px', marginBottom: '50px' }}>
      <CardOne>
        <h1 style={{ marginBottom: '50px' }}>KickTrack Vision</h1>
        <VideoPlayer />
      </CardOne>
    </div>
  );
}

export default App;
