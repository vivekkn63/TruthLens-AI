# TruthLens AI - Multi-Agent Orchestration System

A sophisticated multi-agent system that researches topics, writes engaging blog posts, and edits content with human-in-the-loop feedback.

## 🎯 Features

### Multi-Category Support
- **Science**: In-depth research on AI, technology, and scientific topics with key terms and formulas
- **Politics**: Hard-hitting, fact-based analysis of current affairs and political issues
- **Gaming**: Comprehensive coverage of games, trends, and gaming industry news

### Intelligent Agent Workflow
1. **🔍 Researcher Agent**: Conducts thorough online research using web search
2. **✍️ Writer Agent**: Transforms research into engaging, category-specific blog content
3. **✏️ Editor Agent**: Reviews, fact-checks, and polishes the final content
4. **👤 Human Review**: Human-in-the-loop feedback system with revision capabilities

### Smart Features
- **Iterative Refinement**: Up to 3 revision cycles based on human feedback
- **Category-Specific Prompts**: Each agent adapts its behavior based on topic category
- **Fact-Checking**: Editor verifies all claims against research data
- **Web Research**: Real-time web search using Tavily API for current information
- **Flexible Routing**: Intelligent routing to Writer or Editor based on feedback type

## 🏗️ Project Structure

```
TruthLens AI/
├── main.py                  # Entry point with interactive CLI
├── state.py                 # State management and data models
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── agents/
│   ├── researcher.py       # Research agent with web search
│   ├── writer.py           # Blog writing agent
│   └── editor.py           # Content editing agent
├── graph/
│   └── workflow.py         # LangGraph orchestration
└── prompts/
    ├── researcher_prompts.py  # Research system prompts
    ├── writer_prompts.py      # Writing system prompts
    └── editor_prompts.py      # Editing system prompts
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- OpenAI API key
- Tavily API key (for web search)

### Installation

1. **Clone/Setup the project**
```bash
cd "d:\TruthLens AI"
```

2. **Create virtual environment**
```bash
python -m venv venv
.\venv\Scripts\activate  # On Windows
# or: source venv/bin/activate  # On macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env and add your API keys
# OPENAI_API_KEY=your_key_here
# TAVILY_API_KEY=your_key_here
```

### Running the System

```bash
python main.py
```

Then follow the interactive prompts to:
1. Select a research category (Science/Politics/Gaming)
2. Enter your topic
3. Review the research, draft, and final content
4. Provide feedback or approve for publication

## 📊 Workflow Diagram

```
Input (Category + Topic)
        ↓
    Research  ← → Web Search
        ↓
    Writing   → Blog Draft
        ↓
    Editing   → Polished Blog
        ↓
    Human Review
        ↓
    [Approve?]
    ↙         ↘
   Yes         No (up to 3x)
    ↓          ↓
Publish    Writer/Editor Revise
           ↓
        Re-edit/Review
```

## 🤖 Agent Details

### Researcher Agent
- Conducts multi-query web searches for comprehensive coverage
- Processes and synthesizes search results
- Prioritizes credible, authoritative sources
- Category-specific search strategies:
  - **Science**: Peer-reviewed articles, academic sources
  - **Politics**: News from multiple outlets, official documents, fact-checks
  - **Gaming**: Industry news, developer statements, community feedback

### Writer Agent
- Transforms research into engaging narrative
- Category-specific writing styles:
  - **Science**: Educational, accessible, captures formulas and terminology
  - **Politics**: Direct, fact-based, unsparing about falsehoods
  - **Gaming**: Enthusiastic, technical depth with broad appeal
- Target length: 1500-2500 words

### Editor Agent
- Fact-checks against research data
- Corrects inaccuracies and improves clarity
- Enhances readability and structure
- Polishes language and tone
- Ensures category standards are met

## 🔧 API Keys Setup

### OpenAI API
1. Go to https://platform.openai.com/api-keys
2. Create a new secret key
3. Add to `.env`: `OPENAI_API_KEY=sk-...`

### Tavily API
1. Go to https://tavily.com
2. Sign up for a free account
3. Get your API key from dashboard
4. Add to `.env`: `TAVILY_API_KEY=...`

## 📝 Example Workflows

### Science Topic
```
Topic: "Recent advances in quantum error correction"
→ Research finds latest papers and breakthroughs
→ Writer explains quantum computing concepts clearly
→ Editor verifies technical accuracy and formulas
→ Published: Educational blog with key terminology
```

### Politics Topic
```
Topic: "NEET Scam 2026 and its implications"
→ Research finds news reports and official documents
→ Writer presents facts with harsh assessment of wrongdoing
→ Editor fact-checks all claims rigorously
→ Published: Hard-hitting accountability piece
```

### Gaming Topic
```
Topic: "The rise of AI in competitive gaming"
→ Research finds tournament data and developer statements
→ Writer covers both casual and technical aspects
→ Editor verifies game mechanics and statistics
→ Published: Comprehensive industry analysis
```

## 🎮 Interactive Features

- **Real-time Feedback**: Provide revisions at any stage
- **Smart Routing**: System automatically routes to appropriate agent for revisions
- **Multiple Iterations**: Up to 3 revision cycles to perfect the content
- **Save to File**: Export final blog post as Markdown
- **Full Transparency**: See all agent actions and workflow steps

## ⚙️ Configuration

Edit `main.py` to customize:
- Maximum iterations (currently 3)
- Blog post length targets
- Display length in console (currently shows first 1000-2000 chars)

Edit agent files to customize:
- LLM temperature settings
- Model selection (gpt-4o, gpt-4o-mini, etc.)
- Search result limits
- Output formats

## 🐛 Troubleshooting

### API Key Issues
```
❌ Error: OPENAI_API_KEY not set
→ Check .env file has OPENAI_API_KEY with a valid key
```

### Web Search Not Working
```
⚠️ Warning: TAVILY_API_KEY not set
→ Functionality will be limited. Add key to .env to enable full research
```

### Rate Limiting
- OpenAI has rate limits. If you hit them, wait a moment and try again
- For heavy use, consider upgrading your OpenAI tier

## 📦 Dependencies

- **langgraph**: Multi-agent orchestration
- **langchain**: LLM framework and tools
- **langchain-openai**: OpenAI integration
- **tavily-python**: Web search API
- **python-dotenv**: Environment variable management
- **pydantic**: Data validation

## 🎓 Learning Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Guide](https://platform.openai.com/docs/api-reference)
- [Tavily API Docs](https://docs.tavily.com/)

## 📄 License

This project is open source and available for educational and personal use.

## 🤝 Contributing

Feel free to enhance the system by:
- Adding new categories beyond Science/Politics/Gaming
- Improving agent prompts for better output
- Adding new features (fact-checking, source analysis, etc.)
- Optimizing web search strategies

## ❓ FAQ

**Q: Can I use this for commercial content?**
A: Yes, but ensure you have proper API key subscriptions and respect content licensing.

**Q: How long does a full workflow take?**
A: Typically 3-5 minutes for research, writing, and initial editing. Revisions add 1-2 minutes each.

**Q: Can I customize the prompts?**
A: Yes! Edit the prompt files in `prompts/` directory to adjust agent behavior.

**Q: What if I disagree with the research?**
A: The feedback system allows you to request revisions. Multiple iterations help refine the content.

**Q: How many sources does the researcher use?**
A: Typically 5-10 top sources per search, with multiple searches per topic for comprehensive coverage.

---

**Happy researching and writing! 🚀**
