import os
import sys
from pydantic_ai import Agent

# Simple agent, no complex result types
agent = Agent('groq:llama-3.3-70b-versatile')

# Get the topic from the command line
topic = sys.argv[1] if len(sys.argv) > 1 else "The Future of AI"

print(f"Generating outline for: {topic}...")

# Run the agent and get the simple text back
# In PydanticAI, the basic result is just accessed via .data as a string
result = agent.run_sync(topic)

# Log it to the console
print("\n--- ARCHITECT OUTLINE GENERATED ---\n")
print(result.data)

# Save it to the file
with open("latest_outline.md", "w") as f:
    f.write(f"# Outline for: {topic}\n\n")
    f.write(str(result.data))
