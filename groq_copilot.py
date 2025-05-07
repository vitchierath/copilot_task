import os
import logging
from groq import Groq
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    logging.error("GROQ_API_KEY not found in .env file")
    raise ValueError("GROQ_API_KEY is required")

# Initialize Groq client
try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    logging.error(f"Failed to initialize Groq client: {e}")
    raise

# Store conversation history
history = []

def get_coding_response(prompt, context_file=None):
    """Send prompt to Groq with optional file context."""
    try:
        # Read file context if provided
        context = ""
        if context_file:
            context_file = os.path.normpath(context_file)  # Normalize path for Windows
            if os.path.exists(context_file):
                with open(context_file, 'r', encoding='utf-8') as f:
                    context = f.read()
                prompt = f"File context:\n```python\n{context}\n```\nUser query: {prompt}"
            else:
                logging.warning(f"Context file {context_file} not found")
        
        # Add user prompt to history
        history.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Updated to Llama 3.3
            messages=[
                {"role": "system", "content": "You are a coding copilot. Provide accurate code snippets, explanations, and debugging help. Format code in markdown code blocks."},
                *history[-5:]  # Include last 5 messages for context
            ],
            max_tokens=1000,
            temperature=0.7
        )
        response_text = response.choices[0].message.content
        
        # Add assistant response to history
        history.append({"role": "assistant", "content": response_text})
        logging.info("Successfully retrieved response from Groq API")
        return response_text
    except Exception as e:
        logging.error(f"Error in get_coding_response: {e}")
        return f"Error: {str(e)}"

if __name__ == "__main__":
    prompt = input("Enter Your Prompt here: ")
    response = get_coding_response(prompt)
    print(response)