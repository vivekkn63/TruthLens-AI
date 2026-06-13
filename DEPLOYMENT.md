# DEPLOYMENT & GETTING STARTED GUIDE

## 🎯 What You Have

A complete, production-ready multi-agent AI orchestration system that:

✅ Researches topics using live web search  
✅ Writes category-specific blog posts (Science/Politics/Gaming)  
✅ Edits and polishes content with fact-checking  
✅ Implements human-in-the-loop feedback system  
✅ Supports up to 3 revision cycles  
✅ Exports blogs to Markdown files  

## 📦 Project Structure

```
d:\TruthLens AI/
├── main.py                          # ⭐ Start here: python main.py
├── quick_start.py                   # Demo: python quick_start.py
├── requirements.txt                 # Dependencies
├── state.py                         # State management
├── .env.example                     # API config template
├── .gitignore                       # Git ignore rules
├── setup.bat                        # Windows setup script
├── setup.sh                         # Linux/Mac setup script
│
├── README.md                        # 📖 Full documentation
├── ARCHITECTURE.md                  # 🏗️ System design details
├── API_SETUP.md                     # 🔑 API configuration guide
│
├── agents/
│   ├── researcher.py                # Research agent (web search)
│   ├── writer.py                    # Writing agent (blog creation)
│   ├── editor.py                    # Editing agent (review & polish)
│   └── __init__.py
│
├── graph/
│   ├── workflow.py                  # LangGraph orchestration
│   └── __init__.py
│
└── prompts/
    ├── researcher_prompts.py        # Research instructions
    ├── writer_prompts.py            # Writing instructions
    ├── editor_prompts.py            # Editing instructions
    └── __init__.py
```

## 🚀 Quick Start (5 minutes)

### Step 1: Install Dependencies

**On Windows (PowerShell)**:
```powershell
cd "d:\TruthLens AI"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**On Mac/Linux**:
```bash
cd "d/TruthLens AI"
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# or run: bash setup.sh
```

### Step 2: Configure API Keys

1. **Get OpenAI API Key**:
   - Go to https://platform.openai.com/api-keys
   - Create new secret key
   - Copy the key (starts with `sk-`)

2. **Get Tavily API Key**:
   - Go to https://tavily.com
   - Sign up or log in
   - Find API key in dashboard

3. **Create .env file**:
   ```bash
   # Copy from example
   cp .env.example .env
   
   # Edit .env with your keys
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxx
   TAVILY_API_KEY=tvly-xxxxxxxxxxxx
   ```

### Step 3: Run the System

**Try the demo first**:
```bash
python quick_start.py
```

**Run the interactive system**:
```bash
python main.py
```

**Follow the prompts**:
1. Select category (1=Science, 2=Politics, 3=Gaming)
2. Enter your topic
3. Review research → Draft → Final blog
4. Provide feedback or approve
5. Save to file if desired

## 📚 Complete Usage Guide

### Example 1: Science Topic

```
Category: Science
Topic: "Latest advances in quantum error correction"

↓ [Researcher researches quantum error correction]
↓ [Writer writes educational blog post]
↓ [Editor fact-checks and polishes]
↓ [You review - approve or request changes]
✓ Blog ready for publication!
```

### Example 2: Politics Topic

```
Category: Politics
Topic: "NEET Scam 2026 implications and accountability"

↓ [Researcher finds news reports and facts]
↓ [Writer writes hard-hitting analysis]
↓ [Editor verifies facts and strengthens arguments]
↓ [You review - approve or request changes]
✓ Blog ready for publication!
```

### Example 3: Gaming Topic

```
Category: Gaming
Topic: "AI integration in esports and competitive gaming"

↓ [Researcher finds tournament data and tech news]
↓ [Writer balances technical and casual appeal]
↓ [Editor verifies stats and polishes content]
↓ [You review - approve or request changes]
✓ Blog ready for publication!
```

## ⚙️ Configuration

### Change Default Settings

Edit `main.py`:
```python
# Change max iterations (line ~250)
state.max_iterations = 5  # Up from 3

# Change preview length (line ~150)
preview_length = 3000  # Up from 1000
```

Edit agent files for LLM settings:
```python
# In agents/researcher.py
self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

# In agents/writer.py
self.llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

# In agents/editor.py
self.llm = ChatOpenAI(model="gpt-4o", temperature=0.3)
```

### Customize Prompts

Edit prompts in `prompts/` folder:

```python
# prompts/researcher_prompts.py
RESEARCHER_SCIENCE = """Your custom research instructions..."""

# prompts/writer_prompts.py
WRITER_POLITICS = """Your custom writing instructions..."""

