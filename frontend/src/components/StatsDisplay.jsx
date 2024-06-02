// StatsDisplay.js
import React from "react";
import { CircularProgressbar, buildStyles } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";

const StatsDisplay = ({ stats }) => {
  const team2_possession_percentage = 100 - stats.team1_possession_percentage;

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h3>Real Time Stats</h3>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          margin: "20px 0",
        }}
      >
        <div style={{ flex: 1, textAlign: "center" }}>
          <h4>Team 1</h4>
        </div>
        <div style={{ flex: 1, textAlign: "center" }}>
          <h4>Team 2</h4>
        </div>
      </div>
      <div style={{ margin: "20px 0" }}>
        <p>Passing</p>
      </div>
      <div
        style={{
          display: "flex",
          justifyContent: "space-around",
          alignItems: "center",
          margin: "20px 0",
        }}
      >
        <div style={{ flex: 1, textAlign: "center" }}>
          <p style={{ margin: "10px 0" }}>{stats.team1_passes}</p>
        </div>
        <div>
          <p style={{ margin: "0 20px" }}>|</p>
        </div>
        <div style={{ flex: 1, textAlign: "center" }}>
          <p style={{ margin: "10px 0" }}>{stats.team2_passes}</p>
        </div>
      </div>
      <div style={{ margin: "20px 0" }}>
        <p>Possession</p>
      </div>
      <div
        style={{
          display: "flex",
          justifyContent: "space-around",
          marginTop: "20px",
        }}
      >
        <div style={{ width: "100px", height: "100px", textAlign: "center" }}>
          <CircularProgressbar
            value={stats.team1_possession_percentage}
            text={`${Math.round(stats.team1_possession_percentage)}%`}
            styles={buildStyles({
              textSize: "16px",
              pathColor: `rgba(62, 152, 199, ${
                stats.team1_possession_percentage / 100
              })`,
              textColor: "#FFFFFF",
              trailColor: "#d6d6d6",
              backgroundColor: "#3e98c7",
            })}
          />
        </div>
        <div
          style={{
            width: "100px",
            height: "100px",
            textAlign: "center",
            marginLeft: "10%",
          }}
        >
          <CircularProgressbar
            value={team2_possession_percentage}
            text={`${Math.round(team2_possession_percentage)}%`}
            styles={buildStyles({
              textSize: "16px",
              pathColor: `rgba(62, 152, 199, ${
                team2_possession_percentage / 100
              })`,
              textColor: "#FFFFFF",
              trailColor: "#d6d6d6",
              backgroundColor: "#3e98c7",
              marginLeft: "10%",
            })}
          />
        </div>
      </div>
    </div>
  );
};

export default StatsDisplay;
