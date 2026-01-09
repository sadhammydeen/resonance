import React from 'react';

function StructureView({ sections }) {
  // Calculate total duration
  const totalDuration = sections.length > 0 
    ? sections[sections.length - 1].end_time 
    : 0;

  // Get color for section type
  const getSectionColor = (name) => {
    const colors = {
      'Intro': '#4CAF50',
      'Verse': '#2196F3',
      'Build': '#FF9800',
      'Chorus': '#F44336',
      'Bridge': '#9C27B0',
      'Outro': '#607D8B'
    };
    return colors[name] || '#888';
  };

  return (
    <div className="section">
      <h2>🏗️ Musical Structure</h2>
      <p style={{ marginBottom: '20px', color: '#666' }}>
        How the music is organized into sections
      </p>

      {/* Visual Timeline */}
      <div style={{ 
        background: 'white', 
        padding: '30px 20px', 
        borderRadius: '10px',
        marginBottom: '20px'
      }}>
        <div style={{ 
          display: 'flex', 
          height: '60px', 
          borderRadius: '8px',
          overflow: 'hidden',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
        }}>
          {sections.map((section, index) => {
            const widthPercent = (section.duration / totalDuration) * 100;
            return (
              <div
                key={index}
                style={{
                  width: `${widthPercent}%`,
                  background: getSectionColor(section.name),
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white',
                  fontWeight: 'bold',
                  fontSize: '0.9rem',
                  borderRight: '2px solid white',
                  transition: 'all 0.3s',
                  cursor: 'pointer'
                }}
                title={`${section.name}: ${section.duration.toFixed(1)}s`}
              >
                {widthPercent > 10 && section.name}
              </div>
            );
          })}
        </div>
        <div style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          marginTop: '10px',
          fontSize: '0.85rem',
          color: '#666'
        }}>
          <span>0s</span>
          <span>{totalDuration.toFixed(1)}s</span>
        </div>
      </div>

      {/* Section Details */}
      <div>
        <h3>📋 Section Breakdown</h3>
        {sections.map((section, index) => (
          <div 
            key={index}
            style={{
              background: 'white',
              padding: '15px',
              borderRadius: '10px',
              marginBottom: '10px',
              borderLeft: `6px solid ${getSectionColor(section.name)}`,
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}
          >
            <div>
              <div style={{ 
                fontSize: '1.2rem', 
                fontWeight: 'bold', 
                color: getSectionColor(section.name),
                marginBottom: '5px'
              }}>
                {index + 1}. {section.name}
              </div>
              <div style={{ color: '#666', fontSize: '0.9rem' }}>
                {section.start_time.toFixed(1)}s - {section.end_time.toFixed(1)}s
                ({section.duration.toFixed(1)}s duration)
              </div>
              <div style={{ 
                marginTop: '8px', 
                color: '#333',
                fontStyle: 'italic'
              }}>
                {section.characteristics}
              </div>
            </div>
            <div style={{
              background: getSectionColor(section.name),
              color: 'white',
              padding: '8px 15px',
              borderRadius: '20px',
              fontWeight: 'bold',
              fontSize: '0.9rem'
            }}>
              {((section.duration / totalDuration) * 100).toFixed(0)}%
            </div>
          </div>
        ))}
      </div>

      <div className="explanation-text" style={{ marginTop: '20px' }}>
        <strong>💡 How to read this:</strong> Think of a song like a story with chapters. 
        Each section has its own character. Notice how sections repeat or build on each other - 
        that's what makes music memorable!
      </div>
    </div>
  );
}

export default StructureView;
