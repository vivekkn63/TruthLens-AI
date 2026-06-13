#!/usr/bin/env python3
"""
Quick Start Guide for TruthLens AI
This demonstrates how to use the system programmatically
"""

import os
import sys
from dotenv import load_dotenv

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from state import AgentState
from graph.workflow import create_workflow


def quick_example():
    """Run a quick example"""
    
    # Load environment
    load_dotenv()
    
    # Check API keys
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not configured")
        print("Please copy .env.example to .env and add your API keys")
        return
    
    if not os.getenv("TAVILY_API_KEY"):
        print("⚠️  Warning: TAVILY_API_KEY not configured")
        print("Web search will have limited functionality")
    
    print("🚀 TruthLens AI - Quick Start Example")
    print("="*70)
    
    # Create workflow
    app = create_workflow()
    
    # Create initial state
    state = AgentState(
        category="Science",
        topic="Quantum Computing and Cryptography",
        iteration_count=0,
        max_iterations=1  # Just 1 iteration for quick demo
    )
    
    print(f"\n📚 Topic: {state.topic}")
    print(f"📂 Category: {state.category}")
    print("\n🔄 Running workflow...")
    print("   (This will research, write, and edit the content)\n")
    
    # Run workflow
    result = app.invoke(state)
    
    # Display results
    print("\n" + "="*70)
    print("✓ WORKFLOW COMPLETED")
    print("="*70)
    
    print("\n📊 Results Summary:")
    print(f"  • Research sources: {len(result.research_sources)}")
    print(f"  • Blog draft length: {len(result.blog_draft)} characters")
    print(f"  • Final blog length: {len(result.blog_final)} characters")
    
    print("\n📄 Final Blog Preview:")
    print("-"*70)
    
    # Show preview
    preview_length = 1500
    if len(result.blog_final) > preview_length:
        print(result.blog_final[:preview_length])
        print(f"\n... [Blog continues, {len(result.blog_final)} total chars] ...")
    else:
        print(result.blog_final)
    
    print("\n📚 Sources Used:")
    for i, source in enumerate(result.research_sources[:5], 1):
        print(f"  {i}. {source}")
    
    print("\n✅ Quick start example completed!")
    print("   To process your own topics, run: python main.py")


if __name__ == "__main__":
    quick_example()
