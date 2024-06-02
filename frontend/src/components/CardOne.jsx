import React from 'react';
import './CardOne.css';

const CardOne = ({ children }) => {
  return (
    <div className="new-container">
      <div className="new-box">
        <span></span>
        <div className="new-content">
          {children}
        </div>
      </div>
    </div>
  );
};

export default CardOne;
