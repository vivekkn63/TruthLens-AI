# Customization & Extension Guide

This guide helps you modify and extend TruthLens AI for your specific needs.

---

## 🎯 Customization Checklist

### Modify Agent Behavior

#### Change Research Strategy
**File**: `agents/researcher.py`

```python
# Line ~100: Modify search queries
search_queries = [
    f"{state.topic} {state.category}",  # Modify
    state.topic,                         # Modify
    f"recent research {state.topic}",   # Modify
    f"latest news {state.topic}",       # Modify
]

# Add more queries for deeper research
search_queries.extend([
    f"{state.topic} analysis",
    f"{state.topic} trends",
    f"{state.topic} impact",
])
```

#### Change Writing Style
**File**: `agents/writer.py` or `prompts/writer_prompts.py`

```python
# Make writing more formal/casual
WRITER_SCIENCE = """
You are a technical writer...
[Edit instructions here]
"""

# Adjust target audience
def _get_audience(self, category: str) -> str:
    audiences = {
        "science": "PhD students and researchers",  # Changed from "Students, academics..."
        "politics": "Policy makers and analysts",   # Changed
        "gaming": "Professional esports players",   # Changed
    }
    return audiences.get(category.lower(), "General readers")
```

#### Change Editing Standards
**File**: `agents/editor.py` or `prompts/editor_prompts.py`

```python
# Focus on specific quality metrics
EDITOR_SCIENCE = """
You are an expert science editor...

PRIORITY EDITING FOCUS:
1. Formula accuracy (highest priority)
2. Technical terminology
3. Citation accuracy
[...]
"""
```

### Customize Prompts

#### For Science Topics
**File**: `prompts/researcher_prompts.py`

Add specific focus areas:
```python
RESEARCHER_SCIENCE = """
...existing content...

RESEARCH PRIORITIES:
1. Recent breakthroughs (2024+)
2. Academic consensus
3. Competing theories
4. Practical applications
5. Limitations and unknowns
"""
```

#### For Politics Topics
**File**: `prompts/writer_prompts.py`

Adjust tone:
```python
WRITER_POLITICS = """
...existing content...

TONE GUIDELINES:
- Truthful but diplomatic
- [or: Truthful but unsparing]
- [or: Truthful and provocative]

AUDIENCE LEVEL:
- Academic/policy level
- Educated public
- General readers
"""
```

#### For Gaming Topics
**File**: `prompts/editor_prompts.py`

Add specific checks:
```python
EDITOR_GAMING = """
...existing content...

CRITICAL FACT-CHECKS:
□ Game release dates
□ Player statistics
□ Developer statements
□ Tournament results
□ Technical specifications
"""
```

---

## 🚀 Extensions & New Features

### Add a New Category

#### Step 1: Create Prompts
**File**: `prompts/researcher_prompts.py`

```python
RESEARCHER_HEALTH = """You are a medical researcher specializing in...

MISSION: Research health and medical topics thoroughly.

YOUR APPROACH:
1. Search for peer-reviewed medical journals
2. Find authoritative health organizations
3. Check for clinical trials and evidence
4. Note conflicting medical advice
5. Prioritize established medical consensus

DELIVERABLE FORMAT:
...
"""
```

#### Step 2: Add to Agent Dictionaries
**File**: `agents/researcher.py`

```python
self.prompts = {
    "science": RESEARCHER_SCIENCE,
    "politics": RESEARCHER_POLITICS,
    "gaming": RESEARCHER_GAMING,
    "health": RESEARCHER_HEALTH,  # NEW
}
```

Repeat for writer and editor agents.

#### Step 3: Update Main Menu
**File**: `main.py`

```python
def get_category() -> str:
    """Get topic category from user"""
    print_header("SELECT RESEARCH CATEGORY")
    print("Available categories:")
    print("  1. Science (AI, Technology, Research)")
    print("  2. Politics (Current Affairs, Government)")
    print("  3. Gaming (Games, Industry, Trends)")
    print("  4. Health (Medicine, Wellness, Nutrition)")  # NEW
    
    categories = {
        "1": "Science",
        "2": "Politics",
        "3": "Gaming",
        "4": "Health",  # NEW
    }
```

### Add a Fact-Checking Agent

**File**: `agents/fact_checker.py`

