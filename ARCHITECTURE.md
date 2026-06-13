# System Architecture

Comprehensive overview of TruthLens AI's multi-agent orchestration architecture.

## High-Level Overview

TruthLens AI is a sophisticated multi-agent system built on LangGraph that orchestrates three specialized agents to research topics, write blog posts, and edit content with human-in-the-loop feedback.

```
┌─────────────────────────────────────────────────────────────┐
│                    TRUTHLENS AI SYSTEM                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              STATE MANAGEMENT (AgentState)          │    │
│  │  • Category, Topic, Research, Blog, Feedback        │    │
│  │  • Iteration tracking, Message logging              │    │
│  └─────────────────────────────────────────────────────┘    │
│                          ↓↑                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │         LANGGRAPH WORKFLOW ORCHESTRATION            │    │
│  │  • Research → Write → Edit → Human Review           │    │
│  │  • Conditional routing for revisions                │    │
│  │  • Iteration limit enforcement                      │    │
│  └─────────────────────────────────────────────────────┘    │
│         ↓                    ↓                    ↓         │
│  ┌────────────────┐  ┌─────────────┐  ┌──────────────────┐  │
│  │ RESEARCHER     │  │   WRITER    │  │    EDITOR        │  │
│  │ AGENT          │  │   AGENT     │  │    AGENT         │  │
│  │                │  │             │  │                  │  │
│  │ • Web Search   │  │ • Transform │  │ • Fact-check     │  │
│  │ • Synthesis    │  │ • Blog      │  │ • Polish         │  │
│  │ • Source       │  │ • Category- │  │ • Verify         │  │
│  │   tracking     │  │   specific  │  │ • Refine         │  │
│  └────────────────┘  └─────────────┘  └──────────────────┘  │
│         ↓                    ↓                    ↓         │
│  ┌────────────────┐  ┌─────────────┐  ┌──────────────────┐  │
│  │ TAVILY WEB     │  │  OPENAI LLM │  │  OPENAI LLM      │  │
│  │ SEARCH API     │  │ (GPT-4o)    │  │ (GPT-4o)         │  │
│  │                │  │             │  │                  │  │
│  │ • Real-time    │  │ • Writing   │  │ • Editing        │  │
│  │   search       │  │ • Synthesis │  │ • Review         │  │
│  │ • Source       │  │ • Revision  │  │ • Suggestions    │  │
│  │   tracking     │  │   requests  │  │ • Finalization   │  │
│  └────────────────┘  └─────────────┘  └──────────────────┘  │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              HUMAN-IN-THE-LOOP INTERFACE            │    │
│  │  • Interactive feedback collection                  │    │
│  │  • Approval/revision routing                        │    │
│  │  • File export capabilities                         │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. State Management (`state.py`)

**Purpose**: Define and manage the workflow state

**AgentState Class**:
```python
class AgentState(BaseModel):
    # Inputs
    category: str           # Science, Politics, Gaming
    topic: str             # User-provided topic
    
    # Processing
    research_content: str  # Raw research data
    research_sources: list # Source URLs
    blog_draft: str        # Initial blog post
    blog_final: str        # Polished blog post
    
    # Feedback Loop
    human_feedback: str    # User's revision requests
    human_approved: bool   # Final approval status
    
    # Metadata
    iteration_count: int   # Current iteration
    max_iterations: int    # Maximum allowed
    messages: list         # Action log
```

**Key Features**:
- Pydantic validation ensures data integrity
- Immutable historical tracking
- Iteration counting for safety limits
- Message logging for transparency

### 2. Agents

#### 2.1 Researcher Agent (`agents/researcher.py`)

**Purpose**: Conduct comprehensive online research

**Architecture**:
```
Input (topic) → Multiple Search Queries → Tavily API
                    ↓
            Result Processing → LLM Synthesis
                    ↓
            Structured Research + Sources → Output
```

**Key Methods**:
- `search_topic()`: Execute web searches with Tavily
- `process_search_results()`: Parse and structure results
- `research()`: Main execution with LLM synthesis

**Search Strategy**:
1. Query 1: "{topic} {category}" - Category-specific
2. Query 2: "{topic}" - Direct search
3. Query 3: "recent research {topic}" - Latest findings
4. Query 4: "latest news {topic}" - Current events

**Output Synthesis**:
- Uses GPT-4o-mini (faster, cheaper)
- Synthesizes raw searches into organized research
- Temperature: 0.2 (objective, factual)

#### 2.2 Writer Agent (`agents/writer.py`)

**Purpose**: Transform research into engaging blog content

**Architecture**:
```
Research Data → System Prompt (category-specific)
    ↓
LLM Writing Request → GPT-4o
    ↓
Blog Draft → Revision Handler (if feedback)
    ↓
