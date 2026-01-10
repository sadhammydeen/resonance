import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState(null);
  const [mode, setMode] = useState('simple');
  const [selectedSong, setSelectedSong] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [credits, setCredits] = useState(840);
  
  // Analysis history
  const [analysisHistory, setAnalysisHistory] = useState([]);

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
    formData.append('level', 'advanced');

    try {
      const response = await axios.post('http://localhost:8000/api/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const result = response.data;
      
      // Create analysis card for history
      const historyItem = {
        id: Date.now(),
        fileName: file.name,
        duration: result.structure?.total_duration || 0,
        analysis: result,
        timestamp: new Date().toISOString(),
        thumbnail: generateThumbnail()
      };
      
      setAnalysisHistory([historyItem, ...analysisHistory]);
      setAnalysis(result);
      setSelectedSong(historyItem);
      setFile(null);
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const generateThumbnail = () => {
    const colors = ['#d946ef', '#a855f7', '#ec4899', '#8b5cf6', '#f97316'];
    return colors[Math.floor(Math.random() * colors.length)];
  };

  const formatDuration = (seconds) => {
    if (!seconds) return '00:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleSelectSong = (song) => {
    setSelectedSong(song);
    setAnalysis(song.analysis);
  };

  const handleRemoveSong = (id) => {
    setAnalysisHistory(analysisHistory.filter(song => song.id !== id));
    if (selectedSong?.id === id) {
      setSelectedSong(null);
      setAnalysis(null);
    }
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <span className="logo-icon">🎵</span>
            <span className="logo-text">Resonance<span className="logo-highlight">Music</span></span>
          </div>
          
          <nav className="nav-menu">
            <a href="#pricing">Pricing</a>
            <div className="nav-dropdown">
              <a href="#resources">Resources ▼</a>
            </div>
          </nav>

          <div className="header-right">
            <div className="credits-display">
              <span className="credits-label">Credits:</span>
              <span className="credits-value">{credits}</span>
            </div>
            <select className="language-selector">
              <option>English</option>
              <option>Spanish</option>
              <option>French</option>
            </select>
            <div className="user-avatar">👤</div>
          </div>
        </div>
      </header>

      {/* Main Content - 3 Column Layout */}
      <main className="main-layout">
        {/* Left Sidebar - Control Panel */}
        <aside className="left-sidebar">
          <div className="sidebar-content">
            {/* Mode Selector */}
            <div className="mode-selector">
              <button 
                className={`mode-btn ${mode === 'simple' ? 'active' : ''}`}
                onClick={() => setMode('simple')}
              >
                Simple
              </button>
              <button 
                className={`mode-btn ${mode === 'custom' ? 'active' : ''}`}
                onClick={() => setMode('custom')}
              >
                Custom
                <span className="badge-new">NEW</span>
              </button>
            </div>

            {/* V-Fi Selector */}
            <div className="vfi-selector">
              <button className="vfi-btn">
                <span className="vfi-badge">v-Fi</span>
                <span>▼</span>
              </button>
            </div>

            {mode === 'custom' ? (
              <>
                {/* Custom Mode Controls */}
                <div className="custom-controls">
                  <div className="control-pills">
                    <button className="pill-btn">+ Persona</button>
                    <button className="pill-btn">+ Cover</button>
                    <button className="pill-btn">+ Creative Mode</button>
                  </div>

                  {/* File Upload Area */}
                  <div className="upload-section">
                    <label className="upload-label">Upload Audio File</label>
                    <input
                      type="file"
                      accept=".mp3,.wav,.flac,.ogg,.m4a"
                      onChange={handleFileSelect}
                      className="file-input"
                      id="file-input"
                    />
                    <label htmlFor="file-input" className="file-label">
                      {file ? (
                        <div className="file-selected-compact">
                          <span className="file-icon">🎵</span>
                          <span className="file-name">{file.name}</span>
                        </div>
                      ) : (
                        <div className="file-placeholder">
                          <span>📁 Choose audio file</span>
                        </div>
                      )}
                    </label>
                  </div>

                  {/* Styles Section */}
                  <div className="styles-section">
                    <label className="section-label">Styles (Optional)</label>
                    <input
                      type="text"
                      placeholder="Enter music styles or select from below."
                      className="styles-input"
                    />
                    <button className="random-style-btn">🎲 Random Style</button>
                    
                    <div className="style-tags">
                      <button className="style-tag">#Genre ▸</button>
                      <button className="style-tag">#Moods ▸</button>
                      <button className="style-tag">#Voices ▸</button>
                      <button className="style-tag">#Tempos ▸</button>
                    </div>
                  </div>

                  {/* Advanced Options */}
                  <details className="advanced-options">
                    <summary>
                      Advanced Options
                      <span className="badge-new">NEW</span>
                    </summary>
                    <div className="advanced-content">
                      <label className="checkbox-label">
                        <input type="checkbox" />
                        <span>Enhanced DSP Analysis</span>
                      </label>
                      <label className="checkbox-label">
                        <input type="checkbox" />
                        <span>Include Harmonic Analysis</span>
                      </label>
                    </div>
                  </details>
                </div>
              </>
            ) : (
              <>
                {/* Simple Mode */}
                <div className="simple-controls">
                  <div className="upload-section">
                    <label className="upload-label">Upload Audio File</label>
                    <input
                      type="file"
                      accept=".mp3,.wav,.flac,.ogg,.m4a"
                      onChange={handleFileSelect}
                      className="file-input"
                      id="file-input-simple"
                    />
                    <label htmlFor="file-input-simple" className="file-label-large">
                      {file ? (
                        <div className="file-selected-large">
                          <div className="file-icon-large">🎵</div>
                          <div className="file-info-large">
                            <div className="file-name-large">{file.name}</div>
                            <div className="file-size-large">
                              {(file.size / (1024 * 1024)).toFixed(2)} MB
                            </div>
                          </div>
                          <button 
                            className="remove-file-btn"
                            onClick={(e) => {
                              e.preventDefault();
                              setFile(null);
                            }}
                          >
                            ✕
                          </button>
                        </div>
                      ) : (
                        <div className="file-placeholder-large">
                          <div className="upload-icon-large">📁</div>
                          <div className="upload-text-large">
                            <div className="upload-title">Drop audio file here</div>
                            <div className="upload-subtitle">or click to browse</div>
                            <div className="upload-formats">MP3, WAV, FLAC, OGG, M4A</div>
                          </div>
                        </div>
                      )}
                    </label>
                  </div>
                </div>
              </>
            )}

            {/* Title Input */}
            <div className="title-section">
              <label className="section-label">Title (Optional)</label>
              <input
                type="text"
                placeholder="Enter analysis title..."
                className="title-input"
              />
            </div>

            {/* Analyze Button */}
            <button
              className="analyze-btn-main"
              onClick={handleAnalyze}
              disabled={!file || loading}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Analyzing...
                </>
              ) : (
                <>
                  ✨ Analyze Audio
                </>
              )}
            </button>

            {error && (
              <div className="error-message-compact">
                ⚠️ {error}
              </div>
            )}

            {/* Other Features Menu */}
            <div className="features-menu">
              <button className="feature-menu-item">🎹 Midi Studio</button>
              <button className="feature-menu-item">🎚️ Music Mastering</button>
              <button className="feature-menu-item">✍️ Lyric Writer</button>
              <button className="feature-menu-item">🧪 Experimental ▸</button>
            </div>
          </div>
        </aside>

        {/* Center Area - Analysis History */}
        <section className="center-area">
          <div className="center-header">
            <div className="search-bar">
              <input
                type="text"
                placeholder="please enter the song title to search"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="search-input"
              />
              <button className="search-add-btn">+</button>
              <button className="search-upload-btn">↑</button>
            </div>
          </div>

          <div className="analysis-gallery">
            {analysisHistory.length === 0 ? (
              <div className="empty-state">
                <div className="empty-icon">🎵</div>
                <h3>No analyses yet</h3>
                <p>Upload an audio file and click "Analyze Audio" to get started</p>
              </div>
            ) : (
              analysisHistory
                .filter(song => 
                  searchQuery === '' || 
                  song.fileName.toLowerCase().includes(searchQuery.toLowerCase())
                )
                .map(song => (
                  <div
                    key={song.id}
                    className={`song-card ${selectedSong?.id === song.id ? 'selected' : ''}`}
                    onClick={() => handleSelectSong(song)}
                  >
                    <div 
                      className="song-thumbnail"
                      style={{ background: `linear-gradient(135deg, ${song.thumbnail}, #1a1a2e)` }}
                    >
                      <div className="thumbnail-overlay">🎵</div>
                    </div>
                    
                    <div className="song-info">
                      <h3 className="song-title">{song.fileName}</h3>
                      
                      <div className="song-tags">
                        <span className="song-tag tag-merge">Analysis</span>
                        <span className="song-tag tag-vfi">v-Fi</span>
                      </div>

                      <div className="song-meta">
                        <span className="song-duration">{formatDuration(song.duration)}</span>
                        <span className="song-style">
                          {song.analysis.beat?.tempo_category || 'Unknown'} • 
                          {song.analysis.beat?.bpm ? ` ${Math.round(song.analysis.beat.bpm)} BPM` : ' No BPM'}
                        </span>
                      </div>

                      <div className="song-actions">
                        <button className="song-action-btn extend-btn">Extend</button>
                        <button 
                          className="song-action-btn more-btn"
                          onClick={(e) => {
                            e.stopPropagation();
                            handleRemoveSong(song.id);
                          }}
                        >
                          ⋯
                        </button>
                      </div>
                    </div>
                  </div>
                ))
            )}
          </div>
        </section>

        {/* Right Sidebar - Preview/Details */}
        <aside className="right-sidebar">
          {!selectedSong ? (
            <div className="preview-empty">
              <div className="dj-character">
                <div className="character-illustration">🎧</div>
              </div>
              <p className="preview-text">Select a song to preview.</p>
            </div>
          ) : (
            <div className="preview-details">
              <div className="details-header">
                <h3>Analysis Details</h3>
                <button 
                  className="close-details-btn"
                  onClick={() => {
                    setSelectedSong(null);
                    setAnalysis(null);
                  }}
                >
                  ✕
                </button>
              </div>

              <div className="details-scroll">
                {/* Key Insights */}
                {analysis && (
                  <>
                    <div className="detail-section">
                      <h4 className="detail-section-title">🎯 Key Insights</h4>
                      <div className="insight-grid-compact">
                        <div className="insight-compact">
                          <span className="insight-label-compact">Tempo</span>
                          <span className="insight-value-compact">
                            {analysis.beat?.tempo_category || 'Unknown'}
                          </span>
                        </div>
                        <div className="insight-compact">
                          <span className="insight-label-compact">BPM</span>
                          <span className="insight-value-compact">
                            {analysis.beat?.bpm ? Math.round(analysis.beat.bpm) : 'N/A'}
                          </span>
                        </div>
                        <div className="insight-compact">
                          <span className="insight-label-compact">Regularity</span>
                          <span className="insight-value-compact">
                            {analysis.beat?.regularity || 'N/A'}
                          </span>
                        </div>
                        <div className="insight-compact">
                          <span className="insight-label-compact">Strategy</span>
                          <span className="insight-value-compact">
                            {analysis.orchestration?.strategy || 'N/A'}
                          </span>
                        </div>
                      </div>
                    </div>

                    {/* Explanation */}
                    {analysis.explanation && (
                      <div className="detail-section">
                        <h4 className="detail-section-title">💬 AI Explanation</h4>
                        <p className="explanation-text-compact">{analysis.explanation}</p>
                      </div>
                    )}

                    {/* Structure */}
                    {analysis.structure?.sections && analysis.structure.sections.length > 0 && (
                      <div className="detail-section">
                        <h4 className="detail-section-title">🏗️ Structure</h4>
                        <div className="structure-timeline-compact">
                          {analysis.structure.sections.map((section, idx) => (
                            <div key={idx} className="structure-item-compact">
                              <span className="structure-label-compact">{section.type}</span>
                              <span className="structure-time-compact">
                                {formatDuration(section.start_time)} - {formatDuration(section.end_time)}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Energy Timeline */}
                    {analysis.energy?.timeline && analysis.energy.timeline.length > 0 && (
                      <div className="detail-section">
                        <h4 className="detail-section-title">⚡ Energy Dynamics</h4>
                        <div className="energy-bars-compact">
                          {analysis.energy.timeline.slice(0, 20).map((point, idx) => (
                            <div key={idx} className="energy-bar-compact">
                              <div
                                className={`energy-fill-compact energy-${point.category}`}
                                style={{ height: `${point.intensity * 100}%` }}
                                title={`${formatDuration(point.time)}: ${point.category}`}
                              />
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Pattern Analysis */}
                    {analysis.patterns && (
                      <div className="detail-section">
                        <h4 className="detail-section-title">🔄 Pattern Analysis</h4>
                        <div className="pattern-stats-compact">
                          <div className="pattern-stat-item">
                            <span className="pattern-label-mini">Repetition</span>
                            <div className="progress-mini">
                              <div 
                                className="progress-fill-mini"
                                style={{ width: `${(analysis.patterns.repetition_score || 0) * 100}%` }}
                              />
                            </div>
                          </div>
                          <div className="pattern-stat-item">
                            <span className="pattern-label-mini">Variation</span>
                            <div className="progress-mini">
                              <div 
                                className="progress-fill-mini"
                                style={{ width: `${(analysis.patterns.variation_score || 0) * 100}%` }}
                              />
                            </div>
                          </div>
                          <div className="pattern-stat-item">
                            <span className="pattern-label-mini">Predictability</span>
                            <span className="pattern-value-mini">
                              {analysis.patterns.predictability_score 
                                ? (analysis.patterns.predictability_score * 100).toFixed(0) + '%'
                                : 'N/A'}
                            </span>
                          </div>
                        </div>
                      </div>
                    )}
                  </>
                )}
              </div>

              {/* Character at bottom */}
              <div className="details-character">
                <div className="character-small">🎧</div>
              </div>
            </div>
          )}
        </aside>
      </main>
    </div>
  );
}

export default App;
