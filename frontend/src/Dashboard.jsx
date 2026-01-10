import React, { useState, useEffect } from 'react';
import AgentStatus from './AgentStatus';
import Timeline from './Timeline';
import AlertBox from './AlertBox';

function Dashboard() {
  const [signals, setSignals] = useState({});
  const [alerts, setAlerts] = useState([]);
  const [companyName] = useState('Couchbase');

  useEffect(() => {
    // Fetch signals from backend
    fetchSignals();
    const interval = setInterval(fetchSignals, 30000); // Update every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchSignals = async () => {
    try {
      // In real implementation, would fetch from FastAPI backend
      const mockSignals = {
        CTO: { status: 'declining', severity: 'high' },
        CFO: { status: 'cost-control', severity: 'medium' },
        CEO: { status: 'stable', severity: 'low' },
        CPO: { status: 'declining', severity: 'medium' },
        RISK: { status: 'stable', severity: 'low' }
      };
      setSignals(mockSignals);
    } catch (error) {
      console.error('Error fetching signals:', error);
    }
  };

  return (
    <div className="dashboard">
      <div className="company-snapshot">
        <h2>{companyName}</h2>
        <div className="confidence-score">
          <span>Overall Confidence: 65%</span>
          <span className="risk-level high">Risk Level: HIGH</span>
        </div>
      </div>

      <div className="dashboard-grid">
        <div className="agents-panel">
          <h3>Executive Agents</h3>
          <AgentStatus signals={signals} />
        </div>

        <div className="alerts-panel">
          <AlertBox alerts={alerts} />
        </div>

        <div className="timeline-panel">
          <Timeline />
        </div>

        <div className="thesis-panel">
          <h3>Current Thesis</h3>
          <div className="thesis-content">
            <div className="bull-case">
              <h4>Bull Case</h4>
              <p>Strong product foundation, experienced team</p>
            </div>
            <div className="bear-case">
              <h4>Bear Case</h4>
              <p>Declining engineering velocity, cost pressures</p>
            </div>
            <div className="recent-changes">
              <h4>What Changed Recently</h4>
              <p>Significant drop in commit activity, hiring slowdown</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;