```python
"""
Fact-Checking Agent - Verifies claims in blog posts
"""

class FactCheckingAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.1)
    
    def fact_check(self, state: AgentState) -> AgentState:
        """Verify claims in the blog post"""
        
        # Extract claims from blog
        claim_extraction_prompt = f"""
Extract 10 key factual claims from this blog post:

{state.blog_final}

For each claim, identify what would need to be verified.
"""
        
        response = self.llm.invoke([HumanMessage(content=claim_extraction_prompt)])
        claims = response.content
        
        # Verify against research
        verification_prompt = f"""
Based on this research data:

{state.research_content}

Verify these claims from the blog post:

{claims}

List any discrepancies or unverified claims.
"""
        
        response = self.llm.invoke([HumanMessage(content=verification_prompt)])
        state.fact_check_results = response.content
        
        return state
```

Then add to workflow in `graph/workflow.py`:
```python
workflow.add_node("fact_check", fact_check_node)
workflow.add_edge("edit", "fact_check")
workflow.add_edge("fact_check", "human_review")
```

### Add SEO Optimization

**File**: `agents/seo_optimizer.py`

```python
class SEOOptimizer:
    def optimize(self, state: AgentState) -> AgentState:
        """Add SEO metadata and optimization"""
        
        seo_prompt = f"""
Optimize this blog post for SEO:

Title: {state.topic}
Blog: {state.blog_final}

Provide:
1. Optimized title (50-60 chars)
2. Meta description (155-160 chars)
3. Keywords (5-10 main keywords)
4. Suggested headers structure
5. Internal linking suggestions
"""
        
        # ... implementation
        return state
```

### Add Image Search

**File**: `agents/image_searcher.py`

```python
class ImageSearcher:
    def search_images(self, state: AgentState) -> AgentState:
        """Find relevant images for blog post"""
        
        # Use Unsplash API or similar
        from unsplash.api import Api
        
        api = Api(api_key=os.getenv("UNSPLASH_API_KEY"))
        
        # Search for topic-relevant images
        images = api.search.photos(query=state.topic, per_page=5)
        
        state.suggested_images = [
            {
                "url": photo.urls.full,
                "credit": photo.user.name,
                "description": photo.description
            }
            for photo in images.entries
        ]
        
        return state
```

### Add Social Media Post Generation

**File**: `agents/social_media.py`

```python
class SocialMediaAgent:
    def generate_posts(self, state: AgentState) -> AgentState:
        """Generate social media posts from blog"""
        
        prompt = f"""
From this blog post, create social media posts:

Blog Title: {state.topic}
Blog: {state.blog_final}

Generate:
1. Twitter post (280 chars) - engaging hook
2. LinkedIn post (1300 chars) - professional angle
3. Instagram caption (2200 chars) - visual focus
4. Facebook post (500 chars) - conversational

Each should drive to the blog URL.
"""
        
        # ... implementation
        return state
```

---

## 🔧 Configuration Changes

### Adjust Iteration Limits

**File**: `main.py`

```python
state = AgentState(
    category=category,
    topic=topic,
    iteration_count=0,
    max_iterations=5  # Changed from 3
)
```

### Change Default Models

**File**: `agents/*.py`

```python
# Use faster model for everything
self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

# Or use more powerful model
self.llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.3)
```

### Adjust Temperature Settings

**File**: `agents/*.py`

```python
# Lower = more deterministic/accurate
self.llm = ChatOpenAI(model="gpt-4o", temperature=0.1)

# Higher = more creative/diverse
self.llm = ChatOpenAI(model="gpt-4o", temperature=0.9)
```

### Change Preview Lengths

**File**: `main.py`

```python
# Show more of the blog in preview
if len(blog_final) > 5000:  # Changed from 2000
    print(blog_final[:5000])
```

---

## 🎯 Advanced Customizations

### Multi-Agent Debate System

Have agents argue different perspectives:

```python
def debate_topic(state: AgentState) -> AgentState:
    """Have agents debate the topic"""
    
    agent_a_view = llm.invoke([
        HumanMessage(content=f"Argue FOR {state.topic}...")
    ])
    
    agent_b_view = llm.invoke([
        HumanMessage(content=f"Argue AGAINST {state.topic}...")
    ])
    
    # Synthesize both views
    state.debate_analysis = f"""
For: {agent_a_view}

Against: {agent_b_view}

Both perspectives are valid. Consider them when writing.
"""
    
    return state
```

### Dynamic Prompt Generation

Instead of static prompts, generate them based on context:

```python
def generate_dynamic_prompt(category: str, topic: str) -> str:
    """Generate prompt based on specific topic"""
    
    context_prompt = f"""
Create a research prompt for:
Category: {category}
Topic: {topic}

The prompt should:
1. Tailor search strategy to topic specifics
2. Identify key sources to prioritize
3. Define research success metrics
4. List important concepts to capture
"""
    
    response = llm.invoke([HumanMessage(content=context_prompt)])
    return response.content
```

