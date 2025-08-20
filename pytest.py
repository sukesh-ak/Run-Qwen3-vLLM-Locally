# pip install OpenAi argparse
from openai import OpenAI
import json
import argparse

# === Config ===
# Remote machines use the IP address instead of localhost
BASE_URL = "http://localhost:8000/v1"
API_KEY = "abc"
MODEL = "Qwen/Qwen3-4B-Instruct-2507-FP8"
SYSTEM_PROMPT = "You are a helpful AI assistant specialized in embedded systems and C++ programming."
USER_PROMPT = "Write a C++ class for using websocket with ESP-IDF"
MAX_TOKENS = 1000
TEMPERATURE = 0.7

# === CLI Arguments ===
parser = argparse.ArgumentParser(description='OpenAI Chat Completion')
parser.add_argument('--prompt', type=str, help='Override the default user prompt')
parser.add_argument('--system-prompt', type=str, help='Override the default system prompt')
args = parser.parse_args()

# Use CLI prompts if provided, otherwise use defaults
system_prompt_to_use = args.system_prompt if args.system_prompt else SYSTEM_PROMPT
user_prompt_to_use = args.prompt if args.prompt else USER_PROMPT

# === Client ===
client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
)

# === Chat Completion Streaming ===
try:
    messages = []
    
    # Add system prompt if it exists
    if system_prompt_to_use:
        messages.append({"role": "system", "content": system_prompt_to_use})
    
    # Add user prompt (always required)
    messages.append({"role": "user", "content": user_prompt_to_use})
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        stream=True
    )
    
    print("Starting stream...")
    for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
    
    print("\n\n[Done]")
    
except Exception as e:
    print(f"Error: {e}")