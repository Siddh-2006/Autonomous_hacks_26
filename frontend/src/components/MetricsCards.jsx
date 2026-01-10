import React from 'react';

const MetricsCards = ({ signals }) => {
  if (!signals) return null;

  const cards = [
    { label: 'Velocity Delta', value: `${signals.commit_velocity_change_pct > 0 ? '+' : ''}${signals.commit_velocity_change_pct}%`, color: signals.commit_velocity_change_pct < -30 ? 'red' : 'inherit' },
    { label: 'Active Contributors', value: signals.active_contributors, color: 'inherit' },
    { label: 'Release Cadence', value: signals.release_cadence, color: 'inherit' },
    { label: 'Core Activity', value: signals.core_repo_activity, color: 'inherit' }
  ];

  return (
    <div className="metrics-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '15px', marginBottom: '20px' }}>
      {cards.map((card, index) => (
        <div key={index} style={{ background: 'white', padding: '15px', borderRadius: '4px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <div style={{ fontSize: '0.85em', color: '#666', marginBottom: '5px' }}>{card.label}</div>
          <div style={{ fontSize: '1.2em', fontWeight: 'bold', color: card.color }}>{card.value}</div>
        </div>
      ))}
    </div>
  );
};

export default MetricsCards;
