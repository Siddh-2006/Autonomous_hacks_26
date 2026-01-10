import React from 'react';

const AgentStatus = ({ health, severity, confidence }) => {
  const getColor = (health) => {
    switch (health?.toLowerCase()) {
      case 'strong': return '#4caf50';
      case 'stable': return '#ff9800';
      case 'declining': return '#f44336';
      default: return '#9e9e9e';
    }
  };

  const statusColor = getColor(health);

  return (
    <div className="agent-status-card" style={{ borderLeft: `5px solid ${statusColor}`, padding: '15px', background: '#f5f5f5', borderRadius: '4px', marginBottom: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h3 style={{ margin: 0, color: '#333' }}>Execution Health</h3>
          <h2 style={{ margin: '5px 0', color: statusColor }}>{health || 'Unknown'}</h2>
        </div>
        <div style={{ textAlign: 'right' }}>
           <div className={`badge severity-${severity?.toLowerCase()}`} style={{ 
               padding: '5px 10px', 
               borderRadius: '15px', 
               background: severity === 'High' ? '#ffebee' : severity === 'Medium' ? '#fff3e0' : '#e8f5e9',
               color: severity === 'High' ? '#c62828' : severity === 'Medium' ? '#ef6c00' : '#2e7d32',
               display: 'inline-block',
               fontWeight: 'bold',
               marginBottom: '5px'
           }}>
             Severity: {severity || 'N/A'}
           </div>
           <div style={{ fontSize: '0.9em', color: '#666' }}>
             Confidence: {confidence ? `${(confidence * 100).toFixed(0)}%` : 'N/A'}
           </div>
        </div>
      </div>
    </div>
  );
};

export default AgentStatus;
