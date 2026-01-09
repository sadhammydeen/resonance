import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Area, AreaChart } from 'recharts';

function EmotionTimeline({ emotions }) {
  // Prepare data for visualization
  const emotionData = emotions.map(emo => ({
    time: emo.time.toFixed(1),
    energy: (emo.energy * 100).toFixed(0),
    intensity: (emo.intensity * 100).toFixed(0),
    tension: (emo.tension * 100).toFixed(0),
    label: emo.label
  }));

  // Get emotion color based on label
  const getEmotionColor = (label) => {
    if (label.includes('Calm')) return '#4CAF50';
    if (label.includes('Intense')) return '#F44336';
    if (label.includes('Energetic')) return '#FF9800';
    if (label.includes('Building')) return '#FFC107';
    return '#2196F3';
  };

  return (
    <div className="section">
      <h2>❤️ Emotional Journey</h2>
      <p style={{ marginBottom: '20px', color: '#666' }}>
        Watch how the music's feeling changes over time
      </p>
      
      <div className="rhythm-visualization">
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={emotionData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="time" 
              label={{ value: 'Time (seconds)', position: 'insideBottom', offset: -5 }} 
            />
            <YAxis 
              label={{ value: 'Intensity (%)', angle: -90, position: 'insideLeft' }} 
            />
            <Tooltip 
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  return (
                    <div style={{ 
                      background: 'white', 
                      padding: '15px', 
                      border: '2px solid #764ba2',
                      borderRadius: '5px'
                    }}>
                      <p><strong>{payload[0].payload.label}</strong></p>
                      <p>Time: {payload[0].payload.time}s</p>
                      <p style={{ color: '#667eea' }}>Energy: {payload[0].value}%</p>
                      <p style={{ color: '#764ba2' }}>Tension: {payload[2]?.value}%</p>
                    </div>
                  );
                }
                return null;
              }}
            />
            <Legend />
            <Area 
              type="monotone" 
              dataKey="energy" 
              stackId="1"
              stroke="#667eea" 
              fill="#667eea" 
              fillOpacity={0.6}
              name="Energy"
            />
            <Area 
              type="monotone" 
              dataKey="tension" 
              stackId="2"
              stroke="#764ba2" 
              fill="#764ba2" 
              fillOpacity={0.4}
              name="Tension"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Emotion Cards */}
      <div style={{ marginTop: '30px' }}>
        <h3>🎭 Emotion Timeline</h3>
        {emotions.map((emo, index) => (
          <div 
            key={index} 
            className="emotion-card"
            style={{ 
              borderLeftColor: getEmotionColor(emo.label),
              borderLeftWidth: '6px'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <span className="emotion-label">{emo.label}</span>
                <p style={{ color: '#666', marginTop: '5px' }}>
                  {emo.time.toFixed(1)}s - {(emo.time + 5).toFixed(1)}s
                </p>
              </div>
              <div style={{ textAlign: 'right', fontSize: '0.9rem', color: '#666' }}>
                <div>Energy: {(emo.energy * 100).toFixed(0)}%</div>
                <div>Tension: {(emo.tension * 100).toFixed(0)}%</div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="explanation-text" style={{ marginTop: '20px' }}>
        <strong>💡 How to read this:</strong> Think of emotions as waves in the ocean. 
        Calm sections are like still water, intense sections are like big waves crashing. 
        Watch the flow from start to finish!
      </div>
    </div>
  );
}

export default EmotionTimeline;
