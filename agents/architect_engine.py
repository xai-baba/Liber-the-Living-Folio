import os
import sys
import glob
from pydantic_ai import Agent

# 1. Setup Agent
agent = Agent('groq:llama-3.3-70b-versatile')

# 2. THE VAULT: Load your writing style samples
style_context = ""
vault_files = glob.glob("vault/*.md")
for file_path in vault_files:
    with open(file_path, "r") as f:
        style_context += f.read() + "\n\n"

@agent.system_prompt
def persona_instructions():
    # We give the AI your samples so it can mimic you
    return f"""You are the Liber Architect. 
    Study this writing style and mimic its tone, vocabulary, and structure:
    ---
    {style_context[:2000]} 
    ---
    When creating outlines, ensure the 'hook' and 'headings' reflect this specific voice."""

# 3. Process the topic from the Web UI
topic = sys.argv[1] if len(sys.argv) > 1 else "The Future of AI"

try:
    result = agent.run_sync(topic)
    # Extract the text content from the AI result
    output = getattr(result, 'data', getattr(result, 'content', str(result)))

    with open("latest_outline.md", "w") as f:
        f.write(output)
    print("Architect finished with your unique voice.")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
