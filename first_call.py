import os
import httpx
from dotenv import load_dotenv
from parse_tool_call import parse_tool_call
from datetime import date

today = date.today().isoformat()


tool = [
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "Search the web for recent news on a topic.",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query."}
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
    }
]

system_prompt = f"No text before or after. Today is {today}."


load_dotenv()

API_KEY = os.environ["OPENAI_API_KEY"]
MODEL = os.environ["OPENAI_MODEL"]


class LLMAPIError(Exception):
    """Custom exception for LLM API errors."""

    pass


response = httpx.post(
    "https://api.openai.com/v1/chat/completions",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": "Hi how are you?",
            },
        ],
        "tools": tool,
    },
    timeout=30,
)
if response.status_code != 200:
    raise LLMAPIError(
        f"Request failed with status code {response.status_code}: {response.text}"
    )
data = response.json()
text = data["choices"][0]["message"]

# result = parse_tool_call(text)
print(data)
