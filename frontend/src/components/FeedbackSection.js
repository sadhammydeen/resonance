import React, { useState } from 'react';

function FeedbackSection({ onSubmitFeedback }) {
  const [understanding, setUnderstanding] = useState(null);
  const [comment, setComment] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = () => {
    if (!understanding) return;
    
    onSubmitFeedback(understanding, comment);
    setSubmitted(true);
    
    // Reset after 3 seconds
    setTimeout(() => {
      setSubmitted(false);
      setUnderstanding(null);
      setComment('');
    }, 3000);
  };

  return (
    <div className="feedback-section">
      <h2 style={{ color: '#667eea', marginBottom: '15px' }}>
        💬 Did This Make Sense?
      </h2>
      <p style={{ marginBottom: '20px', color: '#666' }}>
        Your feedback helps us adapt the explanations to your learning style
      </p>

      {!submitted ? (
        <>
          <div className="feedback-buttons">
            <button
              className={`feedback-button ${understanding === 'yes' ? 'selected' : ''}`}
              onClick={() => setUnderstanding('yes')}
            >
              ✅ Yes, Clear!
            </button>
            <button
              className={`feedback-button ${understanding === 'somewhat' ? 'selected' : ''}`}
              onClick={() => setUnderstanding('somewhat')}
            >
              🤔 Somewhat
            </button>
            <button
              className={`feedback-button ${understanding === 'no' ? 'selected' : ''}`}
              onClick={() => setUnderstanding('no')}
            >
              ❌ Not Really
            </button>
          </div>

          {understanding && (
            <div style={{ marginTop: '20px' }}>
              <textarea
                placeholder="Any additional comments? (optional)"
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                style={{
                  width: '100%',
                  padding: '15px',
                  borderRadius: '10px',
                  border: '2px solid #667eea',
                  fontSize: '1rem',
                  fontFamily: 'inherit',
                  marginBottom: '15px',
                  minHeight: '80px'
                }}
              />
              <button
                className="upload-button"
                onClick={handleSubmit}
              >
                Submit Feedback
              </button>
            </div>
          )}
        </>
      ) : (
        <div style={{ 
          background: '#e8f5e9', 
          padding: '20px', 
          borderRadius: '10px',
          color: '#2e7d32',
          fontWeight: 'bold'
        }}>
          ✅ Thank you! Your feedback helps us improve.
        </div>
      )}
    </div>
  );
}

export default FeedbackSection;
