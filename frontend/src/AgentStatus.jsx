import React from 'react';

function AgentStatus({ signals }) {
  const getStatusIcon = (severity) => {
    switch (severity) {
      case 'high': return '🔴';
      case 'medium': return '⚠️';
      case 'low': return '🟢';
      default: return '⚪';
    }
  };

  const agents = [
    { name: 'CEO', role: 'Strategy & Narrative' },
    { name: 'CTO', role: 'Technology & Execution' },
    { name: 'CFO', role: 'Cost & Financial Discipline' },
    { name: 'CPO', role: 'Product & User Reality' },
    { name: 'RISK', role: 'Governance & Risk' }
  ];

  return (
    <div className="agent-status">
      {agents.map(agent => {
        const signal = signals[agent.name] || {};
        return (
          <div key={agent.name} className="agent-card">
            <div className="agent-header">
              <span className="agent-name">{agent.name}</span>
              <span className="status-icon">
                {getStatusIcon(signal.severity)}
              </span>
            </div>
            <div className="agent-role">{agent.role}</div>
            <div className="agent-status-text">
              {signal.status || 'No data'}
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default AgentStatus;