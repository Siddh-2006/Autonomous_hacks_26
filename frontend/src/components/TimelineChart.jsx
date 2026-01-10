import React from 'react';

const TimelineChart = ({ history }) => {
  if (!history || history.length === 0) return <div>No history available</div>;

  return (
    <div className="timeline-chart" style={{ background: 'white', padding: '15px', borderRadius: '4px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
      <h3 style={{ marginTop: 0 }}>Execution History</h3>
      <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
        {history.map((snapshot, index) => (
          <div key={index} style={{ display: 'flex', justifyContent: 'space-between', padding: '10px', borderBottom: '1px solid #eee' }}>
            <div>
              <span style={{ fontWeight: 'bold' }}>{snapshot.execution_health}</span>
              <span style={{ marginLeft: '10px', fontSize: '0.9em', color: '#666' }}>{new Date(snapshot.timestamp).toLocaleString()}</span>
            </div>
            <div>
              <span className={`badge severity-${snapshot.severity?.toLowerCase()}`} style={{ fontSize: '0.8em' }}>{snapshot.severity}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TimelineChart;
