import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function RhythmMap({ beatInfo }) {
  // Create visualization data from beat times
  const createRhythmData = () => {
    const { beat_times } = beatInfo;
    const data = [];
    
    // Group beats into bars (typically 4 beats per bar in 4/4 time)
    const beatsPerBar = 4;
    const totalBars = Math.ceil(beat_times.length / beatsPerBar);
    
    for (let i = 0; i < totalBars; i++) {
      const startBeat = i * beatsPerBar;
      const endBeat = Math.min(startBeat + beatsPerBar, beat_times.length);
      const barsBeats = beat_times.slice(startBeat, endBeat);
      
      data.push({
        bar: i + 1,
        intensity: barsBeats.length, // Number of beats in this bar
        time: barsBeats[0]?.toFixed(1) || 0
      });
    }
    
    return data.slice(0, 32); // Limit to first 32 bars for visibility
  };

  const rhythmData = createRhythmData();

  return (
    <div className="section">
      <h2>📊 Visual Rhythm Map</h2>
      <p style={{ marginBottom: '20px', color: '#666' }}>
        Each bar represents a group of beats. Taller bars = more activity.
      </p>
      
      <div className="rhythm-visualization">
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={rhythmData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="bar" 
              label={{ value: 'Bar Number', position: 'insideBottom', offset: -5 }} 
            />
            <YAxis 
              label={{ value: 'Beat Intensity', angle: -90, position: 'insideLeft' }} 
            />
            <Tooltip 
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  return (
                    <div style={{ 
                      background: 'white', 
                      padding: '10px', 
                      border: '2px solid #667eea',
                      borderRadius: '5px'
                    }}>
                      <p><strong>Bar {payload[0].payload.bar}</strong></p>
                      <p>Time: {payload[0].payload.time}s</p>
                      <p>Beats: {payload[0].value}</p>
                    </div>
                  );
                }
                return null;
              }}
            />
            <Bar dataKey="intensity" fill="#667eea" />
          </BarChart>
        </ResponsiveContainer>
      </div>
      
      <div className="explanation-text" style={{ marginTop: '20px' }}>
        <strong>💡 How to read this:</strong> Each vertical bar is like a footstep in time. 
        The pattern shows you the rhythm's structure - notice where bars repeat or change!
      </div>
    </div>
  );
}

export default RhythmMap;
