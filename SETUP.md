## 🚀 Quick Start Guide

Follow these steps to get Resonance Without Sound running on your machine.

### Prerequisites
- **Python 3.9+** installed
- **Node.js 16+** and npm installed
- **OpenAI API Key** (get one from https://platform.openai.com/api-keys)

---

## Backend Setup

### 1. Navigate to backend directory
```bash
cd backend
```

### 2. Create Python virtual environment
```bash
python -m venv venv
```

### 3. Activate virtual environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Python dependencies
```bash
pip install -r requirements.txt
```

This will install:
- FastAPI (web framework)
- librosa (audio analysis)
- OpenAI Python SDK
- And other required packages

### 5. Configure environment variables

Copy the example env file:
```bash
copy .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

### 6. Run the backend server
```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --reload
```

✅ Backend should now be running at: **http://localhost:8000**

Test it: Open http://localhost:8000 in your browser - you should see a health check message.

---

## Frontend Setup

### 1. Open a NEW terminal (keep backend running)

### 2. Navigate to frontend directory
```bash
cd frontend
```

### 3. Install Node dependencies
```bash
npm install
```

This will install:
- React
- Recharts (for visualizations)
- Axios (for API calls)

### 4. Start the React development server
```bash
npm start
```

✅ Frontend should automatically open at: **http://localhost:3000**

---

## 🎵 Using the Application

1. **Upload a song**: Click the upload area and select an MP3, WAV, or M4A file
2. **Choose learning level**: Select beginner, intermediate, or advanced
3. **Analyze**: Click "Analyze Music" button
4. **Explore results**: 
   - View rhythm map (beat patterns)
   - See emotion timeline (how the music feels)
   - Read structure breakdown (sections like intro, verse, chorus)
   - Read AI explanations in plain language
5. **Provide feedback**: Let us know if it made sense!

---

## Troubleshooting

### Backend won't start
- Make sure Python 3.9+ is installed: `python --version`
- Verify virtual environment is activated (you should see `(venv)` in terminal)
- Check if port 8000 is already in use

### Frontend won't start
- Make sure Node.js is installed: `node --version`
- Delete `node_modules` and `package-lock.json`, then run `npm install` again
- Check if port 3000 is already in use

### Analysis fails
- Verify your OpenAI API key is correct in `.env`
- Make sure the audio file is under 50MB
- Try with a different audio file
- Check backend terminal for error messages

### "Module not found" errors
- Backend: Make sure you activated the virtual environment
- Frontend: Run `npm install` again

---

## File Structure
```
ai_ignite/
├── backend/
│   ├── main.py                 # FastAPI app entry point
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Your configuration (create from .env.example)
│   ├── api/
│   │   └── routes.py          # API endpoints
│   ├── analysis/
│   │   └── audio_analyzer.py  # Core audio analysis engine
│   └── services/
│       ├── config.py          # Configuration management
│       └── llm_service.py     # LLM explanation generator
├── frontend/
│   ├── package.json           # Node dependencies
│   ├── src/
│   │   ├── App.js            # Main React app
│   │   ├── index.js          # React entry point
│   │   ├── index.css         # Global styles
│   │   └── components/       # React components
│   │       ├── RhythmMap.js
│   │       ├── EmotionTimeline.js
│   │       ├── StructureView.js
│   │       ├── ExplanationPanel.js
│   │       └── FeedbackSection.js
│   └── public/
│       └── index.html        # HTML template
└── README.md                 # Project documentation
```

---

## Next Steps

Once everything is running:

1. **Test with different songs**: Try various genres and tempos
2. **Experiment with learning levels**: See how explanations adapt
3. **Gather feedback**: Share with potential users
4. **Iterate**: Based on feedback, improve visualizations and explanations

---

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Look at terminal output for error messages
3. Ensure all dependencies are installed correctly
4. Verify API keys and configuration

---

Built with ❤️ for accessible music education
