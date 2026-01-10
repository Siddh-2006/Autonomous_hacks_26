import React from 'react';

function AlertBox({ alerts }) {
  const currentAlert = {
    type: 'Material Execution Risk',
    message: 'Engineering activity declined sharply while hiring slowed. Risk of roadmap delays and competitive erosion over next 3–6 months.',
    confidence: 0.85,
    timestamp: '2024-01-10 14:20'
  };

  return (
    <div className="alert-box">
      <h3>Active Alerts</h3>
      {currentAlert ? (
        <div className="alert active">
          <div className="alert-header">
            <span className="alert-icon">🚨</span>
            <span className="alert-type">{currentAlert.type}</span>
            <span className="alert-confidence">
              {Math.round(currentAlert.confidence * 100)}% confidence
            </span>
          </div>
          <div className="alert-message">
            {currentAlert.message}
          </div>
          <div className="alert-timestamp">
            {currentAlert.timestamp}
          </div>
        </div>
      ) : (
        <div className="no-alerts">
          <span className="no-alert-icon">✅</span>
          <span>No active alerts</span>
        </div>
      )}
    </div>
  );
}

export default AlertBox;