import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
      setError(null);
    }
  };

  const handleFileSelect = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setError(null);
    }
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please select an audio file first');
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_level', 'beginner');

    try {
      const response = await axios.post('http://localhost:8000/api/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setAnalysis(response.data);
      console.log('✅ Analysis complete:', response.data);
    } catch (err) {
      console.error('❌ Error:', err);
      setError(err.response?.data?.detail || 'Error analyzing audio. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const resetUpload = () => {
    setFile(null);
    setAnalysis(null);
    setError(null);
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <span className="logo-icon">🎵</span>
            <span className="logo-text">Resonance Without Sound</span>
          </div>
          <nav className="nav">
            <a href="#about">About</a>
            <a href="#features">Features</a>
            <a href="#guide">Guide</a>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="main">
        {!analysis ? (
          // Upload Section
          <div className="upload-container">
            <div className="upload-header">
              <h1>Understand Music Through Patterns</h1>
              <p className="subtitle">
                Upload any song to see its rhythm, structure, and energy visualized
              </p>
            </div>

            <div
              className={`upload-area ${dragActive ? 'drag-active' : ''} ${file ? 'has-file' : ''}`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              onClick={() => !file && document.getElementById('file-input').click()}
            >
              <input
                id="file-input"
                type="file"
                accept=".mp3,.wav,.m4a,.flac"
                onChange={handleFileSelect}
                style={{ display: 'none' }}
              />

              {!file ? (
                <>
                  <div className="upload-icon">📁</div>
                  <h3>Drop your audio file here</h3>
                  <p>or click to browse</p>
                  <p className="file-types">Supports MP3, WAV, M4A, FLAC</p>
                </>
              ) : (
                <div className="file-selected">
                  <div className="file-icon">🎵</div>
                  <div className="file-info">
                    <h3>{file.name}</h3>
                    <p>{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                  </div>
                  <button className="remove-btn" onClick={(e) => { e.stopPropagation(); resetUpload(); }}>
                    ✕
                  </button>
                </div>
              )}
            </div>

            {error && (
              <div className="error-message">
                <span>⚠️</span> {error}
              </div>
            )}

            <button
              className="analyze-btn"
              onClick={handleAnalyze}
              disabled={!file || loading}
            >
              {loading ? (
                <>
                  <span className="spinner"></span> Analyzing...
                </>
              ) : (
                <>🎵 Analyze Music</>
              )}
            </button>

            {loading && (
              <div className="loading-info">
                <p>Extracting patterns from your music...</p>
                <div className="progress-bar">
                  <div className="progress-fill"></div>
                </div>
              </div>
            )}

            {/* Features Section */}
            <div className="features-grid">
              <div className="feature-card">
                <div className="feature-icon">🥁</div>
                <h3>Rhythm Analysis</h3>
                <p>See beats, tempo, and timing patterns</p>
              </div>
              <div className="feature-card">
                <div className="feature-icon">🏗️</div>
                <h3>Structure Mapping</h3>
                <p>Discover sections and repetition</p>
              </div>
              <div className="feature-card">
                <div className="feature-icon">❤️</div>
                <h3>Energy Flow</h3>
                <p>Track tension and release over time</p>
              </div>
            </div>
          </div>
        ) : (
          // Results Section
          <div className="results-container">
            <div className="results-header">
              <button className="back-btn" onClick={resetUpload}>
                ← Back
              </button>
              <h2>Analysis: {analysis.filename}</h2>
            </div>

            {/* Insights Summary */}
            <div className="insights-card">
              <h3>🎯 Key Insights</h3>
              <div className="insight-row">
                <div className="insight-item">
                  <span className="insight-label">Primary Characteristic</span>
                  <span className="insight-value">{analysis.analysis.insights.primary_characteristic.replace(/_/g, ' ')}</span>
                </div>
                <div className="insight-item">
                  <span className="insight-label">Complexity</span>
                  <span className="insight-value">{analysis.analysis.insights.complexity}</span>
                </div>
              </div>
              <div className="strategy-box">
                <strong>Learning Strategy:</strong> {analysis.analysis.insights.learning_strategy}
              </div>
            </div>

            {/* Explanation */}
            <div className="explanation-card">
              <h3>📖 Explanation</h3>
              <p className="explanation-text">{analysis.explanation}</p>
            </div>

            {/* Rhythm Stats */}
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-icon">🥁</div>
                <div className="stat-content">
                  <span className="stat-value">{analysis.analysis.rhythm.bpm.toFixed(0)}</span>
                  <span className="stat-label">BPM</span>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">⏱️</div>
                <div className="stat-content">
                  <span className="stat-value">{analysis.analysis.rhythm.tempo_category.replace(/_/g, ' ')}</span>
                  <span className="stat-label">Tempo</span>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">🎚️</div>
                <div className="stat-content">
                  <span className="stat-value">{(analysis.analysis.rhythm.regularity * 100).toFixed(0)}%</span>
                  <span className="stat-label">Regularity</span>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">🎵</div>
                <div className="stat-content">
                  <span className="stat-value">{analysis.analysis.rhythm.time_signature}</span>
                  <span className="stat-label">Time Signature</span>
                </div>
              </div>
            </div>

            {/* Structure Information */}
            <div className="section-card">
              <h3>🏗️ Structure Analysis</h3>
              <div className="structure-info">
                <div className="structure-stat">
                  <strong>Total Sections:</strong> {analysis.analysis.structure.total_sections}
                </div>
                <div className="structure-stat">
                  <strong>Repetition:</strong> {(analysis.analysis.structure.repetition_ratio * 100).toFixed(0)}%
                </div>
                <div className="structure-stat">
                  <strong>Pattern Type:</strong> {analysis.analysis.structure.pattern_type.replace(/_/g, ' ')}
                </div>
              </div>

              <div className="sections-timeline">
                {analysis.analysis.structure.sections.map((section, idx) => (
                  <div key={idx} className="section-block" title={`${section.start.toFixed(1)}s - ${section.end.toFixed(1)}s`}>
                    <div className="section-label">Section {idx + 1}</div>
                    <div className="section-time">{section.start.toFixed(0)}s</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Energy Timeline */}
            <div className="section-card">
              <h3>❤️ Energy & Tension</h3>
              <div className="energy-info">
                <div className="energy-stat">
                  <strong>Overall Energy:</strong> {analysis.analysis.energy.overall}
                </div>
                <div className="energy-stat">
                  <strong>Buildup:</strong> {analysis.analysis.energy.has_buildup ? '✓ Yes' : '✗ No'}
                </div>
                <div className="energy-stat">
                  <strong>Release:</strong> {analysis.analysis.energy.has_release ? '✓ Yes' : '✗ No'}
                </div>
                <div className="energy-stat">
                  <strong>Arc:</strong> {analysis.analysis.energy.arc}
                </div>
              </div>

              <div className="energy-timeline">
                {analysis.analysis.energy.timeline.map((moment, idx) => (
                  <div key={idx} className={`energy-bar energy-${moment.level}`}>
                    <div className="energy-fill" style={{ height: `${moment.intensity * 100}%` }}></div>
                    <span className="energy-time">{moment.time.toFixed(0)}s</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Pattern Logic */}
            <div className="section-card">
              <h3>🧠 Pattern & Variation</h3>
              <div className="pattern-grid">
                <div className="pattern-stat">
                  <span className="pattern-label">Predictability</span>
                  <div className="progress-bar-static">
                    <div className="progress-fill-static" style={{ width: `${analysis.analysis.pattern.predictability * 100}%` }}></div>
                  </div>
                  <span className="pattern-value">{(analysis.analysis.pattern.predictability * 100).toFixed(0)}%</span>
                </div>
                <div className="pattern-stat">
                  <span className="pattern-label">Variation</span>
                  <span className="pattern-value-large">{analysis.analysis.pattern.variation}</span>
                </div>
                <div className="pattern-stat">
                  <span className="pattern-label">Teaching Focus</span>
                  <span className="pattern-value-large">{analysis.analysis.pattern.teaching_focus.replace(/_/g, ' ')}</span>
                </div>
              </div>

              {analysis.analysis.pattern.surprise_moments.length > 0 && (
                <div className="surprises">
                  <strong>🎊 Surprise Moments:</strong> {analysis.analysis.pattern.surprise_moments.map(t => `${t.toFixed(0)}s`).join(', ')}
                </div>
              )}
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="footer">
        <p>Making music visible for everyone • Built with ❤️ for accessible music education</p>
      </footer>
    </div>
  );
}

export default App;
