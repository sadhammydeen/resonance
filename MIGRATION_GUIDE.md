# 🔄 Migration Checklist: Old → New Architecture

If you were using the original OpenAI-based system, follow this checklist to migrate to the new expert system architecture.

## Pre-Migration Assessment

### Check Your Current Setup

- [ ] Identify which version you're running
  ```bash
  # Old system has:
  backend/analysis/audio_analyzer.py (monolithic)
  backend/services/llm_service.py (OpenAI)
  
  # New system has:
  backend/experts/ (4 separate experts)
  backend/orchestrator/music_orchestrator.py
  backend/services/local_llm_service.py (HuggingFace)
  ```

- [ ] Document current API usage patterns
  - How many songs/month?
  - Average response times?
  - Current cost?

- [ ] Check dependencies
  ```bash
  pip list | grep openai  # If present, you're on old system
  ```

## Migration Steps

### Phase 1: Preparation (1 hour)

- [ ] **Back up current system**
  ```bash
  cp -r backend backend_backup_old
  cp -r frontend frontend_backup
  ```

- [ ] **Review new architecture**
  - [ ] Read [ARCHITECTURE_NEW.md](ARCHITECTURE_NEW.md)
  - [ ] Read [ARCHITECTURE_COMPARISON.md](ARCHITECTURE_COMPARISON.md)
  - [ ] Understand expert system concept

- [ ] **Check hardware requirements**
  - [ ] 4GB+ RAM minimum (8GB+ recommended)
  - [ ] ~5GB disk space for model
  - [ ] GPU optional but helpful

- [ ] **Install new dependencies**
  ```bash
  cd backend
  pip install transformers torch accelerate
  ```

### Phase 2: Testing (1 hour)

- [ ] **Test new system alongside old**
  ```bash
  # Keep old system running on :8000
  # Start new system on :8001
  uvicorn main:app --reload --port 8001
  ```

- [ ] **Run architecture test**
  ```bash
  python test_architecture.py
  ```

- [ ] **Compare outputs**
  - [ ] Upload same song to both systems
  - [ ] Compare analysis quality
  - [ ] Compare response times
  - [ ] Document differences

- [ ] **Test with sample files**
  - [ ] Different genres
  - [ ] Different lengths
  - [ ] Edge cases (very short, very long)

### Phase 3: Code Migration (2 hours)

- [ ] **Update route handlers**
  
  **Old routes.py**:
  ```python
  from analysis.audio_analyzer import AudioAnalyzer
  from services.llm_service import ExplanationGenerator
  
  analyzer = AudioAnalyzer()
  explainer = ExplanationGenerator()
  ```
  
  **New routes.py**:
  ```python
  from orchestrator.music_orchestrator import MusicOrchestrator
  from services.local_llm_service import get_llm_service
  
  orchestrator = MusicOrchestrator()
  llm_service = get_llm_service()
  ```

- [ ] **Update analysis calls**
  
  **Old**:
  ```python
  analysis = analyzer.analyze(file_path)
  explanation = explainer.generate(analysis)
  ```
  
  **New**:
  ```python
  music_state = orchestrator.analyze(file_path)
  explanation = llm_service.generate_explanation(music_state)
  ```

- [ ] **Update response format**
  - [ ] Check frontend expects new JSON structure
  - [ ] Update field mappings if needed
  - [ ] Test all visualization components

- [ ] **Remove OpenAI dependencies**
  ```bash
  pip uninstall openai
  ```
  
  ```python
  # Remove from code:
  # import openai
  # openai.api_key = ...
  ```

- [ ] **Update environment variables**
  - [ ] Remove `OPENAI_API_KEY`
  - [ ] Add `LOCAL_MODEL_NAME` (optional)

### Phase 4: Frontend Updates (1 hour)

- [ ] **Update API calls** (if response format changed)
  ```javascript
  // Old
  const { analysis, explanations } = response.data;
  
  // New
  const { analysis, explanation } = response.data;
  // Note: 'analysis' structure is different
  ```

- [ ] **Update data mappings**
  ```javascript
  // Old
  const bpm = analysis.rhythm.bpm;
  
  // New
  const bpm = analysis.rhythm.bpm; // Same!
  ```

- [ ] **Test all visualizations**
  - [ ] RhythmMap component
  - [ ] EmotionTimeline component
  - [ ] StructureView component
  - [ ] ExplanationPanel component

### Phase 5: Validation (1 hour)

- [ ] **Functional testing**
  - [ ] Upload works
  - [ ] Analysis completes
  - [ ] Visualizations render
  - [ ] Explanation displays
  - [ ] Feedback works

- [ ] **Performance testing**
  - [ ] Measure average response time
  - [ ] Compare to old system
  - [ ] Check memory usage
  - [ ] Monitor CPU/GPU usage

- [ ] **Quality testing**
  - [ ] Analysis accuracy
  - [ ] Explanation quality
  - [ ] Edge case handling
  - [ ] Error messages

### Phase 6: Deployment (30 min)

