# ⚡ Quick Reference Card

## 🚀 Start the Application

**Windows:**
```bash
start.bat
```

**Mac/Linux:**
```bash
chmod +x start.sh
./start.sh
```

**Manual Start:**
```bash
# Terminal 1 - Backend
cd backend
venv\Scripts\activate    # Windows: venv\Scripts\activate
python main.py

# Terminal 2 - Frontend
cd frontend
npm start
```

---

## 🔑 Essential URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 📝 Configuration

### Backend (.env)
```bash
cd backend
copy .env.example .env
# Edit .env and add:
OPENAI_API_KEY=sk-your-key-here
```

---

## 🎯 API Endpoints

### Analyze Audio
```bash
POST /api/analyze
Content-Type: multipart/form-data

Body:
- file: audio file (MP3/WAV/M4A)
- user_level: "beginner" | "intermediate" | "advanced"

Returns: Complete analysis with visualizations
```

### Submit Feedback
```bash
POST /api/feedback
Content-Type: multipart/form-data

Body:
- file_id: string
- understanding: "yes" | "somewhat" | "no"
- comment: string (optional)

Returns: Adaptive suggestions
```

---

## 🧪 Testing Checklist

- [ ] Backend starts without errors
- [ ] Frontend opens in browser
- [ ] Can upload audio file
- [ ] Analysis completes successfully
- [ ] All visualizations display
- [ ] AI explanations generate
- [ ] Feedback system works

---

## 🐛 Common Errors & Fixes

| Error | Fix |
|-------|-----|
| "Module not found" | `pip install -r requirements.txt` |
| "Port already in use" | Kill process on port 8000/3000 |
| "OpenAI API error" | Check API key in `.env` |
| "File upload fails" | Check file size < 50MB |
| "Cannot connect" | Start backend first |

---

## 📦 Dependencies

### Backend
- Python 3.9+
- librosa (audio analysis)
- FastAPI (web framework)
- OpenAI (AI explanations)

### Frontend
- Node.js 16+
- React (UI)
- Recharts (visualizations)
- Axios (API client)

---

## 🎵 Sample Test Songs

Good test cases:
1. **Pop song**: Clear beat, repetitive structure
2. **Ballad**: Emotional arc, clear build-up
3. **Classical**: Complex structure, variations
4. **EDM**: Strong rhythm, obvious drops

---

## 📊 Key Metrics to Track

- Upload success rate
- Analysis completion time
- User feedback (yes/somewhat/no)
- Time spent per visualization
- Most common user questions

---

## 🎯 Validation Questions

Test with users:
1. "Can you tell when the music repeats?"
2. "Can you feel tension vs release?"
3. "Do the visuals make sense without sound?"

Success = 7/10 users answer "yes" to each

---

## 🔄 Git Commands

```bash
# Initialize repo
git init
git add .
git commit -m "Initial commit - MVP complete"

# Create GitHub repo
git remote add origin <your-repo-url>
git push -u origin main
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `backend/main.py` | API entry point |
| `backend/analysis/audio_analyzer.py` | Core analysis engine |
| `backend/services/llm_service.py` | AI explanations |
| `frontend/src/App.js` | Main React app |
| `frontend/src/components/` | UI components |

---

## 💡 Quick Tips

1. **Test locally first** - Use sample audio files
2. **Check console logs** - Errors appear in terminal
3. **API docs available** - Visit /docs endpoint
4. **Fallback mode** - Works without OpenAI key (basic explanations)
5. **File cleanup** - Old uploads stored in `backend/uploads/`

---

## 🚨 Before Demo/Pitch

- [ ] Test with 10+ songs
- [ ] Get 5+ user testimonials
- [ ] Record demo video
- [ ] Prepare presentation
- [ ] Document user validation results
- [ ] Create GitHub repo with README
- [ ] Screenshots of best examples

---

## 📞 Support Resources

- **Setup Guide**: `SETUP.md`
- **Validation Guide**: `VALIDATION_GUIDE.md`
- **Full Overview**: `PROJECT_SUMMARY.md`
- **Main README**: `README.md`

---

## 🎓 How It Works (30-Second Explanation)

1. User uploads music file
2. librosa extracts beat patterns, structure, emotions
3. OpenAI converts technical data to plain language
4. React visualizes everything without requiring sound
5. User learns music through patterns, not audio

**Core Innovation**: Redesigns music education without sound dependency

---

Keep this card handy while developing! 🚀
