// StatsDisplay.js
import React from 'react';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

const StatsDisplay = ({ stats }) => {
  const team2_possession_percentage = 100 - stats.team1_possession_percentage;

  return (
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
  );
};

export default StatsDisplay;
