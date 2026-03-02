import os
import sys
from pydantic_ai import Agent

# 1. We explicitly tell the agent to return a string (text)
agent = Agent('groq:llama-3.3-70b-versatile', result_type=str)

@agent.system_prompt
def system_instructions():
    return """You are the Liber Architect. 
    Create a deep-dive, 10-point outline for a 5,000-word article. 
    For each point, include:
    1. A catchy heading.
    2. A brief description of the sub-topics.
    3. An estimated word count for that section."""

# 2. Get the topic from the GitHub Action input
topic = sys.argv[1] if len(sys.argv) > 1 else "The Future of AI in 2026"

# 3. Run the agent
try:
    result = agent.run_sync(topic)
    
    # In PydanticAI, .data contains the successful result
    print("\n--- ARCHITECT OUTLINE GENERATED ---\n")
    print(result.data) 

    # 4. Save to a file so it appears in your repo
    with open("latest_outline.md", "w") as f:
        f.write(f"# Outline for: {topic}\n\n")
        f.write(result.data)

except Exception as e:
    print(f"Agent failed: {e}")
    sys.exit(1)