- [ ] **Update deployment scripts**
  ```bash
  # Old requirements.txt
  - openai==1.x.x
  
  # New requirements.txt
  + transformers==4.36.0
  + torch==2.1.0
  + accelerate==0.25.0
  ```

- [ ] **Update documentation**
  - [ ] Update README
  - [ ] Update API docs
  - [ ] Update setup guides

- [ ] **Deploy to staging**
  - [ ] Test thoroughly
  - [ ] Monitor for issues
  - [ ] Get user feedback

- [ ] **Deploy to production**
  - [ ] Blue-green deployment recommended
  - [ ] Monitor metrics
  - [ ] Have rollback plan ready

### Phase 7: Cleanup (15 min)

- [ ] **Remove old code**
  ```bash
  rm -rf backend/analysis/  # Monolithic analyzer
  rm backend/services/llm_service.py  # OpenAI service
  ```

- [ ] **Update .gitignore**
  ```
  # Add model cache
  .cache/
  models/
  ```

- [ ] **Update documentation**
  - [ ] Archive old docs
  - [ ] Point to new architecture docs

## Cost Comparison

### Old System (OpenAI)
```
Monthly volume: 1000 songs
Cost per song: $0.15
Monthly cost: $150
Yearly cost: $1,800
```

### New System (Local)
```
Monthly volume: 1000 songs
Cost per song: ~$0.001 (electricity)
Monthly cost: ~$1
Yearly cost: ~$12
Savings: $1,788/year
```

**ROI**: Positive after ~30 songs

## Rollback Plan

If you need to revert:

1. **Stop new system**
   ```bash
   # Kill new server
   pkill -f "uvicorn.*8001"
   ```

2. **Restore old code**
   ```bash
   rm -rf backend
   cp -r backend_backup_old backend
   ```

3. **Reinstall old dependencies**
   ```bash
   pip install openai
   ```

4. **Restart old system**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

5. **Update frontend** (if needed)

## Common Issues

### Issue: Model download fails
**Solution**: 
```bash
# Pre-download model
python -c "from transformers import AutoModelForCausalLM; \
           AutoModelForCausalLM.from_pretrained('microsoft/phi-2')"
```

### Issue: Out of memory
**Solutions**:
- Use smaller model: `tinyllama` or `flan-t5-base`
- Reduce batch size
- Close other applications

### Issue: Analysis too slow
**Solutions**:
- Use GPU if available
- Use smaller model
- Reduce audio segment duration

### Issue: Explanation quality poor
**Solutions**:
- Switch to `phi-2` (better quality)
- Adjust temperature/prompts
- Use fallback templates

## Validation Checklist

After migration, verify:

- [ ] All API endpoints work
- [ ] Response format matches frontend expectations
- [ ] Visualizations render correctly
- [ ] Explanation quality acceptable
- [ ] Performance acceptable
- [ ] Error handling works
- [ ] Logs are informative
- [ ] No OpenAI API calls being made
- [ ] Cost reduced to near-zero
- [ ] System works offline

## Timeline Summary

| Phase | Duration | Can Skip? |
|-------|----------|-----------|
| Preparation | 1 hour | No |
| Testing | 1 hour | No |
| Code Migration | 2 hours | No |
| Frontend Updates | 1 hour | If no frontend |
| Validation | 1 hour | No |
| Deployment | 30 min | No |
| Cleanup | 15 min | Yes |
| **Total** | **6-7 hours** | |

## Success Metrics

Track these to ensure successful migration:

- [ ] **Cost**: Reduced by >90%
- [ ] **Latency**: <30 seconds on CPU, <10s on GPU
- [ ] **Accuracy**: Equal or better than before
- [ ] **Uptime**: No regressions
- [ ] **User Satisfaction**: Maintained or improved

## Post-Migration

### Week 1
- [ ] Monitor performance metrics
- [ ] Collect user feedback
- [ ] Fix any issues
- [ ] Tune orchestrator rules if needed

### Week 2-4
- [ ] Optimize performance
- [ ] Improve explanation quality
- [ ] Add customizations
- [ ] Document learnings

### Month 2+
- [ ] Add new experts
- [ ] Enhance visualizations
- [ ] Consider advanced features

## Getting Help

If stuck during migration:

1. **Check docs**: [SETUP_NEW.md](SETUP_NEW.md)
2. **Compare architectures**: [ARCHITECTURE_COMPARISON.md](ARCHITECTURE_COMPARISON.md)
3. **Test in isolation**: Use `test_architecture.py`
4. **Check logs**: Look for detailed error messages

## Migration Complete!

Once all checkboxes are checked:

- [ ] **System runs on new architecture**
- [ ] **All tests pass**
- [ ] **Users can upload and analyze songs**
- [ ] **Costs reduced significantly**
- [ ] **No OpenAI dependencies**
- [ ] **Old code removed**

🎉 **Congratulations!** You're now running the new expert system architecture.

---

**Estimated time to complete**: 6-7 hours  
**Cost savings**: ~$150+/month  
**Benefits**: Offline capability, transparency, customizability
