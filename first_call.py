import os
import httpx
from dotenv import load_dotenv
from parse_tool_call import parse_tool_call
from datetime import date
import json

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


def extract_tool_call(data: dict) -> dict | None:
    message = data['choices'][0]['message']

    if 'tool_calls' in message.keys():
        tool_name = message['tool_calls'][0]['function']['name']
        print(f'The tool name is: {tool_name}')
        args = json.loads(message['tool_calls'][0]['function']['arguments']) 
        return {'tool': tool_name, 'args': args}
    else:
        return None

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
                "content": "How are you?",
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

result = extract_tool_call(data)
print(result)
