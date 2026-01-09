import React, { useState } from 'react';
import axios from 'axios';
import RhythmMap from './components/RhythmMap';
import EmotionTimeline from './components/EmotionTimeline';
import StructureView from './components/StructureView';
import ExplanationPanel from './components/ExplanationPanel';
import FeedbackSection from './components/FeedbackSection';
import './index.css';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState(null);
  const [userLevel, setUserLevel] = useState('beginner');

  const handleFileSelect = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_level', userLevel);

    try {
      const response = await axios.post('/api/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setAnalysis(response.data);
      console.log('✅ Analysis received:', response.data);
    } catch (err) {
      console.error('❌ Upload error:', err);
      setError(err.response?.data?.detail || 'Error analyzing audio. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async (understanding, comment) => {
    if (!analysis) return;

    try {
      const formData = new FormData();
      formData.append('file_id', analysis.file_id);
      formData.append('understanding', understanding);
      if (comment) {
        formData.append('comment', comment);
      }

      const response = await axios.post('/api/feedback', formData);
      console.log('✅ Feedback submitted:', response.data);
      
      // Show suggestion to user
      alert(response.data.suggestion.message + '\n\nNext steps:\n' + 
            response.data.suggestion.next_steps.join('\n'));
    } catch (err) {
      console.error('❌ Feedback error:', err);
    }
  };

  return (
    <div className="container">
      <header className="header">
        <h1>🎵 Resonance Without Sound</h1>
        <p>Understand music through visual patterns, structure, and emotion</p>
      </header>

      <main className="main-content">
        {/* Upload Section */}
        <div className="upload-section" onClick={() => document.getElementById('file-input').click()}>
          <h2>Upload Your Music</h2>
          <p>Choose an MP3, WAV, or M4A file to analyze</p>
          <input
            id="file-input"
            type="file"
            accept=".mp3,.wav,.m4a"
            onChange={handleFileSelect}
          />
          {file && <p style={{ marginTop: '10px', color: '#667eea', fontWeight: 'bold' }}>
            Selected: {file.name}
          </p>}
        </div>

        {/* User Level Selector */}
        <div style={{ textAlign: 'center', margin: '20px 0' }}>
          <label style={{ marginRight: '10px', fontWeight: 'bold' }}>Learning Level:</label>
          <select 
            value={userLevel} 
            onChange={(e) => setUserLevel(e.target.value)}
            style={{ padding: '8px', borderRadius: '5px', border: '2px solid #667eea' }}
          >
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>

        <button 
          className="upload-button" 
          onClick={handleUpload}
          disabled={!file || loading}
        >
          {loading ? '🔄 Analyzing...' : '🎵 Analyze Music'}
        </button>

        {/* Error Display */}
        {error && (
          <div className="error">
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="loading">
            <p>🎵 Analyzing your music...</p>
            <p style={{ fontSize: '1rem', marginTop: '10px', color: '#666' }}>
              Extracting rhythm patterns, structure, and emotions
            </p>
          </div>
        )}

        {/* Analysis Results */}
        {analysis && !loading && (
          <div className="analysis-results">
            <h2 style={{ textAlign: 'center', color: '#667eea', marginBottom: '30px' }}>
              📊 Analysis: {analysis.filename}
            </h2>

            {/* Beat Info Section */}
            <div className="section">
              <h2>🥁 Rhythm Information</h2>
              <div className="beat-info">
                <div className="beat-stat">
                  <span className="value">{analysis.analysis.beat_info.bpm.toFixed(0)}</span>
                  <span className="label">BPM (Beats per Minute)</span>
                </div>
                <div className="beat-stat">
                  <span className="value">{analysis.analysis.beat_info.total_beats}</span>
                  <span className="label">Total Beats</span>
                </div>
                <div className="beat-stat">
                  <span className="value">{analysis.analysis.beat_info.time_signature}</span>
                  <span className="label">Time Signature</span>
                </div>
                <div className="beat-stat">
                  <span className="value">{analysis.analysis.duration.toFixed(0)}s</span>
                  <span className="label">Duration</span>
                </div>
              </div>
            </div>

            {/* Rhythm Map Visualization */}
            <RhythmMap beatInfo={analysis.analysis.beat_info} />

            {/* Structure Sections */}
            <StructureView sections={analysis.analysis.sections} />

            {/* Emotion Timeline */}
            <EmotionTimeline emotions={analysis.analysis.emotional_timeline} />

            {/* Explanations */}
            <ExplanationPanel explanations={analysis.explanations} />

            {/* Feedback Section */}
            <FeedbackSection onSubmitFeedback={handleFeedback} />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
