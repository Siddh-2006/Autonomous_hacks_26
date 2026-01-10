import React from 'react';

function Timeline() {
  const events = [
    {
      timestamp: '2024-01-10 14:30',
      type: 'signal',
      message: 'CTO Agent: Tech health declining (commit rate -52%)'
    },
    {
      timestamp: '2024-01-10 14:25',
      type: 'signal',
      message: 'CFO Agent: Hiring slowdown detected'
    },
    {
      timestamp: '2024-01-10 14:20',
      type: 'alert',
      message: '🚨 Material Execution Risk Alert triggered'
    },
    {
      timestamp: '2024-01-10 13:45',
      type: 'signal',
      message: 'CPO Agent: Product velocity below threshold'
    }
  ];

  return (
    <div className="timeline">
      <h3>Recent Activity</h3>
      <div className="timeline-events">
        {events.map((event, index) => (
          <div key={index} className={`timeline-event ${event.type}`}>
            <div className="event-timestamp">{event.timestamp}</div>
            <div className="event-message">{event.message}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Timeline;