Updated Blog Post → Output
```

**Key Methods**:
- `write_blog()`: Create initial blog post
- `rewrite_with_feedback()`: Revise based on human feedback

**Writing Approach**:
- **Science**: Educational, formula-focused, accessible
- **Politics**: Direct, fact-based, accountability-focused
- **Gaming**: Technical and casual, trend-aware

**Output Characteristics**:
- Target length: 1500-2500 words
- Temperature: 0.7 (creative but accurate)
- Includes structure, flow, and engagement

#### 2.3 Editor Agent (`agents/editor.py`)

**Purpose**: Review, correct, and polish content

**Architecture**:
```
Research + Draft Blog → Fact-checking + Synthesis
    ↓
LLM Review Request → GPT-4o
    ↓
Corrections + Polish → Editor Response
    ↓
Final Blog → Revision Handler (if feedback)
    ↓
Polished Output
```

**Key Methods**:
- `edit_blog()`: Primary editing and polishing
- `final_review()`: Quality assessment before approval
- `rewrite_with_feedback()`: Apply revisions

**Editing Focus**:
- Fact-checking against research data
- Clarity and readability improvement
- Category-appropriate tone and style
- Source verification

**Output Characteristics**:
- Temperature: 0.3 (precise, accurate)
- Includes editorial notes explaining changes
- Final quality assessment

### 3. LangGraph Workflow (`graph/workflow.py`)

**Purpose**: Orchestrate agent execution and manage flow

**Graph Structure**:
```
START
  ↓
research [ResearcherAgent.research()]
  ↓
write [WriterAgent.write_blog()]
  ↓
edit [EditorAgent.edit_blog()]
  ↓
human_review [Prepare for human feedback]
  ↓
[should_revise() conditional]
  ├─→ APPROVE → END (Publication)
  ├─→ WRITING_FEEDBACK → writer_revise → edit → human_review
  └─→ EDITING_FEEDBACK → editor_revise → human_review
```

**Conditional Logic**:
```python
def should_revise(state: AgentState) -> str:
    if state.human_approved:
        return END
    elif state.iteration_count >= state.max_iterations:
        return END  # Safety limit
    else:
        # Route to appropriate agent
        feedback = state.human_feedback.lower()
        if "writing" in feedback or "content" in feedback:
            return "writer_revise"
        else:
            return "editor_revise"
```

**Key Features**:
- Stateful execution (maintains state between nodes)
- Conditional routing based on feedback
- Iteration safety limits (max 3 by default)
- Transparent message logging

### 4. Prompt Engineering (`prompts/`)

**Structure**:
- `researcher_prompts.py` - 3 category-specific research prompts
- `writer_prompts.py` - 3 category-specific writing prompts
- `editor_prompts.py` - 3 category-specific editing prompts

**Prompt Characteristics**:

**Researcher**:
- Instructs on research methodology
- Specifies source prioritization
- Defines deliverable format

**Writer**:
- Defines writing style and tone
- Specifies blog structure
- Identifies target audience

**Editor**:
- Lists editing priorities
- Specifies fact-checking procedures
- Defines quality standards

## Data Flow

### Workflow Execution Flow

```
1. USER INPUT
   Category Selection → Topic Entry → Validation

2. RESEARCH PHASE
   Web Searches → Result Processing → LLM Synthesis
   Output: research_content, research_sources

3. WRITING PHASE
   Research Analysis → System Prompt → GPT-4o
   Output: blog_draft

4. EDITING PHASE
   Fact-checking → Quality Review → Polish
   Output: blog_final, editorial_notes

5. HUMAN REVIEW
   Display blog_final → Collect Feedback → Decision

6A. APPROVAL PATH
    Save to File → End Workflow

6B. REVISION PATH (up to 3 iterations)
    Parse Feedback → Route to Agent → Process → Return to Step 5

7. PUBLICATION
    Blog post ready for publication
```

### State Mutations

```
Initial State: {category, topic, others empty}
            ↓
After Research: {category, topic, research_content, research_sources, messages}
            ↓
After Writing: {category, topic, research_content, research_sources, blog_draft, messages}
            ↓
After Editing: {category, topic, research_content, research_sources, blog_draft, blog_final, messages}
            ↓
After Feedback: {category, topic, ..., human_feedback, iteration_count++}
            ↓
After Revision: {category, topic, ..., updated_content, messages}
            ↓
