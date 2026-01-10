import React from 'react';
import Dashboard from './Dashboard';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Auto-Diligence System</h1>
        <p>Autonomous Agent-Based Investor Due Diligence</p>
      </header>
      <main>
        <Dashboard />
      </main>
    </div>
  );
}

export default App;