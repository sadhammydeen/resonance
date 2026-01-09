import React from 'react';

function ExplanationPanel({ explanations }) {
  const sections = [
    { key: 'overview', icon: '🎵', title: 'Overview', color: '#667eea' },
    { key: 'rhythm_pattern', icon: '🥁', title: 'Rhythm Pattern', color: '#2196F3' },
    { key: 'structure', icon: '🏗️', title: 'Structure', color: '#FF9800' },
    { key: 'emotional_arc', icon: '❤️', title: 'Emotional Arc', color: '#F44336' },
    { key: 'learning_focus', icon: '🎯', title: 'Learning Focus', color: '#9C27B0' }
  ];

  return (
    <div className="section">
      <h2>📖 AI Explanations</h2>
      <p style={{ marginBottom: '20px', color: '#666' }}>
        Understanding your music in plain language
      </p>

      {sections.map(section => {
        const content = explanations[section.key];
        if (!content) return null;

        return (
          <div key={section.key} style={{ marginBottom: '25px' }}>
            <h3 style={{ 
              color: section.color,
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
              marginBottom: '15px'
            }}>
              <span style={{ fontSize: '1.5rem' }}>{section.icon}</span>
              {section.title}
            </h3>
            <div 
              className="explanation-text"
              style={{ 
                borderLeftColor: section.color,
                borderLeftWidth: '4px'
              }}
            >
              {content}
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default ExplanationPanel;
