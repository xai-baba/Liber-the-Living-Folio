import os
import sys
from pydantic_ai import Agent

# Setup agent simply
agent = Agent('groq:llama-3.3-70b-versatile')

topic = sys.argv[1] if len(sys.argv) > 1 else "The Future of AI"

try:
    result = agent.run_sync(topic)
    
    # This is the "Bulletproof" part:
    # It checks for .data (new version) or .content (old version)
    output = getattr(result, 'data', getattr(result, 'content', str(result)))

    print("\n--- LIBER ARCHITECT OUTPUT ---")
    print(output)

    with open("latest_outline.md", "w") as f:
        f.write(f"# Outline: {topic}\n\n{output}")

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
