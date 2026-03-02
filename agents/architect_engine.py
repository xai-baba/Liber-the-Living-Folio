import os
import sys
from pydantic_ai import Agent

# Setup a basic agent
agent = Agent('groq:llama-3.3-70b-versatile')

topic = sys.argv[1] if len(sys.argv) > 1 else "The Future of AI"
print(f"Generating outline for: {topic}...")

try:
    # Run the agent synchronously
    result = agent.run_sync(topic)
    
    # UNIVERSAL DATA EXTRACTOR:
    # We check multiple possible attributes to find the text content
    if hasattr(result, 'data'):
        content = result.data
    elif hasattr(result, 'content'):
        content = result.content
    else:
        content = str(result)

    print("\n--- ARCHITECT OUTLINE GENERATED ---\n")
    print(content)

    # Save to file
    with open("latest_outline.md", "w") as f:
        f.write(f"# Outline for: {topic}\n\n{content}")

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    sys.exit(1)