# prompts/editor_prompts.py
EDITOR_GAMING = """Your custom editing instructions..."""
```

## 🔧 Troubleshooting

### "API Key not set" Error

```
❌ Error: OPENAI_API_KEY not set in .env file

✓ Solution:
  1. Ensure .env file exists in project root
  2. Check it contains: OPENAI_API_KEY=sk-...
  3. Restart terminal/IDE
  4. Run python main.py again
```

### "Module not found" Error

```
❌ Error: ModuleNotFoundError: No module named 'langgraph'

✓ Solution:
  1. Activate virtual environment
  2. Run: pip install -r requirements.txt
  3. Verify all packages installed
```

### "Rate limited" Error

```
❌ Error: Rate limit exceeded for API

✓ Solution:
  1. Wait a few seconds and retry
  2. Check OpenAI account usage
  3. Consider upgrading API tier
  4. Run during off-peak hours
```

### No search results

```
❌ Error: Search returned no results

✓ Solution:
  1. Check Tavily API key is valid
  2. Try a different/simpler topic
  3. Check internet connection
  4. Verify Tavily account has searches left
```

## 📊 Expected Performance

| Phase | Time | Cost |
|-------|------|------|
| Research | 30-60 sec | ~$0.002 |
| Writing | 20-40 sec | ~$0.008 |
| Editing | 15-30 sec | ~$0.008 |
| **Total** | **~2-5 min** | **~$0.02** |

**Per month** (20 blog posts):
- Time: ~2 hours
- Cost: ~$0.40

## 💡 Tips for Best Results

### Research Tips
- Be specific with your topic
- Include relevant keywords
- Reference recent events if time-sensitive

### Writing Tips
- Approve if general quality is good
- Request revisions for specific issues
- Be clear about desired changes

### Editing Tips
- Review for accuracy first
- Check formatting and readability
- Request polish for final quality

### Approval Tips
- You can request up to 3 rounds of revisions
- After 3 rounds, system finalizes current version
- Save blog immediately after approval

## 🔐 Security Notes

✅ **DO**:
- Store API keys only in .env file
- Add .env to .gitignore
- Rotate keys periodically
- Keep keys secret

❌ **DON'T**:
- Commit .env to git
- Share API keys
- Paste keys into code
- Use same key for multiple projects

## 📈 Scaling the System

### For Higher Volume

1. **Upgrade API tiers**:
   - OpenAI: Better rate limits
   - Tavily: More searches per month

2. **Optimize costs**:
   - Use gpt-4o-mini more
   - Reduce search queries
   - Cache common research

3. **Add automation**:
   - Batch process multiple topics
   - Schedule daily runs
   - Build web interface

### For Better Quality

1. **Enhanced prompts**:
   - Customize for your audience
   - Add domain-specific context
   - Include examples

2. **Additional agents**:
   - Fact-checker agent
   - SEO optimizer
   - Social media post generator

3. **Extended feedback**:
   - More revision rounds
   - Specialized reviewers
   - A/B testing

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Full feature documentation |
| `ARCHITECTURE.md` | Technical deep dive |
| `API_SETUP.md` | API configuration guide |
| `DEPLOYMENT.md` | This file - getting started |

## 🎓 Learning Resources

- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **LangChain**: https://python.langchain.com/
- **OpenAI**: https://platform.openai.com/docs/
- **Tavily**: https://docs.tavily.com/

## 🤝 Support

For issues:
1. Check the relevant `.md` file
2. Verify API keys are configured
3. Test with `python quick_start.py`
4. Check error messages in terminal
5. Review TROUBLESHOOTING section above

## ✅ Verification Checklist

Before first use:

- [ ] Python 3.10+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with API keys
- [ ] OpenAI API key is valid (test: https://platform.openai.com/account/api-keys)
- [ ] Tavily API key is valid (test: https://tavily.com/dashboard)
- [ ] No errors when running `python quick_start.py`
- [ ] Can successfully run `python main.py`

## 🎉 Next Steps

1. **Start small**: Test with simple topics first
2. **Explore features**: Try all three categories
3. **Provide feedback**: Customize prompts to your needs
4. **Scale up**: Process more topics as you gain confidence
5. **Integrate**: Consider adding to your publishing workflow

## 🚀 You're Ready!

```bash
cd "d:\TruthLens AI"
python main.py
```

Good luck with your research and writing! 

**Happy blogging! ✨**

---

## Quick Reference Commands

```bash
# Activate environment
.\venv\Scripts\Activate.ps1

# Run demo
python quick_start.py

# Run main system
python main.py

# Check dependencies
pip list

# Update dependencies
pip install --upgrade -r requirements.txt

# Deactivate environment
deactivate
```

**Questions?** Check README.md or ARCHITECTURE.md for detailed information.
