from typing import Literal
from pydantic import BaseModel, Field


class AgentState(BaseModel):
    """State object for the multi-agent workflow"""
    
    # User inputs
    category: str = Field(default="", description="Category: Science, Politics, or Gaming")
    topic: str = Field(default="", description="User-provided topic")
    
    # Research phase
    research_content: str = Field(default="", description="Raw research data from online sources")
    research_sources: list[str] = Field(default_factory=list, description="URLs and sources used")
    
    # Writing phase
    blog_draft: str = Field(default="", description="Initial blog post draft")
    
    # Editing phase
    blog_final: str = Field(default="", description="Final polished blog post")
    
    # Human feedback
    human_feedback: str = Field(default="", description="Human review and requested changes")
    human_approved: bool = Field(default=False, description="Whether human approved the final content")
    
    # Iteration tracking
    iteration_count: int = Field(default=0, description="Number of revision cycles")
    max_iterations: int = Field(default=3, description="Maximum allowed iterations")
    
    # Metadata
    messages: list[str] = Field(default_factory=list, description="Log of all agent actions")


class ResearcherOutput(BaseModel):
    """Output from researcher agent"""
    research: str
    sources: list[str]


class WriterOutput(BaseModel):
    """Output from writer agent"""
    blog_draft: str


class EditorOutput(BaseModel):
    """Output from editor agent"""
    blog_final: str
    suggestions: str
