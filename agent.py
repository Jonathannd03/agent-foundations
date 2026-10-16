from tools import SEARCH_SCHEMA, TOOL_FUNCTIONS
from tool_calls import extract_tool_call
from error import LLMAPIError
from dotenv import load_dotenv
from datetime import date
import os
import httpx

load_dotenv()

API_KEY = os.environ["OPENAI_API_KEY"]
MODEL = os.environ["OPENAI_MODEL"]

today = date.today().isoformat()


prompt = f"What are some news from the apoBank lately?"

tools = [SEARCH_SCHEMA]

response = httpx.post(
    "https://api.openai.com/v1/chat/completions",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": f"Today is {today}.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "tools": tools,
    },
    timeout=30,
)

response_status = response.status_code
result = response.json()


if response_status != 200:
    raise LLMAPIError(
        f"Request failed with status code {response.status_code}: {response.text}"
    )
call = extract_tool_call(result)

if call is None:
    print(result)
else:
    func = TOOL_FUNCTIONS[call["tool"]]
    tool_result = func(**call["args"])
    print(tool_result)
