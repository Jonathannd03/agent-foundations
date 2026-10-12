import os
import httpx
from dotenv import load_dotenv
from parse_tool_call import parse_tool_call

load_dotenv()

API_KEY = os.environ["OPENAI_API_KEY"]
MODEL = os.environ["OPENAI_MODEL"]

response = httpx.post(
    "https://api.openai.com/v1/chat/completions",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a web researcher and bank specialist, reply only with JSON, the exact format {“tool”: “search”, “args”: {“query”: “...”}}, and no text before or afte"
            },
            {
                "role": "user", 
                "content": "Find recent news about the apoBank"
            },
            
        ],
    },
    timeout=30,
)
data = response.json()
text = data['choices'][0]['message']['content']
total_token = data['usage']['total_tokens']

print(text)

#result = parse_tool_call(text)
