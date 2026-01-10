import React from 'react';

const ExplanationBox = ({ explanation }) => {
  return (
    <div className="explanation-box" style={{ background: '#e3f2fd', padding: '15px', borderRadius: '4px', border: '1px solid #bbdefb', marginBottom: '20px' }}>
      <h4 style={{ marginTop: 0, marginBottom: '10px', color: '#1565c0' }}>CTO Analysis</h4>
      <p style={{ margin: 0, lineHeight: '1.5', color: '#0d47a1' }}>
        {explanation || 'No analysis available.'}
      </p>
    </div>
  );
};

export default ExplanationBox;
