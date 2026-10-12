import os
import httpx
from dotenv import load_dotenv
from parse_tool_call import parse_tool_call
from datetime import date

today = date.today().isoformat()

FORMAT = '{"tool": "search", "args": {"query": "..."}}'

system_prompt = (
    f"Reply only with JSON in this format: {FORMAT}. "
    f"No text before or after. Today is {today}."
)

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
                "content": "Find recent news about the apoBank",
            },
        ],
    },
    timeout=30,
)
if response.status_code != 200:
    raise LLMAPIError(
        f"Request failed with status code {response.status_code}: {response.text}"
    )
data = response.json()
print(data)
# text = data["choices"][0]["message"]["content"]
# total_token = data["usage"]["total_tokens"]

# result = parse_tool_call(text)
