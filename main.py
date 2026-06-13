"""
Main Entry Point - Interactive CLI for TruthLens AI
Handles user input, workflow execution, and human-in-the-loop feedback
"""

import os
import sys
from dotenv import load_dotenv
from state import AgentState
from graph.workflow import create_workflow, print_workflow_info


def clear_screen():
    """Clear console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title: str):
    """Print formatted header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def get_category() -> str:
    """Get topic category from user"""
    print_header("SELECT RESEARCH CATEGORY")
    print("Available categories:")
    print("  1. Science (AI, Technology, Research)")
    print("  2. Politics (Current Affairs, Government)")
    print("  3. Gaming (Games, Industry, Trends)")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        categories = {
            "1": "Science",
            "2": "Politics",
            "3": "Gaming"
        }
        
        if choice in categories:
            selected = categories[choice]
            print(f"\n✓ Selected: {selected}")
            return selected
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")


def get_topic() -> str:
    """Get topic from user"""
    print_header("ENTER YOUR TOPIC")
    print("What would you like us to research and write about?")
    print("Examples:")
    print("  • The impact of quantum computing on cybersecurity")
    print("  • NEET Scam 2026 and its implications")
    print("  • The rise of AI in competitive gaming")
    
    topic = input("\nEnter your topic: ").strip()
    
    if not topic:
        print("❌ Topic cannot be empty!")
        return get_topic()
    
    print(f"\n✓ Topic: {topic}")
    return topic


def display_research(research_content: str):
    """Display research content"""
    print_header("RESEARCH FINDINGS")
    
    # Display first 1000 chars and indicate there's more
    if len(research_content) > 1000:
        print(research_content[:1000])
        print(f"\n... [Research continues - {len(research_content)} total characters] ...\n")
    else:
        print(research_content)


def display_blog_draft(blog_draft: str):
    """Display blog draft"""
    print_header("BLOG DRAFT")
    
    if len(blog_draft) > 2000:
        print(blog_draft[:2000])
        print(f"\n... [Blog continues - {len(blog_draft)} total characters] ...\n")
    else:
        print(blog_draft)


def display_final_blog(blog_final: str, sources: list[str]):
    """Display final polished blog"""
    print_header("FINAL POLISHED BLOG POST")
    
    if len(blog_final) > 2000:
        print(blog_final[:2000])
        print(f"\n... [Blog continues - {len(blog_final)} total characters] ...\n")
    else:
        print(blog_final)
    
    print("\n" + "="*70)
    print("SOURCES USED:")
    for i, source in enumerate(sources[:5], 1):
        print(f"  {i}. {source}")
    if len(sources) > 5:
        print(f"  ... and {len(sources) - 5} more sources")


def get_human_feedback(iteration: int) -> tuple[str, bool]:
    """Get feedback from human reviewer"""
    print_header(f"HUMAN REVIEW & FEEDBACK (Iteration {iteration})")
    print("Review the content above.")
    print("\nOptions:")
    print("  • Type 'approve' to publish as-is")
    print("  • Describe what needs to be changed or improved")
    print("  • Type 'show_full' to see the complete blog post")
    
    while True:
        feedback = input("\nYour feedback/decision: ").strip().lower()
        
        if not feedback:
            print("❌ Please provide feedback or approval.")
            continue
        
        if feedback == "approve":
            print("\n✓ Content approved for publication!")
            return "", True
        elif feedback == "show_full":
            return "", False  # Will trigger showing full blog
        else:
            print(f"\n✓ Feedback recorded: {feedback}")
            return feedback, False


def run_workflow(category: str, topic: str):
    """Execute the complete workflow"""
    print_header("STARTING RESEARCH & WRITING WORKFLOW")
    print(f"Category: {category}")
    print(f"Topic: {topic}")
    print("\nInitializing agents...\n")
    
    # Create workflow
    app = create_workflow()
    
    # Initialize state
    state = AgentState(
        category=category,
        topic=topic,
        iteration_count=0,
        max_iterations=3
    )
    
    # Execute workflow
    print("🚀 Executing workflow...\n")
    
    iteration = 0
    max_iteration_count = state.max_iterations
    
    while iteration < max_iteration_count:
        iteration += 1
        print(f"\n{'#'*70}")
        print(f"ITERATION {iteration}/{max_iteration_count}")
        print(f"{'#'*70}")
        
        # Run the workflow
        result = app.invoke(state)
        
        # Update state with results - convert dict back to AgentState if needed
        if isinstance(result, dict):
            state = AgentState(**result)
        else:
            state = result
        
        # Display results
        if state.research_content:
            display_research(state.research_content)
        
        if state.blog_draft:
            display_blog_draft(state.blog_draft)
        
        if state.blog_final:
            display_final_blog(state.blog_final, state.research_sources)
        
        # Get human feedback
        feedback, approved = get_human_feedback(iteration)
        
        if approved or iteration >= max_iteration_count:
            # Publication flow
            print_header("PUBLICATION READY")
            print("✓ Content has been finalized and is ready for publication!")
            print("\n📄 Save this blog post to your publishing platform.")
            
            # Option to save to file
            save_option = input("\nWould you like to save this blog to a file? (y/n): ").strip().lower()
            if save_option == 'y':
                save_blog_to_file(state)
            
            return state
        else:
            # Continue with revisions
            state.human_feedback = feedback
            state.human_approved = False
    
    # If we exit loop without approval
    if not state.human_approved:
        print("\n⚠️  Maximum iterations reached. Finalizing current version...")
        state.human_approved = True
    
    return state


def save_blog_to_file(state: AgentState):
    """Save blog post to file"""
    filename = input("Enter filename (without extension): ").strip()
    if not filename:
        filename = f"blog_{state.category}_{state.topic.replace(' ', '_')[:20]}"
    
    filename_md = f"{filename}.md"
    
    content = f"""# {state.topic}

**Category:** {state.category}

---

{state.blog_final}

---

## Sources

"""
    
    for i, source in enumerate(state.research_sources, 1):
        content += f"{i}. {source}\n"
    
    try:
        with open(filename_md, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n✓ Blog saved to: {filename_md}")
    except Exception as e:
        print(f"\n❌ Error saving file: {e}")


def main():
    """Main function"""
    # Load environment variables
    load_dotenv()
    
    # Check for required API keys
    if not os.getenv("HUGGINGFACEHUB_API_TOKEN"):
        print("❌ Error: HUGGINGFACEHUB_API_TOKEN not set in .env file")
        sys.exit(1)
    
    if not os.getenv("TAVILY_API_KEY"):
        print("⚠️  Warning: TAVILY_API_KEY not set in .env file")
        print("   Web search functionality will be limited")
    
    # Main loop
    while True:
        clear_screen()
        print_workflow_info()
        
        # Get user input
        category = get_category()
        topic = get_topic()
        
        # Run workflow
        final_state = run_workflow(category, topic)
        
        # Ask if user wants to process another topic
        print("\n" + "="*70)
        another = input("Would you like to research another topic? (y/n): ").strip().lower()
        
        if another != 'y':
            print("\n👋 Thank you for using TruthLens AI!")
            print("Happy publishing! 🚀\n")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Workflow interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