After Approval: {category, topic, ..., human_approved=True}
```

## LLM Integration

### Model Selection

**GPT-4o**: Primary model
- **Used by**: Writer, Editor
- **Reason**: Better quality for content creation
- **Cost**: Higher

**GPT-4o-mini**: Efficient model
- **Used by**: Researcher (synthesis only)
- **Reason**: Fast synthesis of search results
- **Cost**: Lower

### Temperature Settings

| Agent | Temperature | Purpose |
|-------|------------|---------|
| Researcher | 0.2 | Objective, factual synthesis |
| Writer | 0.7 | Creative, engaging writing |
| Editor | 0.3 | Precise, accurate editing |

Lower temperature = more deterministic, accurate
Higher temperature = more creative, varied

## API Integration

### Tavily (Web Search)

**Endpoint**: `TavilyClient.search()`
**Parameters**:
- `query`: Search term
- `max_results`: 10 per search
- `include_answer`: True (for summaries)
- `include_raw_content`: True (for full text)

**Response Processing**:
- Extract answer summary
- Parse search results
- Track URLs as sources
- Deduplicate results

### OpenAI (LLM)

**Endpoint**: `ChatOpenAI.invoke()`
**Models**:
- `gpt-4o`: Main content models
- `gpt-4o-mini`: Research synthesis

**Message Format**:
```python
messages = [
    HumanMessage(content=prompt)
]
response = llm.invoke(messages)
```

## Human-in-the-Loop System

### Interactive Loop

```
Agent Output → Display to Human
                    ↓
              Human Provides Feedback
                    ↓
         Parse Feedback (Intent Detection)
                    ↓
    Route to Appropriate Agent for Revision
                    ↓
          Agent Executes Revision
                    ↓
        Updated Content Back to Review
                    ↓
         Approval or Further Revisions
                    ↓
         [Loop continues, max 3 iterations]
```

### Feedback Routing

**Writer Revisions**:
- Triggered by keywords: "writing", "content", "structure", "flow"
- Writer rewrites blog draft based on feedback
- Output flows back to editor for polishing

**Editor Revisions**:
- Triggered by keywords: "editing", "spelling", "grammar", "format", "polish"
- Editor makes corrections to final blog
- Output goes back to human review

## Error Handling

### API Errors
- **Tavily Search Fails**: Fall back to research_content as-is
- **OpenAI API Fails**: Use previous version or error message
- **Rate Limiting**: Automatic retry with backoff (handled by SDK)

### Validation Errors
- **Empty Input**: Reject and re-prompt user
- **Invalid Category**: Default to Science
- **Max Iterations**: Finalize current version

### Edge Cases
- **No Search Results**: Use LLM to generate reasonable output
- **Unclear Feedback**: Default to editor revisions
- **Inconsistent State**: Proceed with available data

## Performance Considerations

### Latency
- Research: 30-60 seconds (web search + synthesis)
- Writing: 20-40 seconds (LLM generation)
- Editing: 15-30 seconds (fact-check + polish)
- **Total**: ~2-5 minutes per iteration

### Cost per Workflow
- Research queries: ~$0.001-0.002
- Writing: ~$0.005-0.010
- Editing: ~$0.005-0.010
- **Total**: ~$0.015-0.025 per blog post

### Token Usage
- Research synthesis: 500-800 tokens
- Blog writing: 1000-1500 tokens
- Blog editing: 1500-2000 tokens
- **Total**: ~3000-4300 tokens per iteration

## Extensibility

### Adding New Categories

1. Create new prompts in `prompts/researcher_prompts.py`
2. Create new prompts in `prompts/writer_prompts.py`
3. Create new prompts in `prompts/editor_prompts.py`
4. Update category selection in `main.py`
5. Update `get_system_prompt()` methods in agents

### Custom Agents

1. Create new agent file in `agents/`
2. Implement required methods
3. Add nodes to workflow graph
4. Add edges and conditional logic

### Advanced Workflows

- Add fact-checking agent between editor and human review
- Implement multi-topic research (combine multiple topics)
- Add image search and generation
- Implement SEO optimization agent
- Add social media post generation

## Security Considerations

### API Keys
- Stored in `.env` file (not committed to git)
- Loaded via `python-dotenv`
- Never logged or displayed

### Data Privacy
- User inputs stored only in-memory during workflow
- No data persistence between sessions
- Files saved only with explicit user approval

### Rate Limiting
- Respects API rate limits
- Backoff handled automatically by SDKs
- User feedback collects are human-paced (seconds)

## Monitoring and Logging

### Built-in Logging

**Console Output**:
- Agent status with emojis
- Processing progress
- Error messages
- Completion summaries

**Message Log**:
- Stored in `state.messages`
- Records each agent action
- Available for audit trail

### External Monitoring (Optional)

- OpenAI Dashboard: View API usage and costs
- Tavily Dashboard: Track search usage
- Application Logging: Add to main.py as needed

## Future Enhancements

1. **Multi-turn Conversation**: Chat-based refinement loop
2. **Image Integration**: Research and include relevant images
3. **SEO Optimization**: Agent to optimize for search
4. **Social Media**: Generate Twitter/LinkedIn posts
5. **Fact-Checking**: Dedicated fact-checking agent
6. **Citation Management**: Formal citation generation
7. **Sentiment Analysis**: Detect and balance tone
8. **Plagiarism Check**: Verify originality
9. **PDF Export**: Generate formatted documents
10. **API Backend**: Expose as REST API service

---

**Architecture designed for clarity, extensibility, and transparency.** 🚀