### Custom Feedback Routing

Intelligent routing instead of keyword matching:

```python
def intelligent_route(state: AgentState) -> str:
    """Use LLM to decide routing"""
    
    routing_prompt = f"""
Given this feedback:
"{state.human_feedback}"

Is this feedback about:
A) Writing (content, structure, tone, flow)
B) Editing (grammar, formatting, accuracy, polish)
C) Research (information accuracy, sources, depth)

Choose the agent to route to for best results.
"""
    
    response = llm.invoke([HumanMessage(content=routing_prompt)])
    
    if "Writing" in response.content:
        return "writer_revise"
    elif "Editing" in response.content:
        return "editor_revise"
    else:
        return "research"  # If research issues, start over
```

---

## 📊 Monitoring & Analytics

### Track Metrics

```python
# In state.py, add tracking
class AgentState(BaseModel):
    # ... existing fields ...
    
    # Tracking
    research_time: float = 0
    write_time: float = 0
    edit_time: float = 0
    total_tokens: int = 0
    total_cost: float = 0
    revision_count: int = 0
    user_satisfaction: int = 0  # 1-5 scale
```

### Log Detailed Metrics

```python
# In agents, track execution time
import time

def research(self, state: AgentState) -> AgentState:
    start_time = time.time()
    
    # ... research code ...
    
    state.research_time = time.time() - start_time
    return state
```

---

## 🔌 Integration Points

### Database Integration

```python
# Save blog posts to database
from sqlalchemy import create_engine, Column, String, DateTime

class BlogPost(Base):
    __tablename__ = "blog_posts"
    id = Column(Integer, primary_key=True)
    topic = Column(String)
    category = Column(String)
    content = Column(String)
    created_at = Column(DateTime)
    published = Column(Boolean)

# After approval:
db.add(BlogPost(topic=state.topic, content=state.blog_final, ...))
db.commit()
```

### API Endpoint Integration

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/research")
async def research_endpoint(category: str, topic: str):
    state = AgentState(category=category, topic=topic)
    result = app.invoke(state)
    return {"blog": result.blog_final, "sources": result.research_sources}
```

### Webhook Integration

```python
import requests

# Send results to external service
result = {
    "blog": state.blog_final,
    "category": state.category,
    "topic": state.topic,
}

requests.post("https://your-service.com/webhook", json=result)
```

---

## ✅ Testing Your Changes

### Test New Category

```bash
# Run quick_start.py
python quick_start.py

# Then try with your new category
# Modify quick_start.py:
state = AgentState(
    category="Your_New_Category",
    topic="Test topic",
)
```

### Test Custom Prompts

```python
# Create test file
from agents.researcher import ResearcherAgent

agent = ResearcherAgent()
prompt = agent.get_system_prompt("your_category")
print(prompt)  # Verify it's correct
```

### Test Workflow Changes

```python
# In test script
from graph.workflow import create_workflow

app = create_workflow()
state = AgentState(category="Science", topic="Test")
result = app.invoke(state)

# Check result structure
print(result.research_content[:100])
print(result.blog_draft[:100])
print(result.blog_final[:100])
```

---

## 🚀 Deployment Customizations

### For High Volume

```python
# Use connection pooling for LLMs
from langchain.callbacks.base import BaseCallbackManager

callback_manager = BaseCallbackManager()

# Batch process multiple topics
topics = [...]
for topic in topics:
    process_topic(topic)
    time.sleep(0.5)  # Rate limiting
```

### For Production Server

```python
# Add logging
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In agents:
logger.info(f"Starting research on {state.topic}")
```

### For Cost Optimization

```python
# Cache research results
cache = {}

def cached_research(topic: str):
    if topic in cache:
        return cache[topic]
    
    result = research(topic)
    cache[topic] = result
    return result
```

---

## 📋 Customization Checklist

- [ ] Customize prompts for your use case
- [ ] Add new categories if needed
- [ ] Adjust temperature settings
- [ ] Change model selections
- [ ] Modify iteration limits
- [ ] Add new agents (fact-checker, SEO, etc.)
- [ ] Integrate with your systems
- [ ] Add analytics tracking
- [ ] Test thoroughly with your data
- [ ] Monitor costs and performance
- [ ] Document your changes

---

## 🆘 Need Help?

- Check ARCHITECTURE.md for component details
- Review agent code comments
- Test changes incrementally
- Start with small modifications
- Use quick_start.py for testing

---

Happy customizing! 🚀
